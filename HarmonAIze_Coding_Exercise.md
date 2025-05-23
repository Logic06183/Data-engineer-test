# 🧪 HarmonAIze Data Engineering Mini-Task

## Goal
Create a Django-based data harmonisation system that can ingest and integrate clinical trial data and environmental data from different sources with varying schemas, and store it in a standardised format in a database.

## Detailed Task Description

### Overview
You will build a Django management command that:
1. Takes CSV data files and their corresponding YAML codebooks as input
2. Maps the data from different schemas to a common harmonised schema
3. Loads the transformed data into a Django model
4. Provides a summary of the ingestion process

### Specific Requirements

#### Data Harmonisation
- Two different clinical trial datasets with different column names and structures need to be mapped to a single harmonised schema
- Additionally, climate data needs to be integrated with the clinical trial data
- Use the provided `harmonized_clinical_schema.yaml` as the target schema for all datasets
- This schema defines how fields from each source dataset should be mapped to the common model
- The datasets should be joined using location identifiers and dates

#### Django Components
1. **Create a Django Model**:
   - Design a model that can store all fields defined in the harmonized schema
   - Include appropriate field types (CharField, DateField, IntegerField, etc.)
   - Add any necessary validation

2. **Implement a Management Command**:
   ```
   python manage.py ingest_data --csv_file=<path_to_csv> --codebook=<path_to_yaml>
   ```
   - The command should accept parameters for the CSV file and its corresponding codebook
   - It should detect which dataset is being processed and apply the appropriate mappings
   - Transform data as needed (e.g., converting "M"/"F" to "Male"/"Female")
   - Handle missing fields gracefully (some fields exist in only one dataset)

#### Data Processing Requirements
- Use the YAML codebook to determine how to map each CSV column to your model
- Apply any necessary data transformations defined in the harmonized schema
- Validate data before inserting into the database
- Handle errors gracefully and report them in the summary

---

## Sample Data Description

### Dataset 1: Clinical Trial
- File: `/sample_data/clinical_trial.csv`
- Codebook: `/sample_data/clinical_trial_codebook.yaml`
- Contains: patient ID, visit date, demographics, vital signs, adverse events, and site location

### Dataset 2: Clinical Trial 2
- File: `/sample_data/clinical_trial_2.csv`
- Codebook: `/sample_data/clinical_trial_2_codebook.yaml`
- Contains: subject ID, visit date, demographics, study group, adverse events, and center ID
- Note: Does not include vital signs data

### Dataset 3: Climate Data
- File: `/sample_data/climate_daily.csv`
- Codebook: `/sample_data/climate_daily_codebook.yaml`
- Contains: site ID, date, temperature, precipitation, humidity, air quality, and location ID
- Note: Contains environmental data that can be joined with clinical datasets

### Harmonised Schema
- File: `/harmonized_clinical_schema.yaml`
- Defines the common fields and mapping rules for all datasets
- Includes transformation rules where needed
- Provides a unified schema for clinical and environmental data

---

## Deliverables

1. **Django Model**:
   - A model class that can store all harmonized data

2. **Management Command**:
   - A command that processes either dataset according to specifications
   - Proper error handling and reporting

3. **Documentation**:
   - A README.md with:
     - Setup instructions
     - Command usage examples
     - Brief explanation of your approach
     - Any assumptions made

---

## Evaluation Criteria
- Code quality and organisation
- Proper implementation of data mapping and transformation
- Error handling and validation
- Documentation clarity
- Use of Github, 
- Grasp of Django

## Submission Instructions
- Fork this repository and implement your solution
- Create a pull request (PR) when you're ready to submit
- Include your name and contact information in the PR description
- Send the PR link to Nicholas Brink (Nicholas.Brink@witsphr.org) and Natasha Lalloo (Natasha.Lalloo@witsphr.org)

**Estimated time:** ~3 hours  
**Questions?** Contact Craig Parker (craig.parker@witsphr.org)
