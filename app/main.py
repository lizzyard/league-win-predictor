from pathlib import Path 
import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_FILE = PROJECT_ROOT / "models" / "win_predictor_15min.pkl"

model = joblib.load(MODEL_FILE)

st.set_page_config(
    page_title="League Win Predictor",
    page_icon="⚔️",
    layout="centered"

)

model = joblib.load(MODEL_FILE)

st.title("League of Legends Win Predictor")
st.write(
    "Estimate Blue Team's chance of winning based on the game state "
    "at 15 minutes."
    )

with st.sidebar:
    st.header("How to enter values")
    st.write(
        "Enter Blue Team's stat minus Red team's stat."
    )

    st.write("Example:")
    st.code(
        """
    Blue gold: 27,500
    Red gold: 25,000
    
    Gold difference = 2,500 
        """
    )


gold_diff = st.number_input(
    "Gold Difference",
    min_value=-20000,
    max_value=20000,
    value=0,
    step=100,
    )

xp_diff = st.number_input(
    "XP difference",
    min_value=-20000,
    max_value=20000,
    value=0,
    step=100,
)

cs_diff = st.number_input(
    "CS difference",
    min_value=-500,
    max_value=500,
    value=0,
    step=5,
)

kill_diff = st.number_input(
    "Kill difference",
    min_value=-30,
    max_value=30,
    value=0,
    step=1,
)

tower_diff = st.number_input(
    "Tower difference",
    min_value=-10,
    max_value=10,
    value=0,
    step=1,
)

dragon_diff = st.number_input(
    "Dragon difference",
    min_value=-4,
    max_value=4,
    value=0,
    step=1,
)

herald_diff = st.number_input(
    "Rift herald difference",
    min_value=-2, 
    max_value=2,
    value=0,
    step=1,
)

if st.button("Predict winner", use_container_width=True):
    input_data = pd.DataFrame(
        [
            {
                "gold_diff_15": gold_diff,
                "xp_diff_15": xp_diff,
                "cs_diff_15": cs_diff,
                "kill_diff_15": kill_diff,
                "tower_diff_15": tower_diff,
                "dragon_diff_15": dragon_diff,
                "herald_diff_15": herald_diff,
            }
        ]
    )

    win_probability = model.predict_proba(input_data)[0][1]
    loss_probability = 1 - win_probability

    st.divider()
    st.subheader("Prediction")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Blue Team",
            f"{win_probability:.1%}"
        )

    with col2:
        st.metric(
            "Red Team",
            f"{loss_probability:.1%}",
        )

    st.progress(float(win_probability))

    if win_probability >= 0.5:
        st.success("Blue Team is predicted to win.")
    else:
        st.error("Red Team is predicted to win.")
    if 0.45 <= win_probability <= 0.55:
        st.warning(
            "The prediction is very close, so the model is uncertain."
        )

st.caption(
    "This model uses gold, XP, and CS differences at 15 minutes. "
    "It is an educational prediction and not a guarenteed outcome."
)




    # st.subheader("Prediction")

    # if prediction:
    #     st.success(f"Predicted Win Probability: {probability:.2%}")
    # else:
    #     st.error(f"Predicted Win Probability: {probability:.2%}")