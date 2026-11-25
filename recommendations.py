from precautions import herb_precautions

def generate_recommendations(prakriti, features, allergies=[]):
    ayurveda = {
        "Vata": {"herbs":["Ashwagandha","Brahmi","Triphala"], "recipe":"Ashwagandha milk at night."},
        "Pitta": {"herbs":["Guduchi","Amalaki","Shatavari"], "recipe":"Guduchi tea twice daily."},
        "Kapha": {"herbs":["Triphala","Tulsi","Punarnava"], "recipe":"Triphala decoction in morning."}
    }

    rec = ayurveda.get(prakriti, {"herbs":[],"recipe":"N/A"})

    safe_herbs, warnings = [], []
    for herb in rec["herbs"]:
        if herb in allergies:
            warnings.append(f"⚠️ Allergy alert: {herb} should be avoided.")
        else:
            safe_herbs.append(herb)
            if herb in herb_precautions:
                warnings.append(f"{herb}: {herb_precautions[herb]}")

    psy_recs, lifestyle, exercise = [], [], []

    if features.get("stress_level",0) >= 8:
        psy_recs.append("High stress → Meditation, CBT, breathing exercises.")
        lifestyle.append("Reduce workload, add journaling breaks.")
        exercise.append("Pranayama + restorative yoga.")
    if features.get("anxiety_level",0) >= 8:
        psy_recs.append("High anxiety → Mindfulness, therapy referral.")
        lifestyle.append("Limit caffeine, reduce screen time.")
        exercise.append("Shavasana + calming yoga.")
    if features.get("depression_score",0) >= 8:
        psy_recs.append("High depression → Structured routine, counseling.")
        lifestyle.append("Stay socially active, outdoor hobbies.")
        exercise.append("Surya Namaskar + brisk walking.")
    if features.get("sleep_hours",7) < 6:
        lifestyle.append("Fixed bedtime, no screens before bed.")
        exercise.append("Evening yoga (Child’s Pose, Viparita Karani).")
    if features.get("screen_time_hours",0) > 6:
        lifestyle.append("Digital detox, outdoor walks.")
        exercise.append("Outdoor sports (cycling, badminton).")

    return {
        "Ayurveda": {"recipe":rec["recipe"], "herbs":safe_herbs, "warnings":warnings},
        "Healthcare": psy_recs,
        "Lifestyle": lifestyle,
        "Exercise": exercise
    }
