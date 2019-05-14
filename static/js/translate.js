// async function for making an api call to fetch the translation data
// returns: ARRAY
async function getTranslation() {
    let response = await fetch('/translate/')
    let data = await response.json()
    return data
}

// function for making an api call fetching the translations an replacing the corresponding keys
// returns: VOID
function translatePage() {
    // get the language cookie
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    var lng = ca[0].replace('lng=', '')

    // get the translation by the formatted cookie and replacing the element by key
    getTranslation().then(function (data) {
        let curr_language = Object.entries(data[lng]['translations'])
        curr_language.forEach(function (item) {
            elem = document.getElementById(item[0])
            if (elem != null) {
                elem.innerHTML = item[1]
            }
        })
    })
}

// function for filling the select where the language can be selected
// returns: VOID
function fillLanguageSelect() {
    // get and decode the language cookie
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    var lng = ca[0].replace('lng=', '')

    // get all the translations and fill the select with them
    getTranslation().then(function (data) {
        let languages = Object.entries(data)
        let dropdown = document.getElementById("language-select")
        languages.forEach(function (language) {
            option = document.createElement("option")
            option.value = language[0]
            option.innerHTML = language[1]["fullname"]
            if (option.value == lng) {
                option.setAttribute('selected', true)
            }
            dropdown.appendChild(option)
        })
    })
}

// function for setting the language cookie and reloading the translation
// returns: VOID
function setLanguage(lng) {
    document.cookie = "lng=" + lng
    translatePage()
}
