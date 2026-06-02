<div align="center">

# ⚖️ Explainability & Compliance (Anti-Blackbox)

[![GDPR Compliant](https://img.shields.io/badge/Compliance-DSGVO_Art._22-003B57?style=for-the-badge)](https://dsgvo-gesetz.de/art-22-dsgvo/)
[![SHAP](https://img.shields.io/badge/Explainability-SHAP-8E44AD?style=for-the-badge)](https://shap.readthedocs.io/)
[![DiCE](https://img.shields.io/badge/Counterfactuals-DiCE-0194E2?style=for-the-badge)](https://github.com/interpretml/DiCE)
[![Microservice](https://img.shields.io/badge/Architecture-Microservice-2ea44f?style=for-the-badge)](https://github.com)

**Ein Microservice-Backend für 100% DSGVO-konforme Machine Learning Vorhersagen.**

*Löst das "Blackbox"-Problem von KI-Modellen (z.B. bei der Kreditvergabe) durch spieltheoretische Erklärbarkeit und entkoppelt asynchrone Compliance-Prozesse von der Echtzeit-Inferenz.*

---
</div>

## 💼 Business Value & BLUF (Bottom Line Up Front)

KI-Systeme in regulierten Märkten (Finance, HR, Healthcare) dürfen laut DSGVO keine rein automatisierten Blackbox-Entscheidungen ohne Erklärbarkeit treffen. Dieses Backend garantiert rechtliche und technische Sicherheit:

<table>
  <tr>
    <td><strong>🛡️ Rechtssicherheit</strong></td>
    <td>Vollständige Erfüllung von <strong>DSGVO Art. 22</strong> (Recht auf Erklärung). Macht jede ML-Entscheidung für Auditoren und Endkunden transparent nachvollziehbar.</td>
  </tr>
  <tr>
    <td><strong>⚡ Ausfallsicherheit</strong></td>
    <td>Strikte architektonische Entkopplung (Decoupling) der blitzschnellen Vorhersage von der rechenintensiven Compliance-Erklärung, um Systemabstürze unter Last zu verhindern.</td>
  </tr>
</table>

---

## 🏗️ Kern-Architektur & Endpunkte

Das System trennt Latenz-kritische Vorgänge von asynchronen Erklärungs-Jobs:

| API-Endpunkt / Feature | Beschreibung & Core Logic |
| :--- | :--- |
| 🚀 **`/predict`** | **Real-time Inference:** Ein auf maximalen Durchsatz optimierter Endpunkt für Vorhersagen in **< 50ms**. Keine blockierenden Analytics-Prozesse im Main-Thread. |
| 🧠 **`/explain`** | **SHAP-Explainer:** Nutzt Spieltheorie (Shapley Values) zur Feature-Attribution. Abgesichert durch einen harten **500ms Fallback-Guard**, um Memory-Leaks oder Timeouts bei komplexen Erklärungen abzufangen. |
| 🔄 **`Counterfactuals`** | **DiCE-Integration:** Berechnet nicht nur *warum* eine Entscheidung getroffen wurde, sondern generiert exakte, umsetzbare Lösungswege ("Was-wäre-wenn") für abgelehnte Kunden (z.B. *"Erhöhen Sie das Eigenkapital um 5.000€ für eine Kreditzusage"*). |

---

## 🚀 Quick Start (Lokales Setup)

<details>
<summary><b>🛠️ Installation & Ausführung (Hier klicken zum Aufklappen)</b></summary>

Um endlose Terminal-Befehle zu vermeiden, ist der gesamte Lifecycle in einem Makefile automatisiert:

### 1. Environment & Pakete installieren
```bash
make install
