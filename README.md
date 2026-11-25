# 🌿 Ayurvedic Prakriti Classification

### Machine Learning-Based Personalized Psychological Treatment Recommendation System

## 📌 Project Overview

The **Ayurvedic Prakriti Classification System** is a Machine Learning-based application designed to classify an individual's Ayurvedic Prakriti and provide personalized psychological wellness recommendations.

The project combines Ayurvedic concepts with Machine Learning techniques to analyze lifestyle, psychological, and wellness-related parameters and generate personalized recommendations.

## 🎯 Objectives

- Classify individuals based on Ayurvedic Prakriti.
- Analyze psychological wellness indicators such as stress, anxiety, and depression.
- Apply Machine Learning algorithms for classification.
- Generate personalized recommendations based on the classification results.
- Provide an easy-to-use graphical interface.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **Data Processing:** Pandas, NumPy
- **GUI Development:** Tkinter
- **Model Persistence:** Pickle
- **Data Visualization:** Matplotlib (if used in the implementation)

## 🧠 Machine Learning Algorithms

The project experiments with multiple classification algorithms:

- Random Forest Classifier
- Extra Trees Classifier
- SGD Classifier
- Passive Aggressive Classifier
- Quadratic Discriminant Analysis (QDA)
- Multi-Layer Perceptron (MLP)
- Voting Classifier

### Model Performance

The experimental results include:

| Algorithm | Accuracy |
|---|---:|
| Random Forest | 98.15% |
| Extra Trees | 98.15% |
| SGD | 17.85% |
| Passive Aggressive | 19.69% |
| QDA | 59.38% |
| MLP | 37.23% |

A Voting Classifier combining Extra Trees, Random Forest, and MLP was also explored.

*These are experimental results from the project dataset, not independently validated clinical results.*

## 📂 Project Structure

```text
Ayurvedic-Prakriti-Classification/
│
├── Dataset/
│   ├── ayurveda_psychology_wellness_dataset.csv
│   └── testdata.csv
│
├── model/
│
├── models/
│
├── Main.py
├── precautions.py
├── recommendations.py
├── bg.png
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd Ayurvedic-Prakriti-Classification
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python Main.py
```

## 💡 Key Features

- Ayurvedic Prakriti classification.
- Psychological wellness parameter analysis.
- Machine Learning-based prediction.
- Personalized recommendations.
- Graphical user interface using Tkinter.

## 🚀 Future Enhancements

- Improve classification performance.
- Expand and validate the dataset.
- Enhance recommendation accuracy.
- Develop a web-based application.
- Integrate additional Machine Learning and Deep Learning techniques.

## ⚠️ Disclaimer

This project is developed for educational and research purposes. Its predictions and recommendations are not a substitute for professional medical or psychological diagnosis and treatment.

## 👩‍💻 Developer

**Amulya Reddy**

B.Tech – Computer Science and Engineering (AI & ML)

GitHub: [Amulyareddy22](https://github.com/Amulyareddy22)

---

⭐ If you find this project interesting, consider starring the repository!
