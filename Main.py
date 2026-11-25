import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from recommendations import generate_recommendations

# -------------------------
# Training Function
# -------------------------
def train_models(dataset_path=r"C:\\Users\\pasun\\OneDrive\\Desktop\\my_project\\B9 - Ayurvedic prakriti classification\\Dataset\\ayurveda_psychology_wellness_dataset.csv"):
    df = pd.read_csv(dataset_path)
    target = "prakriti"

    features = [
        'age','gender','stress_level','anxiety_level','depression_score',
        'maslow_physiological','maslow_safety','maslow_social',
        'maslow_esteem','maslow_self_actualization',
        'sleep_hours','exercise_frequency','diet_type',
        'caffeine_intake','screen_time_hours'
    ]

    X = df[features].copy()
    y = df[target]

    # Encode categorical columns
    categorical_cols = ['gender', 'diet_type']
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])

    # Encode target
    y = LabelEncoder().fit_transform(y)

    # Scale numeric features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train/test split
    x_train, x_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    # Define base models
    log_reg = LogisticRegression(max_iter=1000)
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    svm = SVC(probability=True)

    # Fit base models
    log_reg.fit(x_train, y_train)
    rf.fit(x_train, y_train)
    svm.fit(x_train, y_train)

    # Create ensemble (soft voting)
    ensemble = VotingClassifier(
        estimators=[('lr', log_reg), ('rf', rf), ('svm', svm)],
        voting='soft'
    )
    ensemble.fit(x_train, y_train)

    # Collect results with full metrics
    results = {}
    models = {
        "Logistic Regression": log_reg,
        "Random Forest": rf,
        "SVM": svm,
        "Ensemble": ensemble
    }

    for name, model in models.items():
        y_pred = model.predict(x_test)
        results[name] = {
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred, average="weighted"),
            "Recall": recall_score(y_test, y_pred, average="weighted"),
            "F1": f1_score(y_test, y_pred, average="weighted")
        }

    return ensemble, scaler, results

# -------------------------
# GUI Setup
# -------------------------
root = tk.Tk()
root.title("🌿 Ayurvedic Prakriti Dashboard 🌿")
root.geometry("1100x700")

# Background Image
bg_image = Image.open(r"C:\\Users\\pasun\\OneDrive\\Desktop\\my_project\\B9 - Ayurvedic prakriti classification\\bg.png")
bg_image = bg_image.resize((1100, 700))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=1100, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Heading pinned at top
tk.Label(root, text="🌿 Ayurvedic Prakriti Dashboard 🌿",
         font=("Helvetica", 22, "bold"), fg="#2e8b57", bg="#f0f0f0").place(relx=0.3, rely=0.01)

# Semi-transparent overlay
overlay = tk.Frame(root, bg="#ffffff", bd=0)
overlay.place(relx=0.02, rely=0.08, relwidth=0.96, relheight=0.9)
overlay.configure(bg="#ffffff", highlightbackground="#2e8b57", highlightthickness=2)

# Notebook Tabs
notebook = ttk.Notebook(overlay)
frame_prediction = ttk.Frame(notebook)
frame_recommendations = ttk.Frame(notebook)
frame_precautions = ttk.Frame(notebook)
frame_metrics = ttk.Frame(notebook)

notebook.add(frame_prediction, text="Prediction")
notebook.add(frame_recommendations, text="Recommendations")
notebook.add(frame_precautions, text="Precautions")
notebook.add(frame_metrics, text="Training Results")
notebook.pack(expand=True, fill="both")

# -------------------------
# Metrics Tab
# -------------------------
def show_metrics(results):
    tree = ttk.Treeview(frame_metrics, columns=("Model","Accuracy","Precision","Recall","F1"), show="headings")
    for col in ("Model","Accuracy","Precision","Recall","F1"):
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True)

    for model_name, metrics in results.items():
        tree.insert("", "end", values=(
            model_name,
            metrics["Accuracy"],
            metrics["Precision"],
            metrics["Recall"],
            metrics["F1"]
        ))

    df_results = pd.DataFrame(results).T
    fig, ax = plt.subplots(figsize=(6,4))
    df_results[["Accuracy","F1"]].plot(kind="bar", ax=ax)
    ax.set_title("Model Performance Comparison")
    canvas = FigureCanvasTkAgg(fig, master=frame_metrics)
    canvas.draw()
    canvas.get_tk_widget().pack()

# -------------------------
# Recommendations Tab
# -------------------------
def show_recommendations(prakriti_type, recs):
    for widget in frame_recommendations.winfo_children():
        widget.destroy()
    tk.Label(frame_recommendations, text=f"🌿 Recommendations for {prakriti_type}",
             font=("Helvetica", 18, "bold"), fg="#2e8b57").pack(pady=10)
    # Ayurveda
    tk.Label(frame_recommendations, text="🌿 Ayurveda", font=("Helvetica", 16, "bold"), fg="#006400").pack(anchor="w", pady=5)
    for herb in recs["Ayurveda"]["herbs"]:
        tk.Label(frame_recommendations, text=f"- {herb}", font=("Helvetica", 12)).pack(anchor="w")
    tk.Label(frame_recommendations, text=f"Recipe: {recs['Ayurveda']['recipe']}", font=("Helvetica", 12)).pack(anchor="w")
    tk.Label(frame_recommendations, text=f"Precautions: {', '.join(recs['Ayurveda']['warnings'])}", font=("Helvetica", 12), fg="red").pack(anchor="w")
    # Healthcare
    tk.Label(frame_recommendations, text="💊 Healthcare", font=("Helvetica", 16, "bold"), fg="#8B0000").pack(anchor="w", pady=5)
    for tip in recs["Healthcare"]:
        tk.Label(frame_recommendations, text=f"- {tip}", font=("Helvetica", 12)).pack(anchor="w")
    # Exercise
    tk.Label(frame_recommendations, text="🧘 Exercise", font=("Helvetica", 16, "bold"), fg="#00008B").pack(anchor="w", pady=5)
    for ex in recs["Exercise"]:
        tk.Label(frame_recommendations, text=f"- {ex}", font=("Helvetica", 12)).pack(anchor="w")
    # Lifestyle
    tk.Label(frame_recommendations, text="🏡 Lifestyle", font=("Helvetica", 16, "bold"), fg="#FF8C00").pack(anchor="w", pady=5)
    for life in recs["Lifestyle"]:
        tk.Label(frame_recommendations, text=f"- {life}", font=("Helvetica", 12)).pack(anchor="w")

# -------------------------
# Precautions Tab
# -------------------------
def show_precautions(prakriti_type, recs):
    for widget in frame_precautions.winfo_children():
        widget.destroy()
    tk.Label(frame_precautions, text=f"⚠️ Precautions for {prakriti_type}",
             font=("Helvetica", 18, "bold"), fg="#8B0000").pack(pady=10)
    for warning in recs["Ayurveda"]["warnings"]:
        tk.Label(frame_precautions, text=f"- {warning}", font=("Helvetica", 12), fg="red").pack(anchor="w")
    for tip in recs.get("Precautions", []):
        tk.Label(frame_precautions, text=f"- {tip}", font=("Helvetica", 12)).pack(anchor="w")

def build_prediction_tab(frame, ensemble, scaler):
    tk.Label(frame, text="Enter Your Details", font=("Helvetica", 18, "bold"), fg="#2e8b57").pack(pady=10)

    # Create two-column layout
    form_frame = tk.Frame(frame)
    form_frame.pack(fill="both", expand=True, padx=20, pady=10)

    left_col = tk.Frame(form_frame)
    left_col.pack(side="left", fill="both", expand=True, padx=10)

    right_col = tk.Frame(form_frame)
    right_col.pack(side="right", fill="both", expand=True, padx=10)

    # Variables
    age_var = tk.IntVar(value=25)
    gender_var = tk.StringVar(value="Male")
    stress_var = tk.IntVar(value=5)
    anxiety_var = tk.IntVar(value=5)
    depression_var = tk.IntVar(value=5)
    sleep_var = tk.IntVar(value=7)
    exercise_var = tk.IntVar(value=3)
    diet_var = tk.StringVar(value="Veg")
    caffeine_var = tk.IntVar(value=2)
    screen_var = tk.IntVar(value=5)

    # Left column inputs
    tk.Label(left_col, text="🌿 Age").pack(anchor="w")
    tk.Scale(left_col, from_=10, to=80, orient="horizontal", variable=age_var).pack(fill="x")

    tk.Label(left_col, text="🌿 Gender").pack(anchor="w")
    ttk.Combobox(left_col, textvariable=gender_var, values=["Male","Female"]).pack(fill="x")

    tk.Label(left_col, text="🌿 Stress Level (0-10)").pack(anchor="w")
    tk.Scale(left_col, from_=0, to=10, orient="horizontal", variable=stress_var).pack(fill="x")

    tk.Label(left_col, text="💊 Anxiety Level (0-10)").pack(anchor="w")
    tk.Scale(left_col, from_=0, to=10, orient="horizontal", variable=anxiety_var).pack(fill="x")

    tk.Label(left_col, text="💊 Depression Score (0-10)").pack(anchor="w")
    tk.Scale(left_col, from_=0, to=10, orient="horizontal", variable=depression_var).pack(fill="x")

    # Right column inputs
    tk.Label(right_col, text="💤 Sleep Hours").pack(anchor="w")
    tk.Scale(right_col, from_=0, to=12, orient="horizontal", variable=sleep_var).pack(fill="x")

    tk.Label(right_col, text="🧘 Exercise Frequency (per week)").pack(anchor="w")
    tk.Scale(right_col, from_=0, to=14, orient="horizontal", variable=exercise_var).pack(fill="x")

    tk.Label(right_col, text="🥗 Diet Type").pack(anchor="w")
    ttk.Combobox(right_col, textvariable=diet_var, values=["Veg","Non-Veg","Mixed"]).pack(fill="x")

    tk.Label(right_col, text="☕ Caffeine Intake (cups/day)").pack(anchor="w")
    tk.Scale(right_col, from_=0, to=10, orient="horizontal", variable=caffeine_var).pack(fill="x")

    tk.Label(right_col, text="📱 Screen Time (hours)").pack(anchor="w")
    tk.Scale(right_col, from_=0, to=12, orient="horizontal", variable=screen_var).pack(fill="x")

    # Prediction logic
    def run_prediction():
        gender_map = {"Male": 1, "Female": 0}
        diet_map = {"Veg": 0, "Non-Veg": 1, "Mixed": 2}

        features = [
            age_var.get(),
            gender_map[gender_var.get()],
            stress_var.get(),
            anxiety_var.get(),
            depression_var.get(),
            6, 7, 5, 6, 4,  # Maslow placeholders
            sleep_var.get(),
            exercise_var.get(),
            diet_map[diet_var.get()],
            caffeine_var.get(),
            screen_var.get()
        ]

        scaled_features = scaler.transform([features])
        prediction = ensemble.predict(scaled_features)[0]
        confidence = max(ensemble.predict_proba(scaled_features)[0]) * 100

        # Confidence bar
        progress = ttk.Progressbar(frame, length=300, mode="determinate")
        progress['value'] = confidence
        progress.pack(pady=10)
        tk.Label(frame, text=f"Prediction Confidence: {confidence:.2f}%",
                 font=("Helvetica", 14), fg="#2e8b57").pack()

        # Show recommendations + precautions
        recs = generate_recommendations(prediction)
        show_recommendations(prediction, recs)
        show_precautions(prediction, recs)

    # Button stays visible below both columns
    ttk.Button(frame, text="Run Prediction", command=run_prediction).pack(pady=20)


# -------------------------
# Run Training + Build Tabs
# -------------------------
if __name__ == "__main__":
    ensemble, scaler, results = train_models()
    show_metrics(results)
    build_prediction_tab(frame_prediction, ensemble, scaler)
    root.mainloop()
