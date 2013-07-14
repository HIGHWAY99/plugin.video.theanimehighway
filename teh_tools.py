import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,sys,htmllib
import string,StringIO,logging,random,array,time
import urlresolver
try: import json
except ImportError: import simplejson as json
try: import StorageServer
except: import storageserverdummy as StorageServer
plugin_id='plugin.video.theanimehighway'
cache = StorageServer.StorageServer(plugin_id)
#import SimpleDownloader as downloader
from t0mm0.common.net import Net as net
from t0mm0.common.addon import Addon
###
__settings__ 		= xbmcaddon.Addon(id=plugin_id)
__home__ = __settings__.getAddonInfo('path')
addonPath=__home__
artPath=addonPath+'/art/'
ICON = os.path.join(__home__, 'icon.jpg')
fanart = os.path.join(__home__, 'fanart.jpg')
if __settings__.getSetting("enable-debug") == "true":debugging=True
else: debugging=False
#if (debugging==True): 
if __settings__.getSetting("show-debug") == "true": shoDebugging=True
else: shoDebugging=False
#if (showDebugging==True): 
#############################

#########################################
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

#########################################
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

ICON8 = os.path.join(artPath, 'icon_watchdub.png');ICON7 = os.path.join(artPath, 'icon_dubhappy.png');ICON6 = os.path.join(artPath, 'iconDAOn2.png');ICON5 = os.path.join(artPath, 'iconA44couk.png');ICON4 = os.path.join(artPath, 'icongd.png');ICON3 = os.path.join(artPath, 'iconAPlus.png');ICON2 = os.path.join(artPath, 'iconA44.png');ICON1 = os.path.join(artPath, 'iconAG.png');ICON0 = os.path.join(__home__, 'icon.png')
fanart8 = os.path.join(artPath, 'fanart_watchdub.jpg');fanart7 = os.path.join(artPath, 'fanart_dubhappy.jpg');fanart6 = os.path.join(artPath, 'fanartDAOn2.jpg');fanart5 = os.path.join(artPath, 'fanartA44couk.jpg');fanart4 = os.path.join(artPath, 'fanartgd.jpg');fanart3 = os.path.join(artPath, 'fanartAPlus.jpg');fanart2 = os.path.join(artPath, 'fanartA44.jpg');fanart1 = os.path.join(artPath, 'fanartAG.jpg');fanart0 = os.path.join(__home__, 'fanart.jpg')
if type2==8:			#site 8
	fanart = os.path.join(artPath, 'fanart_watchdub.jpg');ICON = os.path.join(artPath, 'icon_watchdub.png');mainSite='http://www.watchdub.com/'
elif type2==7:			#site 7
	fanart = os.path.join(artPath, 'fanart_dubhappy.jpg');ICON = os.path.join(artPath, 'icon_dubhappy.png');mainSite='http://www.dubhappy.eu/'
elif type2==6:			#site 6
	fanart = os.path.join(artPath, 'fanartDAOn2.jpg');ICON = os.path.join(artPath, 'iconDAOn2.png');mainSite='http://dubbedanimeon.com/'
elif type2==5:			#site 5
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


#########################################
SiteBits=['nosite','animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk','dubbedanimeon.com','dubhappy.eu','watchdub.com']
SiteNames=['nosite','[COLOR blue][COLOR white]Anime[/COLOR]Get[/COLOR]','[COLOR red][COLOR white]Anime[/COLOR]44[/COLOR]','[COLOR darkblue][COLOR white]Anime[/COLOR]Plus[/COLOR]','[COLOR grey]Good[COLOR white]Drama[/COLOR][/COLOR]','[COLOR maroon][COLOR white]Anime[/COLOR]Zone[/COLOR]','[COLOR teal]Dubbed[COLOR white]Anime[/COLOR]On [/COLOR]','[COLOR cornflowerblue][COLOR white]dub[/COLOR]happy[/COLOR]','[COLOR cornflowerblue]Watch[/COLOR][COLOR white]Dub[/COLOR]','','']
SitePrefixes=['nosite','','','','','subanime/','','','','','','','','','','','','']
SiteSufixes= ['nosite','','','','','.html','','','','','','','','','','','','','']
SiteSearchUrls= ['nosite','http://www.animeget.com/search','http://www.anime44.com/anime/search?search_submit=Go&key=','http://www.animeplus.tv/anime/search?search_submit=Go&key=','http://www.gooddrama.net/drama/search?stype=drama&search_submit=Go&key=','No Search Engine for VideoZone','http://dubbedanimeon.com/?s=','','','','','','','']
SiteSearchMethod= ['nosite','post','get','get','get','VideoZone','get','','','','','','','']
Sites=['animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk','dubbedanimeon.com','dubhappy.eu','watchdub.com']
MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyColors=['red','blue','darkblue','grey','maroon','teal','cornflowerblue','cornflowerblue','','','','']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
#############################
MyVideoLinkSrcMatches=['src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkSrcMatchesB=['src="(.+?)"',			'<embed.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkBrackets=['<iframe.+?src="(.+?)"', '<embed.+?src="(.+?)"', '<object.+?data="(.+?)"']
MyAlphabet=	['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=	['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
MySourcesV=		['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com',	'vidzur.com',	'upload2.com','putlocker.com','videoslasher.com','vidbull.com',		'uploadc.com',	'veevr.com',	'rutube.ru']
#MySourcesV=	['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com',	'vidzur.com',	'upload2.com','putlocker.com','videoslasher.com','vidbull.com',		'UploadC',	'veevr.com',	'rutube.ru',	'MP4UPLOAD'		,'AUENGINE']
MyIconsV=		[artPath + 'videoweed.jpg',	artPath + 'video44a.png',	artPath + 'novamov.jpg',	artPath + 'dailymotion.jpg',	artPath + 'videofun.png',	artPath + 'yourupload.jpg',	artPath + 'googlevideo.gif', artPath + 'vidzur.png', artPath + 'upload2.png', artPath + 'putlocker.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png']#BLANK.png
MyNamesV=		['VideoWeed',			'Video44',			'NovaMov',			'DailyMotion',			'VideoFun',			'YourUpload',				'Google Video',			'VidZur',			'Upload2',		'PutLocker',		'VideoSlasher',		'VidBull',		'UploadC',	'Veevr',	'RuTube',			'MP4Upload'		,'AUEngine']
MyColorsV=	['lime',					'red',					'silver',				'green',						'cyan',					'grey',					'blue',					'orange',					'white',					'white',					'white',					'white',					'white',					'white', 			'white', 			'white', 			'white', 			'white', 			'white']
#############################
#########################################

def getURLr(url,dReferer):
	try:
		req = urllib2.Request(url,dReferer)
		req.add_header(MyBrowser[0], MyBrowser[1]) 
		req.add_header('Referer', dReferer)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return(link)
	except:
		return('none')
def getURL(url):
	try:
		req = urllib2.Request(url)
		req.add_header(MyBrowser[0], MyBrowser[1]) 
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return(link)
	except:
		return('none')
def postURL(url,postStr):
		postData=urllib.urlencode(postStr)
		req = urllib2.Request(url,postData)
		req.add_header(MyBrowser[0], MyBrowser[1]) 
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return(link)
def notification(header="", message="", sleep=5000 ):
	xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )
	#notify(msg=message, title=header, delay=sleep, image=ICON)
	#notify(msg=message, title='[COLOR green][B]'+header+'[/B][/COLOR]', delay=sleep, image=ICON0)

#########################################
##Example##VaddDir('[COLOR blue]' + text[0] + '[/COLOR]', '', 0, '', False)
def addFolder(name,name2,url,type2,mode,iconimage,categoryA='Blank'):
		###addDir(name,name2,url,type2,mode,iconimage,fanimage)
		if ('http://' in iconimage) or (artPath in iconimage): t=''
		else: iconimage = artPath + iconimage
		mainSite='http://'+SiteBits[type2]+'/'
		addDir(name,name2,mainSite + url,type2,mode,iconimage,fanart,categoryA)
		#addDirD(name,name2,mainSite + url,type2,mode,artPath + iconimage,fanart,'wow')
### from videolinks.py ###
#def addFolder(name,name2,url,type2,mode,iconimage):
#		##addDir(name,name2,url,type2,mode,iconimage,fanimage)
#		addDir(name,name2,mainSite + url,type2,mode,artPath + iconimage,fanart)
def addDir(name,name2,url,type2,mode,iconimage,fanimage,categoryA='Blank'):
        if (debugging==True): print 'Category: ',category,categoryA
        categoryA=category+' ::: '+categoryA
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)+"&scr="+urllib.quote_plus(iconimage)+"&fan="+urllib.quote_plus(fanimage)+"&show="+urllib.quote_plus(name2)+"&cat="+categoryA
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDirD(name,name2,url,type2,mode,iconimage,fanimage,doSorting=False,categoryA='Blank',Labels='none'):#,plot='Blank',genres='none listed',status='none',released='unknown',rating='none',others='none'):
        if Labels=='none': Labels={ "Title" : name }
        if categoryA=='Blank': categoryA=name
        #if (debugging==True): print 'Category: ',category,categoryA
        categoryA=category+' ::: '+categoryA
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)+"&scr="+urllib.quote_plus(iconimage)+"&fan="+urllib.quote_plus(fanimage)+"&show="+urllib.quote_plus(name2)+"&cat="+urllib.quote_plus(categoryA)
        #
        if (debugging==True): print u
        vc_tag=visited_DoCheck(u)
        #if (name=='Maburaho'): visited_add(u)
        if (debugging==True): print vc_tag
        #
        ok=True
        liz=xbmcgui.ListItem(vc_tag+name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels= Labels ) #"Title": "'" + name + "'", "Plot" : plot, "Genres" : genres } )
        liz.setProperty( "Fanart_Image", fanimage )
        sysname = urllib.quote_plus(name)
        sysurl = urllib.quote_plus(url)
        sysscr = urllib.quote_plus(iconimage)
        sysfan = urllib.quote_plus(fanimage)
        #handle adding context menus
        contextMenuItems = []
        if (debugging==True): print getsetbool('enable-showurl')
        if __settings__.getSetting("enable-showurl") == "true":#doesn't work for some odd reason >> #if getsetbool('enable-showurl') == 'true':#
        	contextMenuItems.append(('[B][COLOR orange]Show[/COLOR][/B] ~  [B]URL[/B]',							'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s)' % (sys.argv[0],mode , sysname, urllib.quote_plus(name2), type2, 'showurl', sysurl, sysscr, sysfan)))
        contextMenuItems.append(('[B][COLOR green]ADD[/COLOR][/B] ~  [B][COLOR tan]Favorite[/COLOR][/B]', 			'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s&show=%s)' % (sys.argv[0],mode , sysname, urllib.quote_plus(name2), type2, 'add', sysurl, sysscr, sysfan,urllib.quote_plus(name2))))
        contextMenuItems.append(('[B][COLOR red]REMOVE[/COLOR][/B] ~  [B][COLOR tan]Favorite[/COLOR][/B]', 		'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s&show=%s)' % (sys.argv[0],mode , sysname, urllib.quote_plus(name2), type2, 'rem', sysurl, sysscr, sysfan,urllib.quote_plus(name2))))
        contextMenuItems.append(('Show Information', 			'XBMC.Action(Info)'))
        #
        #contextMenuItems.append(('[B][COLOR orange]Test[/COLOR][/B] ~  [B]Test[/B]',"notification(%s,%s)" % (sysname,sysurl)))
        if (debugging==True): print getset('enable-clearfavorites')
        if __settings__.getSetting("enable-clearfavorites") == "true":#if getset('enable-clearfavorites')==True:
        	contextMenuItems.append(('[B][COLOR yellow]Clear[/COLOR][/B] ~  [B][COLOR tan]Favorites[/COLOR][/B]', 	'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s)' % (sys.argv[0],mode , sysname, urllib.quote_plus(name2), type2, 'clr', sysurl, sysscr, sysfan)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)#True#liz.addContextMenuItems(contextMenuItems)
        if doSorting==True:
        	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addDirV(name,name2,url,type2,mode,iconimage,fanimage,categoryA=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)+"&cat="+categoryA
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
#def VaddDir(name, url, mode, iconimage, fanimage, is_folder=False,categoryA=''):#VANILLA ADDDIR (kept for reference)
#        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&cat="+categoryA
#        ok=True
#        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
#        liz.setInfo( type="Video", infoLabels={ "Title": name } )
#        liz.setProperty( "Fanart_Image", fanimage )
#        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_folder)
#        return ok
def VaddDir(name, url, mode, iconimage, fanimage, is_folder=False,categoryA=''):#VANILLA ADDDIR (kept for reference)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&cat="+categoryA
        #if (debugging==True): print u
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        contextMenuItems = []
        if __settings__.getSetting("enable-showurl") == "true":
        	contextMenuItems.append(('[B][COLOR orange]Show[/COLOR][/B] ~  [B]URL[/B]',							'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s)' % (sys.argv[0],mode , urllib.quote_plus(name), urllib.quote_plus(name), 877, 'showurl', urllib.quote_plus(url), urllib.quote_plus(iconimage), urllib.quote_plus(fanimage))))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)#True#liz.addContextMenuItems(contextMenuItems)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_folder)
        return ok
### from theanimehighway.py ###
#def addLink(name,url,iconimage):
#        ok=True
#        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
#        liz.setInfo( type="Video", infoLabels={ "Title": name } )
#        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
#        return ok
def addLink(name,url,iconimage=ICON,fanimage=fanart,shoname='none',downloadable=True):
        ok=True
        if shoname=='none':
        	try: shoname=show
        	except:  shoname=name
        if fanimage==fanart:
        	try: fanimage=imgfan
        	except: pass
        if iconimage in MyIconsV:
        	try:
        		iconimage=scr
        	except: pass
        #
        #liz=xbmcgui.ListItem(name, iconImage=artPath+"blank.gif", thumbnailImage=iconimage)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        ##if (debugging==True): print 'sitename name: '+SiteNames[type2] + name
        ##liz.setInfo( type="Video", infoLabels={ "Title": name } )
        Studio=name
        if (' - [COLOR grey]' 	in Studio): Studio = Studio.split(' - [COLOR grey]')[0]
        if (' [COLOR grey]- ' 	in Studio): Studio = Studio.split(' [COLOR grey]- ')[0]
        if ('[COLOR grey] - ' 	in Studio): Studio = Studio.split('[COLOR grey] - ')[0]
        if (' - [COLOR' 				in Studio): Studio = Studio.split(' - [COLOR')[0]
        showtitle=shoname
        if (' [COLOR lime](English Dubbed)[/COLOR]' in showtitle):
        	Studio += ' [COLOR lime](English Dubbed)[/COLOR]'
        	showtitle = showtitle.replace(' [COLOR lime](English Dubbed)[/COLOR]','')
        elif ('English Dubbed' 	in showtitle): Studio += ' [COLOR lime](English Dubbed)[/COLOR]'
        elif ('Eng Dubbed' 			in showtitle): Studio += ' [COLOR lime](English Dubbed)[/COLOR]'
        elif ('Dubbed' 					in showtitle): Studio += ' [COLOR lime](Dubbed)[/COLOR]'
        elif ('English Subbed' 	in showtitle): Studio += ' [COLOR lime](English Subbed)[/COLOR]'
        elif ('Eng Subbed' 			in showtitle): Studio += ' [COLOR lime](English Subbed)[/COLOR]'
        elif ('Subbed' 					in showtitle): Studio += ' [COLOR lime](Subbed)[/COLOR]'
        liz.setInfo( type="Video", infoLabels={ "Title": showtitle, "Studio": Studio } )
        #liz.setProperty( "Fanart_Image", fanimage )
        contextMenuItems = []
        if (debugging==True): print getset('enable-showurl')
        if __settings__.getSetting("enable-showurl") == "true":#if getset('enable-showurl')=='true':
        	contextMenuItems.append(('[B][COLOR orange]Show[/COLOR][/B] ~  [B]URL[/B]',							'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s)' % (sys.argv[0],0 , urllib.quote_plus(shoname), urllib.quote_plus(shoname), 0, 'showurl', urllib.quote_plus(url), iconimage, fanimage)))
        if (__settings__.getSetting("enable-downloading") == "true") and (downloadable == True):#if getset('enable-downloading',True)=='True':
        	#if ('videofun.me' not in url) and ('videoweed.es' not in url) and ('dailymotion.com' not in url):
        	if ('novamov.com' not in url) and ('videoweed.es' not in url) and ('dailymotion.com' not in url):
        		contextMenuItems.append(('[B][COLOR purple]Download[/COLOR][/B] ~  [B]File[/B]',				'XBMC.RunPlugin(%s?mode=%s&name=%s&nm=%s&tp=%s&fav=%s&url=%s&scr=%s&fan=%s)' % (sys.argv[0],0 , urllib.quote_plus(shoname), urllib.quote_plus(shoname), 0, 'download', urllib.quote_plus(url), iconimage, fanimage)))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)#True#liz.addContextMenuItems(contextMenuItems)
        ##liz.addContextMenuItems([('[B][COLOR green]D[/COLOR][/B][B]ownload[/B]',"downloadfile(url,name)")])
        #liz.addContextMenuItems([('[B][COLOR green]D[/COLOR][/B][B]ownload[/B]',"XBMC.RunPlugin(%s?mode=%s&name=%s&url=%s)"%(sys.argv[0],999,name,url))])
        ##xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok



#########################################
def getset(idSetting):#,defaultValue=''):#Addon.getSetting('idNameOfSetting')
	return __settings__.getSetting(idSetting)#==defaultValue

def getsetbool(idSetting):#Addon.getSetting('idNameOfSetting') #Method seems to be an utter failure for BOOL(true/false)'s
	#if (debugging==True): print __settings__.getSetting(idSetting) == 'true'
	return __settings__.getSetting(idSetting) == 'true'
def getsetbool_(idSetting):#Addon.getSetting('idNameOfSetting') #Method seems to be an utter failure for BOOL(true/false)'s
	#if (debugging==True): print __settings__.getSetting(idSetting) == 'true'
	#try: tst=__settings__.getSetting(idSetting) == 'true'
	try: tst=__settings__.getSetting(idSetting)
	except: tst='False'
	if (tst=='true') or (tst=='True') or (tst=='TRUE'): return True
	else: return False
	#return __settings__.getSetting(idSetting) == 'true'
#########################################
def download_it_now(url,name):## mode=1901 ##
	name=name.strip()
	if ('[/COLOR]' in name): name=name.replace('[/COLOR]','')
	if ('[COLOR lime]' in name): name=name.replace('[COLOR lime]','')
	if ('[/color]' in name): name=name.replace('[/color]','')
	if ('[color lime]' in name): name=name.replace('[color lime]','')
	#if ('' in name): name=name.replace('','')
	#if ('' in name): name=name.replace('','')
	#if ('' in name): name=name.replace('','')
	notification(name,'Attempting Download...')
	download_file_prep(url,name,name,name)
	## Example of how to connect to this addon's download feature from another plugin: ##
	#### xbmc.executebuiltin('XBMC.RunPlugin(%s?mode=1901&url=%s&name=%s)' % ('plugin://plugin.video.theanimehighway/', urllib.quote_plus(stream_url), urllib.quote_plus(title)))
	#### Simply make sure to include the quoted name and url for this function to work.
	#### File must be for a downloadable file or video stream, not for a page with a video on it.

def download_metapack(url, dest, displayname=False):
    print 'Downloading Metapack'
    print 'URL: %s' % url
    print 'Destination: %s' % dest
    if not displayname:
        displayname = url
    dlg = xbmcgui.DialogProgress()
    dlg.create('Downloading', '', displayname)
    start_time = time.time()
    if os.path.isfile(dest):
        print 'File to be downloaded already esists'
        return True
    try:
        urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dlg, start_time))
    except:
        #only handle StopDownloading (from cancel),
        #ContentTooShort (from urlretrieve), and OS (from the race condition);
        #let other exceptions bubble 
        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError):
            return False
        else:
            raise
    return True

### 
### Dialog DialogBusy DialogButton Menu DialogContentSettings DialogContentMenu DialogExtendedProgressBar 
### DialogFavourites DialogKaiToast DialogKeyboard DialogOK DialogProgress DialogVolumeBar DialogVideoScan
### DialogVideoInfo DialogTextViewer DialogSlider DialogSelect DialogSeekBar DialogYesNo
### 

def download_file(url='',name='temp',localfilename='temp',localpath=artPath,filext='.flv'):
		t=''
		###url='https://github.com/HIGHWAY99/plugin.video.theanimehighway/archive/master.zip'
		###localfilename='plugin.video.theanimehighway.zip'
		###localpath=__home__
		#localfilewithpath=os.path.join(localpath,localfilename)
		#if (debugging==True): print 'Attempting to download "' + localfilename + '" to "' + localfilewithpath + '" from: ' + url
		###dialogbox('To: ' + localfilewithpath,'Download File: ' + localfilename,'From: ' + url,'[COLOR red]This is still being tested.[/COLOR]')
		#if os.path.isfile(localfilewithpath): 
		#	if (debugging==True): print 'File to be downloaded already esists.'
		#	notification('Download: '+localfilename,'File already exists.')#This function may never happen.
		#	return
		#dialog = xbmcgui.Dialog()
		#if dialog.yesno('Download File', 'Do you wish to download this file?','File: ' + localfilename,'To: ' + localpath):
		#	notification('Attempting to Download File',localfilename + '[CR] This function is still being tested.')#This function may never happen.
		#	try: dp = xbmcgui.DialogProgressBG() ## Only works on daily build of XBMC.
		#	except: dp = xbmcgui.DialogProgress()
		#	dp.create('Downloading', '', localfilename)
		#	####
		#	####urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhookb(nb, bs, fs, dlg, start_time))
		#	####
		#	urllib.urlretrieve(url, localfilewithpath, lambda nb, bs, fs: _pbhookb(nb, bs, fs, dlg, start_time))
		#	#urllib.urlretrieve(url, localfilewithpath)
		#	notification('Download File','Download Complete.[CR] ' + localfilename,15000)
		#	dialogbox_ok('File Size: ' + str(os.path.getsize(localfilewithpath)) + ' (bytes)','Download Complete','Note:','Make sure the size seems right.')
		#	###total_size += os.path.getsize(fp)
		###
		###
		###notification('Download File','Sorry this feature is not yet implimented.')#This function may never happen.

def _pbhookb(numblocks, blocksize, filesize, dlg, start_time):
    try:
        percent = min(numblocks * blocksize * 100 / filesize, 100)
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
        kbps_speed = numblocks * blocksize / (time.time() - start_time)
        if kbps_speed > 0:
            eta = (filesize - numblocks * blocksize) / kbps_speed
        else:
            eta = 0
        kbps_speed /= 1024
        total = float(filesize) / (1024 * 1024)
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total)
        est = 'Speed: %.02f Kb/s ' % kbps_speed
        est += 'ETA: %02d:%02d' % divmod(eta, 60)
        dlg.update(percent, mbs, est)
    except:
        percent = 100
        dlg.update(percent)
    #if dlg.iscanceled(): ## used for xbmcgui.DialogProgress() but causes an error with xbmcgui.DialogProgressBG()
    #    dlg.close()
    #    raise StopDownloading('Stopped Downloading')

def download_file_frodo(url='',name='temp',localfilename='temp',localpath=artPath,filext='.flv'):
		localfilewithpath=os.path.join(localpath,localfilename)
		if (debugging==True): print 'Attempting to download "' + localfilename + '" to "' + localfilewithpath + '" from: ' + url
		#dialogbox('To: ' + localfilewithpath,'Download File: ' + localfilename,'From: ' + url,'[COLOR red]This is still being tested.[/COLOR]')
		if os.path.isfile(localfilewithpath): 
			if (debugging==True): print 'File to be downloaded already esists.'
			notification('Download: '+localfilename,'File already exists.')#This function may never happen.
			return
		dialog = xbmcgui.Dialog()
		if dialog.yesno('Download File', 'Do you wish to download this file?','File: ' + localfilename,'To: ' + localpath):
			notification('Attempting to Download File',localfilename + '[CR] This function is still being tested.')#This function may never happen.
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading', '', localfilename)
			start_time = time.time()
			urllib.urlretrieve(url, localfilewithpath, lambda nb, bs, fs: _pbhookb_frodo(nb, bs, fs, dp, start_time)) #urllib.urlretrieve(url, localfilewithpath)
			##urllib.urlretrieve(url, localfilewithpath, lambda nb, bs, fs: _pbhookb_frodo(nb, bs, fs, dlg, start_time)) #urllib.urlretrieve(url, localfilewithpath)
			notification('Download File','Download Complete.[CR] ' + localfilename,15000)
			dialogbox_ok('File Size: ' + str(os.path.getsize(localfilewithpath)) + ' (bytes)','Download Complete','Note:','Make sure the size seems right.')
			#total_size += os.path.getsize(fp)
		#notification('Download File','Sorry this feature is not yet implimented.')#This function may never happen.

def _pbhookb_frodo(numblocks, blocksize, filesize, dlg, start_time):
    try:
        percent = min(numblocks * blocksize * 100 / filesize, 100)
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024)
        kbps_speed = numblocks * blocksize / (time.time() - start_time)
        if kbps_speed > 0:
            eta = (filesize - numblocks * blocksize) / kbps_speed
        else:
            eta = 0
        kbps_speed /= 1024
        total = float(filesize) / (1024 * 1024)
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total)
        est = 'Speed: %.02f Kb/s ' % kbps_speed
        est += 'ETA: %02d:%02d' % divmod(eta, 60)
        dlg.update(percent, mbs, est)
    except:
        percent = 100
        dlg.update(percent)
    if dlg.iscanceled(): ## used for xbmcgui.DialogProgress() but causes an error with xbmcgui.DialogProgressBG()
        dlg.close()
        raise StopDownloading('Stopped Downloading')


def filename_filter_colorcodes(name=''):
	if ('[/color]' 			in name): name=name.replace('[/color]','')
	if ('[/COLOR]' 			in name): name=name.replace('[/COLOR]','')
	if ('[color lime]' 	in name): name=name.replace('[color lime]','')
	if ('[COLOR lime]' 	in name): name=name.replace('[COLOR lime]','')
	if ('[b]' in name): name=name.replace('[b]','')
	if ('[B]' in name): name=name.replace('[B]','')
	if ('[/b]' in name): name=name.replace('[/b]','')
	if ('[/B]' in name): name=name.replace('[/B]','')
	if ('[cr]' in name): name=name.replace('[cr]','')
	if ('[CR]' in name): name=name.replace('[CR]','')
	#if ('' in name): name=name.replace('','')
	#if ('' in name): name=name.replace('','')
	#if ('' in name): name=name.replace('','')
	return name

def download_file_prep(url,name='none',name2='none',show='none',filext='none'):
	#
	if filext=='none':
		if   '.zip' in url: filext='.zip' #Compressed Files
		elif '.rar' in url: filext='.rar'
		elif '.z7' in url: filext='.z7'
		elif '.png' in url: filext='.png' #images
		elif '.jpg' in url: filext='.jpg'
		elif '.gif' in url: filext='.gif'
		elif '.mp4' in url: filext='.mp4' #Videos
		elif '.mpeg' in url: filext='.mpeg'
		elif '.avi' in url: filext='.avi'
		elif '.flv' in url: filext='.flv'
		elif '.wmv' in url: filext='.wmv'
		elif '.mp3' in url: filext='.mp3' #others
		elif '.txt' in url: filext='.txt'
		else: 							filext='.flv' #Default File Extention ('.flv')
	try: name=filename_filter_colorcodes(name)
	except: name=''
	try: name2=filename_filter_colorcodes(name2)
	except: name2=name
	try: show=filename_filter_colorcodes(show)
	except: show=name
	filname = name + filext
	dialog = xbmcgui.Dialog()
	if dialog.yesno('Local Path', 'Where would you like to download to?', '', filname, 'Shows', 'Movies'):
		localpath = getset('folder-movie')#__settings__.getSetting('folder-movie')
	else:
		localpath = getset('folder-show')#__settings__.getSetting('folder-show')
	if (debugging==True): print localpath
	#download_file(url,name,filname,localpath) ## For nightly builds 13.x+
	download_file_frodo(url,name,filname,localpath) ## For Frodo builds 12.x
	#

#def downloadfile(url,name):
#	import SimpleDownloader as downloader
#	downloader = downloader.SimpleDownloader()
#	url='http://www.xbmcswift.com/en/develop/api.html'
#	dlfold='/tmp'
#	#dlfold='F:\\xbmc\\theanimehighway\\'
#	params = { "url": url, "download_path": dlfold, "Title": name }
#	#params = { "url": url, "download_path": "F:\\xbmc\\theanimehighway\\", "Title": name, "live": "true", "duration": "20" }
#	filenm = name + ".txt"
#	#filenm = name + ".mp4"
#	notification('file download: ' + name, 'Downloading "' + url + '" to "' + filenm + '"')
#	downloader.download(filenm, params)

#def dialogboxyesno(txtMessage="",txtHeader="",txt3="",txt4=""):
#	dialog = xbmcgui.Dialog()
#	if dialog.yesno(txtHeader, txtMessage, txt3, txt4):

def dialogbox_ok(txtMessage="",txtHeader="",txt3="",txt4=""):
	dialog = xbmcgui.Dialog()
	ok = dialog.ok(txtHeader, txtMessage, txt3, txt4)
	#keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")

#import win64clipboard as wc
def copy_to_clipboard(msg):
		notification('Copy-to-Clipboard','Sorry this feature is not yet implimented.')
		#
		#
		#if sys.platform == 'win32':
		#	wc.OpenClipboard()
		#	wc.EmptyClipboard()
		#	wc.SetClipboardData(win32con.CF_TEXT, msg)
		#	wc.CloseClipboard()
		#
		#

def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
	if txtMessage=='None': txtMessage=''
	keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
	keyboard.doModal()
	if keyboard.isConfirmed():
		return keyboard.getText()
	else:
		return False # return ''

def checkForPartNo(url,partInfo=''):
	url=urllib.unquote_plus(url)
	if '_part_' in urllib.unquote_plus(url):
		try:
			matchaptn=re.compile('_part_(.+?).').findall(url)
			partInfo=' - Part # ' + matchaptn[0]
		except:
			partInfo=' - Part # ' + 'Unknown'
	elif '-part-' in urllib.unquote_plus(url):
		try:
			matchaptn=re.compile('-part-(.+?).').findall(url)
			partInfo=' - Part # ' + matchaptn[0]
		except:
			partInfo=' - Part # ' + 'Unknown'
	elif 'part' in urllib.unquote_plus(url):
		try:
			matchaptn=re.compile('part(.+?).').findall(url)
			partInfo=' - Part # ' + matchaptn[0]
		except:
			temp=''
	return partInfo



#########################################
def set_view(content='none',view_mode=50,do_sort=False):
	if (debugging==True): print 'view mode: ',view_mode
	if content=='none': test=''
	else: xbmcplugin.setContent(int(sys.argv[1]), content)
	#types:									# set_view()
	# 50		CommonRootView
	# 51		FullWidthList
	# 500		ThumbnailView
	# 501		PosterWrapView
	# 508		PosterWrapView2_Fanart
	# 505		WideIconView
	# 
	# 
	# 
	# 
	# 
	# set content type so library shows more views and info
	xbmc.executebuiltin("Container.SetViewMode(%s)" % view_mode)
	# set sort methods - probably we don't need all of them
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_NONE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_TITLE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_DATE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_GENRE)
	#
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_FILE)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_STUDIO)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_STUDIO_IGNORE_THE)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_PLAYLIST_ORDER)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_EPISODE)
	xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_DURATION)
	#xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_BITRATE)
	#
	if (do_sort == True):
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)#xbmcplugin.SORT_METHOD_LABEL
	#
	####xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TRACKNUM)
#	#SORT_METHOD_NONE, SORT_METHOD_UNSORTED, SORT_METHOD_VIDEO_TITLE,
#	#                        SORT_METHOD_TRACKNUM, SORT_METHOD_FILE, SORT_METHOD_TITLE
#	#                        SORT_METHOD_TITLE_IGNORE_THE, SORT_METHOD_LABEL
#	#                        SORT_METHOD_LABEL_IGNORE_THE, SORT_METHOD_VIDEO_SORT_TITLE,
#	#                        SORT_METHOD_VIDEO_SORT_TITLE_IGNORE_THE

#########################################
### from theanimehighway.py ###
#def showurl(name,url,scr=ICON0,imgfan=fanart0,type2=0,mode=0):
#	copy_to_clipboard(url)
#	if (debugging==True): print url, name, scr, imgfan
#	kmsg=showkeyboard(url, name)
def showurl(name,url,scr=ICON,imgfan=fanart,type2=0,mode=0):
	copy_to_clipboard(url)
	if (debugging==True): print url, name, scr, imgfan
	kmsg=showkeyboard(url, name)

#########################################
def metaArt_empty():
  saved_fans = cache.get('MetaArt_')
  fans = []
  cache.set('MetaArt_', str(fans))
  notification('[B][COLOR orange]Fanart[/COLOR][/B]','[B] Your Cached Fanart(s) Have Been Wiped Clean. Bye Bye.[/B]')
def emptyFavorites():
  saved_favs = cache.get('favourites_')
  favs = []
  cache.set('favourites_', str(favs))
  notification('[B][COLOR orange]Favorites[/COLOR][/B]','[B] Your Favorites Have Been Wiped Clean. Bye Bye.[/B]')
def addfavorite(name,url,scr=ICON0,imgfan=fanart0,tp2=0,mode=0):
    if (debugging==True): print name,url,scr,imgfan,tp2,mode
    saved_favs = cache.get('favourites_')
    favs = []
    if saved_favs:
        favs = eval(saved_favs)
        if favs:
            if (name,url,scr,imgfan,tp2,mode) in favs:
                notification('[B][COLOR orange]'+name.upper()+'[/COLOR][/B]','[B] Already in your Favorites[/B]')
                #xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+name.upper()+"[/COLOR][/B],[B] Already in your Favourites[/B],5000,"")")
                return
    favs.append((name,url,scr,imgfan,tp2,mode))
    cache.set('favourites_', str(favs))
    notification('[B][COLOR orange]'+name.upper()+'[/COLOR][/B]','[B] Added to Favorites[/B]')
    #xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+name.upper()+"[/COLOR][/B],[B] Added to Favourites[/B],5000,"")")
def removefavorite(name,url,scr=ICON0,imgfan=fanart0,tp2=0,mode=0):#,scr,imgfan
  if (debugging==True): print name,url,scr,imgfan,tp2,mode
  saved_favs = cache.get('favourites_')
  if saved_favs:
    favs = eval(saved_favs)
    if (name,url,scr,imgfan,tp2,mode) in favs:
    	favs.remove((name,url,scr,imgfan,tp2,mode))
    	cache.set('favourites_', str(favs))
    	notification('[B][COLOR orange]'+name.upper()+'[/COLOR][/B]','[B] Removed from Favorites[/B]')
    	if (debugging==True): print name+' Removed from Favorites'
    	#set_view('tvshows',int(getset('viewmode-favs')),True)
    	#VaddDir('[COLOR maroon] Visit with [COLOR tan]Highway[/COLOR] and others @ [COLOR white]#XBMCHUB[/COLOR] on [COLOR white]irc.freenode.net[/COLOR]:6667 [/COLOR]', '', 0, ICON, fanart, False)
    	#LastPage=page_last_update()
    	#xbmc.executebuiltin("XBMC.Container.Update(%s)" % (LastPage))
    	xbmc.executebuiltin("XBMC.Container.Refresh")
    	#VaddDir('[COLOR maroon] Visit with [COLOR tan]Highway[/COLOR] and others @ [COLOR white]#XBMCHUB[/COLOR] on [COLOR white]irc.freenode.net[/COLOR]:6667 [/COLOR]', '', 0, ICON, fanart, False)
    	##xbmc.Container.Refresh
    	#xbmc.sleep(4000)
    else:
    	notification('[B][COLOR orange]'+name.upper()+'[/COLOR][/B]','[B] not found in your Favorites[/B]')
    #xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+name.upper()+"[/COLOR][/B],[B] Removed from Favourites[/B],5000,"")")
def metaArt_add(show_name,show_title_thetvdb,show_id,url_thetvdb,show_fanart,show_poster,show_bannner,show_desc,show_genres,show_status,show_language,show_network,show_rating):#metaArt_add(match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner)
	##if (debugging==True): print name,url,scr,imgfan,tp2,mode
	saved_fans = cache.get('MetaArt_')
	fans = []
	if saved_fans:
		fans = eval(saved_fans)
		if fans:
			if (show_name,show_id,url_thetvdb,show_fanart,show_poster,show_bannner,show_desc) in fans:
				#notification('[B][COLOR orange]'+show_name.upper()+'[/COLOR][/B]','[B] Already in your Cached Fanart(s).[/B]')
				return
	fans.append((show_name,show_title_thetvdb,show_id,url_thetvdb,show_fanart,show_poster,show_bannner,show_desc,show_genres,show_status,show_language,show_network,show_rating))
	cache.set('MetaArt_', str(fans))
	#notification('[B][COLOR orange]'+show_name.upper()+'[/COLOR][/B]','[B] Added to MetaArt[/B]')
	##xbmc.executebuiltin("XBMC.Notification([B][COLOR orange]"+name.upper()+"[/COLOR][/B],[B] Added to Favourites[/B],5000,"")")
#########################################
def getAlphaFolder(alphaTxt='',typeTxt='',slashTxt=''):
	if type2==5: return 'subanime/'
	#elif mode==211: return 'alpha-anime/'
	#elif mode==311: return 'alpha-movies/'
	else: return alphaTxt+typeTxt+slashTxt
def getAlphaEnd(typeTxt='',alphaTxt=''):
	if   (type2==5) and (typeTxt=='anime'):  return '-2'
	elif (type2==5) and (typeTxt=='movies'): return '-3'
	else: return alphaTxt
def showlistdir(vLetterA,vLetterB,vImageC):#SitePrefixes#SiteSufixes
	addFolder('[COLOR ' + MyColors[1] + ']' + vLetterB + '[/COLOR]','shows',getAlphaFolder('alpha-','anime','/') + vLetterA + getAlphaEnd('anime') + SiteSufixes[type2],type2,6,'Glossy_Black\\' + vImageC + '.png')
def movielistdir(vLetterA,vLetterB,vImageC):
	addFolder('[COLOR ' + MyColors[1] + ']' + vLetterB + '[/COLOR]','movies',getAlphaFolder('alpha-','movies','/') + vLetterA + getAlphaEnd('movies') + SiteSufixes[type2],type2,6,'Glossy_Black\\' + vImageC + '.png')



#########################################
def clean_filename(filename):
    # filename = _1CH.unescape(filename)
    return re.sub('[/:"*?<>|]+', ' ', filename)

def ParseDescription(plot): ## Cleans up the dumb number stuff thats ugly.
	if ('&#' in plot) and (';' in plot):
		if ("&#8211;" in plot): plot=plot.replace("&#8211;",";") #unknown
		if ("&#8216;" in plot): plot=plot.replace("&#8216;","'")
		if ("&#8217;" in plot): plot=plot.replace("&#8217;","'")
		if ("&#8220;" in plot): plot=plot.replace('&#8220;','"')
		if ("&#8221;" in plot): plot=plot.replace('&#8221;','"')
		if ("&#215;"  in plot): plot=plot.replace('&#215;','x')
		if ('&#' in plot) and (';' in plot): plot=unescape_(plot)
	return plot
def unescape_(s):
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()

def check_ifUrl_isHTML(pathUrl): ## Doesn't work yet. Needs Fixed.
	######## 'http://s12.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4'
	##timeout=10
	##socket.setdefaulttimeout(timeout) # timeout in seconds
	if (debugging==True): print 'TestingUrl: '+pathUrl
	try:
		req=urllib2.Request(pathUrl)#,timeout=6)
		tUrl=urllib2.urlopen(req)
		return True
	except:
		return False


#########################################

def visited_DoCheck(urlToCheck,s='[B][COLOR yellowgreen]@[/COLOR][/B] ',e='[COLOR black]@[/COLOR] '):
	#visited_empty()
	#return ''
	vc=visited_check(urlToCheck)
	if (vc==True): return s
	else: 
		##visited_add(urlToCheck)
		return e

def visited_check(urlToCheck):
  try: saved_visits = cache.get('visited_')
  except: return False
  erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_visits: return False #xbmc.executebuiltin(erNoFavs)
  if saved_visits == '[]': return False #xbmc.executebuiltin(erNoFavs)
  if saved_visits:
  	visits = eval(saved_visits)
  	if (urlToCheck in visits): return True
  return False

def visited_empty():
  saved_favs = cache.get('visited_')
  favs = []
  cache.set('visited_', str(favs))
  notification('[B][COLOR orange]Visited[/COLOR][/B]','[B] Your Visited Data has been wiped clean. Bye Bye.[/B]')

def visited_add(urlToAdd):
	if (urlToAdd==''): return ''
	elif (urlToAdd==None): return ''
	if (debugging==True): print 'checking rather url has been visited: ' + urlToAdd
	saved_visits = cache.get('visited_')
	visits = []
	if saved_visits:
		#if (debugging==True): print 'saved visits: ',saved_visits
		visits = eval(saved_visits)
		if visits:
			if (urlToAdd) in visits: return
	visits.append((urlToAdd))
	cache.set('visited_', str(visits))

def qp_get(n): ## Deals with errors in using None type within a urllib.quote_plus().
	#print n
	if (n==''): return ''
	elif (n==None): return ''
	else: return urllib.quote_plus(n)
def st_get(n): ## Deals with errors in using None type within a str().
	#print n
	if (n==None): return ''
	else: return str(n)

def page_last_get(defaultLastPage=sys.argv[0]+'?mode=0'):
  try: last_visited = cache.get('lastpage')
  except: return defaultLastPage
  erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not last_visited: return defaultLastPage
  if last_visited == '[]': return defaultLastPage
  if last_visited == '': return defaultLastPage
  if last_visited:
  	return eval(last_visited)
  return defaultLastPage

def page_last_update(defaultLastPage=sys.argv[0]+sys.argv[2]):
	cache.set('lastpage', defaultLastPage)


#########################################



#########################################



#########################################



#########################################








#notification('Current Site',mainSite)
#########################################
