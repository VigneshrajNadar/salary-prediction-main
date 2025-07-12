# Employee Salary Prediction Web App

## 📖 Project Overview

**Employee Salary Prediction Web App** is a powerful, user-friendly platform designed for HR professionals, business leaders, and data enthusiasts to:

- **Predict employee salaries** instantly using a machine learning model trained on real HR data.
- **Explore workforce insights** with interactive, animated visualizations that reveal trends in pay, experience, gender, and department.
- **Identify pay gaps and outliers** to support fair, data-driven compensation decisions.
- **Empower HR strategy** with actionable analytics on workforce structure, diversity, and performance.

### Why This Project?

- **Business Value**: Organizations need to ensure fair, competitive, and equitable pay. This app helps uncover hidden patterns, optimize salary structures, and support transparent HR policies.
- **Target Users**: HR teams, managers, analysts, and anyone interested in workforce analytics or salary benchmarking.
- **Key Capabilities**:
  - Real-time salary prediction based on demographic and job features
  - Deep-dive analytics with animated, interactive charts
  - Modern, responsive UI for seamless experience on any device
  - Easy integration and extensibility for custom datasets or new features

### What Sets It Apart?

- **No TensorFlow/AVX issues**: 100% scikit-learn and Streamlit, fully Mac/Windows/Linux compatible
- **All-in-one**: Combines predictive modeling and rich HR analytics in a single, easy-to-use web app
- **Professional polish**: Lottie animations, branded UI, and smooth user experience
- **Open-source and extensible**: Ready for your data, your models, and your HR challenges

---

## 🧠 Machine Learning Model Details
- **Model**: scikit-learn Linear Regression
- **Features Used**: Age, Experience, Designation, Unit, Gender, and more
- **Preprocessing**: Label encoding (for gender), one-hot encoding (for designation/unit), and feature scaling
- **Training Pipeline**: All preprocessing steps and the model are saved as artifacts for reproducibility
- **Evaluation**: Model performance is measured using MAE and R² on a holdout set
- **Why Linear Regression?**: Simple, interpretable, and effective for continuous salary prediction

---

## 🛠️ Feature Engineering
- **Categorical Encoding**: Designation and Unit are one-hot encoded; Gender is label encoded
- **Scaling**: All numeric features are standardized for optimal model performance
- **Feature Order**: Preserved to ensure correct mapping during prediction
- **Artifact Management**: All encoders, scalers, and feature order are saved and loaded for consistent predictions

---

## 📊 Data Exploration Visualizations
- **Pie Charts**: Employee count by Designation and Unit
- **Histograms**: Salary distribution overall and by role
- **Boxplots**: Salary by Designation, highlighting outliers and spread
- **Animated Charts**: Salary by Designation/Unit/Gender over time or categories, with play/pause and speed control
- **Bar Charts**: Average salary by experience bucket, gender ratio by unit
- **Missing Values Overview**: Visual summary of data completeness

All charts are interactive and responsive, powered by Plotly and Streamlit.

---

## 🎨 UI/UX Highlights
- **Modern, Responsive Design**: Custom header, sidebar branding, and styled result box
- **Lottie Animations**: Engaging visuals in both prediction and exploration pages
- **Dynamic Inputs**: Dropdowns and sliders auto-populated from model encoders
- **Full-Screen Layout**: Optimized for laptops and desktops
- **Professional Color Palette**: Consistent, accessible, and visually appealing
- **User Feedback**: Balloons and spinners for interactive experience

---

## 🚀 Future Improvements
- **Model Comparison**: Add support for more advanced models (e.g., Random Forest, XGBoost)
- **Feature Importance**: Visualize which features most influence salary predictions
- **Upload Your Own Data**: Allow users to analyze and predict on custom datasets
- **Role-based Access**: Different views for HR, managers, and employees
- **Export Reports**: Downloadable analytics and prediction summaries
- **API Integration**: REST API for programmatic access to predictions

---

## 🗂️ Project Structure

```
├── Home.py                    # Main Streamlit app (salary prediction)
├── pages/
│   └── explore.py             # Data exploration & analytics page
├── train_sklearn_model.py     # Script to train and export scikit-learn model & encoders
├── model.pkl                  # Trained scikit-learn LinearRegression model
├── scaler.pkl                 # StandardScaler object
├── label_encoder_sex.pkl      # Label encoder for SEX
├── onehot_encoder_des.pkl     # One-hot encoder for DESIGNATION
├── onehot_encoder_unit.pkl    # One-hot encoder for UNIT
├── feature_order.pkl          # Preserved order of features from training
├── salary prediction.csv      # Dataset
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
```

---

## 🚦 How to Run the App

### Platform-specific Instructions

#### **Mac (Apple Silicon or Intel)**
1. Open Terminal
2. (Recommended) Create a new environment:
   ```bash
   conda create -n sklearn-env python=3.10
   conda activate sklearn-env
   pip install -r requirements.txt
   ```
   Or, using `venv`:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```bash
   streamlit run Home.py
   ```

#### **Windows**
1. Open Anaconda Prompt or Command Prompt
2. (Recommended) Create a new environment:
   ```bat
   conda create -n sklearn-env python=3.10
   conda activate sklearn-env
   pip install -r requirements.txt
   ```
   Or, using `venv`:
   ```bat
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```bat
   streamlit run Home.py
   ```

#### **Linux**
1. Open Terminal
2. (Recommended) Create a new environment:
   ```bash
   conda create -n sklearn-env python=3.10
   conda activate sklearn-env
   pip install -r requirements.txt
   ```
   Or, using `venv`:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```bash
   streamlit run Home.py
   ```

---

## 👤 Author

Vignesh Raj Nadar ([GitHub Profile](https://github.com/VigneshrajNadar))

