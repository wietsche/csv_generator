#!/usr/bin/env python3
"""
CSV Generator - Generate CSV test data from YAML configuration
"""
import csv
import sys
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List
import yaml


class CSVGenerator:
    """Generate CSV data based on YAML configuration."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the CSV generator with configuration.
        
        Args:
            config: Dictionary containing CSV generation configuration
        """
        self.config = config
        self.columns = config.get('columns', [])
        self.num_rows = config.get('num_rows', 10)
        
    def generate_value(self, column_def: Dict[str, Any], row_index: int) -> Any:
        """
        Generate a value for a column based on its definition.
        
        Args:
            column_def: Dictionary containing column definition
            row_index: Current row index (0-based)
            
        Returns:
            Generated value for the column
        """
        col_type = column_def.get('type', 'string')
        pattern = column_def.get('pattern', 'random')
        
        # Handle fixed values
        if pattern == 'fixed':
            return column_def.get('value', '')
        
        # Handle sequential patterns
        if pattern == 'sequential':
            start = column_def.get('start', 1)
            step = column_def.get('step', 1)
            return start + (row_index * step)
        
        # Handle random patterns based on type
        if pattern == 'random':
            if col_type == 'integer':
                min_val = column_def.get('min', 1)
                max_val = column_def.get('max', 100)
                return random.randint(min_val, max_val)
            
            elif col_type == 'float':
                min_val = column_def.get('min', 0.0)
                max_val = column_def.get('max', 100.0)
                decimals = column_def.get('decimals', 2)
                value = random.uniform(min_val, max_val)
                return round(value, decimals)
            
            elif col_type == 'boolean':
                return random.choice([True, False])
            
            elif col_type == 'date':
                start_date = column_def.get('start_date', '2020-01-01')
                end_date = column_def.get('end_date', '2024-12-31')
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                delta = end - start
                random_days = random.randint(0, delta.days)
                random_date = start + timedelta(days=random_days)
                date_format = column_def.get('format', '%Y-%m-%d')
                return random_date.strftime(date_format)
            
            elif col_type == 'choice':
                choices = column_def.get('choices', ['option1', 'option2'])
                return random.choice(choices)
            
            else:  # string type
                length = column_def.get('length', 10)
                chars = column_def.get('charset', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                return ''.join(random.choice(chars) for _ in range(length))
        
        # Handle list pattern (cycle through provided values)
        if pattern == 'list':
            values = column_def.get('values', ['value'])
            return values[row_index % len(values)]
        
        return ''
    
    def generate(self) -> List[List[Any]]:
        """
        Generate CSV data based on configuration.
        
        Returns:
            List of rows, where each row is a list of values
        """
        # Generate header
        headers = [col.get('name', f'column_{i}') for i, col in enumerate(self.columns)]
        rows = [headers]
        
        # Generate data rows
        for i in range(self.num_rows):
            row = []
            for col_def in self.columns:
                value = self.generate_value(col_def, i)
                row.append(value)
            rows.append(row)
        
        return rows
    
    def write_csv(self, filename: str):
        """
        Generate and write CSV data to a file.
        
        Args:
            filename: Output CSV filename
        """
        rows = self.generate()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)


def load_config(config_file: str) -> Dict[str, Any]:
    """
    Load YAML configuration from file.
    
    Args:
        config_file: Path to YAML configuration file
        
    Returns:
        Configuration dictionary
    """
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 3:
        print("Usage: python csv_generator.py <config.yaml> <output.csv>")
        print("\nGenerates CSV test data from a YAML configuration file.")
        sys.exit(1)
    
    config_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        config = load_config(config_file)
        generator = CSVGenerator(config)
        generator.write_csv(output_file)
        print(f"Successfully generated CSV file: {output_file}")
        print(f"Rows generated: {generator.num_rows}")
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in configuration file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
