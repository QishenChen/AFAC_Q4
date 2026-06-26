#!/bin/bash
# Rerun questions that got "?" (random) answers
# Each runs agent.py with --qid for the specific question

set -e

QDIR="public_dataset_upload/questions/group_a"
RESULTS_DIR="results"
mkdir -p "$RESULTS_DIR/raw_responses"

declare -A Q_CATEGORY
Q_CATEGORY[fc_a_001]="financial_contracts_questions"
Q_CATEGORY[fc_a_008]="financial_contracts_questions"
Q_CATEGORY[fc_a_014]="financial_contracts_questions"
Q_CATEGORY[fc_a_018]="financial_contracts_questions"
Q_CATEGORY[fin_a_004]="financial_reports_questions"
Q_CATEGORY[fin_a_011]="financial_reports_questions"
Q_CATEGORY[fin_a_015]="financial_reports_questions"
Q_CATEGORY[res_a_003]="research_questions"
Q_CATEGORY[reg_a_001]="regulatory_questions"
Q_CATEGORY[reg_a_012]="regulatory_questions"

for qid in fc_a_001 fc_a_008 fc_a_014 fc_a_018 fin_a_004 fin_a_011 fin_a_015 res_a_003 reg_a_001 reg_a_012; do
    category="${Q_CATEGORY[$qid]}"
    qfile="$QDIR/${category}.json"
    outfile="$RESULTS_DIR/rerun_${qid}.json"
    
    echo "========================================"
    echo "Running: $qid ($category)"
    echo "========================================"
    
    python3 agent.py --qid "$qid" --questions "$qfile" --output "$outfile" -v
    
    echo ""
    echo "Done: $qid → $outfile"
    echo ""
done

echo "All reruns complete."
echo "Now merge results into all_answers.json with:"
echo "  python3 rerun_merge.py"