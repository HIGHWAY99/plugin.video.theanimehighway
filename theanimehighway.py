### ##########################################
###
### # The Anime Highway - by The Highway 2013.
### # version 0.0.5x
###
### ##########################################
### ##########################################
__plugin__ = "The Anime Highway"
__authors__ = "The Highway"
__credits__ = "o9r1sh of plugin.video.gogoanime for Videoweed and Video44 source parsing. TheHighway(Myself) for AnimeGet plugin (simular site)"
### ##########################################
import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,sys
import string,StringIO,logging,urlresolver,random,array
import videolinks
from videolinks import vvVIDEOLINKS
from videolinks import *
from teh_tools import *
try: import json
except ImportError: import simplejson as json
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
try: import StorageServer
except: import storageserverdummy as StorageServer
plugin_id='plugin.video.theanimehighway'
cache = StorageServer.StorageServer(plugin_id)
local=xbmcaddon.Addon(id=plugin_id)
addon = Addon(plugin_id, sys.argv)
__settings__ 		= xbmcaddon.Addon(id=plugin_id)
__home__ = __settings__.getAddonInfo('path')
##__home__ = 'special://home/addons/plugin.video.theanimehighway/art'
#special://home/addons/plugin.video.theanimehighway/art
#addonPath=os.getcwd()
addonPath=__home__
artPath=addonPath+'/art/'
#icon = xbmc.translatePath( os.path.join( __home__, 'icon.png' ) )
#home = xbmc.translatePath(addon.getAddonInfo('path'))
if __settings__.getSetting("enable-debug") == "true":debugging=True
else: debugging=False
#if (debugging==True): 
if __settings__.getSetting("show-debug") == "true": shoDebugging=True
else: shoDebugging=False
#if (showDebugging==True): 
#########################################
#########################################
params=get_params()
url=None
urlbac=None
name=None
name2=None
type2=None
favcmd=None
mode=None
scr=None
imgfan=None
show=None
category=None

try: category=urllib.unquote_plus(params["cat"])
except: pass
if category==None: category='Base'
try:
        url=urllib.unquote_plus(params["url"])
        urlbac=url
except: pass
try: scr=urllib.unquote_plus(params["scr"])
except: pass
try: imgfan=urllib.unquote_plus(params["fan"])
except: pass
try: favcmd=urllib.unquote_plus(params["fav"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: name2=urllib.unquote_plus(params["nm"])
except: pass
try: show=urllib.unquote_plus(params["show"])
except: pass
try: type2=int(params["tp"])
except: pass
try: mode=int(params["mode"])
except: pass

ICON5 = os.path.join(artPath, 'iconA44couk.png');ICON4 = os.path.join(artPath, 'icongd.png');ICON3 = os.path.join(artPath, 'iconAPlus.png');ICON2 = os.path.join(artPath, 'iconA44.png');ICON1 = os.path.join(artPath, 'iconAG.png');ICON0 = os.path.join(__home__, 'icon.png')
fanart5 = os.path.join(artPath, 'fanartA44couk.jpg');fanart4 = os.path.join(artPath, 'fanartgd.jpg');fanart3 = os.path.join(artPath, 'fanartAPlus.jpg');fanart2 = os.path.join(artPath, 'fanartA44.jpg');fanart1 = os.path.join(artPath, 'fanartAG.jpg');fanart0 = os.path.join(__home__, 'fanart.jpg')
if type2==5:			#site 5
	fanart = os.path.join(artPath, 'fanartA44couk.jpg');ICON = os.path.join(artPath, 'iconA44couk.png');mainSite='http://www.anime44.co.uk/'
	if ('-anime' in url) and ('http://' not in url): url = mainSite + 'subanime/' + url
	if ('-anime' in url) and ('http://' not in scr) and (artPath not in scr): scr = mainSite + 'subanime/' + scr
	if ('-anime' in url) and ('http://' not in imgfan) and (artPath not in imgfan): imgfan = mainSite + 'subanime/' + imgfan
	#if ('-anime' not in url) and ('http://' not in url): url = mainSite + 'english-dubbed/' + url
	#if ('-anime' not in url) and ('http://' not in scr) and (artPath not in scr): scr = mainSite + 'english-dubbed/' + scr
	#if ('-anime' not in url) and ('http://' not in imgfan) and (artPath not in imgfan): imgfan = mainSite + 'english-dubbed/' + imgfan
	#if ('alpha-anime' in url): url.replace('alpha-anime','subanime')
	#if ('alpha-movies' in url): url.replace('alpha-movies','subanime')
	#if ('alpha-anime' in show): show.replace('alpha-anime','subanime')
	#if ('alpha-movies' in show): show.replace('alpha-movies','subanime')
elif type2==4:			#site 4
	fanart = os.path.join(artPath, 'fanartgd.jpg');ICON = os.path.join(artPath, 'icongd.png');mainSite='http://www.gooddrama.net/'
elif type2==3:		#site 3
	fanart = os.path.join(artPath, 'fanartplus.jpg');ICON = os.path.join(artPath, 'iconplus.png');mainSite='http://www.animeplus.tv/'
elif type2==2:		#site 2
	fanart = os.path.join(artPath, 'fanartA44.jpg');ICON = os.path.join(artPath, 'iconA44.png');mainSite='http://www.anime44.com/'
else:							#site 1
	fanart = os.path.join(artPath, 'fanartAG.jpg');ICON = os.path.join(artPath, 'iconAG.png');mainSite='http://www.animeget.com/'

SiteBits=['nosite','animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk']
SiteNames=['nosite','[COLOR blue][COLOR white]Anime[/COLOR]Get[/COLOR]','[COLOR red][COLOR white]Anime[/COLOR]44[/COLOR]','[COLOR darkblue][COLOR white]Anime[/COLOR]Plus[/COLOR]','[COLOR grey]Good[COLOR white]Drama[/COLOR][/COLOR]','[COLOR maroon][COLOR white]Anime[/COLOR]Zone[/COLOR]','','','']
SitePrefixes=['nosite','','','','','subanime/','','','']
SiteSufixes= ['nosite','','','','','.html','','','']
SiteSearchUrls= ['nosite','http://www.animeget.com/search','http://www.anime44.com/anime/search?search_submit=Go&key=','http://www.animeplus.tv/anime/search?search_submit=Go&key=','http://www.gooddrama.net/drama/search?stype=drama&search_submit=Go&key=','No Search Engine for VideoZone','','','','']
SiteSearchMethod= ['nosite','post','get','get','get','VideoZone','','','','']

Sites=['animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk']
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyColors=['red','blue','darkblue','grey','maroon']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
#############################
if debugging==True:
	print 'Category from URL: ',category
	print "Mode: "+str(mode)
	print "URL: "+str(url)
	print "Name: "+str(name)
	print "Name2: "+str(name2)
	print "Type2: "+str(type2)
	print "FavCmd: "+str(favcmd)
	print "uScreenShot: "+str(scr)
	print "uFanart: "+str(imgfan)
	print "show: "+str(show)
	print "Category: "+str(category)
#########################################
#############################
def menu0():#Main Menu
				VaddDir('                          [B][COLOR purple]--  The  Anime  Highway  --[/COLOR][/B]', '', 1, ICON0, fanart0, False)
				VaddDir('[COLOR grey] Please select a site:[/COLOR]', '', 1, ICON0, fanart0, False)
				addDir('[COLOR ' + MyColors[1] + '][COLOR white]Anime[/COLOR]Get[/COLOR]','Site 1 - AnimeGet','ag',1,1,ICON1,fanart1,SiteBits[1])
				addDir('[COLOR ' + MyColors[0] + '][COLOR white]Anime[/COLOR]44 [/COLOR]','Site 2 - Anime44.com','a44',2,1,ICON2,fanart2,SiteBits[2])
				addDir('[COLOR ' + MyColors[2] + '][COLOR white]Anime[/COLOR]Plus [/COLOR]','Site 3 - AnimePlus','aplus',3,1,ICON3,fanart3,SiteBits[3])
				addDir('[COLOR ' + MyColors[4] + '][COLOR white]Anime[/COLOR]Zone [/COLOR]','Site 5 - Anime44.co.uk','aplus',5,1,ICON5,fanart5,SiteBits[5])#animezone = anime44.co.uk and appreantly animeinfo.co.uk and animehere.co.uk
				addDir('[COLOR ' + MyColors[3] + ']Good[COLOR white]Drama[/COLOR] [/COLOR]','Site 4 - GoodDrama','gd',4,1,ICON4,fanart4,SiteBits[4])
				addDir('[COLOR tan]Favorites[/COLOR]','Favorites','favs',1,888,ICON0,fanart0,'Favorites')
				VaddDir('[COLOR maroon] Visit with [COLOR tan]Highway[/COLOR] and others @ [COLOR white]#XBMCHUB[/COLOR] on [COLOR white]irc.freenode.net[/COLOR]:6667 [/COLOR]', '', 1, ICON0, fanart0, False)
				set_view('none',int(getset('viewmode-default')))
def menu1():#Main Menu
        if type2==4:#gooddrama
        	addFolder('[COLOR ' + MyColors[0] + ']Drama Movies[/COLOR]','Movies','drama-movies',type2,3,'movies.png','Drama Movies')
        	addFolder('[COLOR ' + MyColors[1] + ']Drama Series[/COLOR]','List','drama-shows',type2,2,'full.png','Drama Series')
        elif (type2==1) or (type2==3) or (type2==5):#animeget & animeplus & animezone
        	addFolder('[COLOR ' + MyColors[0] + ']Anime Movies[/COLOR]','Movies','anime-movies',type2,3,'movies.png','Anime Movies')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime Series[/COLOR]','List','anime-shows',type2,2,'full.png','Anime Series')
        else:
        	addFolder('[COLOR ' + MyColors[0] + ']Anime Movies[/COLOR]','Movies','category/anime-movies',type2,601,'movies.png','Anime Movies')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime Series[/COLOR]','List','anime-list',type2,2,'full.png','Anime Series')
        if (type2==1) or (type2==2):#animeget & anime44
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing Series[/COLOR]','List','ongoing-anime',type2,6,'plus.png','Ongoing Anime')
        #addDir('Latest Episodes','List',mainSite + 'anime-updates',0,7,artPath + 'full.png',fanart)
        if type2==1:
        	addDir('[COLOR ' + MyColors[1] + ']New Series[/COLOR]','List',mainSite + 'new-anime',type2,6,artPath + 'gogoanime\\newseries.png',fanart,'New Anime Series')
        	addDir('[COLOR ' + MyColors[2] + ']Suprise Me[/COLOR]','List',mainSite + 'surprise',type2,4,artPath + 'surpriseme1.jpg',fanart,'Surprise Me')
        if (type2==5):
        	#addDir('[COLOR ' + MyColors[2] + ']Dubbed Anime List[/COLOR]','List','http://animeinfo.co.uk/index.html',type2,4,artPath + 'full.png',fanart)
        	#addFolder('[COLOR ' + MyColors[2] + ']Dubbed Anime List[/COLOR]','Dubbed Anime','http://animeinfo.co.uk/index.html',type2,601,'full.png')
        	addFolder('[COLOR lime]Dubbed Anime[/COLOR]','Dubbed Anime','http://animeinfo.co.uk/index.html',type2,250,'full.png','Dubbed Anime')
        #if type2==2:
        #	#addFolder('[COLOR tan]Search[/COLOR]','','',type2,400,'search-icon.png')
        if (type2==1) or (type2==2) or (type2==3) or (type2==4):
        	addDir('[COLOR tan]Search[/COLOR]','',mainSite + 'Search',type2,400,artPath + 'search-icon.png',fanart,'Search')
        #addDir('Search','List',mainSite + 'new-anime',0,8,artPath + 'full.png',fanart)
        set_view('none',int(getset('viewmode-default')))
def menu2():#series
        if type2==4:#gooddrama
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','drama-shows',type2,201,'full.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','drama-show-genres',type2,211,'Glossy_Black\\genres.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-shows',type2,6,'BLANK.png','Recent')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-shows',type2,6,'plus.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-shows',type2,6,'BLANK.png')
        elif (type2==1) or (type2==3) or (type2==5):#animeget & animeplus & animezone
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List',SitePrefixes[type2]+'anime-shows'+SiteSufixes[type2],type2,201,'full.png','Index')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List',SitePrefixes[type2]+'anime-genres'+SiteSufixes[type2],type2,211,'Glossy_Black\\genres.png','Genre')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List',SitePrefixes[type2]+'popular-shows'+SiteSufixes[type2],type2,6,'BLANK.png','Popular')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List',SitePrefixes[type2]+'new-shows'+SiteSufixes[type2],type2,6,'BLANK.png','New')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List',SitePrefixes[type2]+'recent-shows'+SiteSufixes[type2],type2,6,'BLANK.png','Recent')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List',SitePrefixes[type2]+'ongoing-shows'+SiteSufixes[type2],type2,6,'plus.png','Ongoing')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List',SitePrefixes[type2]+'completed-shows'+SiteSufixes[type2],type2,6,'BLANK.png','Completed')
        elif type2==2:#anime44
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','anime-list',type2,201,'full.png','Index')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','anime-genres',type2,211,'Glossy_Black\\genres.png','Genre')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-anime',type2,6,'BLANK.png','Popular')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-anime',type2,6,'BLANK.png','New')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-anime',type2,6,'BLANK.png','Recent')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-anime',type2,6,'plus.png','Ongoing')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-anime',type2,6,'BLANK.png','Completed')
        set_view('none',int(getset('viewmode-default')))
def menu3():#movies
        if (type2==1) or (type2==5):
        	addFolder('Index','List',SitePrefixes[type2]+'anime-movies'+SiteSufixes[type2],type2,301,'movies.png')
        	addFolder('Genre','List',SitePrefixes[type2]+'anime-movie-genres'+SiteSufixes[type2],type2,311,'Glossy_Black\\genres.png')
        	addFolder('Popular','List',SitePrefixes[type2]+'popular-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
        	addFolder('New','List',SitePrefixes[type2]+'new-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
        	addFolder('Recent','List',SitePrefixes[type2]+'recent-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
        else:
        	addFolder('Index','List','category/anime-movies',type2,301,'movies.png')
        	addFolder('Genre','List','anime-movie-genres',type2,311,'Glossy_Black\\genres.png')
        	addFolder('Popular','List','popular-movies',type2,6,'BLANK.png')
        	addFolder('New','List','new-movies',type2,6,'BLANK.png')
        	addFolder('Recent','List','recent-movies',type2,6,'BLANK.png')
        set_view('none',int(getset('viewmode-default')))
def menu250():#dubbed-anime
	if (type2==5):
		addFolder('Index  - (05 per page)','List','index.html?max-results=15&sort=1',type2,253,'full.png')
		addFolder('Genre - (15 per page) * Suggested','List','indexef22.html?max-results=15&cat-id=5',type2,252,'Glossy_Black\\genres.png')
		#addFolder('Popular','List',SitePrefixes[type2]+'popular-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
		#addFolder('New','List',SitePrefixes[type2]+'new-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
		#addFolder('Recent','List',SitePrefixes[type2]+'recent-movies'+SiteSufixes[type2],type2,6,'BLANK.png')
	set_view('none',int(getset('viewmode-default')))
def menu252():#dubbed-anime#genres
	if (type2==5):
		addDirD('- All Anime List -',	name,mainSite+'indexef22.html?max-results=15&sort=1&cat-id=5',type2,253,ICON,fanart,True)
		addDirD('action',							name,mainSite+'index2373.html?max-results=15&sort=1&cat-id=9',type2,253,ICON,fanart,True)
		addDirD('adventure',					name,mainSite+'indexcaef.html?max-results=15&sort=1&cat-id=12',type2,253,ICON,fanart,True)
		addDirD('comedy',							name,mainSite+'indexdad4.html?max-results=15&sort=1&cat-id=13',type2,253,ICON,fanart,True)
		addDirD('drama',							name,mainSite+'index9d40.html?max-results=15&sort=1&cat-id=6',type2,253,ICON,fanart,True)
		addDirD('fantasy',						name,mainSite+'index63e1.html?max-results=15&sort=1&cat-id=11',type2,253,ICON,fanart,True)
		addDirD('horror',							name,mainSite+'index918a.html?max-results=15&sort=1&cat-id=8',type2,253,ICON,fanart,True)
		addDirD('magic',							name,mainSite+'indexe1d7.html?max-results=15&sort=1&cat-id=17',type2,253,ICON,fanart,True)
		addDirD('mystery',						name,mainSite+'index5211.html?max-results=15&sort=1&cat-id=14',type2,253,ICON,fanart,True)
		addDirD('psychological',			name,mainSite+'index1919.html?max-results=15&sort=1&cat-id=3',type2,253,ICON,fanart,True)
		addDirD('romance',						name,mainSite+'index7bb9.html?max-results=15&sort=1&cat-id=4',type2,253,ICON,fanart,True)
		addDirD('science fiction',		name,mainSite+'indexb3bc.html?max-results=15&sort=1&cat-id=7',type2,253,ICON,fanart,True)
		addDirD('slice of life',			name,mainSite+'index7e70.html?max-results=15&sort=1&cat-id=15',type2,253,ICON,fanart,True)
		addDirD('supernatural',				name,mainSite+'index5e21.html?max-results=15&sort=1&cat-id=10',type2,253,ICON,fanart,True)
		addDirD('thriller',						name,mainSite+'indexec00.html?max-results=15&sort=1&cat-id=16',type2,253,ICON,fanart,True)
		addDirD('tournament',					name,mainSite+'index09d2.html?max-results=15&sort=1&cat-id=18',type2,253,ICON,fanart,True)
		addDirD('yaoi',								name,mainSite+'indexe2f0.html?max-results=15&sort=1&cat-id=19',type2,253,ICON,fanart,True)
		addDirD('yuri',								name,mainSite+'index16d2.html?max-results=15&sort=1&cat-id=20',type2,253,ICON,fanart,True)
	set_view('none',int(getset('viewmode-default')))

def menu253(url):#dubbed-anime#show-listings
	viewtyp='tvshows'
	link=getURL(url)
	if type2==5:t=''
	else: return
	dat_a=(link.split('<p><b>Filter by Genres:</b>')[1]).split('<div class="navigation">')[0]
	dat_b=(link.split('</div><!--/post-'))
	for dat_show in dat_b:
		if '/><b>Watch ' in dat_show:
			if '/><b>Watch ' in dat_show: show_title=(re.compile('/><b>Watch (.+?)</b>').findall(dat_show)[0]).strip()
			else: show_title='[Unknown]'
			try: show_url=mainSite+(((re.compile("<a href='(.+?)'>Watch This Anime >>></a></b></p>").findall(dat_show)[0]).strip()).replace('../',''))
			except: show_url='Unknown'
			if (show_url=='Unknown') or (show_title=='[Unknown]'): t=''
			else:
				try: show_img=mainSite+(((re.compile('<img src="(.+?)" width="165" height="200" style="float: left;margin:.+?;" /><b>Watch ').findall(dat_show)[0]).strip()).replace('../',''))
				except: show_img=ICON
				try: show_genres=((re.compile('>Genres <font color=".+?"> : (.+?)<').findall(dat_show)[0]).strip())
				except: show_genres='Unknown' ##Example: 'action, adventure, comedy, drama, magic, romance'
				try: show_themes=((re.compile('Themes: (.+?)<').findall(dat_show)[0]).strip())
				except: show_themes='Unknown' ##Example: 'dragons, fanservice, harem, magical girl, school, tsundere'
				try: show_plot=((dat_show.split('> Plot Summary: ')[1]).split('...</p>')[0]).strip()
				except: show_plot='(Not Available)'
				try: show_episode_count=((re.compile('Number of Episodes : (.+?) Episode').findall(dat_show)[0]).strip())
				except: show_episode_count='0'
				try: show_comment_count=((re.compile('Total of Comments :  (.+?) Comment').findall(dat_show)[0]).strip())
				except: show_comment_count='0'
				try: show_votes=((re.compile('title="(.+?) votes,').findall(dat_show)[0]).strip())
				except: show_votes='0'
				#try: show_rating=((re.compile('votes, average: (.+?) out of 5"').findall(dat_show)[0]).strip())
				#try: show_rating=((dat_show.split(' out of 5"')[0]).split('average: ')[1]).strip()
				try: show_rating=((dat_show.split('average: ')[1]).split(' out of 5"')[0]).strip()
				except: show_rating='0'
				#
				thetvdb_data=metaArt_get(show_title,0,'none',fanart,show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
				if (debugging==True): print thetvdb_data
				vid_descr=show_plot #thetvdb_data[6]
				#if vid_descr=='none': vid_descr=show_plot
				if ("&#8217;" in vid_descr): vid_descr=vid_descr.replace("&#8217;","'")
				if ("&#8220;" in vid_descr): vid_descr=vid_descr.replace('&#8220;','"')
				if ("&#8221;" in vid_descr): vid_descr=vid_descr.replace('&#8221;','"')
				vid_status=thetvdb_data[8]
				vid_fanart=thetvdb_data[3]
				if vid_fanart=='none': vid_fanart=fanart
				vid_poster=thetvdb_data[4]
				if vid_poster=='none': vid_poster=show_img
				vid_banner=thetvdb_data[5]
				vid_language=thetvdb_data[9]
				vid_network=thetvdb_data[10]
				vid_id=thetvdb_data[1]
				vid_genres=show_genres #thetvdb_data[7]
				#if vid_genres=='none': vid_genres=show_genres
				vid_rating=show_rating #thetvdb_data[11]
				vid_votes=show_votes #'Unknown'#thetvdb_data[6]##not handled atm
				vid_released='Unknown'#thetvdb_data[]
				vid_type='Dubbed Anime'#'Unknown'#thetvdb_data[6]
				Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':vid_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':vid_fanart, 'Poster':vid_poster, 'Banner':vid_banner, 'Language':vid_language, 'Network':vid_network, 'Genre':vid_genres, 'Theme': show_themes, 'Comments':show_comment_count, 'Total Episodes':show_episode_count } 
				addDirD(show_title,show_title,show_url,type2,254,vid_poster,vid_fanart,True,'',Labels)
	if ('">&gt;</a></li>' in link):
		matchb=re.compile('<li><a href="(.+?)">&gt;</a></li>').findall(link)
		for url3 in matchb:
			if '../' in url3: url3=(url3.replace('../','page/'))
			url3=mainSite+url3
			addDir(' Next',show,url3,type2,253,artPath + 'next-icon.png',fanart)#gogoanime\\next.png
	set_view(viewtyp,int(getset('viewmode-shows')))#set_view('none',508)
def menu253_old(url):#dubbed-anime#show-listings #### fails to display some results
	viewtyp='tvshows'
	link=getURL(url)
	match=re.compile('<img src="../(.+?)" width="165" height="200" style="float: left;margin:.+?;" /><b>Watch (.+?)</b><br/>Genres <font color="#FFFFCC"> : (.+?)<br />\s+<font color="#FFFFCC"> Plot Summary: (.+?)\s+...</p>\s+<p align="right"><b><a href=\'(.+?)\'>Watch This Anime >>></a></b></p>').findall(link)
	if (debugging==True): print match
	#show_img,show_title,show_genres,show_plot,show_url
	for show_img,show_title,show_genres,show_plot,show_url in match:
		if type2==5:
			#
			thetvdb_data=metaArt_get(show_title,0,'none',fanart,mainSite+show_img,'none',show_plot)###( Getting Metadata from thetvdb for show_name )###
			if (debugging==True): print thetvdb_data
			vid_descr=thetvdb_data[6]
			vid_released='Unknown'#thetvdb_data[]
			vid_status=thetvdb_data[8]
			vid_rating=thetvdb_data[11]
			vid_votes='Unknown'#thetvdb_data[6]##not handled atm
			vid_type='Unknown'#thetvdb_data[6]
			show_fanart=thetvdb_data[3]
			if show_fanart=='none': show_fanart=fanart
			show_poster=thetvdb_data[4]
			if show_poster=='none': show_poster=mainSite+show_img
			show_banner=thetvdb_data[5]
			show_genres=thetvdb_data[7]
			show_language=thetvdb_data[9]
			show_network=thetvdb_data[10]
			show_id=thetvdb_data[1]
			if vid_descr=='none': vid_descr=show_plot
			if show_genres=='none': show_genres=show_genres
			Labels={ 'Title':show_title,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			#Labels={ 'Title':show_title,'Plot':show_plot,'Genre':show_genres }
			addDirD(show_title,show_title,mainSite+show_url,type2,254,show_poster,show_fanart,True,'',Labels)
			#addDirD(name,name2,url,type2,mode,iconimage,fanimage,doSorting=False,categoryA='Blank',Labels='none')
		else:
			#addDirD(show_title,show_title,show_url,type2,4,show_img,fanart,False,'',show_plot,show_genres)
			test=''
	matchb=re.compile('<li><a href="(.+?)">&gt;</a></li>').findall(link)
	for url3 in matchb:
		if '..' in url3: url3=url3.replace('..','page')
		addDir(' Next',show,mainSite+url3,type2,253,artPath + 'next-icon.png',fanart)#gogoanime\\next.png
	#set_view('none',508)
	set_view(viewtyp,int(getset('viewmode-shows')))
def menu254(url):#dubbed-anime#list episodes
	test=''
	#
def menu201():#Series by A-Z
	showlistdir('others','#','123')
	for ii in MyAlphabet[:]:
		showlistdir(ii,ii,ii)
	set_view('none',int(getset('viewmode-default')))
def menu301():#Movies by A-Z (if option is available)
	movielistdir('others','#','123')
	for ii in MyAlphabet[:]:
		movielistdir(ii,ii,ii)
	set_view('none',int(getset('viewmode-default')))
def menu211(url):#List Available Genres for series
	genrelist(url,211)
	set_view('none',int(getset('viewmode-default')))#set_view('none',50)
def menu311(url):#List Available Genres for movies
	genrelist(url,311)
	set_view('none',int(getset('viewmode-default')))#set_view('none',50)
def genrelist(url,modeA):#Get list of Available Genres from Site
	link=getURL(url)
	match=re.compile('<tr>\s+<td>\s+<a href="(.+?)">(.+?)</a>\s+</td>\s+<td>(.+?)</td>\s+</tr>').findall(link)
	for url2,name,shocount in match:
		#if type2==5:
		#	addDirD(name + ' - (' + shocount + ')',name,mainSite + 'subanime/' + url2,type2,6,ICON,fanart)#testing: change addDirD back to addDir later
		#else:
		addDirD(name + ' - (' + shocount + ')',name,url2,type2,6,ICON,fanart,True)#testing: change addDirD back to addDir later
	##set_view('none',50)
def showlistnames(url,modeA):
	if ('movie' in url): viewtyp='movies'
	else: viewtyp='tvshows'
	link=getURL(url)
	match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
	for url2,name in match:
		addDir(name,name,url2,type2,5,ICON,fanart)
	matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
	for url3 in matchb:
		addDir('Next','list',url3,type2,modeA,artPath + 'next-icon.png',fanart)#gogoanime\\next.png
	set_view(viewtyp,int(getset('viewmode-shows')),True)#set_view('none',50)
def showlist(url,modeA=0,postBool=False,postData={'search':''}):
	if ('movie' in url): viewtyp='movies'
	else: viewtyp='tvshows'
	if postBool==True:
		#if (debugging==True): print 'showlist function data:',postData,'url:',url
		link=postURL(url,postData)
	else:
		link=getURL(url)
	#set_view(viewtyp,515,True)
	matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
	for url3 in matchb:
		Labels={ 'Title':' Next' }
		if (type2==5):
			addDirD(' Next','list',mainSite + 'subanime/' + url3,type2,modeA,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
		else:
			addDirD(' Next','list',url3,type2,modeA,artPath + 'next-icon.png',fanart,True,' Next',Labels)#gogoanime\\next.png
	match=re.compile('<a href="(.+?)"><img src="(.+?)" width="120" height="168" alt="Watch (.+?) online"').findall(link) #(.*)</li>
	#if (debugging==True): print'match: ',match
	for url2,img2,name in match: #,dat_
		Labels={ 'Title':name }
		#
		thetvdb_data=metaArt_get(name)###( Getting Metadata from thetvdb for show_name )###
		#if (debugging==True): print thetvdb_data
		###0show_name,1show_id,2url_thetvdb,3show_fanart,4show_poster,5show_banner,6show_desc
		######,7match_genres,8match_status,9match_language,10match_network,11match_rating
		if thetvdb_data[3]=='none': thetvdb_fanart=fanart
		else: thetvdb_fanart=thetvdb_data[3]
		#if thetvdb_data[6]=='none': show_desc=''
		#else: show_desc=thetvdb_data[6]
		#
		vid_descr=thetvdb_data[6]
		vid_released='Unknown'#thetvdb_data[]
		vid_status=thetvdb_data[8]
		vid_rating=thetvdb_data[11]
		vid_votes='Unknown'#thetvdb_data[6]##not handled atm
		vid_type='Unknown'#thetvdb_data[6]
		show_fanart=thetvdb_data[3]
		if show_fanart=='none': show_fanart=fanart
		show_poster=thetvdb_data[4]
		show_banner=thetvdb_data[5]
		show_genres=thetvdb_data[7]
		show_language=thetvdb_data[9]
		show_network=thetvdb_data[10]
		show_id=thetvdb_data[1]
		#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
		#
		#
		if (type2==5):
			if show_poster=='none': show_poster=mainSite + 'subanime/' + img2
			oldString='<a href="'+url2+'"><img src="'+img2+'" width="120" height="168" alt="Watch '+name+' online"'#+'.+?'
			htmlPart=(link.split(oldString)[1]).split('</li>')[0]
			if (vid_descr=='none') 		or (vid_descr=='Unknown'): 		vid_descr=		((htmlPart.split('<div class="descr">')[1]).split('[<a href="')[0]).strip()
			if (vid_released=='none') or (vid_released=='Unknown'): vid_released=	(((htmlPart.split('<span class="small">Released:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_status=='none') 	or (vid_status=='Unknown'): 	vid_status=		(((htmlPart.split('<span class="small">Status:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_rating=='none') 	or (vid_rating=='Unknown'): 	vid_rating=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('(')[0]).split('class="bold">')[1]).strip()
			if (vid_votes=='none') 		or (vid_votes=='Unknown'): 		vid_votes=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('Votes)')[0]).split('(')[1]).strip()
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,mainSite + 'subanime/' + url2,type2,4,show_poster,show_fanart,True,name,Labels)
		elif (type2==1):#animeget
			if show_poster=='none': show_poster=img2
			oldString='<a href="'+url2+'"><img src="'+img2+'" width="120" height="168" alt="Watch '+name+' online"'#+'.+?'
			htmlPart=(link.split(oldString)[1]).split('</li>')[0]
			if (vid_descr=='none') 		or (vid_descr=='Unknown'): 		vid_descr=		((htmlPart.split('<div class="descr">')[1]).split('[<a href="')[0]).strip()
			if (vid_released=='none') or (vid_released=='Unknown'): vid_released=	(((htmlPart.split('<span class="small">Released:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_status=='none') 	or (vid_status=='Unknown'): 	vid_status=		(((htmlPart.split('<span class="small">Status:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_rating=='none') 	or (vid_rating=='Unknown'): 	vid_rating=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('(')[0]).split('class="bold">')[1]).strip()
			if (vid_votes=='none') 		or (vid_votes=='Unknown'): 		vid_votes=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('Votes)')[0]).split('(')[1]).strip()
			if (vid_type=='none') 		or (vid_type=='Unknown'): 		vid_type=			((htmlPart.split('<span class="type_indic">')[1]).split('</span>')[0]).strip()
			#if (debugging==True): print name,vid_descr,vid_released,vid_status,vid_rating,vid_votes
			#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating,'Votes':vid_votes,'Type':vid_type }
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,url2,type2,4,show_poster,show_fanart,True,name,Labels)
		elif (type2==2) or (type2==3):#anime44 & animeplus
			if show_poster=='none': show_poster=img2
			oldString='<a href="'+url2+'"><img src="'+img2+'" width="120" height="168" alt="Watch '+name+' online"'#+'.+?'
			htmlPart=(link.split(oldString)[1]).split('</li>')[0]
			if (vid_descr=='none') 		or (vid_descr=='Unknown'): 		vid_descr=		((htmlPart.split('<div class="descr">')[1]).split('[<a href="')[0]).strip()
			if (vid_released=='none') or (vid_released=='Unknown'): vid_released=	(((htmlPart.split('<span class="small">Released:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_status=='none') 	or (vid_status=='Unknown'): 	vid_status=		(((htmlPart.split('<span class="small">Status:</span>')[1]).split('</span>')[0]).split('class="bold">')[1]).strip()
			if (vid_rating=='none') 	or (vid_rating=='Unknown'): 	vid_rating=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('(')[0]).split('class="bold">')[1]).strip()
			if (vid_votes=='none') 		or (vid_votes=='Unknown'): 		vid_votes=		(((htmlPart.split('<span class="small">Rating:</span>')[1]).split('Votes)')[0]).split('(')[1]).strip()
			#if (debugging==True): print name,vid_descr,vid_released,vid_status,vid_rating,vid_votes
			#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating,'Votes':vid_votes,'Type':vid_type }
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,url2,type2,4,show_poster,show_fanart,True,name,Labels)
		else:
			if show_poster=='none': show_poster=img2
			Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
			addDirD(name,name,url2,type2,4,show_poster,show_fanart,True,name,Labels)
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
	set_view(viewtyp,int(getset('viewmode-shows')),True)
def EPISODESlist(url,mediaType='Subbed'):
        #
        if ('movie' in url): viewtyp='movies'
        else: viewtyp='tvshows'
        #if (debugging==True): print 'testing for animeget thetvdb'
        thetvdb_data=metaArt_get(show)
        ###show_name,show_id,url_thetvdb,show_fanart,show_poster,show_banner,show_desc,match_genres,match_status,match_language,match_network,match_rating
        if thetvdb_data[3]=='none': thetvdb_fanart=fanart
        else: thetvdb_fanart=thetvdb_data[3]
        if thetvdb_data[6]=='none': show_desc=''
        else: show_desc=thetvdb_data[6]
        #if (debugging==True): print 'thetvdb_fanart: '+thetvdb_fanart
        #
        link=getURL(url)
        matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        for url3 in matchb:
        	addDirD(' Next',show,url3,type2,mode,artPath + 'next-icon.png',thetvdb_fanart)#gogoanime\\next.png
        img3=''
        matcha=re.compile('<img src="(.+?)" id="series_image" width="250" height="370" alt="').findall(link)
        for img2 in matcha:
          img3=img2
        if thetvdb_data[4]=='none': thetvdb_poster=img3
        else: thetvdb_poster=thetvdb_data[4]
        if (type2==1) or (Sites[0] in url) or (type2==3) or (Sites[2] in url) or (type2==4) or (Sites[3] in url):#animeget, animeplus, gooddrama
        	match=re.compile('<li>\s+<a href="(.+?)">(.+?)</a>\s+<span class="right_text">(.+?)</span>').findall(link)
        	for url2,name,dateadded in match:
        		addDirD(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,thetvdb_fanart)
        		#addDir(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,fanart)
        elif (type2==5):#AnimeZone
        	match=re.compile('<a href="../(.+?)">(.+?)</a><br />').findall(link)
        	if mediaType=='Dubbed': url_pre=mainSite+'english-dubbed/'+''
        	else: url_pre=mainSite+'subanime/'+''
        	for url2,name in match:
        		addDirD(name,name,url_pre+url2,type2,5,img3,thetvdb_fanart)
        else:#type2==2 or Sites[1]#anime44
        	#if (debugging==True): print 'test failed'
        	match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
        	for url2,name in match:
        		if ('Privacy' in name) and ('Disclaimer' in name): continue
        		else:
        			#thetvdb_fanart=thetvdb_com(name)
        			#if thetvdb_fanart=='none':thetvdb_fanart=fanart
        			#addDir(name,name,url2,type2,5,img3,thetvdb_fanart)
        			#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating,'Votes':vid_votes,'Type':vid_type }
        			Labels={ 'Title':name,'Plot':show_desc }
        			addDirD(name,name,url2,type2,5,thetvdb_poster,thetvdb_fanart,True,name,Labels)
        			addDirD(name,name,url2,type2,5,img3,thetvdb_fanart)
        ##matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        ##for url3 in matchb:
        ##        addDir('Next','movies',url3,0,302,artPath + 'gogoanime\\next.png',fanart)
        #set_view('none',50)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        set_view(viewtyp,int(getset('viewmode-episodes')),True)
def VIDEOsource(url,name):
				vvVIDEOLINKS(url,name,name2,scr,imgfan,show,type2,mode)
				linkO=getURL(url)
				if '/2">Playlist 2</a></li>' in linkO: 
					vvVIDEOLINKS(url + '/2',name,name2,scr,imgfan,show,type2,mode)
				if '/3">Playlist 3</a></li>' in linkO: 
					vvVIDEOLINKS(url + '/3',name,name2,scr,imgfan,show,type2,mode)
				xbmcplugin.endOfDirectory(int(sys.argv[1]))
				#url=None	urlbac=None	name=None	name2=None	type2=None	favcmd=None	mode=None	scr=None	imgfan=None	show=None
				#set_view('none',50)

#########################################
def primewire_links(url,name):
	priUrl='http://www.primewire.ag'
	priUrlExt='http://www.primewire.ag/external.php?'
	if priUrl in url: test=''
	else: url=priUrl+url
	#if (debugging==True): print 'PrimeWire.ag URL: '+url
	if 'watch-' in url: 
		test=''
		#if (debugging==True): print '"watch-" is in url: '+url
	else: return
	page_show=getURL(url)
	if page_show=='none': return
	else:
		test=''
		#if (debugging==True): print 'page_show not == "none"'
	if '<meta property="og:title"' in page_show: show_title=re.compile('<meta property="og:title" content="(.+?)">').findall(page_show)[0]
	else: show_title='Unknown'
	if '<meta name="description"' in page_show: show_desc =re.compile('<meta name="description" content="Watch .+? online - (.+?). Download .+?.">').findall(page_show)[0]
	else: show_desc='Unknown'
	if '<meta property="og:type"' in page_show: show_type =re.compile('<meta property="og:type" content="(.+?)">').findall(page_show)[0]
	else: show_type='Unknown'
	if ('movie' in show_type): viewtyp='movies'
	else: viewtyp='tvshows'
	if '<meta property="og:image"' in page_show: show_image=re.compile('<meta property="og:image" content="(.+?)"/>').findall(page_show)[0]
	else: show_image=fanart0
	#if (debugging==True): print show_title,show_desc,show_type,show_image
	#
	Labels={ 'Title':show_title,'Plot':show_desc,'Type':show_type, 'Fanart':show_image, 'Poster':show_image }
	addDirD(show_title,show_title,'' + url,type2,1900,show_image,show_image,False,show_title,Labels)
	#
	if '<h1 class="titles"><span>Derelict Links</span></h1>' in page_show: test=''
	else: return
	page_show_part=(page_show.split('<h1 class="titles"><span>Derelict Links</span></h1>')[1]).split('<h1 class="titles">')[0]
	page_show_parts=page_show_part.split('<tbody>')
	for page_show_tbody in page_show_parts:
		page_show_tbody=page_show_tbody.split('</tbody>')[0]
		if 'sponsored' in page_show_tbody: continue
		else:
			if '<span class=quality_' in page_show_tbody: link_quality=re.compile('<span class=quality_(.+?)></span>').findall(page_show_tbody)[0]
			else: link_quality='Unknown'
			if '<a href="/external.php?' in page_show_tbody: link_extUrl=re.compile('<a href="/external.php?(.+?)"').findall(page_show_tbody)[0]
			else: link_extUrl='Unknown'
			if '<span class="version_host"><script type="text/javascript">document.writeln' in page_show_tbody: link_srcHost=re.compile('<span class="version_host"><script type="text/javascript">document.writeln\(\'(.+?)\'').findall(page_show_tbody)[0]
			else: link_srcHost='Unknown'
			if '<span class="version_veiws"> ' in page_show_tbody: link_verViews=re.compile('<span class="version_veiws"> (.+?) views</span>').findall(page_show_tbody)[0]
			else: link_verViews='Unknown'
			if '>Version ' in page_show_tbody: link_verNo=re.compile('>Version (.+?)<').findall(page_show_tbody)[0]
			else: link_verNo='0'
			if link_extUrl=='Unknown': continue
			else:
				Labels={ 'Title':link_verNo+'. - '+link_srcHost,'Plot':show_desc,'Type':show_type, 'Fanart':show_image, 'Poster':show_image, 'Quality':link_quality, 'Views':link_verViews, 'Host':link_srcHost }
				#if (debugging==True): print Labels
				#hosted_media = urlresolver.HostedMediaFile(url=item['url'], title=label)
				page_ref=getURL(priUrlExt + link_extUrl)
				if ('<noframes>' in page_ref) and ('</noframes>' in page_ref): link_hosterURL=re.compile('<noframes>(.+?)</noframes>').findall(page_ref)[0]
				else: link_hosterURL='Unknown'
				###<noframes>http://filenuke.com/ao1tn5ay9zq9
				if link_hosterURL=='Unknown': 
					#if (debugging==True): print 'hosterURL: '+link_hosterURL
					continue
				else:
					#stream_url=[]
					#hosted_media = urlresolver.HostedMediaFile(link_hosterURL, title=show_title).resolve()
					##if (debugging==True): print hosted_media
					#stream_url.append(hosted_media)
					##usable_url = urlresolver.choose_source(stream_url).get_url()
					#usable_url = stream_url
					usable_url = link_hosterURL
					#if (debugging==True): print usable_url
					filname=show_title+' ['+link_quality+']'
					#if (debugging==True): print filname
					addDirD(link_verNo+'. '+link_quality+' - '+link_srcHost+' ('+link_verViews+' views)',filname,priUrlExt + link_extUrl,type2,1902,show_image,show_image,False,show_title,Labels) ##url: file to download.
					#
					#
				#usable_url = urlresolver.choose_source(stream_url).get_url()
				#usable_url = stream_url
				#
				#usable_url= priUrlExt + link_extUrl
				#addDirD(link_verNo+'. '+link_quality+' - '+link_srcHost+' ('+link_verViews+' views)',link_srcHost,priUrlExt + link_extUrl,type2,1901,show_image,show_image,False,show_title,Labels) ##url: file to download.
				#addDirD(link_verNo+'. '+link_quality+' - '+link_srcHost+' ('+link_verViews+' views)',link_srcHost,usable_url,type2,1902,show_image,show_image,False,show_title,Labels) ##url: page needs parsed.
				#
			#
			#<a href="/external.php?gd=1890694741&title=Derelict&url=aHR0cDovL3d3dy52aWR4ZGVuLmNvbS94dzhnM2R2emwybjg=&domain=dmlkeGRlbi5jb20=&loggedin=0"
			#
			#<span class=quality_dvd></span>
			#
		#
		#
		#
	#
	#Labels={ 'Title':name,'Plot':vid_descr,'Year':vid_released,'Status':vid_status,'Rating':vid_rating, 'ShowID':show_id,'Votes':vid_votes,'Type':vid_type, 'Fanart':show_fanart, 'Poster':show_poster, 'Banner':show_banner, 'Language':show_language, 'Network':show_network, 'Genre':show_genres }
	#addDirD(name,name,mainSite + 'subanime/' + url2,type2,4,show_poster,show_fanart,True,name,Labels)
	#
	if ('movie' in show_type): set_view(viewtyp,int(getset('viewmode-movies')),False)
	else: set_view(viewtyp,int(getset('viewmode-shows')),False)
	#





#########################################
def FAVS():
  saved_favs = cache.get('favourites_')
  erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_favs:
    xbmc.executebuiltin(erNoFavs)
  if saved_favs == '[]':
    xbmc.executebuiltin(erNoFavs)
  if saved_favs:
    favs = sorted(eval(saved_favs), key=lambda fav: fav[0])#favs = eval(saved_favs)
    for fav in favs:
        try:
        	addDirD("%s" % fav[0].upper(),fav[0],fav[1],fav[4],fav[5],fav[2],fav[3])
        except:
        	#addDirD("%s" % fav[0].upper(),fav[0],fav[1],1,6,artPath + ICON0,fanart0)
        	continue
  set_view('tvshows',int(getset('viewmode-favs')),False)
#############################
if favcmd=='add':
        if (debugging==True): print ""+url
        addfavorite(name,url,scr,imgfan,type2,mode)
elif favcmd=='rem':
        if (debugging==True): print ""+url
        removefavorite(name,url,scr,imgfan,type2,mode)
elif favcmd=='clr':
        if (debugging==True): print ""+url
        emptyFavorites()
elif favcmd=='showurl':
        if (debugging==True): print ""+url
        showurl(name,url,scr,imgfan)
elif favcmd=='download':
        if (debugging==True): print ""+url
        download_file_prep(url,name,name2,show)
        #download_file(url,name)
elif favcmd=='metaclear':
        if (debugging==True): print ""+url
        metaArt_empty()
#############################
if mode==None or url==None or len(url)<1:
        if (debugging==True): print ""
        menu0()
elif mode==1:
        if (debugging==True): print ""+url
        menu1()
elif mode==2:
        if (debugging==True): print ""+url
        menu2()
elif mode==201:
        if (debugging==True): print ""+url
        menu201()
#elif mode==202:
#        if (debugging==True): print ""+url
#        CATEGORIESlistab(url)
elif mode==211:
        if (debugging==True): print ""+url
        menu211(url)
elif mode==250:#dubbed anime
        if (debugging==True): print ""+url
        menu250()
elif mode==251:#dubbed anime
        if (debugging==True): print ""+url
        menu251()
elif mode==252:#dubbed anime
        if (debugging==True): print ""+url
        menu252()
elif mode==253:#dubbed anime
        if (debugging==True): print ""+url
        menu253(url)
elif mode==254:#dubbed anime
        if (debugging==True): print ""+url
        EPISODESlist(url,'Dubbed')
elif mode==3:
        if (debugging==True): print ""+url
        menu3()
elif mode==301:
        if (debugging==True): print ""+url
        menu301()
#elif mode==302:
#        if (debugging==True): print ""+url
#        CATEGORIESmoviesab(url)
elif mode==311:
        if (debugging==True): print ""+url
        menu311(url)
elif mode==4:
        if (debugging==True): print ""+url
        EPISODESlist(url)
elif mode==5:
        if (debugging==True): print ""+url
        VIDEOsource(url,name)
elif mode==6:
        if (debugging==True): print ""+url
        showlist(url,mode)
elif mode==601:
        if (debugging==True): print ""+url
        showlistnames(url,mode)
elif mode==400:
        if (debugging==True): print ""+url
        searchwindow(SiteNames[type2],SiteSearchMethod[type2],SiteSearchUrls[type2],mode,type2,name2,url)
elif mode==888:
        if (debugging==True): print ""+url
        FAVS()
elif mode==999:
        if (debugging==True): print ""+url
        downloadfile(url,name)
elif mode==1900:
        if (debugging==True): print ""+url
        primewire_links(url,name)
elif mode==1901:## Mode for use when wanting to download a file. This can be directed from another plugin.
        if (debugging==True): print ""+url
        download_it_now(url,name)
elif mode==1902:## Mode for use when wanting to download a file. This can be directed from another plugin.
        if (debugging==True): print ""+url
        download_it_now(url,name2)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
