# 🧭 Music Activity Analysis
In this project, music preferences of the cities of Springfield and Shelbyville will be compared. Online music data will be studied to test the hypothesis "User activity varies by day of the week and city." and user behavior in these two cities will be compared.

---

## 🔍 Project Overview (P-20250423)

Simulated-world online music streaming data will be explored and information processed about the listening habits of users in two cities: Springfield and Shelbyville.

This project aims to:

- Clean and preprocess simulated-world data with formatting inconsistencies (e.g. non-standard separators, missing headers, strange decimal formats, etc.)
- Perform Exploratory Data Analysis (EDA) with visual tools like boxplots, histograms, and frequency plots.
- Handle missing data, detect duplicates (explicit and implicit), and manage categorical and quantitative variables.
- Conduct statistical hypothesis testing to assess significant patterns.

---

## 🧮 Data Dictionary

- 'userID': uniquely identifies each user;
- 'Track': song title;
- 'artist': artist name;
- 'genre': music genre;
- 'City': user's city;
- 'time': time of day the track was played (HH:MM:SS);
- 'Day': day of the week.

---

## 📂 Project Structure

```bash
├── data/
│   ├── raw/              # Original dataset(s) in CSV format
│   ├── interim/          # Intermediate cleaned versions
│   └── processed/        # Final, ready-to-analyze dataset
│
├── notebooks/
│   └── 01-eda.ipynb     # Main analysis notebook
│
├── src/
│   └── clean_data.py     # Data cleaning and preprocessing functions
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

## 📌 Notes

This project is part of a personal learning portfolio focused on developing strong skills in data analysis, statistical thinking, and communication of insights. Constructive feedback is welcome.

---

🧑‍💻 Author
Luis Sergio Pastrana Lemus
Engineer pivoting into Data Science | Passionate about insights, structure, and solving real-world problems with data.

---
