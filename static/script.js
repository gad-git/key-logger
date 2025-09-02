async function loadData() {
    let response = await fetch('/data');
    let logs = await response.json();
    let table = document.getElementById('logTable');
    table.innerHTML = '';
    logs.forEach((item, i) => {
        let row = `<tr><td>${i+1}</td><td>${item.key}</td></tr>`;
        table.innerHTML += row;
    });
}

setInterval(loadData, 1000);
