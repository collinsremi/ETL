import streamlit as st
import numpy as np
import joblib
import pandas as pd

# -------------------------------
# Load Models
# -------------------------------
mlr_model   = joblib.load("linear_regression_model.pkl")
ridge_model = joblib.load("ridge_model.pkl")
poly_model  = joblib.load("polynomial_model.pkl")

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Concrete Strength Predictor",
    page_icon="🧱",
    layout="centered"
)

# -------------------------------
# Header
# -------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🧱 Concrete Strength Predictor</h1>
    <p style='text-align: center;'>Compare predictions from multiple ML models</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------
# Input Features
# -------------------------------
st.subheader("📥 Input Features")

cement = st.number_input("Cement", min_value=0.0, step=1.0)
slag = st.number_input("Blast Furnace Slag", min_value=0.0, step=1.0)
ash = st.number_input("Fly Ash", min_value=0.0, step=1.0)
water = st.number_input("Water", min_value=0.0, step=1.0)
superplasticizer = st.number_input("Superplasticizer", min_value=0.0, step=0.1)
coarse = st.number_input("Coarse Aggregate", min_value=0.0, step=1.0)
fine = st.number_input("Fine Aggregate", min_value=0.0, step=1.0)
age = st.number_input("Age (days)", min_value=1, step=1)

features = np.array([[cement, slag, ash, water, superplasticizer, coarse, fine, age]])

st.divider()

# -------------------------------
# Prediction Button
# -------------------------------
if st.button("🔍 Compare Models"):

    pred_mlr   = mlr_model.predict(features)[0]
    pred_ridge = ridge_model.predict(features)[0]
    pred_poly  = poly_model.predict(features)[0]

    # -------------------------------
    # Display Results Cards
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div style='background-color:#e3f2fd;padding:15px;border-radius:10px;text-align:center;'>
                <h4>Linear Regression</h4>
                <h2>{pred_mlr:.2f} MPa</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='background-color:#e8f5e9;padding:15px;border-radius:10px;text-align:center;'>
                <h4>Ridge</h4>
                <h2>{pred_ridge:.2f} MPa</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style='background-color:#fff3e0;padding:15px;border-radius:10px;text-align:center;'>
                <h4>Polynomial</h4>
                <h2>{pred_poly:.2f} MPa</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # -------------------------------
    # Comparison Table
    # -------------------------------
    results_df = pd.DataFrame({
        "Model": ["Linear Regression", "Ridge", "Polynomial"],
        "Predicted Strength (MPa)": [pred_mlr, pred_ridge, pred_poly]
    })

    st.subheader("📊 Prediction Comparison")
    st.dataframe(results_df, use_container_width=True)

    # -------------------------------
    # Highlight Best (optional logic)
    # -------------------------------
    best_model = results_df.loc[
        results_df["Predicted Strength (MPa)"].idxmax()
    ]["Model"]

    st.success(f"🏆 Highest predicted strength: **{best_model}**")

# -------------------------------
# Footer
# -------------------------------
st.divider()
st.markdown(
    "<p style='text-align:center; font-size:12px;'>Built with Streamlit • Model Comparison App</p>",
    unsafe_allow_html=True
)