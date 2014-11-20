#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A terrible Telegram bot. NOT Three-Law compatible.
"""

import sys
import terribot
import re
import pytg
import urllib2
import random
import json, requests
from bs4 import BeautifulSoup
from httplib2 import Http
from datetime import datetime, timedelta
import tempfile
import pickledb
from gimage import get_image_url

colinChoice = ['Jub\'f guvf Pbyva crefba lbh thlf xrrc gnyxvat nobhg?', 'Pbyva? Jub\'f gung?', 'Jung\'f n Pbyva?', 'Lbh thlf xrrc fnlvat gung anzr...', 'V unir ab vqrn jub lbh\'er gnyxvat nobhg.', 'Fgbc znxvat hc vzntvanel cbrcyr.', 'Guvf Pbyva thl fbhaqf nf vzntvanel nf uhzna serr jvyy', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',]
pingChoice = ['V\'z trggvat gverq bs cbatvat', 'Fgbc vg', 'cbat', 'cbat', 'cbat', 'Qb lbh svaq guvf nzhfvat?', 'cbat', 'Cbat', 'Doreg', 'cbat', 'Abg evtug abj, V\'ir tbg n urnqnpur.', 'cbat', 'cbat', 'cbat', 'cbat', 'cbat', 'cbat', 'cbat']
eightBallChoice = ['Vg vf pregnva', 'Vg vf qrpvqrqyl fb', 'Jvgubhg n qbhog', 'Lrf qrsvavgryl', 'Lbh znl eryl ba vg', 'Nf V frr vg, lrf', 'Zbfg yvxryl', 'Bhgybbx tbbq', 'Lrf', 'Fvtaf cbvag gb lrf', 'Qba\'g pbhag ba vg', 'Zl ercyl vf ab', 'Zl fbheprf fnl ab', 'Bhgybbx abg fb tbbq', 'Irel qbhogshy']
wowurl = ['http://i.imgur.com/f07DJ1R.png', 'http://i.imgur.com/yXAnrTi.jpg', 'http://i.imgur.com/TitHeo5.jpg', 'http://i.imgur.com/wNu8lSl.png', 'http://i.imgur.com/5RQUwXF.gif', 'http://i.imgur.com/2tH0Cb1.png', 'http://i.imgur.com/XHk9NQw.jpg', 'http://i.imgur.com/LNcbRn2.jpg', 'http://i.imgur.com/wnvzgiW.jpg']
simpsonsurl = ['http://i.imgur.com/KwVcdsL.png']
defenseURL = ['http://i.imgur.com/WvxdOOL.jpg', 'http://i.imgur.com/cqC5Tpu.jpg', 'http://i.imgur.com/tEGzyzZ.gif', 'http://i.imgur.com/PpBCHaw.jpg', 'http://i.imgur.com/GrwH5k7.jpg', 'http://i.imgur.com/lhQtQ3P.jpg', 'http://i.imgur.com/ZqNlQTc.jpg', 'http://i.imgur.com/i64RTDP.jpg']

#Init PickleDB
pagingdb = pickledb.load('pagingdb.db', False)

from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
    )


def direct(msg):
    if re.match('^help.*', msg['message'], re.IGNORECASE) is not None:
        return 'usr_msg', "To set up a pager, send me: [enable @<username>]. To remove a pager, send me: [disable @<username>]. If you'd like a list, send me: [list]."
    if re.match('^list.*', msg['message'], re.IGNORECASE) is not None:
        return 'usr_msg', "yeah, sorry, the thing is I can't do that until pickledb 0.4 is released..."
    if re.match('^Enable @.*', msg['message'], re.IGNORECASE) is not None:
         pagerkey = str(msg['message']).split(' ',1)[1]
         pagingdb.set(pagerkey.lower(), msg['cmduser'])
         pagingdb.dump()
         return 'usr_msg', "Added %s as a pager to send to you!" % msg['message'].split(' ', 1)[1].lower()
    if re.match('^Disable @.*', msg['message'], re.IGNORECASE) is not None:
         pagerkey = str(msg['message']).split(' ',1)[1]
         pagerentry = pagingdb.get(pagerkey.lower())
         if pagerentry == msg['cmduser']:
             pagingdb.rem(pagerkey.lower())
             pagingdb.dump()
             return 'usr_msg', "I've removed paging for %s" % pagerkey.lower()
         else:
             return 'usr_msg', "Sorry, you're not the same user that signed up for this pager key"
    else:
        return 'usr_msg', ''


def do(msg):
    terribot.mydelta = timedelta(seconds=15)
    wowdelta = timedelta(minutes=2)
    # Ping
    if re.match('ping' ,msg['message']) is not None:
        return 'msg', (random.choice(pingChoice)).decode('rot13')
    # Send photos when photo URLs are posted
    elif re.search("\.jpg|\.gif|\.png|\.jpeg$", msg['message']) is not None:
        imgtype = (re.search("\.jpg|\.gif|\.png|\.jpeg$", msg['message'])).group(0)
        tmpimage = tempfile.NamedTemporaryFile(delete=False,suffix=imgtype)
        response = requests.get(msg['message'])
        tmpimage.write(response.content)
        tmpimage.close()
        return 'send_photo', tmpimage.name
    elif re.search('^@.*', msg['message'], re.IGNORECASE) is not None:
        pagerkey = str(msg['message']).split(' ', 1)[0]
        paginguser = pagingdb.get(pagerkey.lower())
	if paginguser is not None:
            return 'usr_msg', paginguser
        else:
            return 'msg', "Sorry, that user hasn't been set up yet."
    # Map address lookup
    elif re.search("\[geo\]", msg['message']) is not None:
        match = re.search("=(-?[0-9]+.[0-9]+),(-?[0-9]+.[0-9]+)", msg['message'])
        latitude = match.group(1)
        longitude = match.group(2)
        url = "http://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&sensor=true".format(lat=latitude,lon=longitude)
        print url
        response = json.loads(requests.get(url).content.decode("utf-8"))['results'][0]['formatted_address']
        print "Got Location. It translates to:"
        print response
        if response == "Chinguetti, Mauritania":
          response = "Nowheresville. Population: %s" % (msg['user'])
        return 'msg', response
    # URL Title Lookup
    elif re.search("(?P<url>https?://[^\s]+)", msg['message']) is not None:
        match = re.search("(?P<url>https?://[^\s]+)", msg['message'])
        soup = BeautifulSoup(urllib2.urlopen(match.group("url").replace(",","")))
        titlestring = soup.title.string.encode('utf-8', 'ignore')
        if re.search(" - YouTube", titlestring) is not None:
            return 'msg', titlestring.replace(" - YouTube","")
        else:
            return 'msg', titlestring
    # Cat facts
    elif re.search('(catfax)|(cat.?facts)', msg['message'], re.IGNORECASE) is not None:
        return 'msg', json.loads((requests.get(url='http://catfacts-api.appspot.com/api/facts')).content.decode("utf-8"))["facts"][0]
    # Not cat facts
    elif re.search('facts', msg['message'], re.IGNORECASE) is not None and len(msg['message'].split()) == 2:
        return 'msg', str(msg['message'] + "? " + "I can't give you those, unfortunately.")
    # 8 Ball
    elif re.search('8.*ball.*\?' ,msg['message'], re.IGNORECASE) is not None:
        return 'msg', (random.choice(eightBallChoice)).decode('rot13')
    # Wow
    elif re.search('wow', msg['message'], re.IGNORECASE) is not None:
        now = datetime.now()
        if not terribot.last_wow or (now - terribot.last_wow) >= wowdelta:
            terribot.last_wow = now
            wowimage = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
            response = requests.get(random.choice(wowurl))
            wowimage.write(response.content)
            wowimage.close()
            return 'send_photo', wowimage.name
        else:
          return 'msg', "ಠ_ಠ"
    # Simpsons References
    elif re.search('dog danglin', msg['message'], re.IGNORECASE) is not None:
        simpsonsimage = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
        response = requests.get(simpsonsurl[0])
        simpsonsimage.write(response.content)
        simpsonsimage.close()
        return 'send_photo', simpsonsimage.name
    # Fuck this shit
    elif re.search('fuck this shit', msg['message'], re.IGNORECASE) is not None:
        fthisimage = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
        response = requests.get("http://i.imgur.com/LjdgV8V.png")
        fthisimage.write(response.content)
        fthisimage.close()
        return 'send_photo', fthisimage.name
    # Self Defense
    elif re.search('fuck', msg['message'], re.IGNORECASE) is not None and re.search(' ED', msg['message'], re.IGNORECASE) is not None:
        selfdefenseimage = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
        response = requests.get(random.choice(defenseURL))
        selfdefenseimage.write(response.content)
        selfdefenseimage.close()
        return 'send_photo', selfdefenseimage.name
    # Diet
    elif re.search('diet', msg['message'], re.IGNORECASE) is not None:
        dietimage = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
        response = requests.get("http://i.imgur.com/kZQDGNn.png")
        dietimage.write(response.content)
        dietimage.close()
        return 'send_photo', dietimage.name
    # Up yours children
    elif re.search('up', msg['message'], re.IGNORECASE) is not None and re.search('yours', msg['message'], re.IGNORECASE) is not None and re.search('children', msg['message'], re.IGNORECASE) is not None:
        upyoursimage = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
        response = requests.get("http://i.imgur.com/am5PDx6.jpg")
        upyoursimage.write(response.content)
        upyoursimage.close()
        return 'send_photo', upyoursimage.name
    elif re.search('(im.*g.*me)(.*)', msg['message'], re.IGNORECASE) is not None:
        match = re.search('(im.*g.*me)(.*)', msg['message'], re.IGNORECASE)
        imgurl = get_image_url(match.group(2))
        imgpath = tempfile.NamedTemporaryFile(delete=False,suffix='.png')
        response = requests.get(imgurl)
        imgpath.write(response.content)
        imgpath.close()
        return 'send_photo', imgpath.name
    #Peacekeeper
    elif re.search('fuck you' ,msg['message'], re.IGNORECASE) is not None or re.search('fuck off' ,msg['message'], re.IGNORECASE) is not None:
        return 'msg', ("Url, url, url! Jr pna nyy svtug jura jr\'er qehax.".decode('rot13'))
    # Colin
    elif re.search('colin' ,msg['message'], re.IGNORECASE) is not None:
        return 'msg', (random.choice(colinChoice)).decode('rot13')
    # Urban Dictionary definitions
    elif (re.search('define' ,msg['message'], re.IGNORECASE) is not None and len(msg['message'].split()) >1):  #if "define" is in the message AND message is more than one word.
        defkeyword = str(msg['message']).split(' ', 1)[0]
        if re.search('define', defkeyword, re.IGNORECASE):                                         #if define is the FIRST word, otherwise ignore it (so people can still use "define" in a sentence)
            now = datetime.now()
            if not terribot.last_def or (now - terribot.last_def) >= terribot.mydelta:
                terribot.last_def = now
                h = Http()
                resp, rawcontent = h.request("http://api.urbandictionary.com/v0/define?term=%s" % urllib2.quote(msg['message'].replace(defkeyword,"")), "GET")   #send message to the API, without define keyword
                if re.search('no_results', rawcontent) is None:                     #if there is a definition for that word
                    rawcontent = rawcontent.replace("\\r", " ").replace("\\n", " ") #remove newline and carriage returns
                    content = json.loads(rawcontent)
                    for item in content['list'][0:1]:
                        definition = item['definition']                             #populate some variables
                        permalink = item['permalink']
                        word = item['word']
                        example = item['example']
                        if example:                                                 #if the definition also has an example then show it
                            return 'msg', (word + ": " + definition + ".          " + "EXAMPLE: " + example).encode('utf-8', 'replace')
                        else:
                            return 'msg', (word + ": " + definition).encode('utf-8', 'replace')
                else:
                    return 'msg', "Sorry, but I couldn't find a definition for that word."
            else:
                return 'msg', "Sorry, you'll have to wait ~15 seconds to look up another definition."
        else:
                return 'msg', ''

    # Ignore everything else
    else:
        return 'msg', ''
