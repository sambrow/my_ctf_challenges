async function fetchData() {
    return await fetch(`/query?price=${price.value}&price_op=${price_op.value}&limit=${limit.value}`).then(r => r.json())
}

async function renderTable() {
    const tableBody = document.querySelector('#data-table tbody')

    const data = await fetchData()

    tableBody.innerHTML = ''

    data.forEach((item) => {
        const row = document.createElement('tr')
        row.innerHTML = `<td><input type="checkbox"></td><td>${item.category}</td><td>${item.name}</td><td>${item.description}</td><td>${item.price}</td>`

        tableBody.appendChild(row)
    })
}

window.onload = function () {
    renderTable();
    query.onclick = renderTable
}
