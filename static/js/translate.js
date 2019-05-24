// function for making an api call fetching the translations an replacing the corresponding keys
// returns: VOID
function translatePage() {
    var lng = getLanguageCookie()

    // get the translation by the formatted cookie and replacing the element by key
    getApiData('/translate/').then(function (data) {
        let curr_language = data[lng]

        for (let item in curr_language["translations"]) {
            elem = document.getElementById(item)
            if (elem != null) {
                elem.innerHTML = curr_language["translations"][item]
            }
        }

        if (curr_language["force_rtl"]) {
            document.getElementById('body').style.textAlign = "right"
            document.dir = "rtl"
        } else {
            document.getElementById('body').style.textAlign = "left"
            document.dir = "ltr"
        }
    })
}

// function for filling the select where the language can be selected
// returns: VOID
function fillLanguageSelect() {
    // get and decode the language cookie
    var lng = getLanguageCookie()

    // get all the translations and fill the select with them
    getApiData('/translate/').then(function (data) {
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