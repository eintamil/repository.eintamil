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
import html
import urllib.error
import urllib.parse
import urllib.request

# py_2x_3x
# import HTMLParser
# from six.moves import urllib

# py_2x_3x
__settings__ = xbmcaddon.Addon(id="plugin.video.einthusan3")
# __settings__ = xbmcaddon.Addon(id="plugin.video.einthusan2")

BASE_URL = __settings__.getSetting("base_url")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"


def addLog(message, level="notice"):
    if level == "error":
        xbmc.log(str(message), level=xbmc.LOGERROR)
    else:
        xbmc.log(str(message), level=xbmc.LOGINFO)


def addDir(name, url, mode, image, lang="", description="", isplayable=False):
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
    thumbnailImage = image
    listitem.setArt({"icon": "DefaultFolder.png", "thumb": thumbnailImage})
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
    addLog("BASE_URL: " + BASE_URL)
    languages = [
        ("tamil", "", "Tamil"),
        ("hindi", "", "Hindi"),
        ("telugu", "", "Telugu"),
        ("malayalam", "", "Malayalam"),
        ("kannada", "", "Kannada"),
        ("bengali", "", "Bengali"),
        ("marathi", "", "Marathi"),
        ("punjabi", "", "Punjabi"),
    ]
    lang_pattern = '<li><a href=".*?\?lang=(.+?)"><div.*?div><img src="(.+?)"><p class=".*?-bg">(.+?)<\/p>'
    try:
        html1 = requests.get(BASE_URL).text
        lang_matches = re.findall(lang_pattern, html1)
        if len(lang_matches) == 0:
            addLog("check lang_pattern", "error")
        else:
            languages = lang_matches
    except:
        addLog("check BASE_URL", "error")
        xbmcgui.Dialog().ok(
            "Base URL Error",
            "Please check and update the Base URL in Addon Settings and restart the addon.",
        )
    for lang_item in languages:
        lang = str(lang_item[0])
        title = str(lang_item[2])
        if "http" not in lang_item[1] and lang_item[1] != "":
            image = "https://" + str(lang_item[1])
        else:
            image = ""
        addDir(title, "", 1, image, lang)
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
        "Most Watched",
        BASE_URL + "/movie/results/?find=Popularity&ptype=View&tp=l30d&" + postData,
        11,
        "DefaultMovies.png",
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
        browse_results(name, postData, language, mode)


def browse_home(name, url, language, mode):
    addLog("browse_home: " + url)
    list_videos(url, "home")


def browse_results(name, url, language, mode):
    addLog("browse_results: " + url)
    list_videos(url, "results")


def list_videos(url, pattern):
    video_list = scrape_videos(url, pattern)

    if video_list[-1][6] != "":
        next_page_list = scrape_videos(BASE_URL + video_list[-1][6], pattern)
        for next_page_item in next_page_list:
            video_list.append(next_page_item)

    for video_item in video_list:
        if "http" not in video_item[4]:
            image = "https:" + video_item[4]
        else:
            image = video_item[4]
        urldata = (
            video_item[0] + "," + video_item[1] + "," + video_item[2] + ",shd," + url
        )
        addDir(
            video_item[2],
            urldata,
            10,
            image,
            video_item[0],
            video_item[5],
            isplayable=True,
        )

        if video_item[3] == "uhd":
            urldata = (
                video_item[0]
                + ","
                + video_item[1]
                + ","
                + video_item[2]
                + ",uhd,"
                + url
            )
            addDir(
                video_item[2] + "[COLOR blue] - Ultra HD[/COLOR]",
                urldata,
                10,
                image,
                video_item[0],
                video_item[5],
                isplayable=True,
            )

    if video_list[-1][6] != "":
        addDir(">>> Next Page >>>", BASE_URL + video_list[-1][6], 11, "")

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def scrape_videos(url, pattern):
    html1 = requests.get(url).text
    results = []
    next_page = ""
    if pattern == "home":
        regexstr = 'name="newrelease_tab".+?img src="(.+?)".+?href="\/movie\/watch\/(.+?)\/\?lang=(.+?)"><h2>(.+?)<\/h2>.+?i class=(.+?)<\/div>'
    else:
        regexstr = '<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?<img src="(.+?)".+?<h3>(.+?)<\/h3>.+?i class(.+?)<p class=".*?synopsis">(.+?)<\/p>.+?<span>Wiki<'
    video_matches = re.findall(regexstr, html1)
    next_matches = re.findall('data-disabled="([^"]*)" href="(.+?)"', html1)
    if len(next_matches) > 0 and next_matches[-1][0] != "true":
        next_page = next_matches[-1][1]
    for item in video_matches:
        movie_name = str(
            item[3].replace(",", "").encode("ascii", "ignore").decode("ascii")
        )
        movie_def = "shd"
        if "ultrahd" in item[4]:
            movie_def = "uhd"
        if pattern == "home":
            image = item[0]
            movie_id = item[1]
            lang = item[2]
            description = ""
        else:
            movie_id = item[0]
            lang = item[1]
            image = item[2]
            try:
                description = item[5].encode("ascii", "ignore").decode("ascii")
            except:
                description = ""
        results.append(
            (
                str(lang),
                str(movie_id),
                str(movie_name),
                str(movie_def),
                str(image),
                str(description),
                str(next_page),
            )
        )
    return results


def play_video(name, url, language, mode):
    LOGIN_ENABLED = __settings__.getSetting("login_enabled")
    RETRY_KEY = __settings__.getSetting("retry_key")

    addLog("play_video: " + url)
    addLog("user_login: " + LOGIN_ENABLED)
    addLog("retry_key: " + RETRY_KEY)

    s = requests.Session()

    lang, movieid, moviename, hdtype, refurl = url.split(",")

    if LOGIN_ENABLED == "true":
        get_loggedin_session(s, lang, refurl)

    result = get_video(s, lang, movieid, hdtype, refurl, RETRY_KEY)

    if result == False:
        return False

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_video(s, language, movieid, hdtype, refererurl, oldejp=""):
    videourl = "%s/movie/watch/%s/?lang=%s" % (BASE_URL, movieid, language)
    videourlajax = "%s/ajax/movie/watch/%s/?lang=%s" % (BASE_URL, movieid, language)

    check_sorry_message = "Our servers are almost maxed"
    check_go_premium = "Go Premium"

    if hdtype == "uhd":
        videourl = videourl + "&uhd=true"
        videourlajax = videourlajax + "&uhd=true"

    addLog("get_video: " + str(videourl))

    headers = {
        "Origin": BASE_URL,
        "Referer": refererurl,
        "User-Agent": USER_AGENT,
    }

    html1 = s.get(videourl, headers=headers, cookies=s.cookies).text

    useoldejp = 0
    if re.search(check_sorry_message, html1):
        addLog(check_sorry_message, "error")
        retry = xbmcgui.Dialog().yesno(
            "Server Error",
            "Sorry. Einthusan servers are almost maxed. Please try later or upgrade to Premium account.",
            yeslabel="Retry",
            nolabel="Close",
            autoclose=5000,
        )
        if retry == True:
            useoldejp = 1
        else:
            return False

    if re.search(check_go_premium, html1):
        addLog(check_go_premium, "error")
        xbmcgui.Dialog().ok(
            "UltraHD Error - Premium Required",
            "Please add Premium Membership Login details in Addon Settings.",
        )
        return False

    ejp = ""
    if useoldejp == 1:
        if oldejp == "default" or oldejp == "":
            addLog("retry failed", "error")
            xbmcgui.Dialog().yesno(
                "Retry Failed",
                "Better Luck Next Time",
                yeslabel="OK",
                nolabel="Close",
                autoclose=5000,
            )
            return False
        else:
            addLog("retry old_ejp")
            ejp = oldejp
    else:
        addLog("found new_ejp")
        ejp = re.findall("data-ejpingables=[\"'](.*?)[\"']", html1)[0]
        __settings__.setSetting("retry_key", ejp)
        addLog("retry_key updated with new_ejp for better luck next time")

    addLog("using_ejp: " + ejp)
    jdata = '{"EJOutcomes":"%s","NativeHLS":false}' % ejp
    csrf1 = re.findall("data-pageid=[\"'](.*?)[\"']", html1)[0]
    # py_2x_3x
    csrf1 = html.unescape(csrf1)
    # csrf1 = HTMLParser.HTMLParser().unescape(csrf1).encode("utf-8")

    postdata = {
        "xEvent": "UIVideoPlayer.PingOutcome",
        "xJson": jdata,
        "arcVersion": "3",
        "appVersion": "59",
        "gorilla.csrf.Token": csrf1,
    }

    rdata = s.post(videourlajax, headers=headers, data=postdata, cookies=s.cookies).text
    ejl = json.loads(rdata)["Data"]["EJLinks"]
    addLog("base64_decodeEInth: " + str(decodeEInth(ejl)))
    url1 = json.loads(base64.b64decode(str(decodeEInth(ejl))))["HLSLink"]
    addLog("url1: " + url1)
    url2 = url1 + ("|%s&Referer=%s&User-Agent=%s" % (BASE_URL, videourl, USER_AGENT))
    addLog("url2: " + url2)
    listitem = xbmcgui.ListItem(name)
    thumbnailImage = xbmc.getInfoImage("ListItem.Thumb")
    listitem.setArt({"icon": "DefaultVideo.png", "thumb": thumbnailImage})
    listitem.setProperty("IsPlayable", "true")
    listitem.setPath(url2)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

    s.close()


def get_loggedin_session(s, language, refererurl):
    LOGIN_USERNAME = __settings__.getSetting("login_username")
    LOGIN_PASSWORD = __settings__.getSetting("login_password")
    addLog("get_loggedin_session: " + refererurl)

    headers = {
        "Origin": BASE_URL,
        "Referer": refererurl,
        "User-Agent": USER_AGENT,
    }

    html1 = s.get(
        BASE_URL + "/login/?lang=" + language, headers=headers, allow_redirects=False,
    ).text

    csrf1 = re.findall("data-pageid=[\"'](.*?)[\"']", html1)[0]

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

    csrf3 = re.findall("data-pageid=[\"'](.*?)[\"']", html3)[0]

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
function_map[3] = browse_home
function_map[4] = menu_alpha
function_map[5] = menu_years
function_map[6] = submenu_decade
function_map[7] = submenu_years
function_map[8] = menu_rating
function_map[9] = menu_search
function_map[10] = play_video
function_map[11] = browse_results

function_map[mode](name, url, language, mode)
