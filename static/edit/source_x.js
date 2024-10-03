function onOpenRow(event) {
    id = event.srcElement.parentElement.querySelector(".item_id").value
    window.location = `/edit/item/${id}`
}
function onDeleteRow(event) {
    id = event.srcElement.parentElement.querySelector(".item_id").value
    fetch("/item/delete", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    })
}
function onItemChange(event) {
    const row = event.srcElement.closest("tr")
    fetch("/item/update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            id: row.querySelector(".item_id").value,
            name: row.querySelector('.item_name').value,
            date_submitted: row.querySelector('.item_date').value,
            data: row.querySelector('.item_data').value,
            status_id: row.querySelector('.status').value
        })
    })
}
document.getElementById("add-item-button").addEventListener("click", event => {
    const rowTemplate = document.getElementById('row-template');
    const newRowFrag = rowTemplate.content.cloneNode(true);
    const newRow = newRowFrag.firstElementChild;
    event.srcElement.parentElement.querySelector('tbody').appendChild(newRow)

    const id = newRow.querySelector(".item_id")
    const updated = newRow.querySelector(".item_updated")

    newRow.querySelector(".item_date").valueAsDate = new Date();
    fetch("/item/create", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'accept': 'application/json',
        },
        body: JSON.stringify({
            source_id: document.getElementById("source").value,
            status_id: newRow.querySelector('.status').value,
            name: newRow.querySelector('.item_name').value,
            date_submitted: newRow.querySelector('.item_date').value,
            data: newRow.querySelector('.item_data').value,
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
        updated.value = data.last_updated
    });
})
fetch("/source", {
    method: "POST",
    headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        id: document.getElementById("source").value,
    })
})
.then(response => {
    if (!response.ok) {
        throw Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log(data, JSON.stringify(data));
    })
fetch("/source/status-groups", {
    method: "POST",
    headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify([{
        id: document.getElementById("source").value,
    }])
})
.then(response => {
    if (!response.ok) {
        throw Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log(data)
    l = []
    data.forEach(group => {
        l.push({id: group.id});
    })
    fetch("/status-group/statuses", {
        method: "POST",
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(l)
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data)
        statuses = document.getElementById("row-template").content.querySelector("select.status")
        data.forEach(status => {
            option = document.createElement("option")
            option.value = status.id
            option.textContent = status.name
            statuses.appendChild(option);
        })
        fetch("/source/items", {
            method: "POST",
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: document.getElementById("source").value
            })
        })
        .then(response => {
            if (!response.ok) {
                throw Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            data.forEach( item => {
                const rowTemplate = document.getElementById('row-template');
                const newRowFrag = rowTemplate.content.cloneNode(true);
                const newRow = newRowFrag.firstElementChild;
                document.getElementById("items").querySelector('tbody').appendChild(newRow)

                newRow.querySelector(".item_date").value = item.date_submitted
                newRow.querySelector(".item_id").value = item.id
                newRow.querySelector('.status').value = item.status_id
                newRow.querySelector('.item_name').value = item.name
                newRow.querySelector('.item_data').value = item.data
                newRow.querySelector('.item_updated').value = item.last_updated
            })
        })
    })
})