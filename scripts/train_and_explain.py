import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import shap
import dice_ml
import joblib
import os
import warnings
warnings.filterwarnings("ignore") # Unterdrückt unnötige Warnungen im Terminal

print("🏦 STARTE ANTI-BLACKBOX TRAINING (KREDIT-SCORING)...\n")

# 1. Daten simulieren (Einkommen, Schufa-Score, Alter)
np.random.seed(42)
N = 500
income = np.random.normal(45000, 15000, N)
credit_score = np.random.normal(600, 80, N)
age = np.random.randint(18, 70, N)

# KI-Regel (Ground Truth): Kredit wird bewilligt (1), wenn Einkommen > 40k UND Schufa > 600
approved = ((income > 40000) & (credit_score > 600)).astype(int)

df = pd.DataFrame({'Income': income, 'Credit_Score': credit_score, 'Age': age, 'Approved': approved})
X = df.drop('Approved', axis=1)
y = df['Approved']

# 2. Modell trainieren
print("⚙️ Trainiere Random Forest Modell...")
model = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
model.fit(X, y)

# 3. Modelle für die API speichern
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/credit_model.pkl')
print("✅ Modell gespeichert in 'model/credit_model.pkl'")

# ==========================================
# COMPLIANCE & EXPLAINABILITY (DSGVO Art. 22)
# ==========================================

# Einen abgelehnten Kunden aus dem Datensatz fischen
rejected_customer = X[y == 0].iloc[[0]]

print("\n---------------------------------------------------")
print("❌ KUNDE ABGELEHNT:")
print(f"Einkommen: {rejected_customer['Income'].values[0]:.0f} € | Schufa: {rejected_customer['Credit_Score'].values[0]:.0f} | Alter: {rejected_customer['Age'].values[0]}")
print("---------------------------------------------------")

# SHAP: Die Diagnose (Warum?)
print("\n🔍 SHAP-ANALYSE (Warum wurde abgelehnt?):")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(rejected_customer)
# Für Binary Classification nehmen wir die Werte für Klasse 1 (Approval)
shap_vals_for_approval = shap_values[0, :, 1] if len(shap_values.shape) == 3 else shap_values[1][0] if isinstance(shap_values, list) else shap_values[0]

for feature, importance in zip(X.columns, shap_vals_for_approval):
    impact = "positiv" if importance > 0 else "negativ"
    print(f" -> Feature '{feature}' hat das Ergebnis {impact} beeinflusst (Wert: {importance:.2f})")

# DiCE: Der Lösungsweg (Was tun?)
print("\n🔮 DiCE COUNTERFACTUAL (Was hätte der Kunde anders machen müssen?):")
d = dice_ml.Data(dataframe=df, continuous_features=['Income', 'Credit_Score', 'Age'], outcome_name='Approved')
m = dice_ml.Model(model=model, backend="sklearn")
exp = dice_ml.Dice(d, m, method="random")

# Generiere exakt 1 Weg, wie dieser Kunde seinen Kredit doch noch bekommt
dice_exp = exp.generate_counterfactuals(rejected_customer, total_CFs=1, desired_class="opposite")
cf_df = dice_exp.cf_examples_list[0].final_cfs_df

print("\n✅ LÖSUNGSWEG UM KREDIT ZU BEKOMMEN:")
print(cf_df)
print("\n(Die geänderten Werte zeigen dem Kunden seinen Handlungsspielraum)")

