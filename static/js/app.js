// function for sending the data to the predict service and using the reponse
// returns: VOID
function sendPredictData() {
    // show spinner
    document.getElementById('main').classList.add("hidden")
    document.getElementById('spinner').classList.remove("hidden")

    // fetch form data
    let input = document.getElementById('upload-input')
    let files = input.files

    // if a file was inputted send the request
    if (files.length) {
        // request settings
        let settings = {
            crossDomain: false,
            processData: false,
            contentType: false,
            type: 'POST',
            url: "http://localhost:5000/predict/",
            mimeType: 'multipart/form-data'
        }

        // create formdata
        let formData = new FormData()
        formData.append("image", files[0])
        settings.data = formData

        // send the request and use the data to fill the result
        // if it fails, show a message
        let response = $.ajax(settings)
            .success(function (response) {
                decodedResponse = JSON.parse(response)

                document.getElementById('result-img').innerHTML = "<img src='http://localhost:5000/" + decodedResponse[1] + "'>"
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

// function for resetting the page to normal
// returns: VOID
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

// function for showing the survey form
// ELEMENT elem, the html element that containes required data
// returns: VOID
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

// function for handling the negative response to the survey
// ELEMENT elem, the html element that contains needed data
// returns: VOID
function negativeHandler(elem) {
    category = document.getElementById('category')
    category.value = elem.value
    sendSaveData()
}

// function for showing the 'thank you!' message
// ELEMENT elem, the element that is to be reset
// returns: VOID
function showMessage(elem) {
    document.getElementById('result-negative').classList.add("hidden")
    document.getElementById('result-positive').classList.remove("hidden")
    elem.selectedIndex = 0
}

// function for filling the categorical select in the survey
// OBJECT data, data from the get classes api call
// returns: VOID
function fillForm(data) {
    newData = JSON.parse(data)
    document.getElementById('category').value = newData[0]
    document.getElementById('location').value = newData[1]
}

// function for sending a request for saving the predicted image to the dataset
// returns: VOID
function sendSaveData() {
    // options
    let settings = {
        crossDomain: false,
        processData: false,
        contentType: false,
        type: 'POST',
        url: "http://localhost:5000/predict/save",
        mimeType: 'multipart/form-data'
    }

    // get values from form
    cat = document.getElementById('category').value
    loc = document.getElementById('location').value

    // create form data
    let formData = new FormData()
    formData.append("category", cat)
    formData.append("location", loc)
    settings.data = formData

    // send the request
    // if it fails show a message
    $.ajax(settings)
    .success(function () {
        document.getElementById('result-positive').classList.remove('hidden')
        target = document.getElementById('categorical-select')
        target.classList.add("hidden")
        target.selectedIndex = 0
    })
    .fail(function () {
        alert("Something went wrong, please try again later")
        reset()
    })
}

// function for filling the result form select with the classes from the get classes api call
// returns: VOID
function fillCategoricalSelect() {
    // setting
    let settings = {
        crossDomain: false,
        processData: false,
        contentType: false,
        type: 'GET',
        url: "http://localhost:5000/predict/classes",
    }

    // make the ajax call
    // if not succesfull, show a message 
    $.ajax(settings)
    .success(function (response) {
        let select = document.getElementById('categorical-select')

        response.forEach( function(item){
            let option = document.createElement('option')
            option.value = item
            option.innerHTML = item
            select.appendChild(option)
        })
    })
    .fail(function () {
        document.getElementById('result-negative').innerHTML = "<h5>Oops... something went wrong fetching the form data, please try again later<h5>"
    })
}

// function containing things that need to happen only once, at the load of the page, like the translations
// returns: VOID
function load() {
    // translate page
    translatePage()
    // fill the select box for languages
    fillLanguageSelect()
}

// function for making a fetch api call
// STRING route, the route to which the call is made
// returns: OBJECT
async function getApiData(route) {
    let response = await fetch(route)
    let data = await response.json()
    return data
}