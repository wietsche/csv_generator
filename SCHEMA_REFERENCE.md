# YAML Configuration Schema Reference

This document provides a comprehensive reference for the CSV Generator YAML configuration format.

## Top-Level Configuration

```yaml
output_file_name: string       # Required: Base name for output file(s)
number_of_records: integer     # Required: Total number of records to generate
file_split_number: integer     # Optional: Number of files to split output (default: 1)
schema: array                  # Required: List of field definitions
```

## File Splitting Behavior

The `file_split_number` parameter controls how records are distributed:

- **file_split_number: 1** (default)
  - Output: `{output_file_name}.csv`
  - All records in a single file

- **file_split_number: N** (where N > 1)
  - Output: `{output_file_name}_1.csv`, `{output_file_name}_2.csv`, ..., `{output_file_name}_N.csv`
  - Records evenly distributed across N files
  - Example: 1000 records with file_split_number: 4 creates 4 files with 250 records each

## Schema Field Structure

Each field in the schema array must have:

```yaml
- name: string           # Required: Column name in CSV
  type: string          # Required: Data type
  generator: object     # Required: Generation configuration
```

## Data Types and Generators

### 1. Integer Type

#### Sequential Method
Generates consecutive integers.

```yaml
name: id
type: integer
generator:
  method: sequential
  start: 1              # Starting value (default: 1)
  step: 1               # Increment step (default: 1)
```

#### Random Method
Generates random integers within a range.

```yaml
name: quantity
type: integer
generator:
  method: random
  min: 0                # Minimum value (inclusive)
  max: 100              # Maximum value (inclusive)
```

### 2. Float Type

#### Random Method
Generates random floating-point numbers.

```yaml
name: price
type: float
generator:
  method: random
  min: 0.0              # Minimum value
  max: 1000.0           # Maximum value
  precision: 2          # Decimal places (default: 2)
```

### 3. String Type

#### Random Method (with source)
Uses predefined lists of realistic data.

```yaml
name: first_name
type: string
generator:
  method: random
  source: first_names   # Available sources:
                        # - first_names
                        # - last_names
                        # - full_names
                        # - company_names
                        # - product_names
                        # - city_names
                        # - country_names
                        # - street_names
```

#### Pattern Method
Generates strings using a pattern with variable substitution.

```yaml
name: username
type: string
generator:
  method: pattern
  pattern: "user_{id}"          # Variables reference other field names
                                 # Format specifiers supported: {id:05d}
```

#### Choice Method
Randomly selects from a predefined list.

```yaml
name: status
type: string
generator:
  method: choice
  choices:
    - active
    - inactive
    - pending
  weights: [0.7, 0.2, 0.1]      # Optional: probability weights
```

#### Fixed Method
Uses the same value for all records.

```yaml
name: category
type: string
generator:
  method: fixed
  value: "Electronics"
```

### 4. Email Type

#### Random Method
Generates realistic email addresses.

```yaml
name: email
type: email
generator:
  method: random
  domain: "example.com"         # Optional: specific domain
                                 # If omitted, uses common domains
```

### 5. Boolean Type

#### Random Method
Generates true/false values with configurable probability.

```yaml
name: is_active
type: boolean
generator:
  method: random
  probability: 0.8              # Probability of true (0.0 to 1.0)
                                 # Default: 0.5
```

### 6. Date Type

#### Random Method
Generates random dates within a range.

```yaml
name: created_at
type: date
generator:
  method: random
  format: "%Y-%m-%d"            # Python strftime format
                                 # Examples:
                                 # "%Y-%m-%d" -> 2024-01-15
                                 # "%Y-%m-%d %H:%M:%S" -> 2024-01-15 14:30:00
                                 # "%m/%d/%Y" -> 01/15/2024
  start_date: "2020-01-01"      # Range start (inclusive)
  end_date: "2024-12-31"        # Range end (inclusive)
```

#### Sequential Method
Generates dates in sequence.

```yaml
name: date
type: date
generator:
  method: sequential
  start_date: "2024-01-01"
  format: "%Y-%m-%d"
  increment: 1                   # Days to increment (default: 1)
```

## Complete Example

```yaml
output_file_name: "test_data"
number_of_records: 100
file_split_number: 2

schema:
  - name: id
    type: integer
    generator:
      method: sequential
      start: 1
  
  - name: username
    type: string
    generator:
      method: pattern
      pattern: "user_{id:04d}"
  
  - name: email
    type: email
    generator:
      method: random
      domain: "test.com"
  
  - name: first_name
    type: string
    generator:
      method: random
      source: first_names
  
  - name: last_name
    type: string
    generator:
      method: random
      source: last_names
  
  - name: age
    type: integer
    generator:
      method: random
      min: 18
      max: 80
  
  - name: balance
    type: float
    generator:
      method: random
      min: 0.0
      max: 10000.0
      precision: 2
  
  - name: is_premium
    type: boolean
    generator:
      method: random
      probability: 0.3
  
  - name: signup_date
    type: date
    generator:
      method: random
      format: "%Y-%m-%d"
      start_date: "2023-01-01"
      end_date: "2024-12-31"
  
  - name: status
    type: string
    generator:
      method: choice
      choices:
        - active
        - inactive
        - suspended
```

This configuration will:
- Generate 100 records
- Split output into 2 files: `test_data_1.csv` and `test_data_2.csv`
- Each file will contain 50 records
- Include all specified columns with appropriate data generation
