# Data Harmonization System

## Overview
This Django-based system harmonizes clinical trial and environmental data from different sources with varying schemas into a standardized database format. It supports:
- Multiple clinical trial data formats
- Environmental/climate data integration
- Automated data type detection and transformation
- Comprehensive validation and error reporting

## Setup Instructions

1. Clone the repository
2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install required dependencies:
   ```powershell
   pip install django pandas pyyaml
   ```

4. Run database migrations:
   ```powershell
   python manage.py migrate
   ```

## Data Ingestion Command

The system provides a Django management command for data ingestion:

```powershell
python manage.py ingest_data --csv_file=<path_to_csv> --codebook=<path_to_yaml>
```

### Examples

1. Ingest clinical trial data:
   ```powershell
   python manage.py ingest_data --csv_file=../sample_data/clinical_trial.csv --codebook=../sample_data/clinical_trial_codebook.yaml
   ```

2. Ingest additional clinical data with different schema:
   ```powershell
   python manage.py ingest_data --csv_file=../sample_data/clinical_trial_2.csv --codebook=../sample_data/clinical_trial_2_codebook.yaml
   ```

3. Add environmental data:
   ```powershell
   python manage.py ingest_data --csv_file=../sample_data/climate_daily.csv --codebook=../sample_data/climate_daily_codebook.yaml
   ```

## How It Works

### 1. Data Type Detection
The system automatically detects whether the input data is clinical or climate data based on column indicators:
- Clinical indicators: patient_id, subject_id, adverse_event
- Climate indicators: daily_temp_c, precip_mm, humidity_pct, aqi

### 2. Data Mapping
The system maps source data to a harmonized schema using:
- YAML codebooks defining field mappings and transformations
- Automatic field name resolution (e.g., patient_id → participant_id)
- Data type conversions and validations
- Value transformations (e.g., "M" → "Male")

### 3. Data Integration
- Clinical data: Creates new records with unique participant/visit combinations
- Climate data: Enriches existing clinical records by matching dates and locations
- Handles duplicates and updates appropriately

### 4. Field Mappings
The system supports mapping different source fields to standardized target fields:

| Target Field | Source Fields |
|--------------|---------------|
| participant_id | patient_id, subject_id |
| visit_date | visit_date, date |
| location_id | site_location, center_id, location_id |
| age | age, age_years |
| sex | sex (with M/F transformation) |
| study_group | arm, trial_group |
| body_temperature | temperature_c |
| temperature | daily_temp_c |
| precipitation | precip_mm |
| humidity | humidity_pct |
| air_quality_index | aqi |

### 5. Validation
The system performs multiple validation checks:
- Required fields presence
- Data type validation
- Allowed values validation
- Duplicate detection
- Referential integrity

### 6. Error Handling
Comprehensive error tracking and reporting:
- Missing required fields
- Type conversion errors
- Validation failures
- Database insertion errors
- Detailed error summaries

## Output

The command provides detailed feedback including:
- Data loading statistics
- Transformation results
- Error reports
- Database operation summaries

Example output:
```
=== Ingestion Summary ===
Input Data:
- Total rows in CSV: 6
- Columns found: patient_id, visit_date, age, sex, arm...
Data Transformation:
- Records successfully mapped: 6
- Records with missing required fields: 0
- Type conversion errors: 0
- Validation errors: 0
Database Insertion:
- Records created: 6
- Duplicates skipped: 0
- Insert errors: 0
```
