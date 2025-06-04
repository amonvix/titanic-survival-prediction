# 🧠 Titanic Survival Prediction – Data Science Project

This project uses a structured machine learning pipeline to predict passenger survival on the Titanic, using open data and popular Python libraries.

## 📚 Technologies Used

- **Python** (v3.12)
- **Pandas**, **NumPy** – data manipulation
- **Matplotlib**, **Seaborn** – data visualization
- **Scikit-learn** – machine learning
- **TensorFlow**, **Keras**, **PyTorch** – deep learning (to be added)
- **Jupyter** – interactive development

## 📁 Project Structure

titanic-survival-prediction/
├── data/
│ ├── titanic.csv # Raw dataset
│ └── titanic_clean.csv # Cleaned dataset
├── scripts/
│ ├── load_dataset.py # Download and save dataset
│ ├── analyze_dataset.py # Initial analysis and profiling
│ ├── clean_dataset.py # Preprocessing and feature formatting
│ └── visualize_dataset.py # Exploratory visualizations
├── requirements.txt
├── README.md
└── venv/


## ✅ Completed Tasks

- [x] Project setup and virtual environment
- [x] Required libraries installed and frozen in `requirements.txt`
- [x] Raw data collected and saved to local directory
- [x] Dataset analyzed with Pandas and statistics reviewed
- [x] Null values handled and categorical features encoded
- [x] Core exploratory visualizations plotted and reviewed

## 🧪 Upcoming Work

- [ ] Train predictive model using Scikit-learn
- [ ] Evaluate model performance with multiple metrics
- [ ] Experiment with TensorFlow/Keras and PyTorch implementations
- [ ] Wrap model in a Django REST API for web deployment

## 🧬 How to Run Locally

```bash
# Step 1: Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Step 2: Run scripts
python scripts/load_dataset.py
python scripts/analyze_dataset.py
python scripts/clean_dataset.py
python scripts/visualize_dataset.py

This project is part of a broader portfolio aimed at showcasing skills in data analysis, model development, and clean code practices for real-world machine learning scenarios.