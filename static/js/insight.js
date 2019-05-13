async function getHistory() {
    let response = await fetch('/insight/data/history')
    let data = await response.json()
    return data
}

async function getReport() {
    let response = await fetch('/insight/data/report')
    let data = await response.json()
    return data
}

async function getClasses() {
    let response = await fetch('/predict/classes')
    let data = await response.json()
    return data
}

async function getConfusionMatrix() {
    let response = await fetch('/insight/data/confusion_matrix')
    let data = await response.json()
    return data
}

async function getCurrentSituation() {
    let response = await fetch('/insight/data/current_situation')
    let data = await response.json()
    return data
}

function plotLineChart(train, val, trainLabel, valLabel, id, percentage = false, startAtZero = false) {
    let chart = document.getElementById(id).getContext('2d');

    if (percentage) {
        let train_percent = []
        let val_percent = []

        train.forEach(element => {
            train_percent.push(element * 100)
        });

        val.forEach(element => {
            val_percent.push(element * 100)
        });

        train = train_percent
        val = val_percent
    }

    let myChart = new Chart(chart, {
        type: 'line',
        data: {
            labels: [...train.keys()],
            datasets: [
                {
                    label: trainLabel,
                    data: train,
                    fill: false,
                    backgroundColor: "#dd4b39",
                    borderColor: "#dd4b39"
                },
                {
                    label: valLabel,
                    data: val,
                    fill: false,
                    backgroundColor: "#000000",
                    borderColor: "#000000"
                }
            ]
        },
        options: {
            legend: {
                position: 'bottom'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: startAtZero
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'epochs'
                    }
                }]
            }
        }
    })
}

function plotReportChart(json_data, data_key, id, percentage = false) {
    let chart = document.getElementById(id).getContext('2d');

    keys = []
    data = []
    for (let key in json_data) {
        if (key != 'macro avg' && key != 'micro avg' && key != 'weighted avg') {
            keys.push(key)
            if (percentage) {
                data.push(json_data[key][data_key] * 100)
            } else {
                data.push(json_data[key][data_key])
            }
        }
    }

    let myChart = new Chart(chart, {
        type: 'bar',
        data: {
            labels: keys,
            datasets: [
                {
                    data: data,
                    backgroundColor: "#dd4b39"
                }
            ]
        },
        options: {
            legend: {
                display: false
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    })
}

function fillTableHead(data) {
    let matrix = document.getElementById('confusion-matrix')
    let head = document.createElement("thead")
    let head_row = document.createElement("tr")

    let empty_th = document.createElement("th")
    empty_th.innerHTML = "Classes"
    head_row.appendChild(empty_th)

    data.forEach(function (label) {
        let th = document.createElement("th")
        th.innerHTML = label
        head_row.appendChild(th)
    })
    head.appendChild(head_row)
    matrix.appendChild(head)
}

function createTableRows(label, row) {
    let table_row = document.createElement("tr")
    let table_label = document.createElement("th")
    table_label.innerHTML = label
    table_row.appendChild(table_label)
    row.forEach(function (item) {
        let td = document.createElement("td")
        td.innerHTML = item
        table_row.appendChild(td)
    })
    return table_row
}

function loadProgress() {
    getCurrentSituation().then(function (data) {
        progbar = document.getElementById("epoch-progress")
        percentage = data[0]['epoch'] / data[0]['epochs'] * 100
        progbar.style.width = percentage + "%"
        progbar.innerHTML = "epoch " + data[0]['epoch'] + " of " + data[0]['epochs']

        current_accuracy = document.getElementById('current-accuracy')
        current_accuracy.innerHTML = Math.round(data[0]['acc'] * 100 * 10) / 10 + "%"
        checkAndColour(current_accuracy, 'acc', data)

        current_validation_accuracy = document.getElementById('current-validation-accuracy')
        current_validation_accuracy.innerHTML = Math.round(data[0]['val_acc'] * 100 * 10) / 10 + "%"
        checkAndColour(current_validation_accuracy, 'val_acc', data)

        current_loss = document.getElementById('current-loss')
        current_loss.innerHTML = Math.round(data[0]['loss'] * 10000) / 10000
        checkAndColour(current_loss, 'loss', data, true)

        current_validation_loss = document.getElementById('current-validation-loss')
        current_validation_loss.innerHTML = Math.round(data[0]['val_loss'] * 10000) / 10000
        checkAndColour(current_validation_loss, 'val_loss', data, true)

        fillCurrentSituationGraphs(data)
    })
}

function fillCurrentSituationGraphs(data) {
    let acc = []
    let val_acc = []
    let loss = []
    let val_loss = []

    data.forEach(function (item){
        acc.push(item['acc'])
        val_acc.push(item['val_acc'])
        loss.push(item['loss'])
        val_loss.push(item['val_loss'])
    })

    plotLineChart(acc, val_acc, "Accuracy", "Validation Accuracy", 'current-accuracy-chart', true, true)
    plotLineChart(loss, val_loss, "Loss", "Validation Loss", 'current-loss-chart')
}

function checkAndColour(elem, key, data, reverse = false) {
    if (reverse) {
        if (data[1][key] < data[0][key]) {
            elem.style.color = "red"
            elem.innerHTML += " <i class='fas fa-angle-up'></i>"
        } else {
            elem.style.color = "#007F0E"
            elem.innerHTML += " <i class='fas fa-angle-down'></i>"
        }
    } else {
        if (data[0][key] < data[1][key]) {
            elem.style.color = "red"
            elem.innerHTML += " <i class='fas fa-angle-down'></i>"
        } else {
            elem.style.color = "#007F0E"
            elem.innerHTML += " <i class='fas fa-angle-up'></i>"
        }
    }
}

getHistory().then(function (data) {
    plotLineChart(data['loss'], data['val_loss'], 'loss', 'validation loss', 'loss-chart')
    plotLineChart(data['acc'], data['val_acc'], 'accuracy', 'validation accuracy', 'accuracy-chart', true, true)
})

getReport().then(function (data) {
    plotReportChart(data, 'precision', 'precision-chart', true)
    plotReportChart(data, 'recall', 'recall-chart', true)
    plotReportChart(data, 'f1-score', 'f-chart', true)
    plotReportChart(data, 'support', 'support-chart')
})

getClasses().then(function (classes) {
    fillTableHead(classes)
    getConfusionMatrix().then(function (data) {
        table_body = document.createElement("tbody")
        for (let key in data) {
            let label = classes[key]
            let row = data[key]
            let table_row = createTableRows(label, row)
            table_body.appendChild(table_row)
        }
        document.getElementById('confusion-matrix').appendChild(table_body)
    })
})

loadProgress()

function togglePopOver(elem) {
    id = $(elem).data('bs.popover').tip.id
    popover = $("#" + id)
    if (popover.hasClass('hidden')) {
        popover.removeClass('hidden')
    } else {
        popover.addClass('hidden')
    }
}

