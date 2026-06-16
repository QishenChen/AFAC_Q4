#!/usr/bin/env python3
"""
MinerU Batch Extraction Script (v4)
- Saves batch_ids to state for crash recovery
- Falls back to single-file submission when batch quota exhausted
- Preserves images alongside markdown output
- Splits PDFs > 200 pages into chunks and integrates after extraction
"""

import os, sys, json, time, requests, shutil, zipfile, traceback, subprocess
from pathlib import Path

TOKEN= "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIzMjUwMDc4MiIsInJvbCI6IlJPTEVfUkVHSVNURVIiLCJpc3MiOiJPcGVuWExhYiIsImlhdCI6MTc4MTQyMzQ5MiwiY2xpZW50SWQiOiJsa3pkeDU3bnZ5MjJqa3BxOXgydyIsInBob25lIjoiIiwib3BlbklkIjpudWxsLCJ1dWlkIjoiYjBlNjIyMjQtOTMyMS00M2Q2LWEwOWMtNDgzZjg4ZDVkYzAyIiwiZW1haWwiOiIiLCJleHAiOjE3ODkxOTk0OTJ9.WXbXiLZbqqeFZnkQORL24AsBelPluoc7YZLUAGL51Ep93KrzLGVWRvAJYYftl4ux7QQiFZxmZnOfX5t6cO3zaw"
BASE_URL = "https://mineru.net/api/v4"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}
SOURCE_DIR = "public_dataset_upload/raw"
OUTPUT_DIR = "public_dataset_upload/extracted"
STATE_FILE = "mineru_batch_state.json"
BATCH_SIZE = 20  # Small enough that CDN URLs don't expire during serial download
POLL_INTERVAL = 10
MAX_WAIT = 900
# Files that can never be processed due to hard limits
OVER_PAGE_LIMIT = set()  # Populated dynamically during collection
PAGE_LIMIT = 200  # MinerU free tier page limit
SPLIT_TMP_DIR = "/tmp/mineru_splits"  # Temp dir for split PDF chunks

# ============================================================
# HELPERS
# ============================================================

def get_page_count(pdf_path):
    """Get page count of a PDF. Returns int or None on failure."""
    try:
        result = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'Pages' in line:
                    return int(line.split(':')[1].strip())
    except:
        pass
    try:
        from PyPDF2 import PdfReader
        return len(PdfReader(pdf_path).pages)
    except:
        pass
    try:
        from pypdf import PdfReader
        return len(PdfReader(pdf_path).pages)
    except:
        pass
    return None


def split_pdf(pdf_path, max_pages=PAGE_LIMIT, tmp_dir=SPLIT_TMP_DIR):
    """Split a PDF into chunks of max_pages each.
    Returns list of dicts with keys: abs_path, name, rel_path, start_page, end_page.
    """
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        try:
            from PyPDF2 import PdfReader, PdfWriter
        except ImportError:
            print(f"    ✗ Cannot split PDF: pypdf/PyPDF2 not available")
            return None

    os.makedirs(tmp_dir, exist_ok=True)
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"    ✗ Cannot read PDF for splitting: {pdf_path} — {e}")
        return None

    total_pages = len(reader.pages)
    if total_pages <= max_pages:
        return None  # No split needed

    chunks = []
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    for start in range(0, total_pages, max_pages):
        end = min(start + max_pages, total_pages)
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        chunk_name = f"{base_name}_p{start+1}-{end}"
        chunk_path = os.path.join(tmp_dir, f"{chunk_name}.pdf")
        with open(chunk_path, 'wb') as f:
            writer.write(f)
        chunks.append({
            'abs_path': chunk_path,
            'name': f"{chunk_name}.pdf",
            'start_page': start + 1,
            'end_page': end,
        })
    print(f"  → Split {os.path.basename(pdf_path)} ({total_pages} pages) into {len(chunks)} chunks")
    return chunks


def collect_files():
    """Collect files, splitting oversized PDFs into chunks."""
    files = []
    split_map = {}  # original_rel_path -> list of chunk rel_paths

    for root, dirs, filenames in os.walk(SOURCE_DIR):
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in ('.pdf', '.html'):
                continue

            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, SOURCE_DIR)
            ftype = ext.lstrip('.')

            if ftype == 'pdf':
                pages = get_page_count(abs_path)
                if pages and pages > PAGE_LIMIT:
                    # Split this PDF into chunks
                    chunks = split_pdf(abs_path, PAGE_LIMIT)
                    if chunks:
                        chunk_rel_paths = []
                        for i, chunk in enumerate(chunks):
                            # Build a rel_path for the chunk that mimics the original structure
                            orig_base = rel_path.rsplit('.', 1)[0]
                            chunk_rel = f"{orig_base}_chunk_{chunk['start_page']}-{chunk['end_page']}.pdf"
                            chunk['rel_path'] = chunk_rel
                            chunk['type'] = 'pdf'
                            files.append(chunk)
                            chunk_rel_paths.append(chunk_rel)
                        split_map[rel_path] = chunk_rel_paths
                        continue  # Don't add the original oversized file
                    else:
                        # Splitting failed — skip this over-limit PDF
                        OVER_PAGE_LIMIT.add(rel_path)
                        print(f"  ⚠ Skipping {rel_path} ({pages} pages) — split failed")
                        continue

            files.append({
                'abs_path': abs_path,
                'rel_path': rel_path,
                'name': fname,
                'type': ftype,
            })

    files.sort(key=lambda x: x['rel_path'])
    return files, split_map


def integrate_split_chunks(original_rel_path, chunk_rel_paths):
    """Merge extracted .md files and images from split chunks back into a single output."""
    original_base = original_rel_path.rsplit('.', 1)[0]
    merged_md_path = os.path.join(OUTPUT_DIR, original_base + '.md')
    merged_img_dir = os.path.join(OUTPUT_DIR, original_base, 'images')

    combined_md = []
    any_success = False

    for chunk_rp in chunk_rel_paths:
        chunk_base = chunk_rp.rsplit('.', 1)[0]
        chunk_md = os.path.join(OUTPUT_DIR, chunk_base + '.md')

        if os.path.exists(chunk_md):
            with open(chunk_md, 'r', encoding='utf-8') as f:
                content = f.read()
            # Add a page-range marker between chunks
            chunk_label = os.path.splitext(os.path.basename(chunk_rp))[0]
            combined_md.append(f"<!-- Chunk: {chunk_label} -->\n\n{content}")
            any_success = True

        # Merge images from chunk
        chunk_img_dir = os.path.join(OUTPUT_DIR, chunk_base, 'images')
        if os.path.exists(chunk_img_dir) and os.path.isdir(chunk_img_dir):
            os.makedirs(merged_img_dir, exist_ok=True)
            for img_name in os.listdir(chunk_img_dir):
                src = os.path.join(chunk_img_dir, img_name)
                dst = os.path.join(merged_img_dir, img_name)
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)

    if any_success:
        os.makedirs(os.path.dirname(merged_md_path), exist_ok=True)
        with open(merged_md_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(combined_md))
        img_count = sum(1 for _ in Path(merged_img_dir).rglob('*')) if os.path.exists(merged_img_dir) else 0
        print(f"  ✓ Integrated: {original_base}.md from {len(chunk_rel_paths)} chunks ({img_count} images)")
    else:
        print(f"  ⚠ Integration: no successful chunks for {original_rel_path}")

    # Clean up chunk outputs (but keep the integrated result)
    for chunk_rp in chunk_rel_paths:
        chunk_base = chunk_rp.rsplit('.', 1)[0]
        for p in [
            os.path.join(OUTPUT_DIR, chunk_base + '.md'),
            os.path.join(OUTPUT_DIR, chunk_base),
        ]:
            if os.path.isfile(p):
                os.remove(p)
            elif os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)

    # Clean up temporary split PDFs
    for chunk_rp in chunk_rel_paths:
        chunk_name = os.path.basename(chunk_rp)
        tmp_pdf = os.path.join(SPLIT_TMP_DIR, chunk_name)
        if os.path.exists(tmp_pdf):
            os.remove(tmp_pdf)

    return any_success


def submit_batch(files_batch, model_version):
    """Submit batch. Returns (batch_id, file_urls) or (None, None) on quota failure."""
    if not files_batch:
        return None, None

    payload = {
        "files": [{"name": f['name'], "data_id": f['rel_path']} for f in files_batch],
        "model_version": model_version,
        "enable_table": True, "enable_formula": True, "language": "ch",
    }
    try:
        resp = requests.post(f"{BASE_URL}/file-urls/batch", headers=HEADERS, json=payload, timeout=60)
        if resp.status_code == 429:
            print("  ✗ 429 Rate limited")
            return None, None
        resp.raise_for_status()
        result = resp.json()
    except requests.exceptions.ConnectionError as e:
        print(f"  ✗ Network error: {e}")
        print("  Will retry on next run (state saved)")
        return None, None
    if result.get("code") != 0:
        msg = result.get("msg", str(result))
        print(f"  ✗ API error: {msg}")
        return None, None
    return result["data"]["batch_id"], result["data"]["file_urls"]



def upload_files(batch_id, file_urls, files_batch):
    """PUT each file to its upload URL. Returns actual batch_id (may differ on retry)."""
    print(f"  Batch {batch_id}: uploading {len(file_urls)} files...")
    for i, f in enumerate(files_batch):
        url = file_urls[i]
        try:
            with open(f['abs_path'], 'rb') as fh:
                put_resp = requests.put(url, data=fh, timeout=120)
                if put_resp.status_code not in (200, 201):
                    print(f"    ✗ Upload {put_resp.status_code}: {f['rel_path']}")
        except Exception as e:
            print(f"    ✗ Upload error: {f['rel_path']} — {e}")
    return batch_id


def poll_batch(batch_id):
    """Poll a batch. Returns list of {rel_path, state, zip_url, err_msg} dicts when complete."""
    start = time.time()
    while True:
        if time.time() - start > MAX_WAIT:
            print(f"  Batch {batch_id}: TIMEOUT")
            return None
        try:
            resp = requests.get(f"{BASE_URL}/extract-results/batch/{batch_id}", headers=HEADERS, timeout=30)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            print(f"  Poll error: {e}, retrying...")
            time.sleep(POLL_INTERVAL)
            continue
        if result.get("code") != 0:
            time.sleep(POLL_INTERVAL)
            continue
        extract_results = result["data"].get("extract_result", [])
        if not extract_results:
            time.sleep(POLL_INTERVAL)
            continue
        states = {}
        items = []
        for er in extract_results:
            if isinstance(er, str):
                continue
            s = er.get("state", "unknown")
            states[s] = states.get(s, 0) + 1
            items.append({
                "rel_path": er.get("data_id", er.get("file_name", "unknown")),
                "state": s,
                "zip_url": er.get("full_zip_url", ""),
                "err_msg": er.get("err_msg", ""),
            })
        done = states.get("done", 0)
        failed = states.get("failed", 0)
        pending = sum(v for k, v in states.items() if k not in ("done", "failed"))
        elapsed = time.time() - start
        print(f"  Batch {batch_id}: {done}✓ {failed}✗ {pending}… ({elapsed:.0f}s)")
        if pending == 0:
            return items
        time.sleep(POLL_INTERVAL)


def save_file(zip_url, rel_path):
    """Download zip, save markdown + images. Returns True/False/'expired'."""
    base = rel_path.rsplit('.', 1)[0]
    md_out = os.path.join(OUTPUT_DIR, base + '.md')
    # Skip if already saved to disk (saves time on re-poll passes)
    if os.path.exists(md_out):
        return True
    try:
        resp = requests.get(zip_url, timeout=60)
        if resp.status_code == 403:
            print(f"    ⚠ CDN URL expired for {rel_path}")
            return 'expired'
        if resp.status_code != 200:
            print(f"    ✗ DL {resp.status_code}: {rel_path}")
            return False
    except Exception as e:
        print(f"    ✗ DL error: {rel_path} — {e}")
        return False
    tmp_zip = f"/tmp/mineru_{os.path.basename(rel_path)}.zip"
    tmp_dir = f"/tmp/mineru_ext_{os.path.basename(rel_path)}"
    try:
        with open(tmp_zip, 'wb') as f: f.write(resp.content)
        os.makedirs(tmp_dir, exist_ok=True)
        with zipfile.ZipFile(tmp_zip, 'r') as zf: zf.extractall(tmp_dir)

        # Save full.md
        md_files = list(Path(tmp_dir).rglob("full.md"))
        md_out = os.path.join(OUTPUT_DIR, base + '.md')
        os.makedirs(os.path.dirname(md_out), exist_ok=True)
        if md_files:
            shutil.copy(str(md_files[0]), md_out)
            print(f"    ✓ {base}.md")
        else:
            any_md = list(Path(tmp_dir).rglob("*.md"))
            if any_md:
                combined = []
                for mdf in any_md:
                    with open(mdf, 'r', encoding='utf-8') as f:
                        combined.append(f.read())
                with open(md_out, 'w', encoding='utf-8') as f:
                    f.write('\n\n'.join(combined))
                print(f"    ✓ {base}.md (combined)")

        # Save main.html for HTML sources
        html_files = list(Path(tmp_dir).rglob("main.html"))
        if html_files:
            html_out = os.path.join(OUTPUT_DIR, base + '_extracted.html')
            os.makedirs(os.path.dirname(html_out), exist_ok=True)
            shutil.copy(str(html_files[0]), html_out)
            print(f"    ✓ {base}_extracted.html")

        # Save images
        for img_dir in [d for d in Path(tmp_dir).rglob("images") if d.is_dir()]:
            dest = os.path.join(OUTPUT_DIR, base, "images")
            os.makedirs(dest, exist_ok=True)
            for f in img_dir.iterdir():
                if f.is_file():
                    shutil.copy2(str(f), os.path.join(dest, f.name))
            n = sum(1 for _ in img_dir.iterdir() if _.is_file())
            if n: print(f"    ✓ {n} images → {base}/images/")
        return True
    except Exception as e:
        print(f"    ✗ Extract: {rel_path} — {e}")
        return False
    finally:
        for p in [tmp_zip, tmp_dir]:
            if os.path.exists(p):
                (os.remove if os.path.isfile(p) else shutil.rmtree)(p)


def process_item(item, completed, failed, pending_batches, batch_id):
    """Process one extract_result item. Returns True, False, or 'expired' if CDN URL stale."""
    rp = item["rel_path"]
    if item["state"] == "done":
        if item["zip_url"]:
            result = save_file(item["zip_url"], rp)
            if result == 'expired':
                return 'expired'  # Signal caller to re-poll for fresh URL
            elif result:
                completed.add(rp)
            else:
                failed.add(rp)
        else:
            failed.add(rp)
        return True
    elif item["state"] == "failed":
        err = item.get("err_msg", "")
        # Check if it's actually a page-limit failure masked as retry exhaustion
        if rp.endswith('.pdf'):
            pages = get_page_count(os.path.join(SOURCE_DIR, rp))
            if pages and pages > PAGE_LIMIT:
                print(f"    ✗ FAILED: {rp} — {pages} pages (exceeds {PAGE_LIMIT}-page limit)")
            else:
                print(f"    ✗ FAILED: {rp} — {err} (pages: {pages or 'unknown'})")
        else:
            print(f"    ✗ FAILED: {rp} — {err}")
        if "retry limit" in err.lower() or "pages exceeds" in err.lower():
            OVER_PAGE_LIMIT.add(rp)
        failed.add(rp)
        return True


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"completed": [], "failed": [], "pending_batches": {}, "split_map": {}}


def save_state(completed, failed, pending_batches, split_map=None):
    state = {
        "completed": sorted(completed),
        "failed": sorted(failed | OVER_PAGE_LIMIT),
        "pending_batches": pending_batches,
    }
    if split_map:
        state["split_map"] = split_map
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def process_single_files(files_batch, model_version, completed, failed, pending_batches):
    """Submit and process files one at a time."""
    for f in files_batch:
        rp = f['rel_path']
        if rp in completed or rp in failed or rp in OVER_PAGE_LIMIT:
            continue
        print(f"  Single: {rp}")
        bid, urls = submit_batch([f], model_version)
        if bid:
            upload_files(bid, urls, [f])
            pending_batches[bid] = [f['rel_path']]
            save_state(completed, failed, pending_batches)
        else:
            print(f"    ✗ Submit failed (quota/error), marking failed")
            failed.add(rp)
        time.sleep(2)
        # Poll immediately for this single file
        if bid:
            items = poll_batch(bid)
            if items:
                for item in items:
                    process_item(item, completed, failed, pending_batches, bid)
                if bid in pending_batches:
                    del pending_batches[bid]
            else:
                # Timed out — leave in pending for next run
                print(f"    ⚠ Batch {bid} timed out, will retry on restart")
            save_state(completed, failed, pending_batches)
    return None


def check_and_integrate_splits(completed, failed, split_map):
    """Check if all chunks of a split PDF are done, and integrate if so."""
    integrated = set()
    for orig_rel_path, chunk_rel_paths in list(split_map.items()):
        all_chunks_done = True
        for crp in chunk_rel_paths:
            if crp not in completed and crp not in failed:
                all_chunks_done = False
                break

        if all_chunks_done:
            # All chunks have been processed (some may have failed)
            successful_chunks = [crp for crp in chunk_rel_paths if crp in completed]
            if successful_chunks:
                integrate_split_chunks(orig_rel_path, successful_chunks)
                completed.add(orig_rel_path)
                # Remove chunk entries from completed/failed sets so they don't show in final counts
                for crp in chunk_rel_paths:
                    completed.discard(crp)
                    failed.discard(crp)
                integrated.add(orig_rel_path)
            else:
                # All chunks failed
                failed.add(orig_rel_path)
                for crp in chunk_rel_paths:
                    failed.discard(crp)
                integrated.add(orig_rel_path)

    # Remove integrated entries from split_map
    for k in integrated:
        del split_map[k]

    return integrated


def main():
    all_files, split_map = collect_files()
    print(f"Found {len(all_files)} files: {sum(1 for f in all_files if f['type']=='pdf')} PDFs + {sum(1 for f in all_files if f['type']=='html')} HTMLs")
    if split_map:
        print(f"  📄 {len(split_map)} oversized PDF(s) split into chunks for processing")

    state = load_state()
    completed = set(state.get("completed", []))
    failed = set(state.get("failed", []))
    pending_batches = state.get("pending_batches", {})

    # Merge saved split_map with the freshly built one (saved takes precedence for tracking)
    saved_split_map = state.get("split_map", {})
    # Use saved split_map but update with any new splits from this run
    for k, v in split_map.items():
        if k not in saved_split_map:
            saved_split_map[k] = v
    split_map = saved_split_map

    # Collect all chunk rel_paths to detect if a file is already split
    all_chunk_set = set()
    for chunk_list in split_map.values():
        all_chunk_set.update(chunk_list)

    # Pre-scan remaining original PDFs (non-split) that exceed the page limit
    for f in all_files:
        if f['type'] == 'pdf' and f['rel_path'] not in all_chunk_set:
            pages = get_page_count(f['abs_path'])
            if pages and pages > PAGE_LIMIT and f['rel_path'] not in split_map:
                # Shouldn't happen if split_map is working, but handle edge case (e.g. splitting failed)
                OVER_PAGE_LIMIT.add(f['rel_path'])
                failed.add(f['rel_path'])

    # === FIRST: poll any orphaned pending batches ===
    if pending_batches:
        print(f"\nRecovering {len(pending_batches)} pending batches...")
        for bid, fpaths in list(pending_batches.items()):
            print(f"  Polling batch {bid} ({len(fpaths)} files)...")
            items = poll_batch(bid)
            if items is None:
                print(f"    ⚠ Timed out, will retry later")
                continue
            for item in items:
                process_item(item, completed, failed, pending_batches, bid)
            del pending_batches[bid]
            save_state(completed, failed, pending_batches, split_map)

        # Check if recovery completed any split chunks
        check_and_integrate_splits(completed, failed, split_map)

    # Mark all chunk rel_paths as "in progress" so they appear in remaining
    all_chunk_rel_paths = set()
    for chunk_list in split_map.values():
        all_chunk_rel_paths.update(chunk_list)

    remaining = [f for f in all_files
                 if f['rel_path'] not in completed
                 and f['rel_path'] not in failed
                 and f['rel_path'] not in OVER_PAGE_LIMIT]

    print(f"\nCompleted: {len(completed)}, Failed: {len(failed)}, Remaining: {len(remaining)}")
    if not remaining:
        # Check if any split integrations are still pending
        check_and_integrate_splits(completed, failed, split_map)
        if not remaining:
            print("All done!")
            return

    vlm = [f for f in remaining if f['type'] == 'pdf']
    html = [f for f in remaining if f['type'] == 'html']
    print(f"PDFs: {len(vlm)}, HTMLs: {len(html)}")

    for model, files in [("vlm", vlm), ("MinerU-HTML", html)]:
        if not files:
            continue
        # Try batch first
        for bi in range(0, len(files), BATCH_SIZE):
            batch = files[bi:bi + BATCH_SIZE]
            batch_files = [f for f in batch if f['rel_path'] not in completed and f['rel_path'] not in failed]
            if not batch_files:
                continue
            print(f"\nBatch {bi//BATCH_SIZE + 1} ({len(batch_files)} files, {model})")

            # Retry batch submission up to 3 times with backoff
            bid, urls = None, None
            for attempt in range(1, 4):
                bid, urls = submit_batch(batch_files, model)
                if bid:
                    break
                if attempt < 3:
                    wait = 5 * attempt
                    print(f"  Retrying batch submission in {wait}s (attempt {attempt}/3)...")
                    time.sleep(wait)
            if bid:
                upload_files(bid, urls, batch_files)
                pending_batches[bid] = [f['rel_path'] for f in batch_files]
                save_state(completed, failed, pending_batches, split_map)
                items = poll_batch(bid)
                if items:
                    # First pass: download all files
                    expired = []
                    for item in items:
                        result = process_item(item, completed, failed, pending_batches, bid)
                        if result == 'expired':
                            expired.append(item)

                    # Re-poll only for files with expired CDN URLs
                    for repoll_count in range(1, 4):
                        if not expired:
                            break
                        print(f"  Re-polling for {len(expired)} expired URLs (attempt {repoll_count}/3)...")
                        time.sleep(2)
                        fresh_items = poll_batch(bid)
                        if fresh_items:
                            fresh_map = {f['rel_path']: f for f in fresh_items}
                            still_expired = []
                            for ei in expired:
                                fi = fresh_map.get(ei['rel_path'])
                                if fi and fi.get('zip_url'):
                                    ei['zip_url'] = fi['zip_url']
                                    result = process_item(ei, completed, failed, pending_batches, bid)
                                    if result == 'expired':
                                        still_expired.append(ei)
                                else:
                                    failed.add(ei['rel_path'])
                            expired = still_expired
                        else:
                            break
                    if bid in pending_batches:
                        del pending_batches[bid]
                else:
                    print(f"  ⚠ Batch {bid} timed out, leaving in pending")
            else:
                # Batch failed after retries — try single-file mode
                print(f"  Batch submission failed after 3 retries, switching to single-file mode...")
                process_single_files(batch_files, model, completed, failed, pending_batches)

            # After each batch, check if any split integrations are ready
            check_and_integrate_splits(completed, failed, split_map)
            save_state(completed, failed, pending_batches, split_map)
            time.sleep(3)

    # Final integration check
    check_and_integrate_splits(completed, failed, split_map)

    # Final summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Completed: {len(completed)}")
    print(f"  Failed permanently: {len(failed)}")
    pending_count = sum(len(v) for v in pending_batches.values())
    print(f"  Pending (orphaned): {pending_count}")
    md = sum(1 for _ in Path(OUTPUT_DIR).rglob("*.md"))
    html_out = sum(1 for _ in Path(OUTPUT_DIR).rglob("*_extracted.html"))
    img = sum(1 for _ in Path(OUTPUT_DIR).rglob("images/*"))
    print(f"  Output: {md} .md, {html_out} .html, {img} images")
    if split_map:
        print(f"  ⚠ {len(split_map)} split PDF(s) still pending integration")
    if failed - OVER_PAGE_LIMIT:
        print(f"\nNon-permanent failures ({len(failed - OVER_PAGE_LIMIT)}):")
        for fp in sorted(failed - OVER_PAGE_LIMIT):
            print(f"  - {fp}")

if __name__ == "__main__":
    main()