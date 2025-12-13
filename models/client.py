class Client:
    def __init__(self, client_id, income, debts, payment_percent):
        self.client_id = client_id
        self.income = income
        self.debts = debts
        self.payment_percent = payment_percent
        self.score = self.calculate_score()
        self.eligibility = "Approved" if self.score >= 2.0 else "Declined"
        self.risk_level = self.calculate_risk()

    def calculate_score(self):
        return round(
            (self.income / (self.debts + 1)) * 0.6 + (self.payment_percent / 100) * 0.4,
            2
        )

    def calculate_risk(self):
        if self.score >= 2.5:
            return "Low"
        elif self.score >= 1.5:
            return "Medium"
        return "High"

    def to_dict(self):
        return {
            "Client ID": self.client_id,
            "Income ($)": self.income,
            "Debts ($)": self.debts,
            "Payment %": self.payment_percent,
            "Score": self.score,
            "Eligibility": self.eligibility,
            "Risk Level": self.risk_level
        }
