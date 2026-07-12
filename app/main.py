import joblib
import pandas as pd
import streamlit as st

MODEL_FILE = "models/win_predictor_15min.pkl"

model = joblib.load(MODEL_FILE)

st.title("League of Legends Win Predictor")
st.write("Predict win probability from 15-minute game state.")

gold_diff = st.number_input("Gold Difference at 15 min", value=0)
xp_diff = st.number_input("XP Difference at 15 min", value = 0)
cs_diff = st.number_input("CS Difference at 15 min", value=0)

if st.button("Predict"):
    input_data = pd.DataFrame(
        [
            {
                "gold_diff_15": gold_diff,
                "xp_diff_15": xp_diff,
                "cs_diff_15": cs_diff,
            }
        ]
    )

    probability = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    st.subheader("Prediction")

    if prediction:
        st.success(f"Predicted Win Probability: {probability:.2%}")
    else:
        st.error(f"Predicted Win Probability: {probability:.2%}")