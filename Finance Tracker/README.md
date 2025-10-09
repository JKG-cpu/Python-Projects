# 💰 Personal Finance Tracker

A terminal-based Python application that helps you manage your personal finances.  
Track income and expenses, set budgets, categorize spending, and visualize your financial habits — all in one place!

---

## 📌 Features

- ✅ Add and categorize transactions (income or expense)
- ✅ View monthly summaries and category-wise breakdowns
- ✅ Set monthly or category-specific budgets
- ✅ Alerts for exceeding budget limits
- ✅ Export transaction data to CSV
- ✅ Simple and intuitive command-line interface

---

## 🗂️ Data Storage

You can choose from:
- **JSON or CSV files** – For a lightweight, file-based approach
- **SQLite or TinyDB** – For structured, queryable data storage

---

## 📊 Visualizations (Optional Enhancements)

- Pie charts for spending by category
- Bar charts comparing income vs. expenses by month
- Libraries: `matplotlib`, `seaborn`, or `plotly`

---

## 🧰 Tech Stack

| Purpose              | Tool/Library       |
|----------------------|--------------------|
| Core Language        | Python 3.9+         |
| Data Management      | `pandas`, `sqlite3`, `TinyDB` |
| CLI Enhancements     | `argparse`, `click`, `rich`, `tabulate` |
| Data Visualization   | `matplotlib`, `seaborn`, `plotly` |
| Exporting Data       | Built-in `csv` module or `pandas` |

---

## 🚀 Stretch Goals

- 🔒 Add user authentication for multiple users
- 🖥️ Build a GUI using **Tkinter** or **PyQt**
- 🌐 Convert it to a web app using **Flask** or **FastAPI**
- 📦 Containerize with Docker
- 📤 Import real bank transaction CSVs
- 🌍 Deploy online (e.g., Heroku, Render, etc.)

---

## 🧠 Skills You'll Practice

- Python file handling & databases (CRUD operations)
- Working with structured data (`pandas`, SQL, JSON)
- Budgeting logic & conditional alerts
- Modular project architecture
- CLI/GUI development & UX design
- Data visualization

---

## 📁 Project Structure (Sample)

personal-finance-tracker/
<br>
│
├── data/ # Data files (CSV, JSON, or SQLite DB)
<br>
├── src/ # Core logic
<br>
│ ├── transactions.py # Add/view transactions
<br>
│ ├── budgets.py # Budget logic
<br>
│ ├── reports.py # Monthly/category summaries
<br>
│ └── visualizations.py # Charts (optional)
<br>
├── main.py # Entry point CLI
<br>
├── requirements.txt # Dependencies
<br>
└── README.md


---
