import streamlit as st

st.title("📊 Credit Eligibility Predictor")
st.write("Use financial data to predict if a client can borrow.")

# --- Function to calculate eligibility score ---
def calculate_score(income, debts, payment_history):
    idr = income / debts if debts > 0 else 0
    payment_percentage = sum(payment_history) / len(payment_history)
    score = 0.5 * idr + 0.5 * payment_percentage
    return score

# --- Sidebar Inputs ---
st.sidebar.header("Client Financial Information")

income = st.sidebar.number_input(
    "Annual Income ($)",
    min_value=0.0,
    max_value=500000.0,
    value=50000.0
)

debts = st.sidebar.number_input(
    "Total Debts ($)",
    min_value=0.0,
    max_value=200000.0,
    value=15000.0
)

st.sidebar.subheader("Payment History (12 Months)")

payment_history = []
for i in range(1, 13):
    status = st.sidebar.selectbox(
        f"Month {i}",
        [1, 0],
        format_func=lambda x: "On-Time (1)" if x == 1 else "Missed (0)",
        key=f"payment_{i}"
    )
    payment_history.append(status)

# --- Predict Button ---
if st.button("Predict Eligibility"):
    score = calculate_score(income, debts, payment_history)

    threshold = 0.75
    eligibility = "✅ Eligible" if score >= threshold else "❌ Not Eligible"

    # --- Display Results ---
    st.subheader("📈 Prediction Results")
    st.write(f"**Score:** {score:.3f}")
    st.write(f"**Eligibility:** {eligibility}")

    # --- Additional Insights ---
    st.write("---")
    st.write("### 🔍 Analysis Details")
    st.write(f"- **Income-to-Debt Ratio:** {income / debts if debts > 0 else 0:.3f}")
    st.write(f"- **On-Time Payment %:** {sum(payment_history) / 12:.2%}")
