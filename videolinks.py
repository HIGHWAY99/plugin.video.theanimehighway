import urllib,urllib2,re,os,xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs,sys,socket
import string,StringIO,logging,urlresolver,random,array
import teh_tools
from teh_tools import *
try: import json
except ImportError: import simplejson as json
try: import StorageServer
except: import storageserverdummy as StorageServer
plugin_id='plugin.video.theanimehighway'
cache = StorageServer.StorageServer(plugin_id)
#import SimpleDownloader as downloader
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

SiteNames=['nosite','[COLOR blue][COLOR white]Anime[/COLOR]Get[/COLOR]','[COLOR red][COLOR white]Anime[/COLOR]44[/COLOR]','[COLOR darkblue][COLOR white]Anime[/COLOR]Plus[/COLOR]','[COLOR grey]Good[COLOR white]Drama[/COLOR][/COLOR]','[COLOR maroon][COLOR white]Anime[/COLOR]Zone[/COLOR]','[COLOR teal]Dubbed[COLOR white]Anime[/COLOR]On [/COLOR]','[COLOR cornflowerblue][COLOR white]dub[/COLOR]happy[/COLOR]','[COLOR cornflowerblue]Watch[/COLOR][COLOR white]Dub[/COLOR]','','']
SiteBits=['nosite','animeget.com','anime44.com','animeplus.tv','gooddrama.net','anime44.co.uk','dubbedanimeon.com','dubhappy.eu','watchdub.com']
MyVideoLinkSrcMatches=['src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkSrcMatchesB=['src="(.+?)"',			'<embed.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"',			'<iframe.+?src="(.+?)"'			,'src="(.+?)"'		,'src="(.+?)"',		'src="(.+?)"']
MyVideoLinkBrackets=['<iframe.+?src="(.+?)"', '<embed.+?src="(.+?)"', '<object.+?data="(.+?)"','<EMBED src="(.+?)"']
MyAlphabet=	['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
MyBrowser=	['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3']
MySourcesV=		['videoweed.es',	'video44.net',	'novamov.com',	'dailymotion.com',	'videofun.me',	'yourupload.com',	'video.google.com',	'vidzur.com',	'upload2.com','putlocker.com','videoslasher.com','vidbull.com',		'uploadc.com',	'veevr.com',	'rutube.ru',	'trollvid.net',	'verilscriptz.com',	'vidup.org','veoh.com',	'megavideo.com']
MyIconsV=		[artPath + 'videoweed.jpg',	artPath + 'video44a.png',	artPath + 'novamov.jpg',	artPath + 'dailymotion.jpg',	artPath + 'videofun.png',	artPath + 'yourupload.jpg',	artPath + 'googlevideo.gif', artPath + 'vidzur.png', artPath + 'upload2.png', artPath + 'putlocker.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'trollvid_net.png',artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png', artPath + 'preview.png']#BLANK.png
MyNamesV=		['VideoWeed',			'Video44',			'NovaMov',			'DailyMotion',			'VideoFun',			'YourUpload',				'Google Video',			'VidZur',			'Upload2',		'PutLocker',		'VideoSlasher',		'VidBull',				'UploadC',			'Veevr',			'RuTube',			'TrollVid',			'VerilScriptz',			'VidUp',		'Veoh',			'MegaVideo',		'MP4Upload'		,'AUEngine']
MyColorsV=	['lime',					'red',					'silver',				'green',						'cyan',					'deepskyblue',			'blue',							'orange',			'lightsalmon','lightsteelblue',	'linen',				'magenta',				'limegreen',		'khaki',			'lemonchiffon','lawngreen', 	'white', 					'white', 					'white', 			'white', 			'white', 			'white', 			'white', 			'white']


#############################
def metaArt_DoCheck(nameToCheck,s=True,e=False):
	mc=metaArt_check(nameToCheck)
	if (mc==True): return s
	else: return e

def metaArt_check(nameToCheck):
  try: saved_metaArts = cache.get('MetaArt_')
  except: return False
  ##erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_metaArts: return False ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts == '[]': return False ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts:
  	metaArts = eval(saved_metaArts)
  	#if (nameToCheck in metaArts): return True
  	for metaArt in metaArts:
  		if (nameToCheck==metaArt[0]) or (nameToCheck==metaArt[1]): return True
  return False

def metaArt_getCache(nameToCheck):
  tn = ('none','none','none','none','none','none','none','none','none','none','none','none')
  try: saved_metaArts = cache.get('MetaArt_')
  except: return tn
  ##erNoFavs='XBMC.Notification([B][COLOR orange]Favorites[/COLOR][/B],[B]You have no favorites saved.[/B],5000,"")'
  if not saved_metaArts: return tn ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts == '[]': return tn ##xbmc.executebuiltin(erNoFavs)
  if saved_metaArts:
  	metaArts = eval(saved_metaArts)
  	#if (nameToCheck in metaArts):
  	for metaArt in metaArts:
  		if (nameToCheck==metaArt[0]) or (nameToCheck==metaArt[1]):#0=given show_title , 1=gotten show_title from thetvdb.com
  			return (metaArt[0],metaArt[2],metaArt[3],metaArt[4],metaArt[5],metaArt[6],metaArt[7],metaArt[8],metaArt[9],metaArt[10],metaArt[11],metaArt[12])
  			#try:
  			#	return (metaArt[0],metaArt[2],metaArt[3],metaArt[4],metaArt[5],metaArt[6],metaArt[7],metaArt[8],metaArt[9],metaArt[10],metaArt[11],metaArt[12])
  			#except: continue
  return tn

def metaArt_get(show_name,show_id='none',url_thetvdb='none',show_fanart='none',show_poster='none',show_banner='none',show_desc='none'): #,get_which=3): #0=name,1=id,2=url_for_showhpage(thetvdb.com),3=fanart_url,4=poster_url,5=banner_url
  if ' - Movie' in show_name: show_name=show_name.replace(' - Movie','')
  if ': Movie' in show_name: show_name=show_name.replace(': Movie','')
  if ' Movie' in show_name: show_name=show_name.replace(' Movie','')
  saved_fans = cache.get('MetaArt_')
  erNoFans='XBMC.Notification([B][COLOR orange]MetaArt: [/COLOR]'+show_name+'[/B],[B]You have no MetaArt saved.[/B],5000,"")'
  fanart_found=False
  fanart_item='none'
  if not saved_fans: xbmc.executebuiltin(erNoFans)
  if saved_fans == '[]': xbmc.executebuiltin(erNoFans)
  if saved_fans:
    #fans = sorted(eval(saved_fans), key=lambda fan: fan[0])#favs = eval(saved_favs)
    fans = eval(saved_fans)
    for fan in fans:
    	if (show_name==fan[0]) or (show_name==fan[1]):#0=given show_title , 1=gotten show_title from thetvdb.com
    		try:
    			#notification('[B][COLOR orange]Metadata: '+fan[0]+'[/COLOR][/B]','[B] Data has been found in cache.[/B]')
    			fanart_item=(fan[0],fan[2],fan[3],fan[4],fan[5],fan[6],fan[7],fan[8],fan[9],fan[10],fan[11],fan[12])
    			fanart_found=True
    		except:
    			continue
  if fanart_found==False:
  	match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner,match_desc,match_genres,match_status,match_language,match_network,match_rating=thetvdb_com(show_name)#,'0','Fan Art')
  	if match_desc=='none': match_desc=show_desc.strip()
  	if show_fanart=='none': show_fanart=show_desc
  	if show_poster=='none': show_poster=show_desc
  	if show_banner=='none': show_banner=show_desc
  	if (match_showname=='none') or (match_showid=='none') or (match_thetvdb_url=='none') or (match_fanart=='none') or (match_poster=='none') or (match_banner=='none') or (match_desc=='none'):
  		fanart_item=(show_name,show_id,url_thetvdb,show_fanart,show_poster,show_banner,show_desc,match_genres,match_status,match_language,match_network,match_rating)
  	else:
  		metaArt_add(show_name,match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner,match_desc,match_genres,match_status,match_language,match_network,match_rating)
  		fanart_item=(match_showname,match_showid,match_thetvdb_url,match_fanart,match_poster,match_banner,match_desc,match_genres,match_status,match_language,match_network,match_rating)
  #else:
  #	fanart_item
  return fanart_item
  set_view('none',504)


def thetvdb_com(show_name,show_id='none',graphic_type='fanart'):
	if (debugging==True): print 'testing thetvdb_com'
	if (debugging==True): print 'showname: '+show_name
	if (debugging==True): print 'showid: '+show_id
	if (debugging==True): print 'graphic type: '+graphic_type
	if (show_id=='none') or (show_id=='0'):
		match=thetvdb_com_search(show_name,show_id)
		#if (debugging==True): print match
		match_showurl,match_name,match_genres,match_status,match_language,match_network,match_rating=match #.group()
		if (debugging==True): print 'match_name: '+match_name
		#### url, name, genres, status, language, network, rating
		#=getURL('http://thetvdb.com'+match_showurl).group()
		if match_showurl=='none': return ('none','none','none','none','none','none','none','none','none','none','none','none')
		match_showurl=urllib.unquote_plus('http://thetvdb.com'+match_showurl)
		if ('&amp;' in match_showurl): match_showurl=match_showurl.replace('&amp;','&')
		#if (debugging==True): print match_showurl
		match_id=re.compile('&id=(.+?)&').findall(match_showurl)[0]
		#match_name,match_language,match_id
		##<h1>Fan Art</h1>
		dat_a=getURL(match_showurl) #.group()
		#if ('/banners/_cache/topfanart/0.jpg' in dat_a): return ('none','none','none','none','none','none','none','none','none','none','none','none')
		#if (debugging==True): print dat_a
		dat_b=(dat_a.split('<h1>Fan Art</h1>')[1]).split('</table>')[0]
		if ('View Full Size' in dat_b):
			match_graphicURL=re.compile('<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>').findall(dat_b)[0]
			match_graphicURL='http://thetvdb.com/'+match_graphicURL
		else: match_graphicURL='none'
		#
		dat_c=(dat_a.split('<h1>Posters</h1>')[1]).split('</table>')[0]
		if ('View Full Size' in dat_c):
			match_posterURL=re.compile('<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>').findall(dat_c)[0]
			match_posterURL='http://thetvdb.com/'+match_posterURL
		else: match_posterURL='none'
		#
		dat_d=(dat_a.split('<h1>Banners</h1>')[1]).split('</table>')[0]
		if ('View Full Size' in dat_d):
			match_bannerURL=re.compile('<tr><td></td><td align=right><a href="(.+?)" target="_blank">View Full Size</a></td></tr>').findall(dat_d)[0]
			match_bannerURL='http://thetvdb.com/'+match_bannerURL
		else: match_bannerURL='none'
		#match_results=(show_name,match_id,match_showurl,match_graphicURL,match_posterURL,match_bannerURL)
		try: match_Desc=((dat_a.split('<h1>'+match_name+'</h1>')[1]).split('</div>')[0]).strip()
		except: match_Desc='none'
		if (match_Desc==''): match_Desc='none'
		if (debugging==True): print 'match_Desc: '+match_Desc
		match_results=(show_name,match_id,match_showurl,match_graphicURL,match_posterURL,match_bannerURL,match_Desc,match_genres,match_status,match_language,match_network,match_rating)
		#if (debugging==True): print match_results
		return match_results
	else:
		return ('none','none','none','none','none','none','none','none','none','none','none','none') #'none'

def thetvdb_com_search(show_name,show_id='none'):
	if (debugging==True): print 'thetvdb.com show: '+show_name
	#getURL('http://thetvdb.com/?searchseriesid=&tab=listseries&function=Search&string='+urllib.quote_plus(show_name))
	#http://thetvdb.com/index.php?fieldlocation=4&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname=Bleach
	#http://thetvdb.com/index.php?searchseriesid=&tab=listseries&function=Search&string=
	#http://thetvdb.com/index.php?fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname=Angel+Beats
	if (debugging==True): print 'thetvdb.com search: '+'http://thetvdb.com/index.php?fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname='+urllib.quote_plus(show_name)
	link=getURL('http://thetvdb.com/index.php?fieldlocation=2&language=7&genre=&year=&network=&zap2it_id=&tvcom_id=&imdb_id=&order=translation&addedBy=&searching=Search&tab=advancedsearch&seriesname='+urllib.quote_plus(show_name))
	if link=='none': return ('none','none','none','none','none','none','none')
	elif 'No Series found.' in link: return ('none','none','none','none','none','none','none')
	else:
		#match=re.compile('<tr><td class=".+?"><a href="(.+?)">(.+?) </a> </td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td></tr>').findall(link)[0]
		try: 
			match=re.compile('<tr><td class=".+?">.+?</td><td class=".+?"><a href="(.+?)">(.+?)</a></td><td class=".+?">(.+?)</a></td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?">.+?</td></tr>').findall(link)[0]
			#match=(match[0],match[1],match[2],match[3],match[4],match[5],match[6])#,match[7])
		except:
			try: 
				match=re.compile('<tr><td class=".+?">.+?</td><td class=".+?"><a href="(.+?)">(.+?)</a></td><td class=".+?">(.+?)</a></td><td class=".+?">(.+?)</td><td class=".+?">(.+?)</td><td class=".+?"></td><td class=".+?">(.+?)</td><td class=".+?">.+?</td></tr>').findall(link)[0]
				match=(match[0],match[1],match[2],match[3],match[4],'none',match[5])
			except: return ('none','none','none','none','none','none','none')
		#									<tr><td class="odd">1</td><td class="odd"><a href="(url)">(title)</a></td><td class="odd">(genres)</a></td><td class="odd">(status)</td><td class="odd">(language)</td><td class="odd">(network)</td><td class="odd">(rating)</td><td class="odd">10</td></tr>
		#<tr><td class="odd">1</td><td class="odd"><a href="/index.php?tab=series&amp;id=150471&amp;lid=7">Angel Beats!</a></td><td class="odd">|Action|Adventure|Animation|Comedy|Drama|</a></td><td class="odd">Ended</td><td class="odd">English</td><td class="odd">Tokyo Broadcasting System</td><td class="odd">9</td><td class="odd">10</td></tr>
		#### url, name, genres, status, language, network, rating
		return match
	#match_showurl,match_name,match_language,match_id=match.group()
	#return (match_showurl,match_name,match_language,match_id)
	##

#def addfav(header="", message="", sleep=5000 ):
#	notify(msg=message, title=header, delay=sleep, image=ICON0)

###########################################
def vvVIDEOLINKS(mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):#vvVIDEOLINKS(mainurl,name,name2,scr,imgfan,show,type2,mode)
	urlA=mainurl
	link=getURL(mainurl)
	ListOfUrls=[]
	if (shoDebugging==True): 
		try: VaddDir('  [COLOR cornsilk][COLOR purple]Episode: [/COLOR]'+show+'[/COLOR]' + '[COLOR grey][/COLOR]', '', 1, ICON, fanart)
		except: t=''
	for VidLinkBrackets in MyVideoLinkBrackets:
		match=[]
		match=re.compile(VidLinkBrackets).findall(link)
		if (debugging==True): print 'Bracket Matches:',match
		ListOfUrls = ListOfUrls,match
		for url in match:
			vvVIDEOLINKS_doChecks(url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	#if (debugging==True): print 'list of urls:',ListOfUrls
	#vvVIDEOLINKS_doChecks_others(ListOfUrls,0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)

def vvVIDEOLINKS_doChecks(url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	vvVIDEOLINKS_doChecks_videofun(4,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_dailymotion(3,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videoweed(0,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_video44(1,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_novamov(2,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_yourupload(5,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_googlevideo(6,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidzur(7,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_upload2(8,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidbull(11,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_uploadc(12,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_putlocker(9,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_videoslasher(10,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_veevr(13,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_rutube(14,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_trollvid(15,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	#vvVIDEOLINKS_doChecks_verilscriptz(16,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_vidup(17,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_veoh(18,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	vvVIDEOLINKS_doChecks_megavideo(19,url,mainurl,name,name2,scr,imgfan,show,type2,mode)
	#

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
		if (debugging==True): print 'A Link ( ' + MySourcesV[tt] + ' ) was found: ' + url
		try:
			linka=getURL(url)
			if 'Error 404 - Not Found' not in linka:
				matcha=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+true').findall(linka)#Screenshot
				linkb=getURL(matcha[0])
				matchb=re.compile('url:\s+"(.+?)",\s+autoPlay:\s+false').findall(linka)#Video
				partInfo=checkForPartNo(matchb[0])
				if (debugging==True): print matcha,matchb
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
	url=urllib.unquote_plus(url)
	if MySourcesV[tt] in url:#dailymotion ( Play: yes , Download: no )
		if 'http://www.dailymotion.com/swf/' in url:
			matcha=url.split('/swf/')[1]
			if '&' in matcha:
				try:
					matcha=re.compile('http://www.dailymotion.com/swf/(.+?)&').findall(url)[0]
				except:
					try:
						matcha=re.compile('http://www.dailymotion.com/swf/(.+?)').findall(url)[0]
					except:
						matcha=url
		#try:
		#	##if (debugging==True): print'dailymotion matcha:',matcha,url,matchaa
		#	#matcha=re.compile('http://www.dailymotion.com/swf/(.+?)&').findall(url)
		linka='http://www.dailymotion.com/video/' + matcha
		#	#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*1a[/COLOR]',url,MyIconsV[tt],imgfan,show)
		#	#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*1b[/COLOR]',linka,MyIconsV[tt],imgfan,show)
		linkb=getURL(linka)
		try:
			matchb=re.compile('var flashvars = {"(.*?)"};').findall(linkb)
			datab=urllib.unquote_plus(matchb[0])###if (debugging==True): print datab
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
		except:
			test=''
		##if (debugging==True): print 'DailyMotion:',vid_url,vid_autoURL,vid_ldURL,vid_sdURL,vid_screenshot,vid_title
		try:
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
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			if '&amp;' in url: url = urllib.unquote_plus(url)
			if '&amp;' in url: url = url.replace('&amp;','&')
			#matchb=url
			#if '&http:' in url:
			#	matcha=url.split('&http:')
			#	#if (debugging==True): print url,matcha
			#	matcha[1]='http:'+matcha[1]
			#	matchb=url.split('&v=')
			#	matcha[0]=matcha[0]+'&v='+matchb[1]
			#else:
			#	try: re.compile('&v=(.+?)&').findall(url)
			#	except: test=''
			linka=getURL(url)
			fil_nam=re.compile('flashvars.file="(.+?)"').findall(linka)[0]
			fil_key=re.compile('flashvars.filekey="(.+?)"').findall(linka)[0]
			linkb = 'http://www.novamov.com/api/player.api.php?key=%s&file=%s' % (fil_key, fil_nam)
			linkc=getURL(linkb)
			if 'The video no longer exists' in linkc:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			else:
				#if (debugging==True): print 'linkb_c: ',linkb,linkc,url,linka
				fil_match=re.compile('url=(.+?)&title').findall(linkc)
				fil_url=fil_match[0]
				#if (debugging==True): print 'fil_url: ',fil_url #,linkb,linkc
				fil_url=urllib.unquote_plus(fil_url)
				try:
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]','http://www.novamov.com/video/' + matchb[1],scr,imgfan,show)#(N/A) NovaMov Page
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',fil_url,scr,imgfan,show)#(N/A) NovaMov Page
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) Combined Link[/COLOR]',urlresolver.resolve(url),scr,imgfan,show)
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) 718x420[/COLOR]',urlresolver.resolve(matcha[0]),scr,imgfan,show)
					#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](N/A) 600x480[/COLOR]',urlresolver.resolve(matcha[1]),scr,imgfan,show)
					#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', url, 1, MyIconsV[tt], fanart)
				except:
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',fil_url,scr,imgfan,show)#MyIconsV[tt])
					except:
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], fanart)

def vvVIDEOLINKS_doChecks_yourupload(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#yourupload
		linka=getURL(url)
		try:
			matcha=re.compile('&image=(.+?)&logo.file').findall(linka)
			matchb=re.compile('flashvars="id=.+?&file=(.+?)&image').findall(linka)
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]',urllib.unquote_plus(matchb[0]),urllib.unquote_plus(matcha[0]),imgfan,show)#MyIconsV[tt])
		except:#failed at initial link
			try:
				#linkb=getURL(matcha[0])
				matcha=re.compile('<meta property="og:image" content="(.+?)"').findall(linka)
				matchb=re.compile('<meta property="og:video" content="(.+?)"').findall(linka)
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey](Some lack time-seeking)[/COLOR]',matchb[0],matcha[0],imgfan,show)
				except:#failed @ og:video
					matchc=re.compile('&logo.link=(.+?)&logo.linktarget').findall(linka)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*3[/COLOR]',unquote_plus(matchc[0]),matcha[0],imgfan,show)
					except:#failed @ logo.link
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  logo.link[/COLOR]', '', 1, MyIconsV[tt],imgfan)
			except:
				try:
					matcha=re.compile(",'image':\s+'(.+?)'").findall(linka)
					matchb=re.compile(",'file':\s+'(.+?)'").findall(linka)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2 Might be slow loading.[/COLOR]',matchb[0],matcha[0],imgfan,show)
					except:#failed @ og:video
						VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)
				except: 
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)
				#VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error - Failed @  File Not Found.[/COLOR]', '', 1, MyIconsV[tt],imgfan)

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
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], matchb[0])

def vvVIDEOLINKS_doChecks_upload2(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#upload2#no-screenshot(only image is for upload2)###unchecked so far
		linka=getURL(url)
		#matchb=re.compile("playlist:\s+\[\s+\{\s+url:\s+'(.+?)'.").findall(linka)
		video_title,video_file,rating=re.compile("&video_title=(.+?)&","&video=(.+?)&","&rating=(.+?)&").findall(linka)
		try:
			addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',matchb[0],scr,imgfan,video_title)
		except:
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',matchb[0],scr,imgfan,show)
			except:#failed @ logo.link
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], matcha[0])

def vvVIDEOLINKS_doChecks_videoslasher(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#videoslasher
		linka=getURL(url)
		if 'File Does not Exist, or Has Been Removed' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			#if 'embed' in url: url=url.replace('embed','video')
			linkd = urlresolver.resolve(url) 
			#linke = urlresolver.HostedMediaFile(linkd)#.resolve()
			###http://www.videoslasher.com/video/
			try:
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',linkd,scr,imgfan,show)
			except:
				try:
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',url,scr,imgfan,show)
				except:#failed @ logo.link
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', url, 1, MyIconsV[tt], imgfan)


def vvVIDEOLINKS_doChecks_vidbull(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	#if (debugging==True): print 'checkVideoBull Link: '+url
	if MySourcesV[tt] in url:#VideoBull.com
		linka=getURL(url)
		#if (debugging==True): print 'VideoBull Link: '+url
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Not Supported Yet.[/COLOR]', '', 1, MyIconsV[tt], imgfan)

def vvVIDEOLINKS_doChecks_veevr(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#veevr.com#13
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			#vid_image,vid_title = re.compile('<img id="vid-thumb" src="(.+?)".+?alt="(.+?)"').findall(linka)[0]
			#if (debugging==True): print 'url: ',url
			##match_image,match_url = re.compile("playlist:.+?url: '(.+?)',.+?scaling: '.+?'.+?url: '(.+?)'").findall(linka)
			#match_image = re.compile("playlist:.+?url: '(.+?)',.+?scaling:").findall(linka)[0]
			#match_url 	= re.compile("playlist:.+?scaling:.+?url: '(.+?)'").findall(linka)[0]
			#vid_image=match_image[0]
			#vid_url=match_url[0]
			##if (debugging==True): print linka
			#vid_image = re.compile("playlist:.+?url: '(.+?)',.+?scaling:").findall(linka)[0]
			#vid_url 	= re.compile("playlist:.+?scaling:.+?url: '(.+?)'").findall(linka)[0]
			vid_image=scr
			vid_url=''
			vid_urla=''
			match=re.compile("url: '(.+?)'").findall(linka)
			for link in match:
				if '.swf' in link:
					test='' 
				else:
					if ('.jpg' in link) and ('images' in link) and ('videos' in link) and ('thumbs' in link):
						vid_image=link
					if ('token' in link) and ('file=' in link) and ('videos' in link) and ('download' in link) and (vid_urla==''):
						vid_urla=urllib.unquote_plus(link)
			vid_image=urllib.unquote_plus(vid_image)
			#vid_url=urllib.unquote_plus(vid_url)
			linkb=getURL(vid_urla)
			vid_url=re.compile('url="(.+?)"').findall(linkb)[0]
			##matcha=re.compile("addVariable\('file','(.+?)'\)").findall(linka)[0]
			##matcha=urlresolver.resolve(matcha)
			##matcha=matcha.replace(' ','%20')
			##matcha=urllib.quote_plus(matcha)
			##if (debugging==True): print 'match: ',matcha
			if (debugging==True): print url,vid_image,vid_urla,vid_url
			try:
				#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,scr,imgfan,show)
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Enjoy the screenshot. Video Bugged.[/COLOR]',vid_url,vid_image,imgfan,show)
				if (shoDebugging==True): addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: *2 Enjoy the screenshot. Video Bugged.[/COLOR]',vid_url+'Seg1-Frag1',vid_image,imgfan,show)
				if (shoDebugging==True): addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: *1 Enjoy the screenshot. Video Bugged.[/COLOR]',vid_urla,vid_image,imgfan,show)
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, MyIconsV[tt], imgfan)
			#
		### 
		### http://veevr.com/embed/kdGk7L9__
		### http://doppler.ch3.hwcdn.net/mh003c3/y2x5c2k3/ads/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil/media_b826368_w880573809.abst/Seg1-Frag1
		### _gaq.push(['_setAccount', 'UA-16111683-1']);
		### _gaq.push(['_setDomainName', 'veevr.com']);
		### _gaq.push(['_trackPageview']);
		### #player-logo {
		###             float:right; margin-right:0; height:19px; width:100px; background:url(http://hwcdn.net/j3v8m4w2/cds/www/images/templates/logo-small.png) no-repeat;
		###         }
		### http://hwcdn.net/j3v8m4w2/cds/www/images/templates/logo-small.png
		### LR_VIDEO_ID: '325384',
		### LR_PARTNERS: '698792',
		### LR_SCAN_566_TITLE: escape('C Control S01E03 720p '),
		### LR_SCAN_566_DESCRIPTION: escape('C Control S01E03 720p '),
		### http://mps.hwcdn.net/y2x5c2k3/ads/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil/Manifest.f4m?file=mp4&bitrate=1373207457&token=4105b834ebb02c8f4e581c3e2005856d
		### http://doppler.ch3.hwcdn.net/mh003c3/y2x5c2k3/ads/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil/media_b826368_w1877115775.abst/
		### mps/videos/download/a2d287cfe9694988b54cd046b5d00ff8.smil
		### Seg1-Frag1
		### 
		### 
		### 
		### 
		### 
		### 
		### 
		### 
		### 

def vvVIDEOLINKS_doChecks_uploadc(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#uploadc.com
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			matcha=re.compile("addVariable\('file','(.+?)'\)").findall(linka)[0]
			#if (debugging==True): print 'match: ',matcha
			try:
				#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,scr,imgfan,show)
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,MyIconsV[tt],imgfan,show)
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, MyIconsV[tt], imgfan)


def vvVIDEOLINKS_doChecks_verilscriptz(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#verilscriptz
		if (debugging==True): print 'doChecks_verilscriptz - url: '+url
		try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',video_url,scr,imgfan,show)
		except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, ICON, fanart)
		#link1=getURL(url)#verilscriptz.com
		#if ('<location>' in link1) and ('<image>' in link1):
		#	video_url=(re.compile('<location>(.+?)</location>').findall(link1)[0]).strip()
		#	video_img=(re.compile('<image>(.+?)</image>').findall(link1)[0]).strip()
		#	try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',video_url,scr,imgfan,show)
		#	except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, ICON, fanart)

def vvVIDEOLINKS_doChecks_veoh(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#veoh.com
		if ('&#038;' in url): url=url.replace('&#038;','&')
		if (debugging==True): print 'doChecks veoh url: '+url
		try: permalinkId=(re.compile('permalinkId=(.+?)&').findall(url)[0]).strip()
		except: permalinkId='none'
		if (permalinkId=='none'):
			if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No ID Found.[/COLOR]', url, 1, MyIconsV[tt], fanart)
			return
		else:
			if (debugging==True): print 'doChecks veoh permalinkId: '+permalinkId
			if (debugging==True): print 'doChecks veoh details url: '+'http://www.veoh.com/rest/video/'+permalinkId+'/details'
			linka=getURL('http://www.veoh.com/rest/video/'+permalinkId+'/details')
			if ('fullPreviewHashPath="' in linka):
				try: fullPreviewHashPath=(re.compile('fullPreviewHashPath="(.+?)"').findall(linka)[0]).strip()
				except: fullPreviewHashPath='none'
				if (debugging==True): print 'doChecks veoh fullPreviewHashPath: '+fullPreviewHashPath
				if (fullPreviewHashPath=='none'):
					if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing...[/COLOR]', '', 1, ICON, fanart)
					return
				else:
					vid_url=fullPreviewHashPath
					try: vid_img=(re.compile('fullHighResImagePath="(.+?)"').findall(linka)[0]).strip()
					except: 
						try: vid_img=(re.compile('fullMedResImagePath="(.+?)"').findall(linka)[0]).strip()
						except: vid_img=ICON
					if (debugging==True): print 'doChecks veoh vid_img: '+vid_img
					try: addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',vid_url,vid_img,fanart,show)
					except:
						try:
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
						except:
							if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing..[/COLOR]', '', 1, ICON, fanart)
			else:
				if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: No Video Found.[/COLOR]', url, 1, MyIconsV[tt], fanart)
				return

def vvVIDEOLINKS_doChecks_megavideo(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#veoh.com
		if (debugging==True): print 'doChecks megavideo url: '+url
		vid_url=url
		#try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]* Error: Undergoing Testing.[/COLOR]',vid_url,scr,fanart,show)
		#except: 	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
		if (shoDebugging==True): VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Host has been shutdown.[/COLOR]', vid_url, 1, ICON, fanart)

def vvVIDEOLINKS_doChecks_vidup(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#vidup
		#http://vidup.org/embed.php?file=2a28113d&w=550&h=420&bg=http://www.verilscriptz.com/anime/animedubbednow.jpg
		if (debugging==True): print 'doChecks_vidup url: '+url
		linka=getURL(url)
		try: vid_img=(re.compile("background-image: url('(.+?)'); background-repeat").findall(linka)[0]).strip()
		except:
			try: vid_img=(re.compile("background-image: url('(.+?)'").findall(linka)[0]).strip()
			except: vid_img=MyIconsV[tt]
		try: vid_clip_dat=(((linka.split('clip:')[1]).split('{')[1]).split('}')[0]).strip()
		except: vid_clip_dat=linka
		try: vid_url=(re.compile('url: "(.+?)",').findall(vid_clip_dat)[0]).strip() ## s11.
		except: 
			try: vid_url=(re.compile('url:(.+?),').findall(vid_clip_dat)[0]).strip() ## s10.
			except: vid_url=''
		if (debugging==True): print 'doChecks_vidup v url: '+vid_url
		if (debugging==True): print 'doChecks_vidup v img: '+vid_img
		if (vid_url==''): t=''
		else:
			try: 		addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Can be slow to load.[/COLOR]',vid_url,vid_img,fanart,show)
			except: 	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', vid_url, 1, MyIconsV[tt], fanart)
			#background-image: url('
		#
		t=''

def vvVIDEOLINKS_doChecks_trollvid(tt,url,mainurl,name,name2='none',scr='none',imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#trollvid.net
		if (type2==6):
			linka=getURLr(url,'http://dubbedanimeon.com/')
		else:
			linka=getURL(url)
		#if (debugging==True): print linka
		try: vid_fanart_of_site=(url.split('&bg=')[1]).strip()
		except: vid_fanart_of_site=imgfan
		try: vid_id1=(re.compile("file=(.+?)&").findall(url)[0]).strip()
		except: vid_id1=''
		if (vid_id1==''): vid_img=ICON
		else: vid_img='http://cdn.trollvid.net/thumbs/'+vid_id1+'.jpg'
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, vid_img, vid_fanart_of_site)
		#elif '<div class="notice">' in linka:
		#	VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Site threw a fit.[/COLOR]', '', 1, vid_img, vid_fanart_of_site)
		else:
			#try: vid_img=(re.compile(";background-image:url('(.+?)');background-repeat:").findall(dat_show)[0]).strip()
			#except: t='' #vid_img=ICON
			if ('&quot;' in linka): linka=linka.replace('&quot;','')
			try: vid_clip_dat=(((linka.split('clip:')[1]).split('{')[1]).split('}')[0]).strip()
			except: vid_clip_dat=linka
			try: vid_url=(re.compile('url: "(.+?)",').findall(vid_clip_dat)[0]).strip() ## s11.
			except: 
				try: vid_url=(re.compile('url:(.+?),').findall(vid_clip_dat)[0]).strip() ## s10.
				except: vid_url=''
			if ('http%3A%2F%2F' in vid_url): vid_url=urllib.unquote_plus(vid_url)
			testString='41c3311b2678a9e93c202586fe8852c4'
			attemptingString=' -  Attempting Work-a-round '
			trollvid_prefixes=['s01','s02','s03','s04','s05','s06','s07','s08','s09','s10','s11','s12','s13','s14','s15','s16','s17','s18','s19','s20']
			if '<div class="notice">' in linka:
				##linka=dReferer(url,'http://dubbedanimeon.com/')
				for trollvid_prefix in trollvid_prefixes:
					#if (check_ifUrl_isHTML('http://'+trollvid_prefix+'.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4')==False):
					addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey]'+attemptingString+''+trollvid_prefix+'[/COLOR]','http://'+trollvid_prefix+'.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4',vid_img,vid_fanart_of_site,show)
				######'http://s12.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4'
				######
			else: 
				if (vid_url==''):
					VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]', '', 1, vid_img, vid_fanart_of_site)
				else: 
					try: vid_img=(re.compile(";background-image:url('(.+?)');background-repeat:").findall(dat_show)[0]).strip()
					except: vid_img=scr
					try: 
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey] -- Click fast before it times out.[/COLOR]',vid_url,vid_img,vid_fanart_of_site,show)
						if (shoDebugging==True):
							for trollvid_prefix in trollvid_prefixes:
								addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey]'+attemptingString+''+trollvid_prefix+'[/COLOR]','http://'+trollvid_prefix+'.trollvid.net/videos/'+testString+'/'+vid_id1+'.mp4',vid_img,vid_fanart_of_site,show)
						#listitem = xbmcgui.ListItem(MyColorsV[tt], iconImage="DefaultVideo.png", thumbnailImage=vid_img)
						#listitem.setProperty('IsPlayable', 'true')
						#listitem.setPath(vid_url)
						#xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
						#
						###
					except: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2 Error: Needs Testing.[/COLOR]', vid_url, 1, vid_img, vid_fanart_of_site)
					#xbmc.executebuiltin('PlayMedia('+vid_url+')')
					##xbmc.executebuiltin('PlayMedia(vid_url)')
					#player = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
					#player.play(vid_url)
					#player.play(vid_url, xbmcgui.ListItem(label=show, path=vid_url))
					#player.play(url, xbmcgui.ListItem(label='Test', path=url))
					#player.stop()
					#xbmc.sleep(1000)
					return
				#
				#
				#
				#
				#
			#
			### 
			### http://sv3.trollvid.net/embed.php?file=5ccf1c9c&site=on&w=566&h=360&bg=http://dubbedanimeon.com/wp-content/uploads/bgg.jpg
			### http://sv3.trollvid.net/embed.php?file=5ccf1c9c&w=566&h=360&bg=http://dubbedanimeon.com/wp-content/uploads/bgg.jpg
			### 
			### 
			### 
			### http://sv3.trollvid.net/embed.php?file=7b89d472&w=598&h=336&bg=
			### http://cdn.trollvid.net/thumbs/7b89d472.jpg
			### http://s11.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/7b89d472.mp4
			### 
			### http://s11.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/7b89d472.mp4
			### http://s10.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/b2f156a3.mp4
			### http://s11.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/5ccf1c9c.mp4 << http://dubbedanimeon.com/episode/is-this-a-zombie-episode-1-english-dubbed/
			### 
			### 
			### 
			### 
			### http://trollvid.net/dub.php?file=9729cf2a&w=560&h=360&bg=http://dubbedanimeon.com/wp-content/uploads/bgg.jpg ## Playable via firefox
			### http://s4.trollvid.net/videos/eg7ha2vktc/9729cf2a.mp4 ## download via firefox
			### http://trollvid.net/images/sup.mp4
			### http://dubbedanimeon.com/wp-content/uploads/bgg.jpg
			### http://s10.trollvid.net/videos/41c3311b2678a9e93c202586fe8852c4/fb6170ff.mp4
			### 
			### 
			#
			#
			#
			#



def vvVIDEOLINKS_doChecks_rutube(tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#rutube.ru
		linka=getURL(url)
		if 'This file was Deleted' in linka:
			VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			#matcha=re.compile("addVariable\('file','(.+?)'\)").findall(linka)[0]
			##if (debugging==True): print 'match: ',matcha
			### 
			### http://video.rutube.ru/64a7da0f3b1158b4830401f3ddfea34c
			### 
			### 
			### 
			### 
			### 
			matcha=url
			try:
				#addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' [COLOR grey][/COLOR]',matcha,scr,imgfan,show)
				addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Needs Testing.[/COLOR]',matcha,MyIconsV[tt],imgfan,show)
			except:
				VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', matcha, 1, MyIconsV[tt], imgfan)

def vvVIDEOLINKS_doChecks_putlocker(tt,url,mainurl,name,name2='none',scr=ICON,imgfan=fanart,show='none',type2=0,mode=0):
	if MySourcesV[tt] in url:#putlocker
		linkaa=getURL(url)
		if 'File Does not Exist, or Has Been Removed' in linkaa: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		elif 'This file is temporary disabled (but not deleted).' in linkaa: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: temporary disabled (but not deleted).[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		elif 'Try again a bit later.' in linkaa: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Try again a bit later.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
		else:
			##if 'embed' in url: url=url.replace('embed','file')
			#linkaa=getURL(url)
			matchaa=re.compile('<input type="hidden" value="(.+?)" name="fuck_you"').findall(linkaa)[0]
			postData = { 'fuck_you' : matchaa , 'confirm' : 'Close Ad and Watch as Free User'}
			linka=postURL(url,postData)
			if 'File Does not Exist, or Has Been Removed' in linka: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: File was Deleted.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			elif 'This file is temporary disabled (but not deleted).' in linka: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: temporary disabled (but not deleted).[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			elif 'Try again a bit later.' in linka: VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error: Try again a bit later.[/COLOR]', '', 1, MyIconsV[tt], imgfan)
			else:
				###if (debugging==True): print 'testing for putlocker:',matchaa,url,linka,postData
				if 'playlist' in linka:
					matcha=re.compile("playlist: '(.+?)',").findall(linka)[0]
					#if (debugging==True): print 'Playlist found:','http://www.putlocker.com',matcha
					linkb=getURL('http://www.putlocker.com'+matcha)
					#matchb=re.compile('<media:content url="(.+?)" type="image/jpeg" /></item>','<media:content url="(.+?)" type="video/x-flv"  duration=".+?" /></item>').findall(linkb)[0]
					#(video_image,video_url)=re.compile('<media:content url="(.+?)" type="image/jpeg" /></item>','<media:content url="(.+?)" type="video/x-flv"  duration=".+?" /></item>').findall(linkb)[0]
					video_image=re.compile('<item><title>Preview</title><media:content url="(.+?)" type="image/jpeg".+?/></item>').findall(linkb)[0]
					video_url=re.compile('<item><title>Video</title><link>.+?</link><media:content url="(.+?)" type="video/x-flv".+?/></item>').findall(linkb)[0]
					#for video_image,video_url in matchb:
					video_url=urllib.unquote_plus(video_url.replace('&amp;','&'))
					video_image=urllib.unquote_plus(video_image)
					try:
						addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + '  [COLOR grey][/COLOR]',video_url,video_image,imgfan,show)
					except:
						try:
							addLink('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]*2[/COLOR]',video_url,scr,imgfan,show)
						except:#failed @ logo.link
							VaddDir('[COLOR ' + MyColorsV[tt] + ']' + MyNamesV[tt] + '[/COLOR]' + ' - [COLOR grey]Error[/COLOR]', '', 1, MyIconsV[tt], imgfan)
				else: notification('Fetching Link: '+MyNamesV[tt],'Failed to find playlist.')


def vvVIDEOLINKS_doChecks_others(ListOfUrls,tt,url,mainurl,name,name2='none',scr='none',imgfan='none',show='none',type2=0,mode=0):
	######## I need to learn how to merge multiple Lists better before enabling this feature I guess. :(
	#ListOfUrls
	icnt = int(0)
	#if (debugging==True): print'test1:',ListOfUrls
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
