async function fetchLogs() {
    const client_id = document.getElementById("client-id").value;
    const word = document.getElementById("word").value;
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;

    const params = new URLSearchParams();
    if(client_id) params.append("client_id", client_id);
    if(word) params.append("word", word);
    if(start) params.append("start", start);
    if(end) params.append("end", end);

    const response = await fetch("/get_logs?" + params.toString());
    const logs = await response.json();
    const tableBody = document.getElementById("logs-body");
    tableBody.innerHTML = "";

    logs.forEach(log => {
        const row = document.createElement("tr");
        const idCell = document.createElement("td");
        idCell.textContent = log.client_id;
        const dateCell = document.createElement("td");
        dateCell.textContent = log.received_at;
        const dataCell = document.createElement("td");
        dataCell.textContent = log.data;
        row.appendChild(idCell);
        row.appendChild(dateCell);
        row.appendChild(dataCell);
        tableBody.appendChild(row);
    });
}

setInterval(fetchLogs, 3000);
window.onload = fetchLogs;

document.getElementById("filter-form").addEventListener("submit", e => {
    e.preventDefault();
    fetchLogs();
});
