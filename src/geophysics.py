# -*- coding: utf-8 -*-
# GoogleMap Geocode
# 曖昧な名前ではエラーが起こりやすい。
# 漢字が間違っているとエラーが返ってくる。
import requests
import urllib.parse
import json
def get_geocode(address):
    sensor = "false"
    url = 'http://maps.google.com/maps/api/geocode/json?'
    
    url_encode = urllib.parse.urlencode({'sensor': sensor.encode("utf-8"), 'address': address.encode("utf-8")})
    try:
        r = requests.get(url + url_encode)
        json_dict = json.loads(r.text)
        print(json_dict)
        return json_dict
    except:
        print("GEOCODE.py ERRER")
        return None
#get_geocode("野々市住吉")
