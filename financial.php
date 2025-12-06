<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Credit Eligibility Predictor</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background: #f4f4f4;
        padding: 20px;
    }
    h1 {
        text-align: center;
    }
    #btn-generate {
        background: #007bff;
        color: white;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        display: block;
        margin: 20px auto;
        font-size: 18px;
        border-radius: 5px;
    }
    #btn-generate:hover {
        background: #0056b3;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 25px;
    }
    table, th, td {
        border: 1px solid #888;
    }
    th {
        background: #007bff;
        color: white;
        padding: 10px;
    }
    td {
        background: white;
        padding: 8px;
        text-align: center;
    }
    .eligible {
        color: green;
        font-weight: bold;
    }
    .not-eligible {
        color: red;
        font-weight: bold;
    }
</style>
</head>
<body>

<h1>Credit Eligibility Predictor</h1>

<button id="btn-generate">Generate Clients & Predict</button>

<table id="client-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Income ($)</th>
            <th>Debts ($)</th>
            <th>Payment %</th>
            <th>Score</th>
            <th>Eligibility</th>
        </tr>
    </thead>
    <tbody></tbody>
</table>

<script>
/* -----------------------
   Generate Random Clients
------------------------- */
function generateClients(num = 30) {
    let clients = [];

    for (let i = 0; i < num; i++) {
        const income = Math.floor(Math.random() * 70000) + 30000;     // 30k–100k
        const debts = Math.floor(Math.random() * 45000) + 5000;      // 5k–50k

        // Payment history (12 months of 0 or 1)
        const paymentHistory = Array.from({ length: 12 }, () =>
            Math.random() > 0.25 ? 1 : 0 // 75% chance of on-time payment
        );

        clients.push({
            id: i + 1,
            income,
            debts,
            paymentHistory
        });
    }

    return clients;
}

/* -----------------------
   Score Algorithm
------------------------- */
function calculateScore(client) {
    // Income-to-Debt Ratio
    const idr = client.income / client.debts;

    // Payment percentage
    const paymentPercentage =
        client.paymentHistory.reduce((a, b) => a + b, 0) / client.paymentHistory.length;

    // Final score (0.0 - 2.0 roughly)
    return 0.5 * idr + 0.5 * paymentPercentage;
}

/* -----------------------
   Eligibility Threshold
------------------------- */
function determineEligibility(score, threshold) {
    return score >= threshold ? "Eligible" : "Not Eligible";
}

/* -----------------------
   Sort Clients by Score
------------------------- */
function rankClients(clients) {
    return clients.sort((a, b) => b.score - a.score);
}

/* -----------------------
   Display Table
------------------------- */
function displayClients(clients) {
    const tbody = document.querySelector("#client-table tbody");
    tbody.innerHTML = ""; // Clear previous data

    clients.forEach(client => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${client.id}</td>
            <td>${client.income.toLocaleString()}</td>
            <td>${client.debts.toLocaleString()}</td>
            <td>${(client.paymentPercentage * 100).toFixed(1)}%</td>
            <td>${client.score.toFixed(2)}</td>
            <td class="${client.eligibility === 'Eligible' ? 'eligible' : 'not-eligible'}">
                ${client.eligibility}
            </td>
        `;

        tbody.appendChild(row);
    });
}

/* -----------------------
   Main Logic on Button Click
------------------------- */
document.getElementById("btn-generate").addEventListener("click", () => {
    let clients = generateClients(30);

    // Hash table simulation (key-value lookup)
    let clientMap = {};

    clients.forEach(client => {
        const score = calculateScore(client);
        const paymentPercentage =
            client.paymentHistory.reduce((a, b) => a + b, 0) / client.paymentHistory.length;

        client.score = score;
        client.paymentPercentage = paymentPercentage;
        client.eligibility = determineEligibility(score, 1.0); // threshold = 1.0

        // Store in hash table by ID
        clientMap[client.id] = client;
    });

    // Rank clients (sorting algorithm)
    clients = rankClients(clients);

    displayClients(clients);
});
</script>

</body>
</html>
