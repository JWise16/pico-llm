#!/bin/bash

# List of Groq models to test
MODELS=(
    "deepseek-r1-distill-llama-70b"
)

# Create timestamp for this run
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BASE_DIR="results/groq_analysis_${TIMESTAMP}"

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
        run_timestamp=$(date +"%Y%m%d_%H%M%S")
        OUTPUT_DIR="${model_dir}/run_${i}_${run_timestamp}"
        mkdir -p "${OUTPUT_DIR}"
        
        # Run the test with the correct output directory
        PICOBOT_OUTPUT_DIR="${OUTPUT_DIR}" \
        GROQ_MODEL="${model}" \
        python -m pytest tests/scenarios/test_groq_prompt_performance.py::test_prompt_performance -v
        
        # Check if the test failed
        if [ $? -ne 0 ]; then
            echo "Test iteration ${i} failed for ${model}"
            # Create a failed summary file
            echo "Test failed" > "${OUTPUT_DIR}/summary.txt"
            echo "{\"error\": \"Test failed\"}" > "${OUTPUT_DIR}/trial_data.json"
        fi
        
        # Add a longer delay between runs to prevent rate limiting
        echo "Waiting 10 seconds before next iteration..."
        sleep 10
    done
    
    # Create model summary
    echo "Creating summary for ${model}..."
    
    # Create a CSV summary for easier analysis
    echo "prompt,coverage,efficiency,steps,tokens,cost,time" > "${model_dir}/model_summary.csv"
    
    # Process each run's summary.txt
    for run_dir in "${model_dir}"/run_*; do
        if [ -f "${run_dir}/summary.txt" ]; then
            # Extract data from summary.txt and append to CSV
            while IFS= read -r line; do
                if [[ $line =~ ^([a-z_]+):$ ]]; then
                    prompt="${BASH_REMATCH[1]}"
                elif [[ $line =~ ^\s+Coverage:\s+([0-9.]+)% ]]; then
                    coverage="${BASH_REMATCH[1]}"
                elif [[ $line =~ ^\s+Efficiency:\s+([0-9.]+) ]]; then
                    efficiency="${BASH_REMATCH[1]}"
                elif [[ $line =~ ^\s+Steps:\s+([0-9]+) ]]; then
                    steps="${BASH_REMATCH[1]}"
                elif [[ $line =~ ^\s+Tokens:\s+([0-9]+) ]]; then
                    tokens="${BASH_REMATCH[1]}"
                elif [[ $line =~ ^\s+Cost:\s+\$([0-9.]+) ]]; then
                    cost="${BASH_REMATCH[1]}"
                elif [[ $line =~ ^\s+Time:\s+([0-9.]+)s ]]; then
                    time="${BASH_REMATCH[1]}"
                    # Write the complete record to CSV
                    echo "${prompt},${coverage},${efficiency},${steps},${tokens},${cost},${time}" >> "${model_dir}/model_summary.csv"
                fi
            done < "${run_dir}/summary.txt"
        fi
    done
    
    echo "Tests completed for ${model}"
}

# Export the function so it can be used by parallel
export -f run_model_tests
export BASE_DIR

# Check if parallel is installed
if ! command -v parallel &> /dev/null; then
    echo "GNU Parallel is not installed. Installing..."
    brew install parallel
fi

# Run tests in parallel for all models
echo "Starting parallel test runs for all models..."
parallel -j 2 --halt-on-error 1 run_model_tests ::: "${MODELS[@]}"

# Create overall summary
echo "Creating overall summary..."
# Create a CSV summary for all models
echo "model,prompt,coverage,efficiency,steps,tokens,cost,time" > "${BASE_DIR}/overall_summary.csv"

# Process each model's summary
for model in "${MODELS[@]}"; do
    if [ -f "${BASE_DIR}/${model}/model_summary.csv" ]; then
        # Skip header and append each line with model name
        tail -n +2 "${BASE_DIR}/${model}/model_summary.csv" | while IFS= read -r line; do
            echo "${model},${line}" >> "${BASE_DIR}/overall_summary.csv"
        done
    fi
done

echo "All tests completed. Results are in ${BASE_DIR}" 