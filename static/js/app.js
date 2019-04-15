function sendData() {
    document.getElementById('main').classList.add("hidden")
    document.getElementById('spinner').classList.remove("hidden")


    let input = document.getElementById('upload-input')
    let files = input.files

    if (files.length) {
        let settings = {
            async: true,
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

        $.ajax(settings)
            .done(function (response) {
                let decodedResponse = JSON.parse(response)

                document.getElementById('result-img').innerHTML = "<img src='" + decodedResponse[1] + "'>"
                document.getElementById('result-text').innerHTML = decodedResponse[0]

                document.getElementById('spinner').classList.add('hidden')
                document.getElementById('result').classList.remove('hidden')
            })
            .fail(function () {
                alert("An error occured")
                reset()
            })
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