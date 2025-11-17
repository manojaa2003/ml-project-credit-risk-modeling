import streamlit as st
from prediction_helper import predict

st.set_page_config(page_title="Lauki Finance — Credit Risk", page_icon="📊", layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #e5e5e5;'>Credit Risk Modelling 📊</h1>",
    unsafe_allow_html=True
)

st.markdown("Enter applicant details and click **Calculate Risk**")

left, right = st.columns([2, 1])

with st.form("input_form"):
    with left:
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age", min_value=18, max_value=100, value=28, step=1)
        income = c2.number_input("Annual Income (₹)", min_value=0, value=1_200_000)
        loan_amount = c3.number_input("Loan Amount (₹)", min_value=0, value=2_560_000)

        c4, c5, c6 = st.columns(3)
        loan_tenure_months = c4.number_input("Loan Tenure (months)", min_value=1, value=36, step=1)
        avg_dpd_per_delinquency = c5.number_input("Avg DPD", min_value=0, value=20)
        num_open_accounts = c6.number_input("Open Loan Accounts", min_value=1, max_value=20, value=2, step=1)

        c7, c8, c9 = st.columns(3)
        delinquency_ratio = c7.number_input("Delinquency Ratio (%)", min_value=0, max_value=100, value=30)
        credit_utilization_ratio = c8.number_input("Credit Utilization (%)", min_value=0, max_value=100, value=30)
        # Categorical choices kept minimal and professional
        residence_type = c9.selectbox("Residence Type", ["Owned", "Rented", "Mortgage"])

        loan_purpose = st.selectbox("Loan Purpose", ["Home", "Education", "Auto", "Personal"])
        loan_type = st.selectbox("Loan Type", ["Secured", "Unsecured"])

    submit = st.form_submit_button("Calculate Risk")

if submit:
    # safety for division
    loan_to_income_ratio = loan_amount / income if income else 0

    # call existing model helper
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )

    # result column layout
    with right:
        st.metric("Loan → Income Ratio", f"{loan_to_income_ratio:.2f}")
        st.metric("Default Probability", f"{probability:.2%}")
        st.metric("Credit Score", f"{credit_score}")
        st.metric("Rating", f"{rating}")

    st.divider()
    st.info("Model outputs are probabilistic — use them together with underwriting judgement.")
