# -*- coding: utf-8 -*-

from googlemaps import GoogleMaps
gmaps = GoogleMaps()
address = u'岡山市'
lat, lng = gmaps.address_to_latlng(address)
print(lat)
print(lng)

# GoogleMap Geocode
# 曖昧な名前ではエラーが起こりやすい。
# 漢字が間違っているとエラーが返ってくる。
# 英語ならば通るが、日本語だと検索できない。エンコードのもんだい？？？
# urlencode使ってもquote使っても、変換はできるが、apiが読めるものにはならない
import requests
import urllib.parse
def get_geocode(address):
    sensor = "false"
    url = 'http://maps.google.com/maps/api/geocode/json?'
    
    url_encode = urllib.parse.urlencode({'sensor': sensor.encode("utf-8"), u'address': address.encode("utf-8")})
    print('test : {}'.format( urllib.parse.quote(address.encode("utf-8")) ))
    print(url + url_encode)
    r = requests.get(url + url_encode)
#    r = requests.get('https://api.r6stats.com/api/v1/players/{}?platform={}'.format(address, sensor))
    print(r)

#get_geocode(u"野々市住吉")
