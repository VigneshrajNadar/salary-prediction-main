import streamlit as st
import numpy as np 
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
import pandas as pd
import pickle
import requests
from streamlit_lottie import st_lottie

# --- Color Palette ---
PRIMARY_COLOR = "#6C47FF"      # Purple
ACCENT_COLOR = "#FFB300"       # Orange/Gold
HEADER_BG = "#231942"          # Deep purple for dark header
TEXT_COLOR = "#FFFFFF"         # White for header text
SUBTEXT_COLOR = "#bdbdbd"        # Light gray for subtext/footer
DESC_COLOR = "#FFD580"         # Light gold for description

# --- Set page config for wide layout ---
st.set_page_config(layout="wide", page_title="Salary Predictor", page_icon="💼")

# --- Lottie Animation Function ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Lottie Animation URL (e.g., business/finance animation) ---
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_ktwnwv5m.json"
lottie_json = load_lottieurl(lottie_url)

# --- Custom Header for Dark Theme ---
st.markdown(f"""
<div style='background: {HEADER_BG}; padding: 1.5rem 2vw 1rem 2vw; border-radius: 1.2rem; margin-bottom: 2em; width: 60vw; margin-left: auto; margin-right: auto; box-shadow: 0 4px 24px 0 rgba(35,25,66,0.18); border: 1.5px solid #3d2c5a; text-align: center;'>
    <h1 style='color: {TEXT_COLOR}; font-size: 2.7em; margin-bottom: 0.2em;'>💼 Salary Predictor</h1>
    <p style='color: #bdbdbd; font-size: 1.2em; margin-top: 0;'>Employee Salary Prediction</p>
    <p style='color: {DESC_COLOR}; font-size: 1.05em; margin-top: 0.2em;'>Enter employee details to predict salary and explore HR analytics with interactive visualizations.</p>
</div>
""", unsafe_allow_html=True)

# --- Load models and encoders ---
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('label_encoder_sex.pkl','rb') as file:
    label_encoder_sex = pickle.load(file)
with open('onehot_encoder_des.pkl','rb') as file:
    onehot_encoder_des = pickle.load(file)
with open('onehot_encoder_unit.pkl','rb') as file:
    onehot_encoder_unit = pickle.load(file)
with open('scaler.pkl','rb') as file:
    scaler = pickle.load(file)

# --- Input Form in Card ---
with st.form("salary_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=70, value=30, step=1, key="age")
        gender_options = list(label_encoder_sex.classes_)
        gender = st.selectbox("Gender", gender_options, key="gender")
        unit_options = list(onehot_encoder_unit.categories_[0])
        unit = st.selectbox("Unit/Department", unit_options, key="unit")
    with col2:
        designation_options = list(onehot_encoder_des.categories_[0])
        designation = st.selectbox("Designation", designation_options, key="designation")
        ratings = st.slider("Performance Rating", min_value=1.0, max_value=5.0, value=3.0, step=0.1, key="ratings")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=5, step=1, key="experience")
    submitted = st.form_submit_button("Predict Salary", use_container_width=True)

# --- Prediction Logic ---
if submitted:
    try:
        # Encode categorical features
        gender_encoded = label_encoder_sex.transform([gender])[0]
        designation_encoded = onehot_encoder_des.transform([[designation]]).toarray()[0]
        unit_encoded = onehot_encoder_unit.transform([[unit]]).toarray()[0]
        # Prepare input for scaler/model
        input_data = np.concatenate((
            [age, gender_encoded, ratings, experience],
            designation_encoded,
            unit_encoded
        )).reshape(1, -1)
        input_data_scaled = scaler.transform(input_data)
        prediction = model.predict(input_data_scaled)
        predicted_salary = prediction[0]
        st.markdown(f"""
        <div style='background: linear-gradient(90deg, #fbeee6 60%, #f6f3ff 100%); border-left: 8px solid {ACCENT_COLOR}; padding: 2em 2vw; margin-top: 2.5em; border-radius: 1em; width: 100vw; position: relative; left: 50%; right: 50%; margin-left: -50vw; margin-right: -50vw;'>
            <h3 style='color: {ACCENT_COLOR}; font-size: 2em; margin-bottom: 0.2em; text-align: center;'>Estimated Salary</h3>
            <p style='font-size: 3em; color: {PRIMARY_COLOR}; font-weight: bold; text-align: center;'>${predicted_salary:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    except ValueError as e:
        st.error(f"Prediction failed: {e}. Please check your input values.")

# --- Footer ---
st.markdown(f"""
---
<div style='text-align: center; color: {SUBTEXT_COLOR}; font-size: 1.1em; margin-top: 2.5em;'>
    &copy; 2024 Salary Predictor &mdash; Powered by Streamlit & scikit-learn
</div>
""", unsafe_allow_html=True)
