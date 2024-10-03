function onDeleteRow(event) {
    const row = event.srcElement.closest('tr')
    fetch("/source-data/delete", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(row.querySelector('.data_id').value)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        row.parentElement.removeChild(row);
    })
    
}
function onDeleteTable(event) {
    const table = event.srcElement.closest('div')
    fetch("/source-type/delete", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(table.querySelector('.type_id').value)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        table.parentElement.removeChild(table);
    })
    
}
function onRowUpdate(event) {
    const row = event.srcElement.closest('tr');
    fetch("/source-data/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(row.querySelector('.data_id').value),
            data_type: row.querySelector('.data_type').value,
            data_display: row.querySelector('.data_display').value,
            data_label: row.querySelector('.data_label').value,
            data_label_pos: row.querySelector('.data_label_pos').value,
            data_edit: row.querySelector('.data_edit').value,
            data_options: row.querySelector('.data_options').value,
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    });
}
function onTitleChange(event) {

    fetch("/source-type/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(event.srcElement.parentElement.querySelector('.type_id').value),
            name: event.srcElement.value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    })
}
function addRowButtonListener(button) {
    button.addEventListener("click", event => {
        const rowTemplate = document.getElementById('row-template');
        const newRowFrag = rowTemplate.content.cloneNode(true);
        const newRow = newRowFrag.firstElementChild;
        button.parentElement.querySelector('tbody').appendChild(newRow)

        const id = newRow.querySelector(".data_id")
        fetch("/source-data/create", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json',
            },
            body: JSON.stringify({
                type_id: Number(button.parentElement.querySelector('.type_id').value),
                data_type: newRow.querySelector('.data_type').value,
                data_display: newRow.querySelector('.data_display').value,
                data_label: newRow.querySelector('.data_label').value,
                data_label_pos: newRow.querySelector('.data_label_pos').value,
                data_edit: newRow.querySelector('.data_edit').value,
                data_options: newRow.querySelector('.data_options').value,
            })
        })
        .then(response => {
            if (!response.ok) {
                throw Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            id.value = data.id
        });
    })
}
document.getElementById("add-table-button").addEventListener("click", event => {
    const dataDisplay = document.getElementById('data-display');
    const tableTemplate = document.getElementById('table-template');
    const newTable = tableTemplate.content.cloneNode(true);

    const id = newTable.querySelector(".type_id");
    console.log(newTable.querySelector(".add-row-button"))
    addRowButtonListener(newTable.querySelector(".add-row-button"));

    dataDisplay.appendChild(newTable);

    fetch("/source-type/create", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            name: "New Type"
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        id.value = data.id
    });
})

function displayData(data) {
    const dataDisplay = document.getElementById('data-display');
    dataDisplay.innerHTML = ''; // Clear existing content

    data.forEach(source => {
        const tableTemplate = document.getElementById('table-template');
        const newTable = tableTemplate.content.cloneNode(true);
        newTable.querySelector('.type_title').value = source.name;
        newTable.querySelector('.type_id').value = source.id
        addRowButtonListener(newTable.querySelector(".add-row-button"));

        const tbody = newTable.querySelector('tbody');
        source.data.forEach(item => {
            const rowTemplate = document.getElementById('row-template');
            const newRow = rowTemplate.content.cloneNode(true);
            newRow.querySelector('.data_id').value = item.id;
            newRow.querySelector('.data_type').value = item.data_type;
            newRow.querySelector('.data_display').value = item.data_display;
            newRow.querySelector('.data_label').value = item.data_label;
            newRow.querySelector('.data_label_pos').value = item.data_label_pos;
            newRow.querySelector('.data_edit').value = item.data_edit
            newRow.querySelector('.data_options').value = item.data_options
            tbody.appendChild(newRow);
        });
        dataDisplay.appendChild(newTable);
    });
}

fetch("/source-type/all", {
    method: "POST",
    headers: {
        'accept': 'application/json',
    },
})
.then(response => {
    if (!response.ok) {
        throw Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log(data, JSON.stringify(data));
    displayData(data);
})