# CSV Generator

A simple and flexible tool for generating CSV test data from YAML configuration files.

## Features

- 🎯 **Simple YAML Configuration** - Define your CSV structure using easy-to-read YAML
- 🔢 **Multiple Data Types** - Support for integers, floats, strings, booleans, dates, and choices
- 🎲 **Flexible Patterns** - Generate data using sequential, random, fixed, or list patterns
- 📊 **Customizable** - Control ranges, formats, and generation rules for each column
- ✅ **Tested** - Comprehensive test suite included

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wietsche/csv_generator.git
cd csv_generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python csv_generator.py <config.yaml> <output.csv>
```

Example:
```bash
python csv_generator.py examples/simple_config.yaml output.csv
```

## Configuration Format

Create a YAML configuration file that defines your CSV structure:

```yaml
num_rows: 10  # Number of data rows to generate

columns:
  - name: column_name      # Column header name
    type: integer          # Data type
    pattern: sequential    # Generation pattern
    # Additional options based on type and pattern
```

### Supported Data Types

#### Integer
```yaml
- name: user_id
  type: integer
  pattern: random
  min: 1        # Minimum value
  max: 1000     # Maximum value
```

#### Float
```yaml
- name: price
  type: float
  pattern: random
  min: 0.0
  max: 100.0
  decimals: 2   # Number of decimal places
```

#### String
```yaml
- name: username
  type: string
  pattern: random
  length: 10    # Length of generated string
```

#### Boolean
```yaml
- name: is_active
  type: boolean
  pattern: random
```

#### Date
```yaml
- name: created_date
  type: date
  pattern: random
  start_date: '2023-01-01'
  end_date: '2024-12-31'
  format: '%Y-%m-%d'  # Python strftime format
```

#### Choice
```yaml
- name: status
  type: choice
  pattern: random
  choices:
    - active
    - inactive
    - pending
```

### Supported Patterns

#### Sequential
Generate sequential values (typically for IDs):
```yaml
pattern: sequential
start: 1      # Starting value
step: 1       # Increment step
```

#### Random
Generate random values within constraints:
```yaml
pattern: random
# Additional options depend on data type
```

#### Fixed
Use the same value for all rows:
```yaml
pattern: fixed
value: 'constant_value'
```

#### List
Cycle through a list of values:
```yaml
pattern: list
values:
  - value1
  - value2
  - value3
```

## Examples

### Simple Example

**Configuration** (`examples/simple_config.yaml`):
```yaml
num_rows: 5

columns:
  - name: id
    type: integer
    pattern: sequential
    start: 1
    step: 1
  
  - name: username
    type: string
    pattern: random
    length: 8
  
  - name: age
    type: integer
    pattern: random
    min: 18
    max: 65
  
  - name: is_active
    type: boolean
    pattern: random
```

**Output**:
```csv
id,username,age,is_active
1,aBcD1234,42,True
2,XyZ98765,28,False
3,qWeRtY12,55,True
4,pLmNbV99,33,False
5,zXcVbNm1,61,True
```

### Advanced Example

See `examples/advanced_config.yaml` for a more comprehensive example with multiple data types and patterns.

## Running Tests

Run the test suite:
```bash
python test_csv_generator.py
```

Or with verbose output:
```bash
python test_csv_generator.py -v
```

## Use Cases

- Generate test data for database testing
- Create sample datasets for application development
- Produce mock data for API testing
- Generate datasets for performance testing
- Create reproducible test fixtures

## Requirements

- Python 3.6+
- PyYAML
- Faker (for future enhancements)

## License

This project is open source and available under the MIT License.
