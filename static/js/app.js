function sendPredictData() {
    console.log("gothere")
    document.getElementById('main').classList.add("hidden")
    document.getElementById('spinner').classList.remove("hidden")


    let input = document.getElementById('upload-input')
    let files = input.files

    if (files.length) {
        let settings = {
            crossDomain: false,
            processData: false,
            contentType: false,
            type: 'POST',
            url: "/predict/",
            mimeType: 'multipart/form-data'
        }

        let formData = new FormData()
        formData.append("image", files[0])
        settings.data = formData

        let response = $.ajax(settings)
            .success(function (response) {
                decodedResponse = JSON.parse(response)

                document.getElementById('result-img').innerHTML = "<img src='" + decodedResponse[1] + "'>"
                document.getElementById('result-text').innerHTML = decodedResponse[0]

                document.getElementById('spinner').classList.add('hidden')
                document.getElementById('result').classList.remove('hidden')

                return decodedResponse
            })
            .fail(function () {
                alert("An error occured")
                reset()
            })

        return response
    }
}

function reset() {
    document.getElementById('spinner').classList.add("hidden")
    document.getElementById("result").classList.add("hidden")
    document.getElementById("main").classList.remove("hidden")
    document.getElementById('result-form').classList.remove('hidden')
    document.getElementById('result-negative').classList.add('hidden')
    document.getElementById('result-positive').classList.add('hidden')
    document.getElementById('upload-input').value = ""
    document.getElementById('categorical-select').classList.remove('hidden')
}

function showForm(elem) {
    document.getElementById('result-form').classList.add('hidden')
    if (elem.value == 1) {
        sendSaveData()
    } else if (elem.value == 2) {
        document.getElementById('result-negative').classList.remove('hidden')
    } else {
        alert("Please select a value")
    }
    elem.selectedIndex = 0
}

function negativeHandler(elem) {
    target = document.getElementById('categorical-select')
    target.value = elem.value
    sendSaveData()
    target.classList.add("hidden")
    target.selectedIndex = 0
}

function showMessage(elem) {
    document.getElementById('result-negative').classList.add("hidden")
    document.getElementById('result-positive').classList.remove("hidden")
    elem.selectedIndex = 0
}

function fillForm(data) {
    newData = JSON.parse(data)
    document.getElementById('category').value = newData[0]
    document.getElementById('location').value = newData[1]
}

function sendSaveData() {
    let settings = {
        crossDomain: false,
        processData: false,
        contentType: false,
        type: 'POST',
        url: "/predict/save",
        mimeType: 'multipart/form-data'
    }

    cat = document.getElementById('category').value
    loc = document.getElementById('location').value

    let formData = new FormData()
    formData.append("category", cat)
    formData.append("location", loc)
    settings.data = formData

    $.ajax(settings)
    .success(function () {
        document.getElementById('result-positive').classList.remove('hidden')
    })
    .fail(function () {
        alert("Something went wrong, please try again later")
        reset()
    })
}
