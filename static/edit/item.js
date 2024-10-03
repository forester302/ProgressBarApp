function updateData(event) {
    o = []
    for (data of document.getElementsByClassName("data")) {
        o.push({id: Number(data.parentElement.querySelector(".id").value), data: data.value})
    }
    fetch("/item/update/data", {
        method: "POST",
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id: Number(document.getElementById("item").value),
            data: JSON.stringify(o)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
    })
    return o
}
async function fetchType(id) {
    let p = new Promise(async (resolve, reject) => {
        response = await fetch("/source-type", {
            method: "POST",
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
            })
        })
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        data = await response.json();
        console.log(data, JSON.stringify(data));
        const item = document.createElement("div")
        item.classList.add("item")
        item.id = "item"
        data.data.forEach(data => {
            console.log(data)
            const field = document.createElement('div');
            field.classList.add("data-field")
            const label = document.createElement('label');
            label.textContent = data.data_label;
            const id = document.createElement('input');
            id.hidden = true;
            id.value = data.id
            id.id = `data_${data.id}`
            id.classList.add("id")
            field.appendChild(id);
            if (data.data_label_pos === "left") {
                field.classList.add("left");
                field.appendChild(label);
            } else if (data.data_label_pos === "up") {
                field.appendChild(label);
            }
            item.appendChild(field)

            if (data.data_edit == "dropdown" && Array.isArray(JSON.parse(data.data_options))) {
                const select = document.createElement("select")
                for (option of JSON.parse(data.data_options)) {
                    const optionEl = document.createElement("option")
                    optionEl.value = option
                    optionEl.textContent = option
                    select.appendChild(optionEl)
                }
                select.onchange = updateData
                select.classList.add("data")
                field.appendChild(select)
            } 
            else if (data.data_edit == "slider" && JSON.parse(data.data_options).min != null) {
                options = JSON.parse(data.data_options)
                const slider = document.createElement("input")
                slider.type = "range"
                slider.min = options.min
                slider.max = options.max
                slider.oninput = event => {
                    event.srcElement.parentElement.querySelector("span.value").textContent = event.srcElement.value
                }
                slider.onchange = updateData
                slider.classList.add("data")
                field.appendChild(slider)

                field.querySelector("label").innerHTML += ": <span class=\"value\">UNDEFINED</span>";
            } 
            else if (data.data_edit == "input") {
                const input = document.createElement("input")
                input.onchange = updateData
                input.classList.add("data")
                field.appendChild(input)
            } 
            else if (data.data_edit == "textbox") {
                const textbox = document.createElement("textarea")
                textbox.onchange = updateData
                textbox.classList.add("data")
                field.appendChild(textbox)
            }
            resolve();
        })
        document.body.appendChild(item)
    });
    return p;
}
async function fetchSource(id) {
    let p = new Promise(async (resolve, reject) => {
        response = await fetch("/source", {
            method: "POST",
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: id,
            })
        })
        if (!response.ok) {
            throw Error(`HTTP error! Status: ${response.status}`);
        }
        data = await response.json();
        console.log(data, JSON.stringify(data));
        await fetchType(data.type)
        resolve();
    })
    return p;
}
fetch("/item", {
    method: "POST",
    headers: {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        id: Number(document.getElementById("item").value),
    })
})
.then(response => {
    if (!response.ok) {
        throw Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
})
.then(async data => {
    console.log(data, JSON.stringify(data));
    document.getElementById("name").textContent = data.name
    await fetchSource(data.source_id)
    console.log(data.data);
    if (data.data == "") data.data = JSON.stringify(updateData());
    data = JSON.parse(data.data);
    for (item of data) {
        document.getElementById(`data_${item.id}`).parentElement.querySelector(".data").value = item.data
    }
});