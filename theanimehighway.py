import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,sys
import string,StringIO,logging,urlresolver,random
import videolinks
from videolinks import vvVIDEOLINKS
from videolinks import *
try:
    import json
except ImportError:
    import simplejson as json
#import map
import array

#The Anime Highway - by The Highway 2013.
#version 0.0.2d

__settings__   	= xbmcaddon.Addon(id='plugin.video.theanimehighway')
__home__ = __settings__.getAddonInfo('path')

##__home__ = 'special://home/addons/plugin.video.theanimehighway/art'
#special://home/addons/plugin.video.theanimehighway/art
#addonPath=os.getcwd()
addonPath=__home__
artPath=addonPath+'/art/'
#icon = xbmc.translatePath( os.path.join( __home__, 'icon.png' ) )
__plugin__ = "The Anime Highway"
__authors__ = "The Highway"
__credits__ = "o9r1sh of plugin.video.gogoanime for Videoweed and Video44 source parsing. TheHighway(Myself) for AnimeGet plugin (simular site)"
#home = xbmc.translatePath(addon.getAddonInfo('path'))

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
params=get_params()
url=None
name=None
name2=None
type2=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name2=urllib.unquote_plus(params["nm"])
except:
        pass
try:
        type2=int(params["tp"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Name2: "+str(name2)
print "Type2: "+str(type2)
#########################################

#ICON = os.path.join(__home__, 'iconA44.png')
ICON4 = os.path.join(__home__, 'icongd.png')
ICON3 = os.path.join(__home__, 'iconAPlus.png')
ICON2 = os.path.join(__home__, 'iconA44.png')
ICON1 = os.path.join(__home__, 'iconAG.png')
ICON0 = os.path.join(__home__, 'icon.png')
#fanart = os.path.join(__home__, 'fanartA44.jpg')
fanart4 = os.path.join(__home__, 'fanartgd.jpg')
fanart3 = os.path.join(__home__, 'fanartAPlus.jpg')
fanart2 = os.path.join(__home__, 'fanartA44.jpg')
fanart1 = os.path.join(__home__, 'fanartAG.jpg')
fanart0 = os.path.join(__home__, 'fanart.jpg')


if type2==4:		#site 4
	fanart = os.path.join(__home__, 'fanart.jpg')#have not grabbed a graphic for this yet.
	ICON = os.path.join(__home__, 'icon.png')#have not grabbed a graphic for this yet.
	mainSite='http://www.gooddrama.net/'
elif type2==3:		#site 3
	fanart = os.path.join(__home__, 'fanartplus.jpg')
	ICON = os.path.join(__home__, 'iconplus.png')
	mainSite='http://www.animeplus.tv/'
elif type2==2:		#site 2
	fanart = os.path.join(__home__, 'fanartA44.jpg')
	ICON = os.path.join(__home__, 'iconA44.png')
	mainSite='http://www.anime44.com/'
else:						#site 1
	fanart = os.path.join(__home__, 'fanartAG.jpg')
	ICON = os.path.join(__home__, 'iconAG.png')
	mainSite='http://www.animeget.com/'

Sites=['animeget.com','anime44.com','animeplus.tv','gooddrama.net']

#############################

MyAlphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyColors=['red','blue','darkblue','grey']
MyBrowser=['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']

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
##Example##VaddDir('[COLOR blue]' + text[0] + '[/COLOR]', '', 0, '', False)
def VaddDir(name, url, mode, iconimage, fanimage, is_folder=False):#VANILLA ADDDIR (kept for reference)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_folder)
        return ok

#############################

def menu0():#Main Menu
				VaddDir('                          [B][COLOR purple]--  The  Anime  Highway  --[/COLOR][/B]', '', 1, ICON0, fanart0, False)
				VaddDir('[COLOR grey] Please select a site:[/COLOR]', '', 1, ICON0, fanart0, False)
				addDir('[COLOR ' + MyColors[1] + '][COLOR white]Anime[/COLOR]Get[/COLOR]','Site 1 - AnimeGet','ag',1,1,ICON1,fanart1)
				addDir('[COLOR ' + MyColors[0] + '][COLOR white]Anime[/COLOR]44 [/COLOR]','Site 2 - Anime44','a44',2,1,ICON2,fanart2)
				addDir('[COLOR ' + MyColors[2] + '][COLOR white]Anime[/COLOR]Plus [/COLOR]','Site 3 - AnimePlus','aplus',3,1,ICON3,fanart3)
				addDir('[COLOR ' + MyColors[3] + ']Good[COLOR white]Drama[/COLOR] [/COLOR]','Site 4 - GoodDrama','gd',4,1,ICON4,fanart4)
def menu1():#Main Menu
        if type2==4:#gooddrama
        	addFolder('[COLOR ' + MyColors[0] + ']Drama Movies[/COLOR]','Movies','drama-movies',type2,3,'movies.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Drama Series[/COLOR]','List','drama-shows',type2,2,'full.png')
        elif type2==1 or type2==3:#animeget & animeplus
        	addFolder('[COLOR ' + MyColors[0] + ']Anime Movies[/COLOR]','Movies','anime-movies',type2,3,'movies.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime Series[/COLOR]','List','anime-shows',type2,2,'full.png')
        else:
        	addFolder('[COLOR ' + MyColors[0] + ']Anime Movies[/COLOR]','Movies','category/anime-movies',type2,601,'movies.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Anime Series[/COLOR]','List','anime-list',type2,2,'full.png')
        if type2==1 or type2==2:#animeget & anime44
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing Series[/COLOR]','List','ongoing-anime',type2,6,'plus.png')
        #addDir('Latest Episodes','List',mainSite + 'anime-updates',0,7,artPath + 'full.png',fanart)
        if type2==1:
        	addDir('[COLOR ' + MyColors[1] + ']New Series[/COLOR]','List',mainSite + 'new-anime',type2,6,artPath + 'gogoanime\\newseries.png',fanart)
        	addDir('[COLOR ' + MyColors[2] + ']Suprise Me[/COLOR]','List',mainSite + 'surprise',type2,4,artPath + 'surpriseme1.jpg',fanart)
        #addDir('Search','List',mainSite + 'new-anime',0,8,artPath + 'full.png',fanart)
def menu2():#series
        if type2==4:#gooddrama
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','drama-shows',type2,201,'full.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','drama-show-genres',type2,211,'Glossy_Black\\genres.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-shows',type2,6,'plus.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-shows',type2,6,'BLANK.png')
        elif type2==1 or type2==3:#animeget & animeplus
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','anime-shows',type2,201,'full.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','anime-show-genres',type2,211,'Glossy_Black\\genres.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-shows',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-shows',type2,6,'plus.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-shows',type2,6,'BLANK.png')
        else:
        	addFolder('[COLOR ' + MyColors[1] + ']Index[/COLOR]','List','anime-list',type2,201,'full.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Genre[/COLOR]','List','anime-genres',type2,211,'Glossy_Black\\genres.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Popular[/COLOR]','List','popular-anime',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']New[/COLOR]','List','new-anime',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Recent[/COLOR]','List','recent-anime',type2,6,'BLANK.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Ongoing[/COLOR]','List','ongoing-anime',type2,6,'plus.png')
        	addFolder('[COLOR ' + MyColors[1] + ']Completed[/COLOR]','List','completed-anime',type2,6,'BLANK.png')

def menu3():#movies
        if type2==1:
        	addFolder('Index','List','anime-movies',type2,301,'movies.png')
        else:
        	addFolder('Index','List','category/anime-movies',type2,301,'movies.png')
        addFolder('Genre','List','anime-movie-genres',type2,311,'Glossy_Black\\genres.png')
        addFolder('Popular','List','popular-movies',type2,6,'BLANK.png')
        addFolder('New','List','new-movies',type2,6,'BLANK.png')
        addFolder('Recent','List','recent-movies',type2,6,'BLANK.png')
def menu201():#Series by A-Z
	showlistdir('others','#','123')
	for ii in MyAlphabet[:]:
		showlistdir(ii,ii,ii)
def menu301():#Movies by A-Z (if option is available)
	movielistdir('others','#','123')
	for ii in MyAlphabet[:]:
		movielistdir(ii,ii,ii)
def menu211(url):#List Available Genres for series
	genrelist(url,211)
def menu311(url):#List Available Genres for movies
	genrelist(url,311)
def showlistdir(vLetterA,vLetterB,vImageC):
	addFolder('[COLOR ' + MyColors[1] + ']' + vLetterB + '[/COLOR]','shows','alpha-anime/' + vLetterA,type2,6,'Glossy_Black\\' + vImageC + '.png')
def movielistdir(vLetterA,vLetterB,vImageC):
	addFolder('[COLOR ' + MyColors[1] + ']' + vLetterB + '[/COLOR]','movies','alpha-movies/' + vLetterA,type2,6,'Glossy_Black\\' + vImageC + '.png')
def genrelist(url,modeA):#Get list of Available Genres from Site
        link=getURL(url)
        match=re.compile('<tr>\s+<td>\s+<a href="(.+?)">(.+?)</a>\s+</td>\s+<td>(.+?)</td>\s+</tr>').findall(link)
        for url2,name,shocount in match:
                addDir(name + ' - (' + shocount + ')',name,url2,type2,6,ICON,fanart)
def showlistnames(url,modeA):
        link=getURL(url)
        match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
        for url2,name in match:
                addDir(name,name,url2,type2,5,ICON,fanart)
        matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        for url3 in matchb:
                addDir('Next','list',url3,type2,modeA,artPath + 'gogoanime\\next.png',fanart)
def showlist(url,modeA):
        link=getURL(url)
        match=re.compile('<a href="(.+?)"><img src="(.+?)" width="120" height="168" alt="Watch (.+?) online"').findall(link)
        for url2,img2,name in match:
                addDir(name,name,url2,type2,4,img2,fanart)
        matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        for url3 in matchb:
                addDir('Next','list',url3,type2,modeA,artPath + 'gogoanime\\next.png',fanart)
def EPISODESlist(url):
        link=getURL(url)
        img3=''
        matcha=re.compile('<img src="(.+?)" id="series_image" width="250" height="370" alt="').findall(link)
        for img2 in matcha:
          img3=img2
        if type2==1 or Sites[0] in url or type2==3 or Sites[2] in url or type2==4 or Sites[3] in url:#animeget, animeplus, gooddrama
        	match=re.compile('<li>\s+<a href="(.+?)">(.+?)</a>\s+<span class="right_text">(.+?)</span>').findall(link)
        	for url2,name,dateadded in match:
        		addDir(name + ' - (' + dateadded + ')',name,url2,type2,5,img3,fanart)
        else:#type2==2 or Sites[1]#anime44
        	match=re.compile('<li>\s+<a href="(.+?)"\>(.+?)</a>').findall(link)
        	for url2,name in match:
        		addDir(name,name,url2,type2,5,img3,fanart)
        #matchb=re.compile('<li><a href="(.+?)">Next</a></li>').findall(link)
        #for url3 in matchb:
        #        addDir('Next','movies',url3,0,302,artPath + 'gogoanime\\next.png',fanart)

def VIDEOsource(url,name):
				vvVIDEOLINKS(url,name)

#########################################





def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,name2,url,type2,mode,iconimage,fanimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&nm="+urllib.quote_plus(name2)+"&tp="+str(type2)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
if mode==None or url==None or len(url)<1:
        print ""
        menu0()
elif mode==1:
        print ""+url
        menu1()
elif mode==2:
        print ""+url
        menu2()
elif mode==201:
        print ""+url
        menu201()
#elif mode==202:
#        print ""+url
#        CATEGORIESlistab(url)
elif mode==211:
        print ""+url
        menu211(url)
elif mode==3:
        print ""+url
        menu3()
elif mode==301:
        print ""+url
        menu301()
#elif mode==302:
#        print ""+url
#        CATEGORIESmoviesab(url)
elif mode==311:
        print ""+url
        menu311(url)
elif mode==4:
        print ""+url
        EPISODESlist(url)
elif mode==5:
        print ""+url
        VIDEOsource(url,name)
elif mode==6:
        print ""+url
        showlist(url,mode)
elif mode==601:
        print ""+url
        showlistnames(url,mode)
#elif mode==16:
#        print ""+url
#        VIDEOLINKStrailers(url,name,name2,type2)




xbmcplugin.endOfDirectory(int(sys.argv[1]))
