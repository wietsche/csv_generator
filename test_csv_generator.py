#!/usr/bin/env python3
"""
Tests for CSV Generator
"""
import os
import csv
import tempfile
import unittest
from csv_generator import CSVGenerator, load_config


class TestCSVGenerator(unittest.TestCase):
    """Test cases for CSVGenerator class."""
    
    def test_sequential_integer(self):
        """Test sequential integer generation."""
        config = {
            'num_rows': 5,
            'columns': [
                {'name': 'id', 'type': 'integer', 'pattern': 'sequential', 'start': 1, 'step': 1}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        self.assertEqual(len(rows), 6)  # header + 5 data rows
        self.assertEqual(rows[0], ['id'])
        self.assertEqual(rows[1], [1])
        self.assertEqual(rows[2], [2])
        self.assertEqual(rows[5], [5])
    
    def test_fixed_value(self):
        """Test fixed value generation."""
        config = {
            'num_rows': 3,
            'columns': [
                {'name': 'company', 'type': 'string', 'pattern': 'fixed', 'value': 'Acme Corp'}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        self.assertEqual(len(rows), 4)  # header + 3 data rows
        self.assertEqual(rows[1], ['Acme Corp'])
        self.assertEqual(rows[2], ['Acme Corp'])
        self.assertEqual(rows[3], ['Acme Corp'])
    
    def test_random_integer_range(self):
        """Test random integer within range."""
        config = {
            'num_rows': 10,
            'columns': [
                {'name': 'age', 'type': 'integer', 'pattern': 'random', 'min': 1, 'max': 10}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        # Check all values are within range
        for i in range(1, len(rows)):
            value = rows[i][0]
            self.assertGreaterEqual(value, 1)
            self.assertLessEqual(value, 10)
    
    def test_list_pattern(self):
        """Test list pattern cycling through values."""
        config = {
            'num_rows': 5,
            'columns': [
                {'name': 'role', 'type': 'string', 'pattern': 'list', 
                 'values': ['admin', 'user', 'moderator']}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        self.assertEqual(rows[1], ['admin'])
        self.assertEqual(rows[2], ['user'])
        self.assertEqual(rows[3], ['moderator'])
        self.assertEqual(rows[4], ['admin'])  # cycles back
        self.assertEqual(rows[5], ['user'])
    
    def test_choice_pattern(self):
        """Test choice pattern selects from choices."""
        config = {
            'num_rows': 10,
            'columns': [
                {'name': 'status', 'type': 'choice', 'pattern': 'random', 
                 'choices': ['active', 'inactive']}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        # Check all values are from the choices
        for i in range(1, len(rows)):
            value = rows[i][0]
            self.assertIn(value, ['active', 'inactive'])
    
    def test_multiple_columns(self):
        """Test generation with multiple columns."""
        config = {
            'num_rows': 3,
            'columns': [
                {'name': 'id', 'type': 'integer', 'pattern': 'sequential', 'start': 1, 'step': 1},
                {'name': 'company', 'type': 'string', 'pattern': 'fixed', 'value': 'Acme'},
                {'name': 'active', 'type': 'boolean', 'pattern': 'random'}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        self.assertEqual(len(rows), 4)  # header + 3 data rows
        self.assertEqual(rows[0], ['id', 'company', 'active'])
        self.assertEqual(rows[1][0], 1)
        self.assertEqual(rows[1][1], 'Acme')
        self.assertIn(rows[1][2], [True, False])
    
    def test_write_csv_file(self):
        """Test writing CSV to file."""
        config = {
            'num_rows': 2,
            'columns': [
                {'name': 'id', 'type': 'integer', 'pattern': 'sequential', 'start': 1, 'step': 1},
                {'name': 'name', 'type': 'string', 'pattern': 'fixed', 'value': 'Test'}
            ]
        }
        generator = CSVGenerator(config)
        
        # Use temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            temp_file = f.name
        
        try:
            generator.write_csv(temp_file)
            
            # Read back and verify
            with open(temp_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 3)  # header + 2 data rows
                self.assertEqual(rows[0], ['id', 'name'])
                self.assertEqual(rows[1], ['1', 'Test'])
                self.assertEqual(rows[2], ['2', 'Test'])
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_random_string_generation(self):
        """Test random string generation."""
        config = {
            'num_rows': 5,
            'columns': [
                {'name': 'code', 'type': 'string', 'pattern': 'random', 'length': 10}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        # Check all strings have correct length
        for i in range(1, len(rows)):
            value = rows[i][0]
            self.assertEqual(len(value), 10)
    
    def test_float_generation(self):
        """Test float generation with decimals."""
        config = {
            'num_rows': 5,
            'columns': [
                {'name': 'price', 'type': 'float', 'pattern': 'random', 
                 'min': 0.0, 'max': 100.0, 'decimals': 2}
            ]
        }
        generator = CSVGenerator(config)
        rows = generator.generate()
        
        # Check all floats are within range and properly rounded
        for i in range(1, len(rows)):
            value = rows[i][0]
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 100.0)
            # Check that rounding to 2 decimals doesn't change the value
            self.assertEqual(value, round(value, 2))


if __name__ == '__main__':
    unittest.main()
