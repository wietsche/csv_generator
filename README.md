# CSV Generator

A flexible tool for generating CSV test data from YAML configuration files.

## YAML Configuration Structure

The YAML configuration file defines how CSV test data should be generated. It consists of the following main sections:

### Configuration Parameters

- **`output_file_name`** (required): The base name for the output CSV file(s) without extension
- **`number_of_records`** (required): Total number of data records to generate
- **`file_split_number`** (optional, default: 1): Number of files to split the output into
  - If set to 1 (default): All records in a single file named `{output_file_name}.csv`
  - If set to N > 1: Records distributed across N files named `{output_file_name}_1.csv`, `{output_file_name}_2.csv`, etc.
- **`schema`** (required): List of field definitions for the CSV columns

### Schema Field Definition

Each field in the schema defines a column in the generated CSV:

```yaml
- name: field_name          # Column name
  type: data_type           # Data type (see supported types below)
  generator:                # Generator configuration (type-specific)
    method: generation_method
    # Additional parameters based on method
```

### Supported Data Types

#### Integer
```yaml
type: integer
generator:
  method: sequential    # Generate sequential numbers
  start: 1             # Starting value
```
```yaml
type: integer
generator:
  method: random       # Generate random integers
  min: 1              # Minimum value
  max: 100            # Maximum value
```

#### Float
```yaml
type: float
generator:
  method: random
  min: 0.0
  max: 100.0
  precision: 2        # Decimal places
```

#### String
```yaml
type: string
generator:
  method: random
  source: first_names  # Use predefined source (first_names, last_names, full_names, company_names, product_names, etc.)
```
```yaml
type: string
generator:
  method: pattern
  pattern: "user_{id}"  # Pattern with variable substitution
```
```yaml
type: string
generator:
  method: choice
  choices:             # Pick randomly from list
    - Option1
    - Option2
    - Option3
```
```yaml
type: string
generator:
  method: fixed
  value: "Fixed Value"  # Same value for all records
```

#### Email
```yaml
type: email
generator:
  method: random
  domain: "example.com"  # Optional: specific domain
```

#### Boolean
```yaml
type: boolean
generator:
  method: random
  probability: 0.7      # Probability of true (0.0 to 1.0)
```

#### Date
```yaml
type: date
generator:
  method: random
  format: "%Y-%m-%d"           # Date format
  start_date: "2020-01-01"     # Start range
  end_date: "2024-12-31"       # End range
```

## Example Configurations

### Simple Example
See `examples/simple.yaml` for a basic configuration generating 10 records.

### User Data Example
See `examples/users.yaml` for generating user data with various field types.

### Product Data Example
See `examples/products.yaml` for generating product catalog data.

### Large Dataset with Splitting
See `examples/large_dataset.yaml` for generating 1000 records split across 5 files.

## Configuration Reference

For a complete configuration reference with all supported options, see `config.schema.yaml`.
