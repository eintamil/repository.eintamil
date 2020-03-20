# Credits https://github.com/humla/
# Credits https://github.com/reasonsrepo/
# Credits https://github.com/eintamil/

import base64
import datetime
import json
import re
import requests
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin

# py_2x_3x
# import html
# import urllib.error
# import urllib.parse
# import urllib.request

# py_2x_3x
import HTMLParser
from six.moves import urllib

# py_2x_3x
# __settings__ = xbmcaddon.Addon(id="plugin.video.einthusan3")
__settings__ = xbmcaddon.Addon(id="plugin.video.einthusan2")

BASE_URL = __settings__.getSetting("base_url")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"


def addDir(name, url, mode, iconimage, lang="", description="", isplayable=False):
    u = (
        sys.argv[0]
        + "?url="
        + urllib.parse.quote_plus(url)
        + "&mode="
        + str(mode)
        + "&name="
        + urllib.parse.quote_plus(name)
        + "&lang="
        + urllib.parse.quote_plus(lang)
        + "&description="
        + urllib.parse.quote_plus(description)
    )

    listitem = xbmcgui.ListItem(name)
    iconImage = "DefaultFolder.png"
    thumbnailImage = iconimage
    listitem.setArt({"icon": iconImage, "thumb": thumbnailImage})
    listitem.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    listitem.setProperty("IsPlayable", "true")
    isfolder = True
    if isplayable:
        isfolder = False
    ok = xbmcplugin.addDirectoryItem(
        handle=int(sys.argv[1]), url=u, listitem=listitem, isFolder=isfolder
    )
    return ok


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace("?", "")
        if params[len(params) - 1] == "/":
            params = params[0 : len(params) - 2]
        pairsofparams = cleanedparams.split("&")
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split("=")
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


def select_lang(name, url, language, mode):
    xbmc.log("BASE_URL: " + BASE_URL, level=xbmc.LOGNOTICE)
    languages = [
        "Tamil",
        "Hindi",
        "Telugu",
        "Malayalam",
        "Kannada",
        "Bengali",
        "Marathi",
        "Punjabi",
    ]
    for lang in languages:
        addDir(lang, "", 1, "", str.lower(lang))
    addDir("Addon Settings", "", 2, "DefaultAddonService.png", "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def select_menu(name, url, language, mode):
    postData = "lang=" + language
    addDir(
        "Featured",
        BASE_URL + "/movie/browse/?" + postData,
        3,
        "DefaultAddonsRecentlyUpdated.png",
        language,
    )
    addDir(
        "Recently Added",
        BASE_URL + "/movie/results/?find=Recent&" + postData,
        11,
        "DefaultRecentlyAddedMovies.png",
        language,
    )
    addDir(
        "Staff Picks",
        BASE_URL + "/movie/results/?find=StaffPick&" + postData,
        11,
        "DefaultDirector.png",
        language,
    )
    addDir(
        "A-Z",
        BASE_URL + "/movie/results/?" + postData,
        4,
        "DefaultMovieTitle.png",
        language,
    )
    addDir(
        "Year",
        BASE_URL + "/movie/results/?" + postData,
        5,
        "DefaultYear.png",
        language,
    )
    addDir(
        "Rating",
        BASE_URL + "/movie/results/?" + postData,
        8,
        "DefaultGenre.png",
        language,
    )
    addDir(
        "Search",
        BASE_URL + "/movie/results/?" + postData,
        9,
        "DefaultAddonsSearch.png",
        language,
    )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def select_settings(name, url, language, mode):
    __settings__.openSettings()


def menu_alpha(name, url, language, mode):
    addDir("Numbers", url + "&find=Numbers", 11, "")
    azlist = map(chr, list(range(65, 91)))
    for letter in azlist:
        addDir(letter, url + "&find=Alphabets&alpha=" + letter, 11, "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def menu_years(name, url, language, mode):
    addDir("Decade", url, 6, "DefaultYear.png")
    addDir("Years", url, 7, "DefaultYear.png")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def submenu_decade(name, url, language, mode):
    postData = url + "&find=Decade&decade="
    values = [
        repr(x) for x in reversed(list(range(1940, datetime.date.today().year + 1, 10)))
    ]
    for attr_value in values:
        if attr_value != None:
            addDir(
                str(attr_value) + "s", postData + str(attr_value), 11, "DefaultYear.png"
            )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def submenu_years(name, url, language, mode):
    postData = url + "&find=Year&year="
    values = [
        repr(x) for x in reversed(list(range(1940, datetime.date.today().year + 1)))
    ]
    for attr_value in values:
        if attr_value != None:
            addDir(attr_value, postData + str(attr_value), 11, "DefaultYear.png")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def menu_rating(name, url, language, mode):
    postData = url + "&find=Rating"
    addDir(
        "Action (4+ stars)",
        postData + "&action=4&comedy=0&romance=0&storyline=0&performance=0&ratecount=1",
        11,
        "",
    )
    addDir(
        "Comedy (4+ stars)",
        postData + "&action=0&comedy=4&romance=0&storyline=0&performance=0&ratecount=1",
        11,
        "",
    )
    addDir(
        "Romance (4+ stars)",
        postData + "&action=0&comedy=0&romance=4&storyline=0&performance=0&ratecount=1",
        11,
        "",
    )
    addDir(
        "Storyline (4+ stars)",
        postData + "&action=0&comedy=0&romance=0&storyline=4&performance=0&ratecount=1",
        11,
        "",
    )
    addDir(
        "Performance (4+ stars)",
        postData + "&action=0&comedy=0&romance=0&storyline=0&performance=4&ratecount=1",
        11,
        "",
    )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def menu_search(name, url, language, mode):
    keyb = xbmc.Keyboard("", "Search")
    keyb.doModal()
    if keyb.isConfirmed():
        search_term = urllib.parse.quote_plus(keyb.getText())
        postData = url + "&query=" + str(search_term)
        scrape_videos(name, postData, language, mode)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def play_video(name, url, language, mode):
    LOGIN_ENABLED = __settings__.getSetting("login_enabled")
    RETRY_KEY = __settings__.getSetting("retry_key")
    xbmc.log("play_video: " + url, level=xbmc.LOGNOTICE)
    xbmc.log("user_login: " + LOGIN_ENABLED, level=xbmc.LOGNOTICE)
    xbmc.log("retry_key: " + RETRY_KEY, level=xbmc.LOGNOTICE)

    s = requests.Session()

    name, url, lang, hdtype, refurl = url.split(",")

    if LOGIN_ENABLED == "true":
        get_loggedin_session(s, lang, refurl)

    mainurl = "%s/movie/watch/%s/?lang=%s" % (BASE_URL, url, lang)
    mainurlajax = "%s/ajax/movie/watch/%s/?lang=%s" % (BASE_URL, url, lang)

    if hdtype == "uhd":
        dialog = xbmcgui.Dialog()
        ret1 = dialog.select(
            "Quality Options",
            ["Play SD/HD [Default]", "Play UHD [Premium Membership Required]"],
            autoclose=5000,
            preselect=0,
        )
        if ret1 == 1:
            mainurl = mainurl + "&uhd=true"
            mainurlajax = mainurlajax + "&uhd=true"
        else:
            pass
    else:
        pass

    headers = {
        "Origin": BASE_URL,
        "Referer": BASE_URL + "/movie/browse/?lang=" + lang,
        "User-Agent": USER_AGENT,
    }
    ret2 = get_video(s, lang, mainurl, mainurlajax, headers, RETRY_KEY)

    if ret2 == False:
        return False
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_video(s, language, mainurl, mainurlajax, headers=None, oldejp=""):
    xbmc.log("get_video: " + str(mainurl), level=xbmc.LOGNOTICE)

    # py_2x_3x
    # html1 = s.get(mainurl, headers=headers, cookies=s.cookies).text
    html1 = s.get(mainurl, headers=headers, cookies=s.cookies).text.encode("utf-8")

    useoldejp = 0
    if re.search("Our servers are almost maxed", html1):
        xbmc.log(
            "Sorry. Our servers are almost maxed. Remaining quota is for premium members.",
            level=xbmc.LOGERROR,
        )
        retry = xbmcgui.Dialog().yesno(
            "Server Error",
            "Sorry. Einthusan servers are almost maxed.",
            "Please try again in 5 - 10 mins or upgrade to a Lifetime Premium account.",
            yeslabel="Retry",
            nolabel="Close",
            autoclose=5000,
        )
        if retry == True:
            useoldejp = 1
        else:
            return False

    if re.search("Go Premium", html1):
        xbmc.log(
            "Go Premium. Please Login or Register an account then re-visit this page to continue.",
            level=xbmc.LOGERROR,
        )
        xbmcgui.Dialog().ok(
            "UltraHD Error",
            "Premium Membership Required for UltraHD Movies.",
            "Please add Premium Membership Login details in Addon Settings.",
        )
        return False

    ejp = ""
    if useoldejp == 1:
        if oldejp == "default" or oldejp == "":
            xbmc.log("retry failed", level=xbmc.LOGNOTICE)
            xbmcgui.Dialog().yesno(
                "Retry Failed",
                "Better Luck Next Time",
                yeslabel="OK",
                nolabel="Close",
                autoclose=5000,
            )
            return False
        else:
            xbmc.log("retry old_ejp using retry_key", level=xbmc.LOGNOTICE)
            ejp = oldejp
    else:
        xbmc.log("try new_ejp", level=xbmc.LOGNOTICE)
        ejp = re.findall("data-ejpingables=[\"'](.*?)[\"']", html1)[0]
        __settings__.setSetting("retry_key", ejp)
        xbmc.log(
            "retry_key updated with new_ejp for better luck next time",
            level=xbmc.LOGNOTICE,
        )

    xbmc.log("using_ejp: " + ejp, level=xbmc.LOGNOTICE)
    jdata = '{"EJOutcomes":"%s","NativeHLS":false}' % ejp
    csrf1 = re.findall("data-pageid=[\"'](.*?)[\"']", html1)[0]
    # py_2x_3x
    # csrf1 = html.unescape(csrf1)
    csrf1 = HTMLParser.HTMLParser().unescape(csrf1).encode("utf-8")

    postdata = {
        "xEvent": "UIVideoPlayer.PingOutcome",
        "xJson": jdata,
        "arcVersion": "3",
        "appVersion": "59",
        "gorilla.csrf.Token": csrf1,
    }

    rdata = s.post(mainurlajax, headers=headers, data=postdata, cookies=s.cookies).text
    ejl = json.loads(rdata)["Data"]["EJLinks"]
    xbmc.log("base64_decodeEInth: " + str(decodeEInth(ejl)), level=xbmc.LOGNOTICE)
    url1 = json.loads(base64.b64decode(str(decodeEInth(ejl))))["HLSLink"]
    xbmc.log("url1: " + url1, level=xbmc.LOGNOTICE)
    url2 = url1 + ("|%s&Referer=%s&User-Agent=%s" % (BASE_URL, mainurl, USER_AGENT))
    xbmc.log("url2: " + url2, level=xbmc.LOGNOTICE)
    listitem = xbmcgui.ListItem(name)
    iconImage = "DefaultVideo.png"
    thumbnailImage = xbmc.getInfoImage("ListItem.Thumb")
    listitem.setArt({"icon": iconImage, "thumb": thumbnailImage})
    listitem.setProperty("IsPlayable", "true")
    listitem.setPath(url2)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

    s.close()


def get_loggedin_session(s, language, refererurl):
    LOGIN_USERNAME = __settings__.getSetting("login_username")
    LOGIN_PASSWORD = __settings__.getSetting("login_password")
    xbmc.log("get_loggedin_session: " + refererurl, level=xbmc.LOGNOTICE)

    headers = {
        "Origin": BASE_URL,
        "Referer": refererurl,
        "User-Agent": USER_AGENT,
    }

    html1 = s.get(
        BASE_URL + "/login/?lang=" + language, headers=headers, allow_redirects=False,
    ).text

    # py_2x_3x
    # csrf1 = re.findall("data-pageid=[\"'](.*?)[\"']", html1)[0]
    csrf1 = re.findall("data-pageid=[\"'](.*?)[\"']", html1.encode("utf-8"))[0]

    if "&#43;" in csrf1:
        csrf1 = csrf1.replace("&#43;", "+")

    headers["X-Requested-With"] = "XMLHttpRequest"
    headers["Referer"] = BASE_URL + "/login/?lang=" + language

    postdata2 = {
        "xEvent": "Login",
        "xJson": '{"Email":"'
        + LOGIN_USERNAME
        + '","Password":"'
        + LOGIN_PASSWORD
        + '"}',
        "arcVersion": 3,
        "appVersion": 59,
        "tabID": csrf1 + "48",
        "gorilla.csrf.Token": csrf1,
    }

    html2 = s.post(
        BASE_URL + "/ajax/login/?lang=" + language,
        headers=headers,
        cookies=s.cookies,
        data=postdata2,
        allow_redirects=False,
    )

    html3 = s.get(
        BASE_URL
        + "/account/?flashmessage=success%3A%3A%3AYou+are+now+logged+in.&lang="
        + language,
        headers=headers,
        cookies=s.cookies,
    ).text

    # py_2x_3x
    # csrf3 = re.findall("data-pageid=[\"'](.*?)[\"']", html3)[0]
    csrf3 = re.findall("data-pageid=[\"'](.*?)[\"']", html3.encode("utf-8"))[0]

    postdata4 = {
        "xEvent": "notify",
        "xJson": '{"Alert":"SUCCESS","Heading":"AWESOME!","Line1":"You+are+now+logged+in.","Buttons":[]}',
        "arcVersion": 3,
        "appVersion": 59,
        "tabID": csrf1 + "48",
        "gorilla.csrf.Token": csrf3,
    }

    html4 = s.post(
        BASE_URL + "/ajax/account/?lang=" + language,
        headers=headers,
        cookies=s.cookies,
        data=postdata4,
    )

    return s


def menu_featured(name, url, language, mode):
    xbmc.log("menu_featured: " + url, level=xbmc.LOGNOTICE)
    html1 = requests.get(url).text
    matches = re.compile(
        'name="newrelease_tab".+?img src="(.+?)".+?href="\/movie\/watch\/(.+?)\/\?lang=(.+?)"><h2>(.+?)<\/h2>.+?i class=(.+?)<\/div>'
    ).findall(html1)

    for img, movieid, lang, name, ishd in matches:
        description = ""
        if "http" not in img:
            image = "https:" + img
        else:
            image = img

        name = str(name.replace(",", "").encode("ascii", "ignore").decode("ascii"))
        if "ultrahd" in ishd:
            title = name + "[COLOR blue] - Ultra HD[/COLOR]"
            urldata = str(name) + "," + str(movieid) + "," + lang + ",uhd," + url
        else:
            title = name
            urldata = str(name) + "," + str(movieid) + "," + lang + ",shd," + url

        addDir(title, urldata, 10, image, lang, description, isplayable=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def scrape_videos(name, url, language, mode):
    xbmc.log("scrape_videos: " + url, level=xbmc.LOGNOTICE)
    html1 = requests.get(url).text
    matches = re.compile(
        '<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?<img src="(.+?)".+?<h3>(.+?)<\/h3>.+?i class(.+?)<p class=".*?synopsis">(.+?)<\/p>.+?<span>Wiki<'
    ).findall(html1)
    nextpage = re.findall('data-disabled="([^"]*)" href="(.+?)"', html1)[-1]
    for movieid, lang, img, name, ishd, synopsis in matches:
        description = ""
        if "http" not in img:
            image = "https:" + img
        else:
            image = img

        name = str(name.replace(",", "").encode("ascii", "ignore").decode("ascii"))
        if "ultrahd" in ishd:
            title = name + "[COLOR blue] - Ultra HD[/COLOR]"
            urldata = str(name) + "," + str(movieid) + "," + lang + ",uhd," + url
        else:
            title = name
            urldata = str(name) + "," + str(movieid) + "," + lang + ",shd," + url
        try:
            description = synopsis.encode("ascii", "ignore").decode("ascii")
        except:
            description = ""
        addDir(title, urldata, 10, image, lang, description, isplayable=True)
    if nextpage[0] != "true":
        nextPage_Url = BASE_URL + nextpage[1]
        addDir(">>> Next Page >>>", nextPage_Url, 11, "", "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def decodeEInth(lnk):
    t = 10
    # var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r = lnk[0:t] + lnk[-1] + lnk[t + 2 : -1]
    return r


### main starts here
params = get_params()
url = ""
name = ""
mode = 0
language = ""
description = ""

try:
    url = urllib.parse.unquote_plus(params["url"])
except:
    pass

try:
    name = urllib.parse.unquote_plus(params["name"])
except:
    pass

try:
    mode = int(params["mode"])
except:
    pass

try:
    language = urllib.parse.unquote_plus(params["lang"])
except:
    pass

try:
    description = urllib.parse.unquote_plus(params["description"])
except:
    pass

function_map = {}

function_map[0] = select_lang
function_map[1] = select_menu
function_map[2] = select_settings
function_map[3] = menu_featured
function_map[4] = menu_alpha
function_map[5] = menu_years
function_map[6] = submenu_decade
function_map[7] = submenu_years
function_map[8] = menu_rating
function_map[9] = menu_search
function_map[10] = play_video
function_map[11] = scrape_videos

function_map[mode](name, url, language, mode)
