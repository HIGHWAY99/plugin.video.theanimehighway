import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,sys
import string,StringIO,logging,urlresolver,random
try:
    import json
except ImportError:
    import simplejson as json

__settings__ 		= xbmcaddon.Addon(id='plugin.video.theanimehighway')
__home__ = __settings__.getAddonInfo('path')
addonPath=__home__
artPath=addonPath+'/art/'
ICON = os.path.join(__home__, 'icon.jpg')
fanart = os.path.join(__home__, 'fanart.jpg')

#############################

MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
MySourcesV=	['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com']
MyIconsV=		[artPath + 'videoweed.jpg',	artPath + 'video44a.png',	artPath + 'novamov.jpg',	artPath + 'dailymotion.jpg',	artPath + 'videofun.png',	artPath + 'yourupload.jpg',	artPath + 'googlevideo.gif']#BLANK.png
MyNamesV=		['VideoWeed',			'Video44',			'NovaMov',			'DailyMotion',			'VideoFun',			'YourUpload',			'Google Video']
MyColorsV=	['lime',					'red',					'silver',				'green',						'cyan',					'grey',					'blue']

def addFolder(name,name2,url,type2,mode,iconimage):
		##addDir(name,name2,url,type2,mode,iconimage,fanimage)
		addDir(name,name2,mainSite + url,type2,mode,artPath + iconimage,fanart)
def getURL(url):
		req = urllib2.Request(url)
		req.add_header(MyBrowser[0], MyBrowser[1]) 
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return(link)

#############################

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
def addDirV(name,name2,url,type2,mode,iconimage,fanimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def VaddDir(name, url, mode, iconimage, fanimage, is_folder=False):#VANILLA ADDDIR (kept for reference)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_folder)
        return ok

###########################################

def vvVIDEOLINKS(url,name):
        urlA=url
        link=getURL(url)
        match=re.compile('src="(.+?)"').findall(link)
        print match
        for url in match:#MySourcesV[] MyNamesV[] MyColorsV[]
                tt=0
                if MySourcesV[tt] in url:#videoweed
                        link=getURL(url)
                        match=re.compile('flashvars.advURL="(.+?)"').findall(link)
                        try:
                                addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urlresolver.resolve(match[0]),MyIconsV[tt])
                        except:
                                VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart, False)
                                continue
                tt=1
                if MySourcesV[tt] in url:#video44#no-screenshot
                				link=getURL(url)
                				match=re.compile(' file: "(.+?)"').findall(link)
				                addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',match[0],MyIconsV[tt])
                tt=2
                if MySourcesV[tt] in url:#novamov#no-screenshot
                        try:
                        	addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',match[0],MyIconsV[tt])
                        except:
                        	try:
                        		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',urlresolver.resolve(match[0]),MyIconsV[tt])
                        	except:
                        		VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart, False)
                        		continue
                        	continue
                tt=3
                if MySourcesV[tt] in url:#dailymotion
                        try:
                                addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urlresolver.resolve(match[0]),MyIconsV[tt])
                        except:
                                VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart, False)
                                continue
                tt=4
                if MySourcesV[tt] in url:#videofun.me
                        try:
                                addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urlresolver.resolve(match[0]),MyIconsV[tt])
                        except:#failed at initial link
                                linka=getURL(url)
                                matcha=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+true').findall(linka)#Screenshot
                                try:
                                	linkb=getURL(matcha[0])
                                	matchb=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+false').findall(linka)#Video
                                	print ""+matcha[0]
                                	print ""+matchb[0]
                                	try:
                                		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',urllib.unquote_plus(matchb[0]),matcha[0])
                                	except:#failed @ og:video
                                		try:
                                			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*3[/COLOR]',unquote_plus(matchb[0]),matcha[0])
                                		except:#failed @ logo.link
                                			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @ unqouting[/COLOR]', '', 1, MyIconsV[tt], matcha[0], False)
                                			continue
                                except:
                                	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart, False)
                                	continue
                                continue
                tt=5
                if MySourcesV[tt] in url:#yourupload
                        try:
                                addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urlresolver.resolve(match[0]),MyIconsV[tt])
                        except:#failed at initial link
                                linka=getURL(url)
                                matcha=re.compile('<meta property="og:image" content="(.+?)"').findall(linka)
                                try:
                                	linkb=getURL(matcha[0])
                                	matchb=re.compile('<meta property="og:video" content="(.+?)"').findall(linka)
                                	print ""+matcha[0]
                                	print ""+matchb[0]
                                	try:
                                		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Might take a moment once clicked[/COLOR]',matchb[0],matcha[0])
                                	except:#failed @ og:video
                                		matchc=re.compile('&logo.link=(.+?)&logo.linktarget').findall(linka)
                                		#print "" + unquote_plus(matchc[0])
                                		try:
                                			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Maybe in my DREAMS[/COLOR]',unquote_plus(matchc[0]),matcha[0])
                                		except:#failed @ logo.link
                                			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  logo.link[/COLOR]', '', 1, MyIconsV[tt], matcha[0], False)
                                			continue
                                except:
                                	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart, False)
                                	continue
                                continue
                tt=6
                if MySourcesV[tt] in url:#google video
                        try:
                        	addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',match[0],MyIconsV[tt])
                        except:
                        	try:
                        		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',urlresolver.resolve(match[0]),MyIconsV[tt])
                        	except:
                        		VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart, False)
                        		continue
                        	continue



        xbmcplugin.endOfDirectory(int(sys.argv[1]))
                       
