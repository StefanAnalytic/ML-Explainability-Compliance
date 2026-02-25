Explainability & Compliance (Anti-Blackbox)

## 📌 Business Value (BLUF)
Dieses Microservice-Backend liefert 100% DSGVO-konforme (Art. 22) Machine Learning Vorhersagen (z.B. für Kreditvergabe). Es entkoppelt die blitzschnelle Vorhersage (`/predict`) von der rechenintensiven Compliance-Erklärung (`/explain`), um Systemabstürze zu verhindern und Ausfallsicherheit zu garantieren.

## 🏗️ Architektur
* **`/predict`**: Sub-50ms Inference-Endpunkt.
* **`/explain`**: SHAP-Explainer (Spieltheorie) mit 500ms Fallback-Guard.
* **Counterfactuals**: DiCE-Integration zur Berechnung exakter Lösungswege für abgelehnte Kunden.

## 🚀 Quickstart (Makefile)
Anstatt lange Befehle zu tippen, nutze einfach diese Shortcuts im Terminal:

1. **`make install`** - Installiert alle nötigen Pakete
2. **`make train`** - Trainiert das KI-Modell und speichert es
3. **`make run`** - Startet den API-Server lokal
