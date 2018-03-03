# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import urlresolver
import urlparse
import json
#Място за дефиниране на константи, които ще се използват няколкократно из отделните модули
__addon_id__= 'plugin.video.envymovies'
__Addon = xbmcaddon.Addon(__addon_id__)
searchicon = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/search.png")
folder = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/folder.png")
series = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/series.png")

MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър


#Меню с директории в приставката
def CATEGORIES():
        addDir('Търсене на видео','https://envymovies.com/?s=',2,searchicon)
        addDir('Всички филми','https://envymovies.com/movies/',1,folder)
        addDir('Сериали','https://envymovies.com/series/',3,series)
        addDir('Анимация','https://envymovies.com/genre/animation/',1,folder)
        addDir('Документален','https://envymovies.com/genre/documentary/',1,folder)
        addDir('Исторически','https://envymovies.com/genre/history/',1,folder)
        addDir('Мистерия','https://envymovies.com/genre/mistery/',1,folder)
        addDir('Психологически','https://envymovies.com/genre/psychological/',1,folder)
        addDir('Трилър','https://envymovies.com/genre/thriller/',1,folder)
        addDir('Sci-fi','https://envymovies.com/genre/sci-fi/',1,folder)
        addDir('Биографичен','https://envymovies.com/genre/biography/',1,folder)
        addDir('Драма','https://envymovies.com/genre/drama/',1,folder)
        addDir('Комедия','https://envymovies.com/genre/comedy/',1,folder)
        addDir('Музикален','https://envymovies.com/genre/musical/',1,folder)
        addDir('Романтичен','https://envymovies.com/genre/romance/',1,folder)
        addDir('Ужаси','https://envymovies.com/genre/horror/',1,folder)
        addDir('Военен','https://envymovies.com/genre/war/',1,folder)
        addDir('Екшън','https://envymovies.com/genre/action/',1,folder)
        addDir('Криминален','https://envymovies.com/genre/crime/',1,folder)
        addDir('Приключенски','https://envymovies.com/genre/adventure/',1,folder)
        addDir('Семеен','https://envymovies.com/genre/family/',1,folder)
        addDir('Фантастика','https://envymovies.com/genre/fantasy/',1,folder)        
        #addDir('','',1,'')


#Разлистване видеата на първата подадена страница
def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('div data-movie-id=".+?".title="(.+?)".+?href="(https.+?)".+?src="(.+?)"').findall(data)
        for title,vid,thumbnail in match:
            #print thumbnail
            #print title
            addLink(title,vid,5,thumbnail)
            br = br + 1
            #print 'Items counter: ' + str(br)
        if br >= 40: #тогава имаме следваща страница и конструираме нейния адрес
            getpage=re.compile('class=..>(.+?)</a>.*href=.(https.+?)/page/./.>').findall(data)
            for page,baseurl in getpage:
                newpage = int(page)
                nextpage = newpage + 1
                url = baseurl + '/page/' + str(nextpage) + '/'
                print 'URL OF THE NEXT PAGE IS' + url
                thumbnail='DefaultFolder.png'
                addDir('следваща страница>>',url,1,thumbnail)
                #addLink('следваща страница>>',newurl,1,thumbnail)
        #else:
                #addDir('Върнете се назад в главното меню за да продължите',page,1,"DefaultFolderBack.png")
def INDEXSERIALS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('</h2></div>.<a href="(.+?)".+?src="(.+?)".title="(.+?)"').findall(data)
        for vid,thumbnail,title in match:
            #print thumbnail
            #print title
            addLink(title,vid,4,thumbnail)
            br = br + 1
            
def INDEXSERIES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        #print 'request page url:' + url
        data=response.read()
        response.close()

        #Начало на обхождането
        br = 0 #Брояч на видеата в страницата - 24 за този сайт
        match = re.compile('url.(https.+?jpg).".href="(.+?)".+?</i>(.+?)</span>').findall(data)
        for thumbnail,url,title, in match:
         title = name + '  ' + title
            #print thumbnail
            #print title
         addLink(title,url,6,thumbnail)
        br = br + 1

#Търсачка
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Търсачка')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            searchText=searchText.replace(' ','+')
            searchurl = url + searchText
            searchurl = searchurl.encode('utf-8')
            #print 'SEARCHING:' + searchurl
            req = urllib2.Request(searchurl)
            req.add_header('User-Agent', UA)
            response = urllib2.urlopen(req)
            #print 'request page url:' + url
            data=response.read()
            response.close()
            match = re.compile('href="(.+?)".*\n.*src="(.+?)" title="(.+?)"').findall(data)
            for vid,thumbnail,title in match:
             addLink(title,vid,5,thumbnail)

        else:
             addDir('Върнете се назад в главното меню за да продължите','','',"DefaultFolderBack.png")

def SHOW(url):
       req = urllib2.Request(url)
       req.add_header('User-Agent', UA)
       response = urllib2.urlopen(req)
       data=response.read()
       response.close()
       match = re.compile('class="movieplay">.+?data-lazy-src="(.+?embed/.+?/).+?" width="100%"').findall(data)
       for link in match:
        matchi = re.compile('style="background-image:.+?(https:.+?.jpg)').findall(data)
        for thumbnail in matchi:
         try:
          matchd = re.compile('class="film-desc.+?<p class="f-desc.+?>(.+?)</p>').findall(data)
          for description in matchd:
           desc = description       
         except:
           desc = 'не могах да намеря описание'
         if 'openload' in link:
           addLink2(name,link,8,desc,thumbnail)
         if not 'openload' in link:
           addLink2(name,link,7,desc,thumbnail)

def SHOWSERIAL(url):
       url1 = url
       req = urllib2.Request(url)
       req.add_header('User-Agent', UA)
       response = urllib2.urlopen(req)
       data=response.read()
       response.close()
       match = re.compile('class="movieplay">.+?data-lazy-src="(.+?)" width="100%"').findall(data)
       for link in match:
        matchi = re.compile('meta property="og:image" content="(.+?)"').findall(data)
        for thumbnail in matchi:
         matchd = re.compile('class="film-desc.+?<p class="f-desc.+?>(.+?)</p>').findall(data)
         for desc in matchd:
          addLink2(name,link,7,desc,thumbnail)

#Зареждане на видео
def PLAY(url):
        li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=url)
        li.setInfo('video', { 'title': name })
        link = url
        try: stream_url = urlresolver.HostedMediaFile(link).resolve()
        except:
               deb('Link URL Was Not Resolved',link); deadNote("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL."); return

        ##xbmc.Player().stop()
        play=xbmc.Player() ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
        try: _addon.resolve_url(url)
        except: t=''
        try: _addon.resolve_url(stream_url)
        except: t=''
        play.play(stream_url, li); xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
        try: _addon.resolve_url(url)
        except: t=''
        try: _addon.resolve_url(stream_url)
        except: t=''

def PLAYOL(url):
        match = re.compile('https.+?embed/(.+?)/').findall(url)
        for  link in match:
         link = 'https://api.openload.co/1/streaming/get?file=' + link
         req = urllib2.Request(link)
         req.add_header('User-Agent', UA)
         response = urllib2.urlopen(req)
         #print 'request page url:' + url
         data=response.read()
         response.close()
         #print data
         jsonrsp = json.loads(data)
         path = jsonrsp['result']['url'].replace('?mime=true','')
         li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=path)
         li.setInfo('video', { 'title': name })
         xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
         try:
           xbmc.Player().play(path, li)
         except:
           xbmc.executebuiltin("Notification('Грешка','Видеото липсва на сървъра!')")


#Модул за добавяне на отделно заглавие и неговите атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink2(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.setProperty("IsPlayable" , "false")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

#Модул за добавяне на отделна директория и нейните атрибути към съдържанието на показваната в Kodi директория - НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

#НЯМА НУЖДА ДА ПРОМЕНЯТЕ НИЩО ТУК
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







params=get_params()
url=None
name=None
iconimage=None
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
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


#Списък на отделните подпрограми/модули в тази приставка - трябва напълно да отговаря на кода отгоре
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        SEARCH(url)

elif mode==3:
        print ""+url
        INDEXSERIALS(url)

elif mode==4:
        print ""+url
        INDEXSERIES(url)

elif mode==5:
        print ""+url
        SHOW(url)

elif mode==6:
        print ""+url
        SHOWSERIAL(url)
        
elif mode==7:
        print ""+url
        PLAY(url)

elif mode==8:
        print ""+url
        PLAYOL(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
