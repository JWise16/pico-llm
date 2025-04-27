#!/usr/bin/env python3
"""Script to view and analyze test results."""

import sys
import xml.dom.minidom
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

def format_xml(xml_file):
    """Format XML file for better readability."""
    with open(xml_file) as f:
        xml_content = f.read()
    
    # Parse and pretty print XML
    dom = xml.dom.minidom.parseString(xml_content)
    return dom.toprettyxml()

def parse_junit_xml(xml_file):
    """Parse JUnit XML file and extract key metrics."""
    with open(xml_file) as f:
        xml_content = f.read()
    
    dom = xml.dom.minidom.parseString(xml_content)
    testsuite = dom.getElementsByTagName('testsuite')[0]
    
    # Extract basic metrics
    metrics = {
        'tests': int(testsuite.getAttribute('tests')),
        'failures': int(testsuite.getAttribute('failures')),
        'errors': int(testsuite.getAttribute('errors')),
        'skipped': int(testsuite.getAttribute('skipped')),
        'time': float(testsuite.getAttribute('time')),
    }
    
    # Extract test cases
    testcases = []
    for testcase in dom.getElementsByTagName('testcase'):
        case = {
            'name': testcase.getAttribute('name'),
            'time': float(testcase.getAttribute('time')),
            'status': 'passed'
        }
        
        # Check for failures
        failures = testcase.getElementsByTagName('failure')
        if failures:
            case['status'] = 'failed'
            case['message'] = failures[0].getAttribute('message')
        
        testcases.append(case)
    
    return metrics, testcases

def display_results(xml_file):
    """Display test results in a nice format."""
    console = Console()
    
    # Parse results
    metrics, testcases = parse_junit_xml(xml_file)
    
    # Display summary
    console.print(Panel.fit(
        f"Test Results Summary\n"
        f"Total Tests: {metrics['tests']}\n"
        f"Passed: {metrics['tests'] - metrics['failures'] - metrics['errors']}\n"
        f"Failed: {metrics['failures']}\n"
        f"Errors: {metrics['errors']}\n"
        f"Skipped: {metrics['skipped']}\n"
        f"Total Time: {metrics['time']:.2f}s",
        title="Summary",
        border_style="blue"
    ))
    
    # Create test cases table
    table = Table(title="Test Cases")
    table.add_column("Test Name", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Time (s)", justify="right", style="blue")
    
    for case in testcases:
        status_style = "green" if case['status'] == 'passed' else "red"
        table.add_row(
            case['name'],
            case['status'].upper(),
            f"{case['time']:.2f}",
            style=status_style
        )
    
    console.print(table)

def main():
    """Main function."""
    xml_file = Path("results/test_analysis/junit.xml")
    if not xml_file.exists():
        print(f"Error: {xml_file} not found")
        return 1
    
    # Display formatted results
    display_results(xml_file)
    
    # Ask if user wants to see raw XML
    console = Console()
    if console.input("\nWould you like to see the raw XML? (y/n): ").lower() == 'y':
        formatted_xml = format_xml(xml_file)
        print("\nFormatted XML content:")
        print(formatted_xml)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 