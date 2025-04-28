#!/bin/bash

# Create timestamp for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="results/anthropic_analysis_${TIMESTAMP}"

# Create base directory
mkdir -p "${BASE_DIR}"

# List of Anthropic models to test
MODELS=(
    "claude-3-opus-20240229"
    "claude-3-sonnet-20240229"
    "claude-3-haiku-20240307"
    "claude-3-5-sonnet-20240620"
    "claude-3-5-haiku-20241022"
    "claude-3-7-sonnet-20250219"
)

# Run test 10 times for each model
for model in "${MODELS[@]}"; do
    echo "Testing model: ${model}"
    MODEL_DIR="${BASE_DIR}/${model}"
    mkdir -p "${MODEL_DIR}"
    
    for i in {1..10}; do
        echo "Running test iteration ${i} for ${model}..."
        OUTPUT_DIR="${MODEL_DIR}/run_${i}"
        PICOBOT_OUTPUT_DIR="${OUTPUT_DIR}" python -m pytest tests/scenarios/test_anthropic_prompt_performance.py::test_prompt_performance -v --model-name="${model}"
        
        # Add a small delay between runs to prevent rate limiting
        sleep 5
    done
    
    # Create model summary
    echo "Creating summary for ${model}..."
    cat "${MODEL_DIR}"/run_*/summary.txt > "${MODEL_DIR}/model_summary.txt" 2>/dev/null || echo "No summary files found"
done

# Create overall summary
echo "Creating overall summary..."
cat "${BASE_DIR}"/*/model_summary.txt > "${BASE_DIR}/overall_summary.txt" 2>/dev/null || echo "No summary files found"

echo "All tests completed. Results are in ${BASE_DIR}" 