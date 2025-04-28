#!/bin/bash

# Create timestamp for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="results/openai_analysis_${TIMESTAMP}"

# Create base directory
mkdir -p "${BASE_DIR}"

# Run test 10 times
for i in {1..10}; do
    echo "Running test iteration ${i}..."
    OUTPUT_DIR="${BASE_DIR}/run_${i}"
    PICOBOT_OUTPUT_DIR="${OUTPUT_DIR}" python -m pytest tests/scenarios/test_openai_prompt_performance.py::test_prompt_performance -v
    
    # Add a small delay between runs to prevent rate limiting
    sleep 5
done

# Create overall summary
echo "Creating overall summary..."
cat "${BASE_DIR}"/run_*/summary.txt > "${BASE_DIR}/overall_summary.txt" 2>/dev/null || echo "No summary files found"

echo "All tests completed. Results are in ${BASE_DIR}" 