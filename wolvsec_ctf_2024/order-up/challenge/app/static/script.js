async function fetchData() {
    return await fetch('/query?col1=category&col2=item_name&col3=description&col4=price&order=category,item_name').then(r => r.json())
}

async function renderTable() {
    const tableBody = document.querySelector('#data-table tbody')

    const data = await fetchData()

    tableBody.innerHTML = ''

    data.forEach((item) => {
        const row = document.createElement('tr')
        row.innerHTML = `<td><input type="checkbox"></td><td>${item.category}</td><td>${item.item_name}</td><td>${item.description}</td><td>${item.price}</td>`

        tableBody.appendChild(row)
    })
}

window.onload = function () {
  renderTable();
}
