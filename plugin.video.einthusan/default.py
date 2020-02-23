
# Einthusan.com plugin written by humla.
# einthusan.ca Plugin maintained by ReasonsRepo


import os
import re
import urllib.request
import urllib.parse
import urllib.error
import xbmcplugin
import xbmcaddon
import xbmcgui
from datetime import date

import HTTPInterface
import JSONInterface
import DBInterface

import requests
import html
import base64
import json

# s = requests.Session()

NUMBER_OF_PAGES = 3

ADDON = xbmcaddon.Addon(id='plugin.video.einthusan')
username = ADDON.getSetting('username')
password = ADDON.getSetting('password')

locationStr = xbmcplugin.getSetting(int(sys.argv[1]), 'location')
Locations = ['No Preference', 'San Francisco', 'Dallas', 'Washington, D.C.', 'Toronto', 'London', 'Sydney']

locationId = int(locationStr)
if (locationId > len(Locations) - 1):
    locationId = len(Locations) - 1

location = Locations[locationId]
BASE_URL = 'https://einthusan.ca'
# break cdn url into parts leaving the server number
# https://cdn1.einthusan.io/
CDN_PREFIX = "https://cdn"
CDN_ROOT = ".io/"
CDN_BASE_URL = ".einthusan" + CDN_ROOT

##
# Prints the main categories. Called when id is 0.
##
def main_categories(name, url, language, mode):
    # cwd = ADDON.getAddonInfo('path')
    # img_path = cwd + '/images/' 
    addDir('Tamil', '', 7, '', 'tamil')
    addDir('Hindi', '', 7, '', 'hindi')
    addDir('Telugu', '', 7, '', 'telugu')
    addDir('Malayalam', '', 7, '', 'malayalam')
    addDir('Kannada', '', 7, '', 'kannada')
    addDir('Bengali', '', 7, '', 'bengali')
    addDir('Marathi', '', 7, '', 'marathi')
    addDir('Punjabi', '', 7, '', 'punjabi')
    addDir('Addon Settings', '', 12, 'DefaultAddonService.png', '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows categories for each language
##
def inner_categories(name, url, language, mode, bluray=False): 
    # cwd = ADDON.getAddonInfo('path')
    # img_path = cwd + '/images/'

    postData = 'lang=' + language
    # if bluray:
    #     postData = 'lang=' + language + '&bluray=1&'

    addDir('Featured', BASE_URL+'/movie/browse/?'+postData, 4, 'DefaultAddonsRecentlyUpdated.png', language)
    addDir('Recently Added', BASE_URL+'/movie/results/?find=Recent&'+postData, 1, 'DefaultRecentlyAddedMovies.png', language)
    addDir('Staff Picks', BASE_URL+'/movie/results/?find=StaffPick&'+postData, 1, 'DefaultDirector.png', language)
    addDir('A-Z', BASE_URL+'/movie/results/?'+postData, 8, 'DefaultMovieTitle.png', language)
    addDir('Year', BASE_URL+'/movie/results/?'+postData, 9, 'DefaultYear.png', language)
    addDir('Rating', BASE_URL+'/movie/results/?'+postData, 5, 'DefaultGenre.png', language)
    addDir('Search', BASE_URL+'/movie/results/?'+postData, 6, 'DefaultAddonsSearch.png', language)
    #addDir('[COLOR red]Actors[/COLOR]', postData, 10, img_path + 'actors.png', language)
    #addDir('[COLOR red]Director[/COLOR]', postData, 11, img_path + 'director.png', language)
    #addDir('Recent', postData, 3, img_path + 'recent.png', language)
    #addDir('[COLOR red]Top Rated[/COLOR]', postData, 5, img_path + 'top_rated.png', language)
    #if not bluray:
        #addDir('Featured', '', 4, img_path + 'featured_videos.png', language)
        #addDir('[COLOR red]Blu-Ray[/COLOR]', '', 13, img_path + 'Bluray.png', language)
        #addDir('Search', postData, 6, img_path + 'Search_by_title.png', language)
        #addDir('[COLOR red]Music Video[/COLOR]', '' , 14, img_path + 'music_videos.png', language)
        #addDir('Mp3 Music', '', 16, '', language)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# FUNCTION NOT IN USE
# Displays the categories for Blu-Ray
#
def display_BluRay_listings(name, url, language, mode):
    inner_categories(name, url, language, mode, True)

##
# FUNCTION NOT IN USE
# Just displays the two recent sections. Called when id is 3.
##
def show_recent_sections(name, url, language, mode):
    # cwd = ADDON.getAddonInfo('path')
    # img_path = cwd + '/images/' 

    # postData = 'https://einthusan.ca/movie/results/?'+url + '&find='
    # addDir('Recently Posted',  postData + 'Recent', 1, img_path + 'recently_added.png')
    # #addDir('[COLOR red]Recently Viewed[/COLOR]', postData + 'RecentlyViewed', 15, img_path + 'recently_viewed.png')
    # xbmcplugin.endOfDirectory(int(sys.argv[1]))
    return 1

##
# FUNCTION NOT IN USE
# Displays the menu for mp3 music..
# Called when id is 16
## 
def mp3_menu(name, url, language, mode):
    #addDir('')
    return 1

##
# FUNCTION NOT IN USE
# Make a post request to the JSON API and list the movies..
# Interacts with the other interfaces..
##
def list_movies_from_JSON_API(name, url, language, mode):
    # HACK: Used "url" to transport postData because we know the API url
    #       and dont need it here.
    postData = url
    response = JSONInterface.apply_filter(postData)

    if ('results' in response):
        movie_ids = response['results']

        bluray = False
        if (url.find('bluray') > -1):
            bluray = True
        add_movies_to_list(movie_ids, bluray)

        max_page = int(response['max_page']) 
        next_page = int(response['page']) + 1

        if (next_page <= max_page):
            addDir("[B]Next Page[/B] >>>", url + "&page=" + str(next_page), mode, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

# FUNCTION NOT IN USE
def add_movies_to_list(movie_ids, bluray):
    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    DB_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'movie_info_cache.db')

    COVER_BASE_URL = 'http://www.einthusan.ca/images/covers/'
    if (bluray):
        BASE_URL = 'http://www.einthusan.ca/movies/watch.php?bluray=true&id='
    else:
        BASE_URL = 'http://www.einthusan.ca/movies/watch.php?id='
    for m_id in movie_ids:
        movie_info = DBInterface.get_cached_movie_details(DB_FILE, m_id)
        if (movie_info == None):
            _, name, image = JSONInterface.get_movie_detail(m_id)
            if (image == None):
                image = ''
            DBInterface.save_move_details_to_cache(DB_FILE, m_id, name, image)
        else:
            _, name, image = movie_info
        addDir(name, BASE_URL + str(m_id) ,2, COVER_BASE_URL + image)

##
# FUNCTION NOT IN USE
# Displays a list of music videos
##
def list_music_videos(name, url, language, mode):
    if (url == "" or url == None):
        url = 'http://www.einthusan.ca/music/index.php?lang=' + language
    get_movies_and_music_videos(name, url, language, mode)

# FUNCTION NOT IN USE
def playtrailer( name,url,language,mode ):
    dialog.notification( addon.get_name(), 'fetching trailer', addon.get_icon(), 4000)
    trail = 'plugin://plugin.video.youtube/play/?videoid='+url
    xbmc.log(trail, level=xbmc.LOGNOTICE)
    xbmc.log(sys.argv[0], level=xbmc.LOGNOTICE)
    xbmc.log(sys.argv[1], level=xbmc.LOGNOTICE)
    listitem = xbmcgui.ListItem(name)
    listitem.setPath(url)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    xbmc.Player().play(url, listitem)
    sys.exit()

def http_request_with_login(url):
    username = xbmcplugin.getSetting(int(sys.argv[1]), 'username')
    password = xbmcplugin.getSetting(int(sys.argv[1]), 'password')
    xbmc.log(username)
    xbmc.log(password)

    ADDON_USERDATA_FOLDER = xbmc.translatePath(ADDON.getAddonInfo('profile'))
    COOKIE_FILE = os.path.join(ADDON_USERDATA_FOLDER, 'cookies')

    return HTTPInterface.http_get(url, COOKIE_FILE,username, password)

##
#  Scrapes a list of movies and music videos from the website. Called when mode is 1.
##
def get_movies_and_music_videos(name, url, language, mode):
    get_movies_and_music_videos_helper(name, url, language, mode, 1)

def get_movies_and_music_videos_helper(name, url, language, mode, page):
    xbmc.log("get_movies_and_music_videos_helper: "+url, level=xbmc.LOGNOTICE)
    referurl = url
    html1 =  requests.get(url).text
    # match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.*?)".*?<h3>(.*?)</h3>.+?i class(.+?)<p').findall(html1)
    match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?<img src="(.+?)".+?<h3>(.+?)<\/h3>.+?i class(.+?)<p class="synopsis">(.+?)<\/p>.+?<span>Wiki<').findall(html1)
    nextpage = re.findall('data-disabled="([^"]*)" href="(.+?)"', html1)[-1]
    print("I was here")
    # Bit of a hack
    # MOVIES_URL = "https://einthusan.ca/movies/watch/"
    for movie, lang, image, name, ishd, synopsis in match:
        if (mode == 1):
            if 'http' not in image:
                image = 'http:' + image
            else:
                image = image
            trailer = ''
            name = str(name.replace(",","").encode('ascii', 'ignore').decode('ascii'))
            movie = str(name)+','+str(movie)+','+lang+','
            if 'ultrahd' in ishd:
                name = str(name + '[COLOR blue] - Ultra HD[/COLOR]')
                movie = movie+'uhd,'+referurl
            else:
                movie = movie+'shd,'+referurl
            if 'youtube' in trailer: trail = trailer.split('watch?v=')[1].split('">')[0]
            else: trail=None
            try:
                description = synopsis.encode('ascii', 'ignore').decode('ascii')
            except:
                description=""

        # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
        addDir(name, movie, 2, image, lang, description, isplayable=True)
    if nextpage[0]!='true':
        nextPage_Url = BASE_URL+nextpage[1]
        # if (page > NUMBER_OF_PAGES):
        addDir('>>> Next Page >>>', nextPage_Url,1,'','')
        # else:
            # get_movies_and_music_videos_helper(name, nextPage_Url, language, mode, page+1)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # s.close()

# Shows the movie in the homepage..
def show_featured_movies(name, url, language, mode):
    xbmc.log("show_featured_movies: "+url, level=xbmc.LOGNOTICE)
    page_url = url

    html1 = requests.get(page_url).text
    matches = re.compile('name="newrelease_tab".+?img src="(.+?)".+?href="\/movie\/watch\/(.+?)\/\?lang=(.+?)"><h2>(.+?)<\/h2>.+?i class=(.+?)<\/div>').findall(html1)

    staffPicks_matches = re.compile('<a class="title" href="\/movie\/watch\/(.+?)\/\?lang=.+?"><h3>(.+?)<\/h3><\/a><div class="info">.+?<i class="(.+?)">.+?<\/i>.+?<\/i>Subtitle<\/p><\/div><p class="synopsis">(.+?)<\/p><div class="professionals">  <input type=.+?<img src="(.+?)"><\/div>').findall(html1)
    staffPicks_matches = staffPicks_matches[:10]
    print("it works")
    allmatches = []
    for img, id,lang, name, ishd in matches:
        img = img.replace('"><img src="','')
        img = "https:" + img

        name = name.replace(",","").encode('ascii', 'ignore').decode('ascii')
        allmatches.append((img,id,name,ishd))
    for link,name,ishd,image,ishd in staffPicks_matches:
        allmatches.append((image, link, name, ishd))

    for img, id, name, ishd in allmatches:
        print("this is id" + id)
        movieid = id
        print(movieid)
        movielang= lang
        print(movielang + "this is lang")
        movie = name+','+movieid+','+movielang
        if 'ultrahd' in ishd:
            title=name + '[COLOR blue] - Ultra HD[/COLOR]'
            movie = movie+',uhd,'+page_url
        else:
            title=name
            movie = movie+',shd,'+page_url
        link = BASE_URL+str(id)
        
        image = img
        if 'http' not in image:
            image = 'https:' + img
        else:
            image = img
        xbmc.log(image + " " + name, level=xbmc.LOGNOTICE)

        addDir(title, movie, 2, image, language, isplayable=True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # s.close()

##
# Displays the options for Top Rated. Called when id is 5.
##
def show_top_rated_options(name, url, language, mode):
    postData = url + '&find=Rating'
    addDir('Action (4+ stars)', postData + '&action=4&comedy=0&romance=0&storyline=0&performance=0&ratecount=1', 1, '')
    addDir('Comedy (4+ stars)', postData + '&action=0&comedy=4&romance=0&storyline=0&performance=0&ratecount=1', 1, '')
    addDir('Romance (4+ stars)', postData + '&action=0&comedy=0&romance=4&storyline=0&performance=0&ratecount=1', 1, '')
    addDir('Storyline (4+ stars)', postData + '&action=0&comedy=0&romance=0&storyline=4&performance=0&ratecount=1', 1, '')
    addDir('Performance (4+ stars)', postData + '&action=0&comedy=0&romance=0&storyline=0&performance=4&ratecount=1', 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Displays the options for A-Z view. Called when id is 8.
##
def show_A_Z(name, url, language, mode):
    addDir('Numbers', url+'&find=Numbers', 1, '')
    azlist = map(chr, list(range(65,91)))
    for letter in azlist:
        addDir(letter, url+'&find=Alphabets&alpha='+letter, 1, '')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Single method that shows the list of years, actors and directors. 
# Called when id is 9, 10, 11
# 9 : List of Years
# 10: List of Actors # NOT IN USE
# 11: List of directors # NOT IN USE
## 
def show_list(name, url, language, mode):
    addDir('Decade', url, 10, 'DefaultYear.png')
    addDir('Years', url, 11, 'DefaultYear.png')
    # if (mode == 9):
    #     postData = url + '&find=Year&year='
    #     values = [repr(x) for x in reversed(list(range(1940, date.today().year + 1)))]
    # elif (mode == 10):
    #     postData = url + '&organize=Cast'
    #     values = JSONInterface.get_actor_list(language)
    # else:
    #     postData = url + '&organize=Director'
    #     values = JSONInterface.get_director_list(language)

    # postData = postData + '&filtered='

    # for attr_value in values:
    #     if (attr_value != None):
    #         addDir(attr_value, postData + str(attr_value), 1, '')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_decade(name, url, language, mode):
    postData = url + '&find=Decade&decade='
    values = [repr(x) for x in reversed(list(range(1940, date.today().year + 1,10)))]
    for attr_value in values:
        if (attr_value != None):
            addDir(str(attr_value)+'s', postData + str(attr_value), 1, 'DefaultYear.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def show_years(name, url, language, mode):
    postData = url + '&find=Year&year='
    values = [repr(x) for x in reversed(list(range(1940, date.today().year + 1)))]
    for attr_value in values:
        if (attr_value != None):
            addDir(attr_value, postData + str(attr_value), 1, 'DefaultYear.png')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##
# Shows the search box for serching. Shown when the id is 6.
##
def show_search_box(name, url, language, mode):
    xbmc.log("show_search_box: "+url, level=xbmc.LOGNOTICE)
    # search_term = GUIEditExportName("")
    keyb = xbmc.Keyboard('', 'Search for Movies')
    keyb.doModal()
    if (keyb.isConfirmed()):
        search_term = urllib.parse.quote_plus(keyb.getText())
        postData = url+'&query=' + search_term
        headers={'Origin':'https://einthusan.ca','Referer':'https://einthusan.ca/movie/browse/?lang=tamil','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        html1 = requests.get(postData, headers=headers).text
        match = re.compile('<div class="block1">.*?href=".*?watch\/(.*?)\/\?lang=(.*?)".*?src="(.+?)".+?<h3>(.*?)<\/h3>.+?i class(.+?)<p').findall(html1)
        nextpage = re.findall('data-disabled="([^"]*)" href="(.+?)"', html1)[-1]

        for movie, lang, image, name, ishd in match:
            name = name.replace(",","").encode('ascii', 'ignore').decode('ascii')
            image = 'http:' + image
            movie = str(name)+','+str(movie)+','+lang+','
            if 'ultrahd' in ishd:
                name = name + '[COLOR blue] - Ultra HD[/COLOR]'
                movie = movie+'uhd,'+postData
            else:
                movie = movie+'shd,'+postData
            # addDir(name, MOVIES_URL + str(movie)+'/?lang='+lang, 2, image, lang)
            
            addDir(name, movie, 2, image, lang, isplayable=True)
        if nextpage[0]!='true':
            addDir('>>> Next Page >>>', BASE_URL+nextpage[1],1,'','')

    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

def decodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
def encodeEInth(lnk):
    t=10
    #var t=10,r=e.slice(0,t)+e.slice(e.length-1)+e.slice(t+2,e.length-1)
    r=lnk[0:t]+lnk[-1]+lnk[t+2:-1]
    return r
    
##
# Plays the video. Called when the id is 2.
##
def play_video(name, url, language, mode):
    s = requests.Session()    
    print("Playing: " + name + ", with url:"+ url)
    xbmc.log("play_video: " + url, level=xbmc.LOGNOTICE)
    
    name,url,lang,whathd,referurl=url.split(',')

    if whathd=='uhd':
        dialog = xbmcgui.Dialog()
        ret1 = dialog.select('Quality Options',
                            ['Play SD/HD','Play UHD [Premium Membership Required]'],
                            autoclose=5000,
                            preselect=0)
        
        if ret1==0:
            # whathd = 'shd'
            mainurl='https://einthusan.ca/movie/watch/%s/?lang=%s'%(url,lang)
            mainurlajax='https://einthusan.ca/ajax/movie/watch/%s/?lang=%s'%(url,lang)
            print(mainurlajax)
            headers={'Origin':'https://einthusan.ca','Referer':'https://einthusan.ca/movie/browse/?lang=tamil','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            ret2 = get_video(s,mainurl,mainurlajax, headers)

        if ret1==1:
            # whathd = 'uhd'
            headers={'Origin':'https://einthusan.ca','Referer':'https://einthusan.ca/movie/browse/?lang=tamil','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            mainurl='https://einthusan.ca/movie/watch/%s/?lang=%s&uhd=true'%(url,lang)
            mainurlajax='https://einthusan.ca/ajax/movie/watch/%s/?lang=%s&uhd=true'%(url,lang)
            #ultraHD needs lifetime premium login
            login_info(s, referurl)
            ret2 = get_video(s,mainurl,mainurlajax, headers)
            
    else:
        mainurl='https://einthusan.ca/movie/watch/%s/?lang=%s'%(url,lang)
        mainurlajax='https://einthusan.ca/ajax/movie/watch/%s/?lang=%s'%(url,lang)
        headers={'Origin':'https://einthusan.ca','Referer':'https://einthusan.ca/movie/browse/?lang=tamil','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        ret2 = get_video(s,mainurl,mainurlajax, headers)

    if ret2 == False: return False
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def get_video(s, mainurl, mainurlajax, headers=None):
    xbmc.log("get_video: " + str(mainurl), level=xbmc.LOGNOTICE)

    #htm=getUrl(mainurl,headers=headers,cookieJar=cookieJar)
    
    htm=s.get(mainurl, headers=headers, cookies=s.cookies).text
    #xbmc.log(htm, level=xbmc.LOGNOTICE)

    if re.search("Our servers are almost maxed",htm):
        xbmc.log("Sorry. Our servers are almost maxed. Remaining quota is for premium members.", level=xbmc.LOGERROR)
        xbmcgui.Dialog().yesno('Server Error',
                               'Sorry. Einthusan servers are almost maxed.',
                               'Please try again in 5 - 10 mins or upgrade to a Lifetime Premium account.',
                               yeslabel='Ok',
                               nolabel='Close',
                               autoclose=5000)
        return False

    if re.search("Go Premium",htm):
        xbmc.log("Go Premium. Please Login or Register an account then re-visit this page to continue.", level=xbmc.LOGERROR)
        xbmcgui.Dialog().ok('UltraHD Error',
                            'Premium Membership Required for UltraHD Movies.',
                            'Please add Login details in Addon Settings.')
        return False

    lnk=re.findall('data-ejpingables=["\'](.*?)["\']',htm)[0]
    #xbmc.log("lnk: " + lnk, level=xbmc.LOGNOTICE)
    r=decodeEInth(lnk)
    jdata='{"EJOutcomes":"%s","NativeHLS":false}'%lnk

    gid=re.findall('data-pageid=["\'](.*?)["\']',htm)[0]
    
    gid=html.unescape(gid)

    postdata={'xEvent':'UIVideoPlayer.PingOutcome','xJson':jdata,'arcVersion':'3','appVersion':'59','gorilla.csrf.Token':gid}
    
    rdata=s.post(mainurlajax,headers=headers,data=postdata,cookies=s.cookies).text
    
    r=json.loads(rdata)["Data"]["EJLinks"]
    xbmc.log("decodeEInth: " + str(decodeEInth(r)), level=xbmc.LOGNOTICE)
    lnk=json.loads(base64.b64decode(str(decodeEInth(r))))["HLSLink"]
	
    lnk = preferred_server(lnk, mainurl)
    xbmc.log("lnk: "+lnk, level=xbmc.LOGNOTICE)
    urlnew=lnk+('|https://einthusan.ca&Referer=%s&User-Agent=%s'%(mainurl,'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'))
    xbmc.log("urlnew: "+urlnew, level=xbmc.LOGNOTICE)
    listitem = xbmcgui.ListItem(name)
    iconImage = 'DefaultVideo.png'
    thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" )
    listitem.setArt({'icon':iconImage, 'thumb':thumbnailImage})
    listitem.setProperty('IsPlayable', 'true')
    listitem.setPath(urlnew)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    
    s.close()
    # xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def preferred_server(lnk, mainurl):
	xbmc.log("preferred_server_loc: "+location, level=xbmc.LOGNOTICE)
	if location != 'No Preference':
		if location == 'Dallas':
			servers = [23,24,25,29,30,31,35,36,37,38,45]
		elif location == 'Washington, D.C.':
			servers = [1,2,3,4,5,6,7,8,9,10,11,13,41,44]
		elif location == 'San Francisco':
			servers = [19,20,21,22,46]
		elif location == 'Toronto':
			servers = [26,27]
		elif location == 'London':
			servers = [14,15,16,17,18,32,33,39,40,42]
		else: # location == 'Sydney'
			servers = [28,34,43]
		server_num = lnk.split(CDN_BASE_URL)[0].strip(CDN_PREFIX)
		xbmc.log("preferred_server_num: "+server_num, level=xbmc.LOGNOTICE)
		SERVER_OFFSET = []
		if int(server_num) > 100:
			SERVER_OFFSET.append(100)
		else:
			SERVER_OFFSET.append(0)
		servers.append(int(server_num) - SERVER_OFFSET[0])
		vidpath = lnk.split(CDN_ROOT)[1]
		xbmc.log("vidpath: "+vidpath, level=xbmc.LOGNOTICE)
		new_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'Referer':mainurl, 'Origin':'https://einthusan.ca'}
		for i in servers:
			urltry = (CDN_PREFIX + str(i+SERVER_OFFSET[0]) + CDN_BASE_URL + vidpath)

			isitworking = requests.get(urltry, headers=new_headers).status_code
			xbmc.log(urltry, level=xbmc.LOGNOTICE)
			xbmc.log(str(isitworking), level=xbmc.LOGNOTICE)
			if isitworking == 200:
				lnk = urltry
				break
	return lnk
	
def login_info(s, referurl):
    headers={'Host':'einthusan.ca', 'Origin':'https://einthusan.ca','Referer':referurl,'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    
    htm = s.get('https://einthusan.ca/login/?lang=tamil', headers=headers, allow_redirects=False).text
    csrf=re.findall('data-pageid=["\'](.*?)["\']',htm)[0]
    if '&#43;' in csrf: csrf = csrf.replace('&#43;', '+')
    
    body = {'xEvent':'Login','xJson':'{"Email":"'+username+'","Password":"'+password+'"}', 'arcVersion':3, 'appVersion':59,'tabID':csrf+'48','gorilla.csrf.Token':csrf}
    #xbmc.log(str(body))
    headers['X-Requested-With']='XMLHttpRequest'
    
    
    headers['Referer']='https://einthusan.ca/login/?lang=tamil'
    html2= s.post('https://einthusan.ca/ajax/login/?lang=tamil',headers=headers,cookies=s.cookies, data=body,allow_redirects=False)
    
    html3=s.get('https://einthusan.ca/account/?flashmessage=success%3A%3A%3AYou+are+now+logged+in.&lang=tamil', headers=headers, cookies=s.cookies)
    
    csrf3 = re.findall('data-pageid=["\'](.*?)["\']',html3.text)[0]
    body4 = {'xEvent':'notify','xJson':'{"Alert":"SUCCESS","Heading":"AWESOME!","Line1":"You+are+now+logged+in.","Buttons":[]}', 'arcVersion':3, 'appVersion':59,'tabID':csrf+'48','gorilla.csrf.Token':csrf3}
    html4 = s.post('https://einthusan.ca/ajax/account/?lang=tamil', headers=headers, cookies=s.cookies, data=body4)
    
    return s
##
# Displays the setting view. Called when mode is 12
##
def display_setting(name, url, language, mode):
    ADDON.openSettings()

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

#########################################################
# Function  : GUIEditExportName                         #
#########################################################
# Parameter :                                           #
#                                                       #
# name        sugested name for export                  #
#                                                       # 
# Returns   :                                           #
#                                                       #
# name        name of export excluding any extension    #
#                                                       #
#########################################################
def GUIEditExportName(name):
    exit = True 
    while (exit):
          kb = xbmc.Keyboard('default', 'heading', True)
          kb.setDefault(name)
          kb.setHeading("Enter the search term")
          kb.setHiddenInput(False)
          kb.doModal()
          if (kb.isConfirmed()):
              name = kb.getText()
              exit = False
          else:
              break
    return(name)

def addLink(name,url,iconimage):
    listitem = xbmcgui.ListItem(name)
    iconImage = 'DefaultVideo.png'
    thumbnailImage = iconimage
    listitem.setArt({'icon':iconImage, 'thumb':thumbnailImage})
    listitem.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=listitem)
    return ok

def addDir(name, url, mode, iconimage, lang='', description='', isplayable=False):
    u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&lang="+urllib.parse.quote_plus(lang)+'&description='+urllib.parse.quote_plus(description)
    
    listitem = xbmcgui.ListItem(name)
    iconImage = 'DefaultFolder.png'
    thumbnailImage = iconimage
    listitem.setArt({'icon':iconImage, 'thumb':thumbnailImage})
    listitem.setInfo(type="Video", infoLabels={"Title": name,"Plot":description})
    listitem.setProperty('IsPlayable', 'true')
    isfolder=True
    if isplayable:
        isfolder=False
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=listitem,isFolder=isfolder)
    return ok

params=get_params()
url=''
name=''
mode=0
language=''
description=''

try:
    url=urllib.parse.unquote_plus(params["url"])
except:
    pass

try:
    name=urllib.parse.unquote_plus(params["name"])
except:
    pass

try:
    mode=int(params["mode"])
except:
    pass

try:
    language=urllib.parse.unquote_plus(params["lang"])
except:
    pass

try:
    description=urllib.parse.unquote_plus(params["description"])
except:
    pass

# Modes
# 0: The main Categories Menu. Selection of language
# 1: For scraping the movies from a list of movies in the website
# 2: For playing a video
# 3: The Recent Section
# 4: The top viewed list. like above
# 5: The top rated list. Like above
# 6: Search options
# 7: Sub menu
# 8: A-Z view.
# 9: Years view
# 10: Decade view
# 11: Yearly view
# 12: Show Addon Settings

function_map = {}
function_map[0] = main_categories
function_map[1] = get_movies_and_music_videos
function_map[2] = play_video
function_map[3] = show_recent_sections
function_map[4] = show_featured_movies
function_map[5] = show_top_rated_options
function_map[6] = show_search_box
function_map[7] = inner_categories
function_map[8] = show_A_Z
function_map[9] = show_list
function_map[10] = show_decade
function_map[11] = show_years
function_map[12] = display_setting
function_map[13] = display_BluRay_listings
function_map[14] = list_music_videos
function_map[15] = list_movies_from_JSON_API
function_map[16] = mp3_menu

function_map[mode](name, url, language, mode)