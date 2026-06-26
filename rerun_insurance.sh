#!/bin/bash
# Rerun insurance questions ins_a_003 through ins_a_010
set -e

QDIR="public_dataset_upload/questions/group_a"
QFILE="$QDIR/insurance_questions.json"
RESULTS_DIR="results"
mkdir -p "$RESULTS_DIR/raw_responses"

for i in 003 004 005 006 007 008 009 010; do
    qid="ins_a_$i"
    outfile="$RESULTS_DIR/rerun_${qid}.json"
    
    echo "========================================"
    echo "Running: $qid"
    echo "========================================"
    
    python3 agent.py --qid "$qid" --questions "$QFILE" --output "$outfile" -v
    
    echo ""
    echo "Done: $qid → $outfile"
    echo ""
done

echo "All insurance reruns complete."
echo "Now merge with: python3 rerun_merge.py"
echo "Then regenerate CSV: python3 generate_submission.py results/all_answers.json results/submission.csv"