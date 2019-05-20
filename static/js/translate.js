// function for making an api call fetching the translations an replacing the corresponding keys
// returns: VOID
function translatePage() {
    var lng = getLanguageCookie()

    console.log("inside translatepage")
    console.log(lng)

    // get the translation by the formatted cookie and replacing the element by key
    getApiData('/translate/').then(function (data) {
        let curr_language = data[lng]["translations"]

        for (let item in curr_language) {
            elem = document.getElementById(item)
            if (elem != null) {
                elem.innerHTML = curr_language[item]
            }
        }
    })
}

// function for filling the select where the language can be selected
// returns: VOID
function fillLanguageSelect() {
    // get and decode the language cookie
    var lng = getLanguageCookie()

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
    clearCookies(['language'])
    document.cookie = "language=" + lng
    translatePage()
}

// function for getting the language cookie
// returns: STRING
function getLanguageCookie() {
    // get the language cookie
    let decodedCookie = decodeURIComponent(document.cookie);
    let cookieArray = decodedCookie.split('; ');

    // find out if there is a language cookie, and if so return it, else return default language
    let lng

    for (let cookie in cookieArray) {
        cookieString = cookieArray[cookie]
        if (cookieString.includes('language=')) {
            lng = cookieString.replace('language=', '')
            break
        } else {
            lng = "en"
        }
    }

    console.log("inside get language cookie")
    console.log(lng)
    return lng
}

// function for clearing cookies by giving it a list of names to clear
// ARRAY names, array of string containing names of the cookies to be cleared
// returns: VOID
function clearCookies (names) {
	var i = 0, namesLength = names.length;
	for (i; i < namesLength; i += 1) {
		document.cookie = names[i] + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/';
	}
}