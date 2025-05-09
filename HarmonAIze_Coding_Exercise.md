# 🧪 HarmonAIze Technical Exercise

## Fork-and-Extend: Backend Data Engineering Mini-Feature

### 🎯 Goal
Demonstrate your backend data engineering and Django skills by building a feature that integrates harmonized structured data (CSV/YAML) into a Django/PostgreSQL database. You will design Django models, implement mapping/ingestion logic, and ensure the data is ready for use within a Django environment. This exercise reflects real-world backend work with Django, schema design, and data harmonization.

---

## 📋 Task Instructions
⏱ **Estimated time**: ~3 hours  
🔗 **Start here**: Fork and clone the HarmonAIze repo into your GitHub account.

---

## 📝 Step-by-Step Submission Checklist

1. **Fork the HarmonAIze repo** to your own GitHub account.
2. **Clone your fork** to your local machine.
3. **Create a new folder or branch** for your solution.
4. **Choose ONE feature** from the options below and implement it in Python.
5. **Use the sample data** in `/sample_data/` or create your own mock data if you prefer.
6. **Commit all your code and documentation** to your forked repo.
7. **Update or create a `README.md`** in your solution folder/branch:
    - Explain which feature you built,
    - How to run your code,
    - Any assumptions or mock data you created.
8. **Push your changes** to your forked repo on GitHub.
9. **Submit your assignment** by sending the link to your fork/branch to Nicholas Brink ([Nicholas.Brink@witsphr.org](mailto:Nicholas.Brink@witsphr.org)) and Natasha Lalloo ([Natasha.Lalloo@witsphr.org](mailto:Natasha.Lalloo@witsphr.org)).

A `README.md` is required in your solution folder/branch. It should:
- Explain which feature you built
- How to run your code
- Any assumptions or mock data you created

If you have any technical questions or need help, please reach out to Craig Parker ([craig.parker@witsphr.org](mailto:craig.parker@witsphr.org)).

---

## ✅ Build One Feature
Choose **one** of the following Django backend–focused features to build. You must use Django models and ORM for data ingestion and schema design:

### 🔧 Feature Options
#### 🔹 Option A: Harmonized Data Loader (Django)
- Define Django models for the harmonized data (based on the codebook/YAML).
- Read a sample CSV and YAML codebook (see `/sample_data/`).
- Map and harmonize variables using the YAML structure.
- Load the cleaned data into the Django database via ORM.
- Clearly indicate unmapped variables (e.g., in logs or ingestion summary).

#### 🔹 Option B: Mapping Summary Tool (Django)
- After harmonization and ingestion, provide a Django management command or script that:
    - Outputs summary stats: % mapped, % unmapped, type mismatches, missing columns, etc.
    - Optionally, exposes this as a Django admin action or view.

#### 🔹 Option C: Django Command-Line Ingestion Script
- Build a Django management command (`python manage.py ingest_data`) that:
    - Accepts file paths to CSV + YAML,
    - Performs mapping and loads data into the Django database,
    - Outputs a log and summary.

---

## 🗂️ Sample Data

This repo includes synthetic sample data for assessment in `/sample_data/`:

- `clinical_trial.csv` & `clinical_trial_codebook.yaml`: Synthetic clinical trial data and codebook.
- `climate_yearly.csv` & `climate_codebook.yaml`: Synthetic yearly climate data and codebook.

You may use these for your HarmonAIze exercise, or create your own mock data if you prefer.

---

## 📂 Deliverables
- All code committed to your forked repo (in a new folder or branch).
- Django project with models, migration files, and ingestion logic.
- Updated or new `README.md`:
    - Explains your Django model choices and feature,
    - How to run migrations and ingestion,
    - Notes any assumptions or mock data you created.
- (Optional) Short video walkthrough (5–10 min).
- (Optional) Dashboard or Django admin view: Allowed as an output, but not the main focus. The primary deliverable must be the backend Django data engineering work (harmonization, mapping, ingestion, schema design).

---

## 🚦 What Skills Are Being Tested?
This exercise is designed to assess your practical Django data engineering skills, including:
- Django model and schema design (normalized, clear, ready for PostgreSQL)
- Data mapping and harmonization logic
- Loading structured data into Django ORM
- Logging, error handling, and reporting
- (Optional) Django admin or dashboard integration

**Note:** The exercise is meant to be challenging but not overly difficult. Focus on clarity, correctness, and clean code. You are not expected to build a full web app or dashboard. Dashboards are allowed as an output, but should not be the main focus.

---

## 🚫 Please Do Not
- Submit a dashboard as your primary deliverable — the main focus must be backend data engineering.
- Change the core logic unless clearly justified.
- Create unrelated schemas or use SQLite (PostgreSQL is the assumed backend).

---

## ❓ Questions or Help?
If you have any issues or questions, please contact Craig Parker at [craig.parker@witsphr.org](mailto:craig.parker@witsphr.org).

---

## ✅ Compatibility and Feasibility
This exercise is designed to be compatible with the existing [HarmonAIze](https://github.com/drnicholasbrink/HarmonAIze) repository. The tasks described (data loading, mapping, harmonization, CLI ingestion, and summary reporting) are all possible within the repo’s structure, using Python and the provided sample data. If you encounter any blockers or repo-specific issues, please reach out for support.
