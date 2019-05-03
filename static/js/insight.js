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

function plotLineChart(train, val, trainLabel, valLabel, id) {
    let chart = document.getElementById(id).getContext('2d');
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
            }
        }
    })
}

function plotPrecisionChart(json_data) {
    let chart = document.getElementById('precision-chart').getContext('2d');

    keys= []
    data = []
    for (let key in json_data) {
        if (key != 'macro avg' && key != 'micro avg' && key != 'weighted avg') {
            keys.push(key)
            data.push(json_data[key]['precision'])
        }
    }

    console.log(data)

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
            }
        }
    })
}

getHistory().then(function(data) {
    plotLineChart(data['loss'], data['val_loss'], 'loss', 'validation loss', 'loss-chart')
    plotLineChart(data['acc'], data['val_acc'], 'accuracy', 'validation accuracy', 'accuracy-chart')
})

getReport().then(function(data) {
    plotPrecisionChart(data)
})