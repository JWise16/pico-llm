#!/bin/bash

# List of Claude models to test
MODELS=(
   "claude-3-5-haiku-20241022"
   "claude-3-7-sonnet-20250219"
)

# Create timestamp for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="results/claude_analysis_${TIMESTAMP}"

# Create base directory
mkdir -p "${BASE_DIR}"

# Function to run tests for a single model
run_model_tests() {
    local model=$1
    local model_dir="${BASE_DIR}/${model}"
    mkdir -p "${model_dir}"
    
    echo "Starting tests for ${model}..."
    
    # Run test 10 times
    for i in {1..10}; do
        echo "Running test iteration ${i} for ${model}..."
        OUTPUT_DIR="${model_dir}/run_${i}"
        PICOBOT_OUTPUT_DIR="${OUTPUT_DIR}" \
        ANTHROPIC_MODEL="${model}" \
        python -m pytest tests/scenarios/test_prompt_comparison.py::test_prompt_performance -v
        
        # Add a small delay between runs to prevent rate limiting
        sleep 5
    done
    
    # Create model summary
    echo "Creating summary for ${model}..."
    cat "${model_dir}"/run_*/summary.txt > "${model_dir}/model_summary.txt" 2>/dev/null || echo "No summary files found"
    
    echo "Tests completed for ${model}"
}

# Export the function so it can be used by parallel
export -f run_model_tests
export BASE_DIR

# Run tests in parallel for all models
echo "Starting parallel test runs for all models..."
parallel -j 3 run_model_tests ::: "${MODELS[@]}"

# Create overall summary
echo "Creating overall summary..."
cat "${BASE_DIR}"/*/model_summary.txt > "${BASE_DIR}/overall_summary.txt" 2>/dev/null || echo "No summary files found"

echo "All tests completed. Results are in ${BASE_DIR}" 