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

import html
import urllib.error
import urllib.parse
import urllib.request

ADDON = xbmcaddon.Addon(id="plugin.video.einthusan")
BASE_URL = ADDON.getSetting("base_url")
DEBUG_LOG = ADDON.getSetting("log_level_debug")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"


def add_log(message, level="notice"):
    if level == "error":
        xbmc.log(str(message), level=xbmc.LOGERROR)
    elif DEBUG_LOG == "true":
        xbmc.log(str(message), level=xbmc.LOGINFO)
    elif level == "debug":
        xbmc.log(str(message), level=xbmc.LOGDEBUG)
    else:
        xbmc.log(str(message), level=xbmc.LOGINFO)


def add_dir_item(name, url, mode, image, lang="", description="", isplayable=False):
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
    listitem.setArt({"icon": "DefaultFolder.png", "thumb": image})
    tags = listitem.getVideoInfoTag()
    tags.setTitle(name)
    tags.setPlot(description)
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
    add_log("base_url: " + BASE_URL)
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
            add_log("check lang_pattern", "error")
        else:
            languages = lang_matches
    except:
        add_log("check base_url", "error")
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
        add_dir_item(title, "", 1, image, lang)
    add_dir_item("Addon Settings", "", 2, "DefaultAddonService.png", "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def select_menu(name, url, language, mode):
    postData = "lang=" + language
    add_dir_item(
        "Featured",
        BASE_URL + "/movie/browse/?" + postData,
        3,
        "DefaultAddonsRecentlyUpdated.png",
        language,
    )
    add_dir_item(
        "Recently Added",
        BASE_URL + "/movie/results/?find=Recent&" + postData,
        11,
        "DefaultRecentlyAddedMovies.png",
        language,
    )
    add_dir_item(
        "Most Watched",
        BASE_URL + "/movie/results/?find=Popularity&ptype=View&tp=l30d&" + postData,
        11,
        "DefaultMovies.png",
        language,
    )
    add_dir_item(
        "Staff Picks",
        BASE_URL + "/movie/results/?find=StaffPick&" + postData,
        11,
        "DefaultDirector.png",
        language,
    )
    add_dir_item(
        "A-Z",
        BASE_URL + "/movie/results/?" + postData,
        4,
        "DefaultMovieTitle.png",
        language,
    )
    add_dir_item(
        "Year",
        BASE_URL + "/movie/results/?" + postData,
        5,
        "DefaultYear.png",
        language,
    )
    add_dir_item(
        "Rating",
        BASE_URL + "/movie/results/?" + postData,
        8,
        "DefaultGenre.png",
        language,
    )
    add_dir_item(
        "Search",
        BASE_URL + "/movie/results/?" + postData,
        9,
        "DefaultAddonsSearch.png",
        language,
    )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def select_settings(name, url, language, mode):
    ADDON.openSettings()


def menu_alpha(name, url, language, mode):
    add_dir_item("Numbers", url + "&find=Numbers", 11, "")
    azlist = map(chr, list(range(65, 91)))
    for letter in azlist:
        add_dir_item(letter, url + "&find=Alphabets&alpha=" + letter, 11, "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def menu_years(name, url, language, mode):
    add_dir_item("Decade", url, 6, "DefaultYear.png")
    add_dir_item("Years", url, 7, "DefaultYear.png")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def submenu_decade(name, url, language, mode):
    postData = url + "&find=Decade&decade="
    values = [
        repr(x) for x in reversed(list(range(1940, datetime.date.today().year + 1, 10)))
    ]
    for attr_value in values:
        if attr_value != None:
            add_dir_item(
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
            add_dir_item(attr_value, postData + str(attr_value), 11, "DefaultYear.png")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def menu_rating(name, url, language, mode):
    postData = url + "&find=Rating"
    add_dir_item(
        "Action (4+ stars)",
        postData + "&action=4&comedy=0&romance=0&storyline=0&performance=0&ratecount=1",
        11,
        "",
    )
    add_dir_item(
        "Comedy (4+ stars)",
        postData + "&action=0&comedy=4&romance=0&storyline=0&performance=0&ratecount=1",
        11,
        "",
    )
    add_dir_item(
        "Romance (4+ stars)",
        postData + "&action=0&comedy=0&romance=4&storyline=0&performance=0&ratecount=1",
        11,
        "",
    )
    add_dir_item(
        "Storyline (4+ stars)",
        postData + "&action=0&comedy=0&romance=0&storyline=4&performance=0&ratecount=1",
        11,
        "",
    )
    add_dir_item(
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
    add_log("browse_home: " + url)
    list_videos(url, "home")


def browse_results(name, url, language, mode):
    add_log("browse_results: " + url)
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
        add_dir_item(
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
            add_dir_item(
                video_item[2] + "[COLOR blue] - Ultra HD[/COLOR]",
                urldata,
                10,
                image,
                video_item[0],
                video_item[5],
                isplayable=True,
            )

    if video_list[-1][6] != "":
        add_dir_item(">>> Next Page >>>", BASE_URL + video_list[-1][6], 11, "")

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
    LOGIN_ENABLED = ADDON.getSetting("login_enabled")
    RETRY_KEY = ADDON.getSetting("retry_key")

    add_log("play_video: " + url)
    add_log("user_login: " + LOGIN_ENABLED)
    add_log("retry_key: " + RETRY_KEY, "debug")

    s = requests.Session()

    lang, movieid, moviename, hdtype, refurl = url.split(",")

    if LOGIN_ENABLED == "true":
        get_loggedin_session(s, lang, refurl)

    result = get_video(s, lang, movieid, hdtype, refurl, RETRY_KEY)

    if result == False:
        return False

    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_video(s, language, movieid, hdtype, refererurl, defaultejp="default"):
    video_url = "/movie/watch/%s/?lang=%s" % (movieid, language)

    check_go_premium = "Go Premium"
    check_sorry_message = "SERVERS ARE ALMOST AT CAPACITY"

    headers = {
        "Origin": BASE_URL,
        "Referer": refererurl,
        "User-Agent": USER_AGENT,
    }

    check_premium = s.get(
        BASE_URL + video_url, headers=headers, cookies=s.cookies, allow_redirects=False
    )
    if check_premium.status_code in [301, 302, 307, 308]:
        add_log("check_premium: " + str(check_premium.status_code), "debug")
        add_log("redirect_location: " + check_premium.headers["location"], "debug")
        video_url = "/premium" + video_url

    if hdtype == "uhd":
        video_url = video_url + "&uhd=true"

    add_log("get_video: " + str(video_url))

    html1 = s.get(BASE_URL + video_url, headers=headers, cookies=s.cookies).text

    if re.search(check_go_premium, html1):
        add_log("go_premium: " + check_go_premium, "error")
        xbmcgui.Dialog().ok(
            "UltraHD Error - Premium Required",
            "Please add Premium Membership Login details in Addon Settings.",
        )
        return False

    ejp = ""
    if re.search(check_sorry_message, html1):
        add_log("sorry: " + check_sorry_message, "error")
        if defaultejp == "default":
            add_log("no old_ejp", "error")
            retry = xbmcgui.Dialog().yesno(
                "Server Error",
                "Einthusan servers are busy. Please try later or upgrade to Premium account.",
                yeslabel="Retry",
                nolabel="Close",
                autoclose=5000,
            )
            return False
        else:
            add_log("use old_ejp")
            ejp = defaultejp
    else:
        ejp = re.findall("data-ejpingables=[\"'](.*?)[\"']", html1)[0]
        if ejp == "":
            add_log("no new_ejp", "error")
            xbmcgui.Dialog().yesno(
                "Loading Failed",
                "Please try after some time",
                yeslabel="OK",
                nolabel="Close",
                autoclose=5000,
            )
            return False
        else:
            add_log("found new_ejp")
            ADDON.setSetting("retry_key", ejp)

    add_log("using_ejp: " + ejp, "debug")
    jdata = '{"EJOutcomes":"%s","NativeHLS":false}' % ejp
    csrf1 = re.findall("data-pageid=[\"'](.*?)[\"']", html1)[0]
    csrf1 = html.unescape(csrf1)
    add_log("csrf1: " + csrf1, "debug")

    postdata = {
        "xEvent": "UIVideoPlayer.PingOutcome",
        "xJson": jdata,
        "arcVersion": "3",
        "appVersion": "59",
        "gorilla.csrf.Token": csrf1,
    }

    rdata = s.post(
        BASE_URL + "/ajax" + video_url,
        headers=headers,
        data=postdata,
        cookies=s.cookies,
    ).text

    ejl = json.loads(rdata)["Data"]["EJLinks"]
    add_log("base64_decodeEInth: " + str(decodeEInth(ejl)), "debug")
    url1 = json.loads(base64.b64decode(str(decodeEInth(ejl))))["HLSLink"]
    add_log("url1: " + url1, "debug")
    url2 = url1 + ("|%s&Referer=%s&User-Agent=%s" % (BASE_URL, video_url, USER_AGENT))
    add_log("url2: " + url2, "debug")
    listitem = xbmcgui.ListItem(name)
    thumbnailImage = xbmc.getInfoImage("ListItem.Thumb")
    listitem.setArt({"icon": "DefaultVideo.png", "thumb": thumbnailImage})
    listitem.setProperty("IsPlayable", "true")
    listitem.setPath(url2)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

    s.close()


def get_loggedin_session(s, language, refererurl):
    LOGIN_USERNAME = ADDON.getSetting("login_username")
    LOGIN_PASSWORD = ADDON.getSetting("login_password")
    add_log("get_loggedin_session: " + refererurl)

    headers = {
        "Origin": BASE_URL,
        "Referer": refererurl,
        "User-Agent": USER_AGENT,
    }

    html1 = s.get(
        BASE_URL + "/login/?lang=" + language,
        headers=headers,
        allow_redirects=False,
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


if __name__ == "__main__":
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
