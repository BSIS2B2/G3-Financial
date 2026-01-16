class Client:
    def __init__(self, client_id, income, debts, loan_amount=10000, name="", debt_details=None):
        self.client_id = client_id
        self.income = income
        self.debts = debts
        self.loan_amount = loan_amount  # Requested loan
        self.name = name
        self.debt_details = debt_details if debt_details else []

        self.dti = self.calculate_dti()
        self.score = self.calculate_score()

        self.eligibility = self.calculate_eligibility()
        self.risk_level = self.calculate_risk_level()

    def calculate_dti(self):
        return round(self.debts / max(self.income, 1), 2)

    def calculate_score(self):
        income_factor = min(self.income / 4000, 1)
        debt_factor = 1 - min(self.dti, 1)
        return round((income_factor * 0.6) + (debt_factor * 0.4), 2)

    def calculate_risk_level(self):
        if self.score >= 0.7:
            return "Low"
        elif self.score >= 0.4:
            return "Medium"
        return "High"

    def calculate_eligibility(self):
        if self.score >= 0.7:
            return "Eligible"
        elif self.score >= 0.4:
            return "Conditionally Eligible"
        return "Not Eligible"

    def to_dict(self):
        return {
            "Client ID": self.client_id,
            "Name": self.name,
            "Income (PHP)": self.income,
            "Debts (PHP)": self.debts,
            "Loan Amount": self.loan_amount,  # <-- include only once
            "Debt Details": self.debt_details,
            "DTI": self.dti,
            "Score": self.score,
            "Eligibility": self.eligibility,
            "Risk Level": self.risk_level
        }
