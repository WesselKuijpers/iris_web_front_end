function sendPredictData() {
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

function showMessage(elem) {
    document.getElementById('result-negative').classList.add("hidden")
    document.getElementById('result-positive').classList.remove("hidden")
    elem.selectedIndex = 0
}

function fillForm(data) {
    console.log(data)
    document.getElementById('category').value = data[0]
    document.getElementById('location').value = data[1]
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

    console.log(settings.data)

    $.ajax(settings).success(function (response) {
        console.log(response)
        document.getElementById('result-positive').classList.remove('hidden')        
    })
}