
# 🏥 Post-Surgical Recovery & Complication Analysis

This repository provides a comprehensive framework for analyzing post-surgical recovery patterns, predicting medical complications, and supporting chatbot-based patient care. It includes data processing, exploratory data analysis (EDA), predictive modeling, and chatbot QA system development.

---

## 📁 Project Structure

```
.
├── Recovery_Pattern_Analysis.ipynb
├── EDA_Complication_Prediction.ipynb
├── Model_Training_Complication_Prediction.ipynb
├── recovery_logs.csv
├── complication_prediction_data.csv
├── chatbot_qa_data.csv
└── README.md
```

---

## 📊 Datasets

### 1. `recovery_logs.csv`
- **Rows**: 15,000
- **Description**: Daily recovery logs for patients.
- **Key Columns**:
  - `patient_id`: Unique identifier
  - `day`: Recovery day number
  - `pain_score`: Pain level (0–10)
  - `temperature`: Body temperature
  - `mood`: Patient’s emotional state
  - `sleep_hours`: Sleep duration
  - `wound_check`: Wound condition (e.g., Clean, Redness)
  - `recovery_flag`: Categorical status - `On Track`, `At Risk`

### 2. `complication_prediction_data.csv`
- **Rows**: 5,000
- **Description**: Patient features for complication prediction.
- **Key Columns**:
  - `patient_id`, `age`, `surgery_type`
  - `pain_score`, `fever`, `wound_status`, `mobility_level`
  - `day_of_recovery`, `complication_flag` (target: Yes/No)

### 3. `chatbot_qa_data.csv`
- **Rows**: 300
- **Description**: Synthetic QA dataset for training a recovery-assistant chatbot.
- **Key Columns**:
  - `question_text`: User query
  - `intent`: Category (e.g., `pain_mgmt`, `mobility`)
  - `response_text`: Bot reply

---

## 📒 Notebooks

### ✅ 1. `Recovery_Pattern_Analysis.ipynb`
- **Purpose**: 
  - Analyze trends in patient recovery over time
  - Identify signs of deviation such as mood deterioration or poor wound healing
- **Techniques**:
  - Time-series aggregation by patient
  - Visualization of pain and temperature trends
  - Mood and wound condition correlations with recovery status

### 🔬 2. `EDA_Complication_Prediction.ipynb`
- **Purpose**: 
  - Explore clinical features linked to post-op complications
  - Inform feature selection for predictive modeling
- **Highlights**:
  - Distribution plots for variables like `pain_score`, `fever`, `age`
  - Crosstab analyses for `wound_status`, `mobility_level` vs. `complication_flag`

### 🤖 3. `Model_Training_Complication_Prediction.ipynb`
- **Purpose**:
  - Build machine learning models to predict post-surgical complications
- **Models Used**:
  - Logistic Regression, Random Forest, XGBoost
- **Pipeline**:
  - Data encoding, train-test split
  - Cross-validation and evaluation using metrics like accuracy, recall, and ROC-AUC
- **Outcome**:
  - Binary classification of `complication_flag` (Yes/No)

---

## 💬 Chatbot QA Module

- Based on `chatbot_qa_data.csv`, this module simulates a rule-based or retrieval-based assistant.
- Can be extended with NLP embeddings or fine-tuned transformer models for improved generalization.
- Use-case: Instant responses to common patient concerns post-surgery.

---

## 📌 Key Findings (from Notebooks)

- Mood and wound condition are strong indicators of recovery trajectory.
- High `pain_score`, persistent fever, and low mobility increase complication risks.
- Machine learning models achieved ROC-AUC > 0.85 with proper feature engineering.

---

## 🛠 Setup & Requirements

1. Clone this repo:
   ```bash
   git clone https://github.com/<your-username>/surgical-recovery-analysis.git
   cd surgical-recovery-analysis
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run the notebooks in Jupyter or VSCode.

---

## 📚 Future Improvements

- Integration with live hospital EMRs or wearable device APIs
- Fine-tuning LLMs for chatbot QA
- Time-series forecasting models (e.g., LSTMs) for recovery prediction

---

## 👤 Author

Developed by Rohit  
📧 rohitmudili5@gmail.com

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
