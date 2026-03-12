import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Model Monitoring Dashboard")

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "prediction_logs.csv")

if not os.path.exists(LOG_FILE):
    st.warning("No predictions yet.")
    st.stop()

df = pd.read_csv(LOG_FILE)

st.write(f"Total Predictions: {len(df)}")

if len(df) > 0:

    st.subheader("Prediction Distribution")
    st.bar_chart(df["prediction"].value_counts())

    st.subheader("Probability Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["probability"], bins=20)
    st.pyplot(fig)

    mean_prob = df["probability"].mean()
    st.write(f"Mean Probability: {mean_prob:.4f}")

    if mean_prob > 0.9 or mean_prob < 0.1:
        st.error("Possible Drift Detected!")
    else:
        st.success("Model Stable")
