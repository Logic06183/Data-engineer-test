# 🧪 HarmonAIze Technical Exercise

## Fork-and-Extend: Backend Data Engineering Mini-Feature

### 🎯 Goal
Demonstrate your backend data engineering capability by building a small feature that integrates with the existing [HarmonAIze](https://github.com/drnicholasbrink/HarmonAIze) repository. This should reflect your ability to work with structured data, apply mapping logic, and output clean, harmonized results.

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
9. **Submit your assignment** by sending the link to your fork/branch to Craig Parker at [craig.parker@witsphr.org](mailto:craig.parker@witsphr.org).

If you have any questions or need clarification, please reach out to Craig directly.

---

## ✅ Build One Feature
Choose **one** of the following backend-focused features to build. It must:
- Use or respect the repo’s structure and goals,
- Be written in Python,
- Output harmonized results suitable for database ingestion (as CSV, JSON, or SQL-insertable format),
- Include logging and basic error handling.

### 🔧 Feature Options
#### 🔹 Option A: Harmonized Data Loader
- Read a sample CSV and YAML codebook (see `/sample_data/` for examples).
- Map variables using the YAML structure.
- Output a cleaned and harmonized `.csv` file.
- Clearly indicate unmapped variables.

#### 🔹 Option B: Mapping Summary Tool
- Parse a harmonization attempt (CSV or intermediate result).
- Output summary stats:
    - % mapped, % unmapped,
    - Any warnings (e.g., type mismatches, missing columns).

#### 🔹 Option C: Command-Line Ingestion Script
- Build a `ingest.py` CLI that:
    - Accepts file paths to CSV + YAML,
    - Performs mapping (reusing or simplifying logic),
    - Outputs a log + harmonized `.csv`.

---

## 🗂️ Sample Data

This repo includes synthetic sample data for assessment in `/sample_data/`:

- `clinical_trial.csv` & `clinical_trial_codebook.yaml`: Synthetic clinical trial data and codebook.
- `climate_yearly.csv` & `climate_codebook.yaml`: Synthetic yearly climate data and codebook.

You may use these for your HarmonAIze exercise, or create your own mock data if you prefer.

---

## 📂 Deliverables
- All code committed to your forked repo (in a new folder or branch).
- Updated or new `README.md`:
    - Explains the feature you built,
    - How to run it,
    - Notes any assumptions or mock data you created.
- (Optional) Short video walkthrough (5–10 min).
- (Optional) Dashboard: You may include a dashboard as an **output** of your project, but it should not be the main focus. The primary deliverable must be the backend data engineering work (data harmonization, mapping, etc.).

---

## 🚦 What Skills Are Being Tested?
This exercise is designed to assess your practical data engineering skills, including:
- Working with structured data (CSV, YAML)
- Data mapping and harmonization logic
- Outputting results suitable for database ingestion
- Database schema awareness (PostgreSQL is assumed, but you do NOT need to build a database)
- Logging and basic error handling

**Note:** The exercise is meant to be challenging but not overly difficult. Focus on clarity, correctness, and clean code. You are not expected to build a full database. Dashboards are allowed as an output, but should not be the main focus.

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
