import streamlit as st
import pandas as pd
from models.client import Client
from dashboard.layout import load_css
import requests
from streamlit_lottie import st_lottie

class Dashboard:

    def render(self):
        load_css()
        
        st.title("Borrower Credit Evaluation Dashboard")

        # =========================
        # SESSION STATE INIT
        # =========================
        if "clients" not in st.session_state:
            st.session_state.clients = []

        if "debt_inputs" not in st.session_state:
            st.session_state.debt_inputs = [{"name": "", "amount": 0}]

        if "form_submitted" not in st.session_state:
            st.session_state.form_submitted = False
            
        # Helper to track if we just finished the form and haven't navigated yet
        if "just_added" not in st.session_state:
            st.session_state.just_added = False

        option = st.session_state.get("selected_dashboard", "Borrower Overview")

        # =========================
        # ADD BORROWER FORM
        # =========================
        if not st.session_state.form_submitted:
            st.subheader("Add New Borrower")
            name = st.text_input("Borrower Name", "")
            income = st.number_input("Monthly Income (PHP)", 0, 500000, 1000)
            loan_amount = st.number_input("Requested Loan Amount (PHP)", 0, 1000000, 10000)

            st.markdown("### Existing Debts")
            total_debt = 0
            for i, debt in enumerate(st.session_state.debt_inputs):
                col1, col2 = st.columns(2)
                debt["name"] = col1.text_input(f"Debt Name #{i+1}", debt["name"], key=f"debt_name_{i}")
                debt["amount"] = col2.number_input("Amount (PHP)", 0, 1000000, debt["amount"], key=f"debt_amount_{i}")
                total_debt += debt["amount"]

            col_add, col_submit = st.columns(2)
            if col_add.button("➕ Add Another Debt"):
                st.session_state.debt_inputs.append({"name": "", "amount": 0})
                st.rerun()

            if col_submit.button("Add Borrower"):
                if not name.strip():
                    st.warning("Please enter borrower name")
                else:
                    # MODIFICATION: Format Name and Debt Details to Title Case
                    formatted_name = name.strip().title()
                    client_id = len(st.session_state.clients) + 1
                    
                    debt_details = [
                        {
                            "name": d.get("name", "").strip().title() or "Unnamed Debt", 
                            "amount": d.get("amount", 0)
                        } for d in st.session_state.debt_inputs
                    ]
                    
                    client = Client(client_id, income, total_debt, loan_amount=loan_amount, name=formatted_name, debt_details=debt_details)
                    st.session_state.clients.append(client.to_dict())
                    st.session_state.debt_inputs = [{"name": "", "amount": 0}]
                    st.session_state.form_submitted = True
                    st.session_state.just_added = True # Flag that we just submitted
                    st.rerun()
            
            # --- CRITICAL FIX ---
            # If the form is currently being filled out, stop here.
            # This prevents the Overview/List from showing below the form.
            return

        # ==========================================
        # SUCCESS MESSAGE (Logic fix for sidebar)
        # ==========================================
        elif st.session_state.form_submitted and st.session_state.just_added:
            st.markdown("---")
            st.success("✅ Borrower added successfully!")
            st.info("📊 **Evaluation Complete:** You can now view this borrower's detailed information, credit overview, and recommendations by selecting the options from the **sidebar menu**.")
            
            if st.button("➕ Add Another New Borrower"):
                st.session_state.form_submitted = False
                st.session_state.just_added = False
                st.rerun()
            return 

        if not st.session_state.clients:
            st.info("Add a borrower to begin evaluation.")
            return

        # =========================
        # PAGE ROUTING (Results)
        # =========================
        if option == "Borrower's List":
            st.markdown("### All Requested Borrowers")
            df_list = pd.DataFrame(st.session_state.clients)
            display_df = df_list[["Name", "Income (PHP)", "Debts (PHP)", "DTI", "Loan Amount", "Eligibility"]].copy()
            st.dataframe(display_df, use_container_width=True)

            st.markdown("---")
            st.subheader("Manage Borrowers")
            names = [c["Name"] for c in st.session_state.clients]
            selected_to_delete = st.selectbox("Select Borrower to Delete", names)
            
            if st.button("🗑️ Delete Selected Borrower", type="primary"):
                st.session_state.clients = [c for c in st.session_state.clients if c["Name"] != selected_to_delete]
                st.success(f"Deleted {selected_to_delete}")
                st.rerun()

        else:
            # Only show results if the form isn't currently active
            st.markdown("### Select Records to Display")
            all_names = [c["Name"] for c in st.session_state.clients]
            
            selected_borrower_name = st.selectbox(
                "Choose a borrower to view their specific data:", 
                all_names, 
                index=len(all_names)-1
            )
            
            borrower = next(c for c in st.session_state.clients if c["Name"] == selected_borrower_name)
            st.markdown("---")

            if option == "Borrower Overview":
                st.markdown(f"### Financial Overview for {borrower['Name']}")
                col1, col2, col3, col4, col5 = st.columns(5)
                dti_color = "#16a34a" if borrower['DTI'] < 0.4 else "#dc2626"
                
                metrics = {
                    "Name": {"value": borrower["Name"], "color": "#065f46"},
                    "Monthly Income": {"value": f"PHP {borrower['Income (PHP)']:,}", "color": "#065f46"},
                    "Existing Debt": {"value": f"PHP {borrower['Debts (PHP)']:,}", "color": "#065f46"},
                    "Debt-to-Income Ratio": {"value": f"{borrower['DTI']:.2f}", "color": dti_color},
                    "Requested Loan": {"value": f"PHP {borrower['Loan Amount']:,}", "color": "#065f46"}
                }

                for idx, (title, info) in enumerate(metrics.items()):
                    with [col1, col2, col3, col4, col5][idx]:
                        st.markdown(f"""
                            <div style="background-color:#ffffff; padding:20px; border-radius:12px; text-align:center; box-shadow:0 4px 8px rgba(0,0,0,0.1);">
                                <div style="font-weight:bold; font-size:18px; color:#065f46;">{title}</div>
                                <div style="font-size:24px; margin-top:5px; color:{info['color']};">{info['value']}</div>
                            </div>
                        """, unsafe_allow_html=True)

                st.markdown("### Decision Factors")
                col1, col2 = st.columns(2)
                with col1:
                    income_stability = "Strong" if borrower['Income (PHP)'] >= 2000 else "Weak"
                    dti_status = "Healthy" if borrower['DTI'] < 0.4 else "Risky"
                    st.markdown(f"- **Income Stability:** {income_stability}")
                    st.markdown(f"- **Debt-to-Income Ratio:** {dti_status}")
                with col2:
                    eligibility_color = "#16a34a" if borrower['Eligibility'] == "Eligible" else "#f59e0b"
                    st.markdown(f"- **Eligibility:** <span style='color:{eligibility_color}; font-weight:bold'>{borrower['Eligibility']}</span>", unsafe_allow_html=True)
                    st.markdown(f"- **Risk Level:** {borrower['Risk Level']}")

            elif option == "Debts Overview":
                st.markdown(f"### Debts for {borrower['Name']}")
                if borrower.get("Debt Details"):
                    for debt in borrower["Debt Details"]:
                        st.markdown(f"""<div style="background-color:#ffffff; padding:15px; border-radius:10px; margin-bottom:10px; box-shadow:0 3px 6px rgba(0,0,0,0.1);">
                            <strong>Debt Name:</strong> {debt.get('name', 'Unnamed Debt')} <br>
                            <strong>Amount:</strong> PHP {debt.get('amount', 0):,}</div>""", unsafe_allow_html=True)
                else:
                    st.info("No debts added for this borrower.")

            elif option == "Recommendations":
                st.markdown(f"### Recommendations for {borrower['Name']}")
                recommendations = []
                if borrower['DTI'] < 0.4: recommendations.append({"text": "✅ Keep DTI below 40%", "type": "good"})
                else: recommendations.append({"text": "⚠️ Reduce outstanding debt", "type": "warning"})
                
                for rec in recommendations:
                    color = "#16a34a" if rec["type"] == "good" else "#f59e0b"
                    st.markdown(f'<div style="background-color:{color}33; padding:15px; border-left:6px solid {color}; border-radius:8px; margin-bottom:10px;">{rec["text"]}</div>', unsafe_allow_html=True)

            elif option == "Loan Summary":
                st.markdown(f"### Summary for {borrower['Name']}")
                st.markdown(f"""<div style="background-color:#ffffff; padding:25px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.15);">
                    <h3>Loan Eligibility: {borrower['Eligibility']}</h3>
                    <p><strong>Loan Amount:</strong> PHP {borrower['Loan Amount']:,}</p>
                    <p><strong>DTI Ratio:</strong> {borrower['DTI']:.2f}</p>
                    <p><strong>Risk Score:</strong> {borrower['Score']}</p></div>""", unsafe_allow_html=True)

    @staticmethod
    def load_lottie_url(url: str):
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None