async function getTranslation() {
    let response = await fetch('/translate/')
    let data = await response.json()
    return data
}

function translatePage() {
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    var lng = ca[0].replace('lng=', '')

    getTranslation().then(function (data) {
        let curr_language = Object.entries(data[lng]['translations'])
        curr_language.forEach(function(item){
            elem = document.getElementById(item[0])
            if(elem != null) {
                elem.innerHTML = item[1]
            }
        })
    })
}

function fillLanguageSelect() {
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    var lng = ca[0].replace('lng=', '')

    getTranslation().then(function (data) {
        let languages = Object.entries(data)
        let dropdown = document.getElementById("language-select")
        languages.forEach(function(language){
            option = document.createElement("option")
            option.value = language[0]
            option.innerHTML = language[1]["fullname"]
            if(option.value == lng) {
                option.setAttribute('selected', true)
            }
            dropdown.appendChild(option)
        })
    })
}

function setLanguage(lng) {
    document.cookie = "lng=" + lng
    translatePage()
}
