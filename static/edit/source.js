function onSourceChange(event) {
    fetch("/source/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(event.srcElement.parentElement.querySelector('.source_id').value),
            name: event.srcElement.parentElement.querySelector('.source_title').value,
            type_id: event.srcElement.parentElement.querySelector('.source_type').value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    })
}
function onGroupRowUpdate(event) {
    const row = event.srcElement.closest('tr');
    fetch("/status-group/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: row.querySelector(".group_id").value,
            name: row.querySelector(".group_name").value,
            type: row.querySelector(".status_type").value
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    });
}
function onStatusRowUpdate() {
    const row = event.srcElement.closest('tr');
    fetch("/status/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: row.querySelector(".status_id").value,
            name: row.querySelector(".status_name").value,
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    });
}
function onDeleteGroupRow() {
    const row = event.srcElement.closest('tr')
    fetch("/status-group/delete", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(row.querySelector('.group_id').value)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        row.parentElement.removeChild(row);
    })
}
function onDeleteStatusRow() {
    const row = event.srcElement.closest('tr')
    fetch("/status/delete", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(row.querySelector('.status_id').value)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        row.parentElement.removeChild(row);
    })
}
function onDeleteTable() {
    const table = event.srcElement.closest('div')
    fetch("/source/delete", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: Number(table.querySelector('.source_id').value)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        table.parentElement.removeChild(table);
    })
}
function addStatusRowButtonListener(button) {
    button.addEventListener("click", event => {
        const rowTemplate = document.getElementById('status-row-template');
        const newRowFrag = rowTemplate.content.cloneNode(true);
        const newRow = newRowFrag.firstElementChild;
        button.parentElement.querySelector('tbody').appendChild(newRow)
        const id = newRow.querySelector(".status_id")
        fetch("/status/create", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json',
            },
            body: JSON.stringify({
                status_group_id: Number(button.closest('tr').querySelector('.group_id').value),
                name: newRow.querySelector('.status_name').value,
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
function addRowButtonListener(button) {
    button.addEventListener("click", event => {
        const rowTemplate = document.getElementById('row-template');
        const newRowFrag = rowTemplate.content.cloneNode(true);
        const newRow = newRowFrag.firstElementChild;
        button.parentElement.querySelector('tbody').appendChild(newRow)

        addStatusRowButtonListener(newRow.querySelector(".add-row-button"));

        const id = newRow.querySelector(".group_id")
        fetch("/status-group/create", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'accept': 'application/json',
            },
            body: JSON.stringify({
                source_id: Number(button.parentElement.querySelector('.source_id').value),
                name: newRow.querySelector('.group_name').value,
                type: newRow.querySelector('.status_type').value,
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
document.getElementById("add-source-button").addEventListener("click", event => {
    const dataDisplay = document.getElementById('data-display');
    const tableTemplate = document.getElementById('table-template');
    const newTable = tableTemplate.content.cloneNode(true);

    const id = newTable.querySelector(".source_id");
    const source_type = newTable.querySelector(".source_type")
    addRowButtonListener(newTable.querySelector(".add-row-button"));

    dataDisplay.appendChild(newTable);

    fetch("/source/create", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            name: "New Source",
            type_id: source_type.value
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

function getStatuses() {
    values = []
    for (group of document.getElementsByClassName("group_id")) {
        values.push({id: Number(group.value)})
    }
    fetch("/status-group/statuses", {
        method: "POST",
        headers: {
            'accept': 'application/json',
            "Content-Type": "application/json"
        },
        body: JSON.stringify(values)
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
        data.forEach(status => {
            source = Array.from(document.getElementsByClassName("group_id"))
                    .filter(e => e.value == status.status_group_id)[0]
                    .closest("tr")
                    .querySelector("tbody");
            const rowTemplate = document.getElementById("status-row-template");
            const newRow = rowTemplate.content.cloneNode(true);
            newRow.querySelector(".status_id").value = status.id;
            newRow.querySelector(".status_name").value = status.name;
            source.appendChild(newRow);
        });
    });
}
function getStatusGroups() {
    values = []
    for (source of document.getElementsByClassName("source_id")) {
        values.push({id: Number(source.value)});
    }
    fetch("/source/status-groups", {
        method: "POST",
        headers: {
            'accept': 'application/json',
            "Content-Type": "application/json"
        },
        body: JSON.stringify(values)
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        data.forEach(status_group => {
            source = Array.from(document.getElementsByClassName("source_id"))
                .filter(e => e.value == status_group.source_id)[0]
                .closest("div")
                .querySelector("tbody");
            const rowTemplate = document.getElementById("row-template")
            const newRow = rowTemplate.content.cloneNode(true);
            newRow.querySelector(".group_name").value = status_group.name
            newRow.querySelector(".group_id").value = status_group.id
            newRow.querySelector(".status_type").value = status_group.type
            addStatusRowButtonListener(newRow.querySelector(".add-row-button"))
            source.appendChild(newRow)
        })
        getStatuses();
    })
}
function getSources() {
    fetch("/source/all", {
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
        const template = document.getElementById("table-template")
        const datadisplay = document.getElementById("data-display")
        data.forEach(source => {
            console.log(data)
            const clone = template.content.cloneNode(true);
            
            clone.querySelector(".source_title").value = source.name
            clone.querySelector(".source_id").value = source.id
            clone.querySelector(".source_type").value = source.type

            addRowButtonListener(clone.querySelector(".add-row-button"));

            datadisplay.appendChild(clone);
        })
        getStatusGroups()
    })
}
function getSourceTypes() {
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
        const template = document.getElementById("table-template")
        const select = template.content.querySelector('.source_type')

        data.forEach(type => {
            const option = document.createElement("option")
            option.value = type.id
            option.textContent = type.name
            select.appendChild(option)
        })

        getSources()
    })
}
getSourceTypes()