# Credits https://github.com/humla/
# Credits https://github.com/reasonsrepo/

import base64
import datetime
import json
import re
import requests
import sys
import xbmcaddon
import xbmcgui
import xbmcplugin

import HTMLParser
from six.moves import urllib


ADDON = xbmcaddon.Addon(id="plugin.video.einthusan2")
BASE_URL = "https://einthusan.tv"


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
    addDir("Tamil", "", 1, "", "tamil")
    addDir("Hindi", "", 1, "", "hindi")
    addDir("Telugu", "", 1, "", "telugu")
    addDir("Malayalam", "", 1, "", "malayalam")
    addDir("Kannada", "", 1, "", "kannada")
    addDir("Bengali", "", 1, "", "bengali")
    addDir("Marathi", "", 1, "", "marathi")
    addDir("Punjabi", "", 1, "", "punjabi")
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
    ADDON.openSettings()


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
    keyb = xbmc.Keyboard("", "Search for Movies")
    keyb.doModal()
    if keyb.isConfirmed():
        search_term = urllib.parse.quote_plus(keyb.getText())
        postData = url + "&query=" + str(search_term)
        scrape_videos(name, postData, language, mode)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def play_video(name, url, language, mode):
    s = requests.Session()
    print("Playing: " + name + ", with url:" + url)
    xbmc.log("play_video: " + url, level=xbmc.LOGNOTICE)

    name, url, lang, whathd, referurl = url.split(",")

    if whathd == "uhd":
        dialog = xbmcgui.Dialog()
        ret1 = dialog.select(
            "Quality Options",
            ["Play SD/HD", "Play UHD [Premium Membership Required]"],
            autoclose=5000,
            preselect=0,
        )

        if ret1 == 0:
            # whathd = 'shd'
            mainurl = "%s/movie/watch/%s/?lang=%s" % (BASE_URL, url, lang)
            mainurlajax = "%s/ajax/movie/watch/%s/?lang=%s" % (BASE_URL, url, lang,)
            print(mainurlajax)
            headers = {
                "Origin": BASE_URL,
                "Referer": BASE_URL + "/movie/browse/?lang=tamil",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            }
            ret2 = get_video(s, mainurl, mainurlajax, headers)

        if ret1 == 1:
            # whathd = 'uhd'
            headers = {
                "Origin": BASE_URL,
                "Referer": BASE_URL + "/movie/browse/?lang=tamil",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
            }
            mainurl = "%s/movie/watch/%s/?lang=%s&uhd=true" % (BASE_URL, url, lang,)
            mainurlajax = "%s/ajax/movie/watch/%s/?lang=%s&uhd=true" % (
                BASE_URL,
                url,
                lang,
            )
            # ultraHD needs lifetime premium login
            # login_info(s, referurl)
            ret2 = get_video(s, mainurl, mainurlajax, headers)

    else:
        mainurl = "%s/movie/watch/%s/?lang=%s" % (BASE_URL, url, lang)
        mainurlajax = "%s/ajax/movie/watch/%s/?lang=%s" % (BASE_URL, url, lang)
        headers = {
            "Origin": BASE_URL,
            "Referer": BASE_URL + "/movie/browse/?lang=tamil",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        }
        ret2 = get_video(s, mainurl, mainurlajax, headers)

    if ret2 == False:
        return False
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def get_video(s, mainurl, mainurlajax, headers=None):
    xbmc.log("get_video: " + str(mainurl), level=xbmc.LOGNOTICE)

    htm = s.get(mainurl, headers=headers, cookies=s.cookies).text.encode("utf-8")
    # xbmc.log(htm, level=xbmc.LOGNOTICE)

    if re.search("Our servers are almost maxed", htm):
        xbmc.log(
            "Sorry. Our servers are almost maxed. Remaining quota is for premium members.",
            level=xbmc.LOGERROR,
        )
        xbmcgui.Dialog().yesno(
            "Server Error",
            "Sorry. Einthusan servers are almost maxed.",
            "Please try again in 5 - 10 mins or upgrade to a Lifetime Premium account.",
            yeslabel="Ok",
            nolabel="Close",
            autoclose=5000,
        )
        return False

    if re.search("Go Premium", htm):
        xbmc.log(
            "Go Premium. Please Login or Register an account then re-visit this page to continue.",
            level=xbmc.LOGERROR,
        )
        xbmcgui.Dialog().ok(
            "UltraHD Error",
            "Premium Membership Required for UltraHD Movies.",
            "Please add Login details in Addon Settings.",
        )
        return False

    lnk = re.findall("data-ejpingables=[\"'](.*?)[\"']", htm)[0]
    # xbmc.log("lnk: " + lnk, level=xbmc.LOGNOTICE)
    r = decodeEInth(lnk)
    jdata = '{"EJOutcomes":"%s","NativeHLS":false}' % lnk
    gid = re.findall("data-pageid=[\"'](.*?)[\"']", htm)[0]
    gid = HTMLParser.HTMLParser().unescape(gid).encode("utf-8")

    postdata = {
        "xEvent": "UIVideoPlayer.PingOutcome",
        "xJson": jdata,
        "arcVersion": "3",
        "appVersion": "59",
        "gorilla.csrf.Token": gid,
    }

    rdata = s.post(mainurlajax, headers=headers, data=postdata, cookies=s.cookies).text
    r = json.loads(rdata)["Data"]["EJLinks"]
    xbmc.log("decodeEInth: " + str(decodeEInth(r)), level=xbmc.LOGNOTICE)
    lnk = json.loads(base64.b64decode(str(decodeEInth(r))))["HLSLink"]
    # lnk = preferred_server(lnk, mainurl)
    xbmc.log("lnk: " + lnk, level=xbmc.LOGNOTICE)
    urlnew = lnk + (
        "|%s&Referer=%s&User-Agent=%s"
        % (
            BASE_URL,
            mainurl,
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        )
    )
    xbmc.log("urlnew: " + urlnew, level=xbmc.LOGNOTICE)
    listitem = xbmcgui.ListItem(name)
    iconImage = "DefaultVideo.png"
    thumbnailImage = xbmc.getInfoImage("ListItem.Thumb")
    listitem.setArt({"icon": iconImage, "thumb": thumbnailImage})
    listitem.setProperty("IsPlayable", "true")
    listitem.setPath(urlnew)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

    s.close()


def menu_featured(name, url, language, mode):
    xbmc.log("menu_featured: " + url, level=xbmc.LOGNOTICE)
    page_url = url
    html1 = requests.get(page_url).text
    matches = re.compile(
        'name="newrelease_tab".+?img src="(.+?)".+?href="\/movie\/watch\/(.+?)\/\?lang=(.+?)"><h2>(.+?)<\/h2>.+?i class=(.+?)<\/div>'
    ).findall(html1)

    for img, id, lang, name, ishd in matches:
        img = img.replace('"><img src="', "")
        img = "https:" + img

        image = img
        if "http" not in image:
            image = "https:" + img
        else:
            image = img

        name = name.replace(",", "").encode("ascii", "ignore").decode("ascii")
        movie = name + "," + id + "," + lang
        if "ultrahd" in ishd:
            title = name + "[COLOR blue] - Ultra HD[/COLOR]"
            movie = movie + ",uhd," + page_url
        else:
            title = name
            movie = movie + ",shd," + page_url

        addDir(title, movie, 10, image, lang, isplayable=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def scrape_videos(name, url, language, mode):
    xbmc.log("scrape_videos: " + url, level=xbmc.LOGNOTICE)
    page_url = url
    html1 = requests.get(url).text
    # matches = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html1)
    matches = re.compile(
        '<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?<img src="(.+?)".+?<h3>(.+?)<\/h3>.+?i class(.+?)<p class="synopsis">(.+?)<\/p>.+?<span>Wiki<'
    ).findall(html1)
    nextpage = re.findall('data-disabled="([^"]*)" href="(.+?)"', html1)[-1]
    for movie, lang, image, name, ishd, synopsis in matches:
        description = ""
        if "http" not in image:
            image = "https:" + image
        else:
            image = image
        name = str(name.replace(",", "").encode("ascii", "ignore").decode("ascii"))
        movie = str(name) + "," + str(movie) + "," + lang
        if "ultrahd" in ishd:
            title = name + "[COLOR blue] - Ultra HD[/COLOR]"
            movie = movie + ",uhd," + page_url
        else:
            title = name
            movie = movie + ",shd," + page_url
        try:
            description = synopsis.encode("ascii", "ignore").decode("ascii")
        except:
            description = ""
        addDir(title, movie, 10, image, lang, description, isplayable=True)
    if nextpage[0] != "true":
        nextPage_Url = BASE_URL + nextpage[1]
        addDir(">>> Next Page >>>", nextPage_Url, 11, "", "")
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def decodeEInth(lnk):
    t = 10
    # var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r = lnk[0:t] + lnk[-1] + lnk[t + 2 : -1]
    return r


def encodeEInth(lnk):
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
