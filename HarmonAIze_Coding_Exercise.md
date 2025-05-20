# 🧪 HarmonAIze Data Engineering Mini-Task

**Goal:**  
Write a Django management command (`python manage.py ingest_data`) that loads data from a CSV file, using a YAML codebook for mapping, into a simple Django model.

---

## What to Do

- Use the provided sample data:
  - `/sample_data/clinical_trial.csv`
  - `/sample_data/clinical_trial_codebook.yaml`
- Implement a Django model to store the harmonized data.
- Your command should:
  - Take the CSV and YAML file paths as input.
  - Map CSV columns to model fields using the codebook.
  - Load the data into the database.
  - Print a summary: number of records loaded, unmapped columns, and any errors.

---

## Deliverables

- Django management command for ingestion
- Django model for the data
- Short `README.md` with:
  - How to run your command
  - Example usage

---

**Estimated time:** ~1 hour  
**Questions?** Contact Craig Parker (craig.parker@witsphr.org)
