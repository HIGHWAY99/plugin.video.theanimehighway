import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,sys
import string,StringIO,logging,urlresolver,random
try:
    import json
except ImportError:
    import simplejson as json

#import SimpleDownloader as downloader

__settings__ 		= xbmcaddon.Addon(id='plugin.video.theanimehighway')
__home__ = __settings__.getAddonInfo('path')
addonPath=__home__
artPath=addonPath+'/art/'
ICON = os.path.join(__home__, 'icon.jpg')
fanart = os.path.join(__home__, 'fanart.jpg')

#############################

Sites=['animeget.com','anime44.com','animeplus.tv','gooddrama.net']
MyVideoLinkSrcMatches=['src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkSrcMatchesB=['src="(.+?)"',			'<embed.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkBrackets=['<iframe.+?src="(.+?)"', '<embed.+?src="(.+?)"']
MyAlphabet=	['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=	['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
MySourcesV=	['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com'	,'vidzur.com']
#MySourcesV=	['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com'	,'vidzur.com',	'MP4UPLOAD'		,'AUENGINE'		'UploadC']
MyIconsV=		[artPath + 'videoweed.jpg',	artPath + 'video44a.png',	artPath + 'novamov.jpg',	artPath + 'dailymotion.jpg',	artPath + 'videofun.png',	artPath + 'yourupload.jpg',	artPath + 'googlevideo.gif', artPath + 'vidzur.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png', artPath + 'BLANK.png']#BLANK.png
MyNamesV=		['VideoWeed',			'Video44',			'NovaMov',			'DailyMotion',			'VideoFun',			'YourUpload',			'Google Video'			,'VidZur',			'MP4Upload'		,'AUEngine',		'UploadC']
MyColorsV=	['lime',					'red',					'silver',				'green',						'cyan',					'grey',					'blue',					'orange',					'white',					'white',					'white',					'white']

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

def download_file(url='',name='temp',localfilename='temp',localpath=artPath,filext='.flv'):
		#url='https://github.com/HIGHWAY99/plugin.video.theanimehighway/archive/master.zip'
		#localfilename='plugin.video.theanimehighway.zip'
		#localpath=__home__
		#
		localfilewithpath=os.path.join(localpath,localfilename)
		print 'Attempting to download "' + localfilename + '" to "' + localfilewithpath + '" from: ' + url
		#dialogbox('To: ' + localfilewithpath,'Download File: ' + localfilename,'From: ' + url,'[COLOR red]This is still being tested.[/COLOR]')
		#
		dialog = xbmcgui.Dialog()
		if dialog.yesno('Download File', 'Do you wish to download this file?','File: ' + localfilename,'To: ' + localpath):
			#if os.path.isfile(localfilewithpath):
			#	notification('Download File','File Already Exists.[CR]file: ' + localfilename + '[CR]local: ' + localpath,5000)
			#else:
			notification('Attempting to Download File',localfilename + '[CR] This function is still being tested.')#This function may never happen.
			dp = xbmcgui.DialogProgress()
			dp.create('Downloading', '', localfilename)
			urllib.urlretrieve(url, localfilewithpath)
			notification('Download File','Download Complete.[CR] ' + localfilename,15000)
			dialogbox_ok('File Size: ' + str(os.path.getsize(localfilewithpath)) + ' (bytes)','Download Complete','Note:','Make sure the size seems right.')
			#total_size += os.path.getsize(fp)
		#
		#
		#notification('Download File','Sorry this feature is not yet implimented.')#This function may never happen.

def download_file_prep(url,name='none',name2='none',show='none',filext='none'):
	#
	if filext=='none':
		if   '.zip' in url:#Compressed Files
			filext='.zip'
		elif '.rar' in url:
			filext='.rar'
		elif '.z7' in url:
			filext='.z7'
		elif '.png' in url:#images
			filext='.png'
		elif '.jpg' in url:
			filext='.jpg'
		elif '.gif' in url:
			filext='.gif'
		elif '.mp4' in url:#Videos
			filext='.mp4'
		elif '.mpeg' in url:
			filext='.mpeg'
		elif '.avi' in url:
			filext='.avi'
		elif '.flv' in url:
			filext='.flv'
		elif '.mp3' in url:#others
			filext='.mp3'
		elif '.txt' in url:
			filext='.txt'
		else:							 #Default File Extention ('.flv')
			filext='.flv'
	filname = name + filext
	dialog = xbmcgui.Dialog()
	if dialog.yesno('Local Path', 'Where would you like to download to?', '', filname, 'Shows', 'Movies'):
		localpath = getset('folder-movie')#__settings__.getSetting('folder-movie')
	else:
		localpath = getset('folder-show')#__settings__.getSetting('folder-show')
	print localpath
	download_file(url,name,filname,localpath)
	#

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
	keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
	keyboard.doModal()
	if keyboard.isConfirmed():
		return keyboard.getText()
	else:
		return ''

def notification(header="", message="", sleep=5000 ):
	xbmc.executebuiltin( "XBMC.Notification(%s,%s,%i)" % ( header, message, sleep ) )
	#notify(msg=message, title=header, delay=sleep, image=ICON)
	#notify(msg=message, title='[COLOR green][B]'+header+'[/B][/COLOR]', delay=sleep, image=ICON0)

#def addfav(header="", message="", sleep=5000 ):
#	notify(msg=message, title=header, delay=sleep, image=ICON0)

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


def getset(idSetting):#,defaultValue=''):#Addon.getSetting('idNameOfSetting')
	return __settings__.getSetting(idSetting)#==defaultValue

def getsetbool(idSetting):#Addon.getSetting('idNameOfSetting') #Method seems to be an utter failure for BOOL(true/false)'s
	#print __settings__.getSetting(idSetting) == 'true'
	return __settings__.getSetting(idSetting) == 'true'

def addLink(name,url,iconimage,fanimage=fanart,shoname='none',downloadable=True):
        ok=True
        if shoname=='none':
        	try: shoname=show
        	except: pass
        if fanimage==fanart:
        	try: fanimage=imgfan
        	except: pass
        if iconimage in MyIconsV:
        	try:
        		iconimage=scr
        	except: pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": shoname } )
        liz.setProperty( "Fanart_Image", fanimage )
        contextMenuItems = []
        #print getset('enable-showurl')
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
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)#True#liz.addContextMenuItems(contextMenuItems)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_folder)
        return ok
###########################################
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

def vvVIDEOLINKS(mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):#vvVIDEOLINKS(mainurl,name,name2,scr,imgfan,show,type2,mode)
	urlA=mainurl
	link=getURL(mainurl)
	ListOfUrls=[]
	for VidLinkBrackets in MyVideoLinkBrackets:
		match=[]
		match=re.compile(VidLinkBrackets).findall(link)
		print 'Bracket Matches:',match
		ListOfUrls = ListOfUrls,match
		for url in match:
			vvVIDEOLINKS_doChecks(url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	print 'list of urls:',ListOfUrls
	vvVIDEOLINKS_doChecks_others(ListOfUrls,0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)

def vvVIDEOLINKS_doChecks(url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	vvVIDEOLINKS_doChecks_videofun(4,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_dailymotion(3,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videoweed(0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_video44(1,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_novamov(2,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_yourupload(5,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_googlevideo(6,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidzur(7,url,mainurl,name,name2,scr,imgfan,show,type2,mode)

def vvVIDEOLINKS_doChecks_video44(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#video44#no-screenshot
		try:
			link=getURL(url)
			matcha=re.compile('file:\s+"(.+?)"').findall(link)
			partInfo=checkForPartNo(matcha[0])
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + partInfo,urllib.unquote_plus(matcha[0]),scr,imgfan,show)
		except:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(url),scr,imgfan,imgfan,show)

def vvVIDEOLINKS_doChecks_videofun(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videofun.me
		#print 'A Link ( ' + MySourcesV[tt] + ' ) was found: ' + url
		try:
			linka=getURL(url)
			if 'Error 404 - Not Found' not in linka:
				matcha=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+true').findall(linka)#Screenshot
				linkb=getURL(matcha[0])
				matchb=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+false').findall(linka)#Video
				partInfo=checkForPartNo(matchb[0])
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]' + partInfo,urllib.unquote_plus(matchb[0]),matcha[0],imgfan,show)
				except:
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',matchb[0],matcha[0],imgfan,show)
					except:
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		except:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Possible 404 Not Found.[/COLOR]', '', 1, MyIconsV[tt], imgfan)

def vvVIDEOLINKS_doChecks_dailymotion(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#dailymotion ( Play: yes , Download: no )
		try:
			matcha=re.compile('http://www.dailymotion.com/swf/(.+?)&').findall(url)
			linka='http://www.dailymotion.com/video/' + matcha[0]
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*1a[/COLOR]',url,MyIconsV[tt],imgfan,show)
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*1b[/COLOR]',linka,MyIconsV[tt],imgfan,show)
			linkb=getURL(linka)
			matchb=re.compile('var flashvars = {"(.*?)"};').findall(linkb)
			datab=urllib.unquote_plus(matchb[0])##print datab
			vid_titlea=urllib.unquote_plus(re.compile('"title":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_title=urllib.unquote_plus(re.compile('"videoTitle":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_id=urllib.unquote_plus(re.compile('"videoId":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_desc=urllib.unquote_plus(re.compile('"videoDescription":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_screenshot=urllib.unquote_plus(re.compile('"videoPreviewURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_videoauthor=urllib.unquote_plus(re.compile('"videoOwnerLogin":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_lang=urllib.unquote_plus(re.compile('"videoLang":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_whenUploaded=urllib.unquote_plus(re.compile('"videoUploadDateTime":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_url=urllib.unquote_plus(re.compile('"video_url":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_autoURL=urllib.unquote_plus(re.compile('"autoURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_ldURL=urllib.unquote_plus(re.compile('"ldURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_sdURL=urllib.unquote_plus(re.compile('"sdURL":"(.*?)"').findall(datab)[0]).replace('\/','/')
			vid_visual_science_video_view=urllib.unquote_plus(re.compile('"visual_science_video_view":"(.*?)"').findall(datab)[0]).replace('\/','/')
			#print 'DailyMotion:',vid_url,vid_autoURL,vid_ldURL,vid_sdURL,vid_screenshot,vid_title
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (Url) [COLOR grey][/COLOR]',vid_url,vid_screenshot,imgfan,vid_title)
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (AutoUrl) [COLOR grey][/COLOR]',vid_autoURL,vid_screenshot,imgfan,vid_title)# doesn't seem to work atm #
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (LD) [COLOR grey][/COLOR]',vid_ldURL,vid_screenshot,imgfan,vid_title)
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - (SD) [COLOR grey][/COLOR]',vid_sdURL,vid_screenshot,imgfan,vid_title)
		except:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_videoweed(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videoweed#no-screenshot###Needs worked on, wont show video.
		#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)
		try:
			link=getURL(url)
			matcha=re.compile('flashvars.advURL="(.+?)"').findall(link)
			partInfo=checkForPartNo(matcha[0])
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR] ' + partInfo,urlresolver.resolve(matcha[0]),scr,imgfan,show)
		except:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_novamov(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#novamov#no-screenshot
		matcha=url.split('&http:')
		matcha[1]='http:'+matcha[1]
		matchb=url.split('&v=')
		matcha[0]=matcha[0]+'&v='+matchb[1]
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',urlresolver.resolve('http://www.novamov.com/video/' + matchb[1]),scr,imgfan,show)#(N/A) NovaMov Page
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) Combined Link[/COLOR]',urlresolver.resolve(url),scr,imgfan,show)
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) 718x420[/COLOR]',urlresolver.resolve(matcha[0]),scr,imgfan,show)
			#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) 600x480[/COLOR]',urlresolver.resolve(matcha[1]),scr,imgfan,show)
			#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', url, 1, MyIconsV[tt], fanart)
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',urlresolver.resolve(url),scr,imgfan,show)#MyIconsV[tt])
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_yourupload(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#yourupload
		try:
			linka=getURL(url)
			matcha=re.compile('&image=(.+?)&logo.file').findall(linka)
			matchb=re.compile('flashvars="id=.+?&file=(.+?)&image').findall(linka)
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(matchb[0]),urllib.unquote_plus(matcha[0]),imgfan,show)#MyIconsV[tt])
		except:#failed at initial link
			try:
				linkb=getURL(matcha[0])
				matcha=re.compile('<meta property="og:image" content="(.+?)"').findall(linka)
				matchb=re.compile('<meta property="og:video" content="(.+?)"').findall(linka)
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2 Might be slow loading.[/COLOR]',matchb[0],matcha[0],imgfan,show)
				except:#failed @ og:video
					matchc=re.compile('&logo.link=(.+?)&logo.linktarget').findall(linka)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*3[/COLOR]',unquote_plus(matchc[0]),matcha[0],imgfan,show)
					except:#failed @ logo.link
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  logo.link[/COLOR]', '', 1, MyIconsV[tt],imgfan)
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)

def vvVIDEOLINKS_doChecks_googlevideo(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#google video
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(url),scr,imgfan,show)#MyIconsV[tt])
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',urllib.unquote_plus(url),scr,imgfan,show)#MyIconsV[tt])
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_vidzur(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#vidzur#no-screenshot
		linka=getURL(url)
		matchb=re.compile("playlist:\s+\[\s+\{\s+url:\s+'(.+?)'.").findall(linka)
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',urllib.unquote_plus(matchb[0]),scr,imgfan,show)
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',matchb[0],scr,imgfan,show)
			except:#failed @ logo.link
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], matcha[0])

 
#	vvVIDEOLINKS_doChecks_video44(0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
#	vvVIDEOLINKS_doChecks_ novamov (0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
#	vvVIDEOLINKS_doChecks_ yourupload (0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
#	vvVIDEOLINKS_doChecks_ googlevideo (0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
#	vvVIDEOLINKS_doChecks_ vidzur (0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
#	vvVIDEOLINKS_doChecks_ others (0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)

def vvVIDEOLINKS_doChecks_others(ListOfUrls,tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	######## I need to learn how to merge multiple Lists better before enabling this feature I guess. :(
	#ListOfUrls
	icnt = int(0)
	#print'test1:',ListOfUrls
	#for urlItemA in ListOfUrls:
	#	print'test2:',urlItemA
	#	for urlItem in urlItemA:
	#		vsCheck=False
	#		print'test3:',MySourcesV
	#		for VSites in MySourcesV:
	#			if (VSites in urlItem): 
	#				vsCheck=True # and ('yourupload' not in VSites):#Checking that it doesnt match any known site.
	#				print VSites +' is in '+ urlItem
	#		if ('facebook.com' in urlItem) or ('ads' in urlItem): 
	#			print'fb/ads: true'
	#			vsCheck=True
	#		if ('novamov' in urlItem): 
	#			print'novamov: true'
	#			vsCheck=False
	#		if vsCheck==False:
	#			icnt=(int(icnt) + 1)
	#			print 'Unknown Link Found For: # '+str(icnt)+'.) '+show,urllib.unquote_plus(url)
	#			#addLink('[COLOR white]Unknown[/COLOR] - [COLOR grey]Please report the Show and Episode to me[/COLOR]',urllib.unquote_plus(url),ICON, fanart,show)#MyIconsV[tt])
	#			VaddDir('[COLOR white]Unknown[/COLOR] - [COLOR grey]Please report the Show and Episode to me[/COLOR]', urllib.unquote_plus(url), 1, ICON, fanart)



#xbmcplugin.endOfDirectory(int(sys.argv[1]))
