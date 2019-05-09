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

function plotReportChart(json_data, data_key, id) {
    let chart = document.getElementById(id).getContext('2d');

    keys= []
    data = []
    for (let key in json_data) {
        if (key != 'macro avg' && key != 'micro avg' && key != 'weighted avg') {
            keys.push(key)
            data.push(json_data[key][data_key] * 100)
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
                        min: Math.min(...data) - 10
                    }
                }]
            }
        }
    })
}

function plotSupportChart(json_data) {
    let chart = document.getElementById('support-chart').getContext('2d');

    keys= []
    data = []
    for (let key in json_data) {
        if (key != 'macro avg' && key != 'micro avg' && key != 'weighted avg') {
            keys.push(key)
            data.push(json_data[key]["support"])
        }
    }

    let myChart = new Chart(chart, {
        type: 'doughnut',
        data: {
            labels: keys,
            datasets: [
                {
                    data: data,
                    backgroundColor: ["#DD4B39", 
                                      "#000000", 
                                      "#ff0000", 
                                      "#c0c0c0", 
                                      "#404040", 
                                      "#7f0000", 
                                      "#bc0000", 
                                      "#606060",
                                      "#5b0000",
                                      "#350000",
                                      "#8b6969",
                                      "#cd9b9b",
                                      "#802a2a",
                                      "#a52a2a",
                                      "#EE2c2c",
                                      "#600000",
                                      "#330000",
                                      "#e60000",
                                      "#ff4141",
                                      "#ffbbbb",
                                      "#fee8e7",
                                      "#e3170d",
                                      "#e7dddc",
                                      "#FF664D",
                                      "#ffe8e6",
                                      "#8b7d7b",
                                      "#8A3324",
                                      "#C1AEA8",
                                      "#FF5721",
                                      "#5E2612",
                                      "#5C4033",
                                      "#FF6600",
                                      "#B78D6F",
                                      "#D0CECD",
                                      "#FFE2C8",
                                      "#B67C3D",
                                      "#DFC9AC",
                                      "#FFA114"
                                    ]
                }
            ]
        },
        options: {
            legend: {
                display: true,
                position: "bottom"
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

    data.forEach(function(label) {
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
    row.forEach(function(item) {
        let td = document.createElement("td")
        td.innerHTML = item
        table_row.appendChild(td)
    })
    return table_row
}

function loadProgress() {
    getCurrentSituation().then(function(data) {
        progbar = document.getElementById("epoch-progress")
        percentage = data['epoch'] / data['epochs'] * 100
        progbar.style.width = percentage + "%"
        progbar.innerHTML = "epoch " + data['epoch'] + " of " + data['epochs']

        document.getElementById('current-accuracy').innerHTML = Math.round(data['acc'] * 100 * 10) / 10 + "%" 
        document.getElementById('current-validation-accuracy').innerHTML = Math.round(data['val_acc'] * 100 * 10) / 10 + "%"
        document.getElementById('current-loss').innerHTML = Math.round(data['loss'] * 10000) / 10000
        document.getElementById('current-validation-loss').innerHTML = Math.round(data['val_loss'] * 10000) / 10000
    })
}

getHistory().then(function(data) {
    plotLineChart(data['loss'], data['val_loss'], 'loss', 'validation loss', 'loss-chart')
    plotLineChart(data['acc'], data['val_acc'], 'accuracy', 'validation accuracy', 'accuracy-chart', true, true)
})

getReport().then(function(data) {
    plotReportChart(data, 'precision', 'precision-chart')
    plotReportChart(data, 'recall', 'recall-chart')
    plotReportChart(data, 'f1-score', 'f-chart')
    plotSupportChart(data)
})

getClasses().then(function(classes) {
    fillTableHead(classes)
    getConfusionMatrix().then(function(data) {
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

