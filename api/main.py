from fastapi import FastAPI
from api.schemas import CustomerData, PredictResponse, ExplainResponse
import joblib
import pandas as pd
import shap
import time

app = FastAPI(title="Anti-Blackbox API (Compliance Guard)")

# Modell in den RAM laden
model = joblib.load('model/credit_model.pkl')

# CFO-Fallback: Falls die SHAP-Berechnung abstürzt oder zu lange dauert
GLOBAL_FALLBACK = {
    "Income": "Generell starker positiver Einfluss",
    "Credit_Score": "Das wichtigste Kriterium für die Zusage",
    "Age": "Neutraler Einfluss"
}

@app.post("/predict", response_model=PredictResponse)
def predict(data: CustomerData):
    df = pd.DataFrame([data.model_dump()])
    prediction = model.predict(df)[0]
    return {"Approved": int(prediction)}

@app.post("/explain", response_model=ExplainResponse)
def explain(data: CustomerData):
    start_time = time.time()
    df = pd.DataFrame([data.model_dump()])
    
    try:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(df)
        
        if (time.time() - start_time) > 0.5:
            return {"status": "TIMEOUT_FALLBACK_ACTIVE", "shap_explanation": GLOBAL_FALLBACK}
            
        # Extrahiere SHAP Werte für "Approved=1"
        if len(shap_values.shape) == 3:
            val = shap_values[0, :, 1]
        elif isinstance(shap_values, list):
            val = shap_values[1][0]
        else:
            val = shap_values[0]
            
        shap_dict = {col: round(float(val[i]), 3) for i, col in enumerate(df.columns)}
        return {"status": "SUCCESS", "shap_explanation": shap_dict}
        
    except Exception as e:
        return {"status": "ERROR_FALLBACK_ACTIVE", "shap_explanation": GLOBAL_FALLBACK}
