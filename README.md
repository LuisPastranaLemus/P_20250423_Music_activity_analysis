# 🧭 Music Activity Analysis
Music activity difference bewteen in Springfield and Shelbyville cities.

---

## 🔍 Project Overview (P-20250423)

In this project, music preferences of the cities of Springfield and Shelbyville will be compared. Simulated-world online music data will be studied to test the hypothesis outlined below and compare user behavior in these two cities.

Hypothesis:   
User music activity varies by day of the week and city.

Key questions:

- Which days and time of the day have the most music activity?
- Which city has the most music activity?

---

## 🧮 Data Dictionary

Below is a data dictionary that lists the columns in the table and describes the data they contain.

- `music_project_en.csv` 
    - `'userID'`: uniquely identifies each user
    - `'Track'`: song title
    - `'artist'`: artist name
    - `'genre'`: music genre
    - `'City'`: user's city
    - `'time'`: time of day the track was played (HH:MM:SS)
    - `'Day'`: day of the week.

---

## 📚 Guided Foundations (Historical Context)

The notebook `00-guided-analysis_foundations.ipynb` reflects an early stage of my data analysis learning journey, guided by TripleTen. It includes data cleaning, basic EDA, and early feature exploration, serving as a foundational block before implementing the improved structure and methodology found in the main analysis.

---

## 📂 Project Structure

```bash
├── data/
│   ├── raw/              # Original dataset(s) in CSV format
│   ├── interim/          # Intermediate cleaned versions
│   └── processed/        # Final, ready-to-analyze dataset
│
├── notebooks/
│   ├── 00-guided-analysis_foundations.ipynb     ← Initial guided project (TripleTen)
│   ├── 01_cleaning.ipynb                        ← Custom cleaning 
│   ├── 02_feature_engineering.ipynb             ← Custom feature engineering
│   ├── 03_eda_and_insights.ipynb                ← Exploratory Data Analysis & visual storytelling
│   └── 04-sda_hypotheses.ipynb                  ← Business insights and hypothesis testing
│
├── src/
│   ├── init.py              # Initialization for reusable functions
│   ├── data_cleaning.py     # Data cleaning and preprocessing functions
│   ├── data_loader.py       # Loader for raw datasets
│   ├── eda.py               # Exploratory data analysis functions
│   ├── features.py          # Creation and transformation functions for new variables to support modeling and EDA
│   └── utils.py             # General utility functions for reusable helpers
│
├── outputs/
│   └── figures/          # Generated plots and visuals
│
├── requirements/
│   └── requirements.txt      # Required Python packages
│
├── .gitignore            # Files and folders to be ignored by Git
└── README.md             # This file
```
---

🛠️ Tools & Libraries

- Python 3.11
- os, pathlib, sys, pandas, NumPy, Matplotlib, seaborn, IPython.display, scipy.stats
- Jupyter Notebook
- Git & GitHub for version control

---

Explore the interactive Tableau dashboard on:   
[![View on Tableau Public](https://img.shields.io/badge/View%20Dashboard-Tableau%20Public-blue?logo=tableau)](https://public.tableau.com/views/Music_Activity_Shelbyville_Springfield/Dashboard1?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

## 📌 Notes

This project is part of a personal learning portfolio focused on developing strong skills in data analysis, statistical thinking, and communication of insights. Constructive feedback is welcome.

---

## 👤 Author   

##### Luis Sergio Pastrana Lemus   
##### Engineer pivoting into Data Science | Passionate about insights, structure, and solving real-world problems with data.   
##### [GitHub Profile](https://github.com/LuisPastranaLemus)   
##### 📍 Querétaro, México     
##### 📧 Contact: luis.pastrana.lemus@engineer.com   
---
