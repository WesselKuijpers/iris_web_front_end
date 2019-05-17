// async funtions for fetching the required data
// TODO: condense these functions

// history
// returns: OBJECT
async function getHistory() {
    let response = await fetch('/insight/data/history')
    let data = await response.json()
    return data
}

// classification report
// returns: OBJECT
async function getReport() {
    let response = await fetch('/insight/data/report')
    let data = await response.json()
    return data
}

// predict classes
// returns: OBJECT
async function getClasses() {
    let response = await fetch('/predict/classes')
    let data = await response.json()
    return data
}

//confusion matrix
// returns: OBJECT
async function getConfusionMatrix() {
    let response = await fetch('/insight/data/confusion_matrix')
    let data = await response.json()
    return data
}

// current training data
// returns: OBJECT
async function getCurrentSituation() {
    let response = await fetch('/insight/data/current_situation')
    let data = await response.json()
    return data
}

// function for plotting a line chart for history objects
// takes:
// OBJECT train, train data
// OBJECT val, validation data
// STRING trainLabel, train data label
// STRING valLabel, validation data label
// STRING id, the id of the canvas that should be a chart
// BOOL percentage, specify if the data in train and val arrays should be converted to percentages
// BOOL startAtZero, specify if the charts Y-axis should start at 0
// returns: VOID
function plotLineChart(train, val, trainLabel, valLabel, id, percentage = false, startAtZero = false) {
    let chart = document.getElementById(id).getContext('2d');

    // if the percentage bool is true convert it to percentages
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

    // plot the chart
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
            },
            animation: {
                duration: 0
            }
        }
    })
}

// function for plotting bar charts for the classification report
// OBJECT json_data, classification report api call data
// STRING data_key, what sub-array of the json_data array should be used in the graph E.G: 'support' of 'f1'
// STRING id, the id of the canvas that should be a chart
// BOOL percentage, whether the data from the json_data should be converted to a percentage
// returns: VOID
function plotReportChart(json_data, data_key, id, percentage = false) {
    let chart = document.getElementById(id).getContext('2d');

    keys = []
    data = []

    // fill the keys and data arrays with the required data
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

    // plot the chart
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

// a function for filling the confusion matrix head
// OBJECT data, data from the confusion matrix api call
// returns: VOID
function fillTableHead(data) {
    // get and create required elements
    let matrix = document.getElementById('confusion-matrix')
    let head = document.createElement("thead")
    let head_row = document.createElement("tr")
    let empty_th = document.createElement("th")

    // add leftmost th to table head
    empty_th.innerHTML = "Classes"
    head_row.appendChild(empty_th)

    // fill the rest of the tr
    data.forEach(function (label) {
        let th = document.createElement("th")
        th.innerHTML = label
        head_row.appendChild(th)
    })
    head.appendChild(head_row)
    matrix.appendChild(head)
}

// function for creating a row in the confusion matrix
// STRING label, the leftmost item of the row
// OBJECT row, the data the row should be filled with
// returns: 'tr' element
function createTableRow(label, row) {
    // create a table row
    let table_row = document.createElement("tr")
    // fill it
    let table_label = document.createElement("th")
    table_label.innerHTML = label
    table_row.appendChild(table_label)
    row.forEach(function (item) {
        let td = document.createElement("td")
        td.innerHTML = item
        table_row.appendChild(td)
    })
    // return it
    return table_row
}

// function for updating the progress metrics of the current situation
// is stored in a variable to be called at an interval
// returns: VOID
lp = function loadProgress() {
    // make an api caal
    getCurrentSituation().then(function (data) {
        // if it contains a substantial ammount of data, continue, else show a message
        if (data.length != 1) {
            // fill the progbar accordingly
            progbar = document.getElementById("epoch-progress")
            percentage = data[0]['epoch'] / data[0]['epochs'] * 100
            progbar.style.width = percentage + "%"
            progbar.innerHTML = "epoch " + data[0]['epoch'] + " of " + data[0]['epochs']

            // fill the current accuracy metric
            current_accuracy = document.getElementById('current-accuracy')
            current_accuracy.innerHTML = Math.round(data[0]['acc'] * 100 * 10) / 10 + "%"
            checkAndColour(current_accuracy, 'acc', data)

            // fill the current validation accuracy metric 
            current_validation_accuracy = document.getElementById('current-validation-accuracy')
            current_validation_accuracy.innerHTML = Math.round(data[0]['val_acc'] * 100 * 10) / 10 + "%"
            checkAndColour(current_validation_accuracy, 'val_acc', data)

            // fill the current loss metric
            current_loss = document.getElementById('current-loss')
            current_loss.innerHTML = Math.round(data[0]['loss'] * 10000) / 10000
            checkAndColour(current_loss, 'loss', data, true)

            // fill the current validation loss metric
            current_validation_loss = document.getElementById('current-validation-loss')
            current_validation_loss.innerHTML = Math.round(data[0]['val_loss'] * 10000) / 10000
            checkAndColour(current_validation_loss, 'val_loss', data, true)

            // fill the current situation graphs
            fillCurrentSituationGraphs(data)
        } else {
            document.getElementById("current-training-metrics").innerHTML = "<h1>No metrics were found</h1>"
        }
    })
}

// function for filling the graphs concerning the current training process
// OBJECT data, data from the current situation api call
// returns: VOID
function fillCurrentSituationGraphs(data) {
    // metric arrays
    let acc = []
    let val_acc = []
    let loss = []
    let val_loss = []

    // fill the metric arrays
    data.forEach(function (item){
        acc.push(item['acc'])
        val_acc.push(item['val_acc'])
        loss.push(item['loss'])
        val_loss.push(item['val_loss'])
    })

    // plot the current situation graphs on the metic arrays
    plotLineChart(acc, val_acc, "Accuracy", "Validation Accuracy", 'current-accuracy-chart', true, true)
    plotLineChart(loss, val_loss, "Loss", "Validation Loss", 'current-loss-chart')
}

// function for checking if the current situation is better than the previous situation
// if so, colour it green
// if not, colour it red
// ELEMENT elem, the html element that should be coloured
// STRING key, the key of the sub-array that should taken from the data array
// OBJECT data, the data from the current situation api call
// BOOL reverse, indicates if the value needs to be higher or lower then the previous situation to be coloured green
// returns: VOID
function checkAndColour(elem, key, data, reverse = false) {
    // if reverse means the action should be the other way around
    if (reverse) {
        // if the previous situation is smaller than the current situation colour it red 
        if (data[1][key] < data[0][key]) {
            elem.style.color = "red"
            elem.innerHTML += " <i class='fas fa-angle-up'></i>"
        } else {
            elem.style.color = "#007F0E"
            elem.innerHTML += " <i class='fas fa-angle-down'></i>"
        }
    } else {
        // if the current situation is smaller than the previous situation colour it red
        if (data[0][key] < data[1][key]) {
            elem.style.color = "red"
            elem.innerHTML += " <i class='fas fa-angle-down'></i>"
        } else {
            elem.style.color = "#007F0E"
            elem.innerHTML += " <i class='fas fa-angle-up'></i>"
        }
    }
}

// IMPORTANT: this action overwrites the standard popover evenhandler
// function for showing or hiding the informative popovers
// ELEMENT elem, the html element to be toggled
// returns, VOID
function togglePopOver(elem) {
    id = $(elem).data('bs.popover').tip.id
    popover = $("#" + id)
    if (popover.hasClass('hidden')) {
        popover.removeClass('hidden')
    } else {
        popover.addClass('hidden')
    }
}

// calls that need to happen only once, when the page loads:

// call the getHistory api call and call the required functions with the data it returns
getHistory().then(function (data) {
    plotLineChart(data['loss'], data['val_loss'], 'loss', 'validation loss', 'loss-chart')
    plotLineChart(data['acc'], data['val_acc'], 'accuracy', 'validation accuracy', 'accuracy-chart', true, true)
})

// call the getReport api call and call the required functions with the data it returns
getReport().then(function (data) {
    plotReportChart(data, 'precision', 'precision-chart', true)
    plotReportChart(data, 'recall', 'recall-chart', true)
    plotReportChart(data, 'f1-score', 'f-chart', true)
    plotReportChart(data, 'support', 'support-chart')
})

// call the getClasses api call and call the required functions with the data it returns
getClasses().then(function (classes) {
    fillTableHead(classes)
    getConfusionMatrix().then(function (data) {
        table_body = document.createElement("tbody")
        for (let key in data) {
            let label = classes[key]
            let row = data[key]
            let table_row = createTableRow(label, row)
            table_body.appendChild(table_row)
        }
        document.getElementById('confusion-matrix').appendChild(table_body)
    })
})

// load the progress for the current situation
lp()
// set an interval for loading the progress, every 100 seconds
setInterval(lp, 100000)
