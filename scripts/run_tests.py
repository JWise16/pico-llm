#!/usr/bin/env python3
"""Script to run tests and save detailed output."""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def ensure_dir(directory):
    """Ensure directory exists, create if it doesn't."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def run_tests():
    """Run tests and save output."""
    # Ensure results directory exists
    results_dir = Path("results/test_analysis")
    ensure_dir(results_dir)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Run pytest with output to both console and file
    cmd = [
        "python", "-m", "pytest",
        "tests/scenarios/test_prompt_comparison.py",
        "-v",
        "--junitxml=results/test_analysis/junit.xml",
        "--html=results/test_analysis/report.html",
        "--self-contained-html"
    ]
    
    # Run the command and capture output
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Save console output
    output_file = results_dir / f"test_output_{timestamp}.txt"
    with open(output_file, "w") as f:
        f.write("=== Test Output ===\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("\n=== Errors ===\n")
            f.write(result.stderr)
    
    # Print summary
    print(f"\nTest results saved to:")
    print(f"- Console output: {output_file}")
    print(f"- JUnit XML: {results_dir}/junit.xml")
    print(f"- HTML report: {results_dir}/report.html")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests()) 