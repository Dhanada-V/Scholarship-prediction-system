**AI-Based Scholarship Eligibility & Recommendation System**

**Overview**

This project presents an Explainable Hybrid AI system designed to predict student eligibility for various scholarships and recommend suitable schemes. The system integrates Machine Learning models, Rule-based logic, OCR (Optical Character Recognition), and Explainable AI (XAI) to provide accurate and transparent predictions.
The objective of this project is to assist students in identifying eligible scholarships based on their academic and socio-economic background while ensuring interpretability and fairness in decision-making.

**Features**
1. Scholarship eligibility prediction using ML models
2. OCR-based document data extraction
3. Rule-based validation for government policies
4. Explainable AI using SHAP for transparency
5. User-friendly frontend using Streamlit
6. Confidence scores and reasoning for predictions
   
**Technologies Used**
- Python
- Scikit-learn
- XGBoost
- Pandas, NumPy
- SHAP (Explainable AI)
- Tesseract OCR
- Streamlit
- Flask (Backend API)

**System Architecture**

The system follows a modular pipeline:

1. User input (form and document upload)
2. OCR extracts document data
3. Data preprocessing & feature engineering
4. Machine learning prediction
5. Rule engine validation
6. SHAP-based explanation
7. Final scholarship recommendation

**Machine Learning Models**
1. Random Forest
2. XGBoost 
3. E-Grantz Model (with SMOTE & weighting)

**Implementation Modules**
1. Data Collection and Preprocessing
2. Feature Engineering (Encoding, Normalization)
3. Data Balancing (SMOTE for E-Grantz dataset)
4. Model Training and Evaluation
5. Data Visualization
6. Explainable AI (SHAP)
7. OCR Module
8. Rule Engine
9. Backend API (Flask)
10 Frontend Interface (Streamlit)

**How to Run the Project**
1. Clone the Repository
git clone https://github.com/your-username/scholarship-prediction-system.git
cd scholarship-system

3. Create Virtual Environment
python -m venv venv
venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

4. Run Application
python run.py

**Sample Output**

1. Eligible scholarships
2. Prediction probabilities
3. Explanation (why eligible / not eligible)

**Author**

Dhanada V
M.Sc Computer Science (Specialized in Data Science)

