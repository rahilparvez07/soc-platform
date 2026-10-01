async function loadAlerts() {

    const response = await fetch(
        "http://127.0.0.1:5000/api/alerts"
    );

    const alerts = await response.json();

    updateStatistics(alerts);
    displayAlerts(alerts);
}


function updateStatistics(alerts) {

    document.getElementById("total-alerts").textContent =
        alerts.length;

    const high = alerts.filter(
        alert => alert.severity === "HIGH"
    ).length;

    const medium = alerts.filter(
        alert => alert.severity === "MEDIUM"
    ).length;

    const low = alerts.filter(
        alert => alert.severity === "LOW"
    ).length;

    document.getElementById("high-alerts").textContent = high;
    document.getElementById("medium-alerts").textContent = medium;
    document.getElementById("low-alerts").textContent = low;
}


function displayAlerts(alerts) {

    const table = document.getElementById("alerts-table");

    table.innerHTML = "";

    alerts.forEach(alert => {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${alert.id}</td>

            <td>
                <a href="/investigation.html?id=${alert.id}"
                   class="alert-link">
                    ${alert.rule}
                </a>
            </td>

            <td class="severity-${alert.severity.toLowerCase()}">
                ${alert.severity}
            </td>

            <td>${alert.source_ip}</td>

            <td>${alert.failed_attempts}</td>

            <td>${alert.mitre_attack}</td>
        `;

        table.appendChild(row);
    });
}
loadAlerts();