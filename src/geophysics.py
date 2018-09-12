# -*- coding: utf-8 -*-
# GoogleMap Geocode
# 曖昧な名前ではエラーが起こりやすい。
# 漢字が間違っているとエラーが返ってくる。
import requests
import urllib.parse
import json
def getGeocode(address):
    sensor = "false"
    url = 'http://maps.google.com/maps/api/geocode/json?'
    
    url_encode = urllib.parse.urlencode({'sensor': sensor, 'address': address})
    try:
        r = requests.get(url + url_encode)
        json_dict = json.loads(r.text)
        if json_dict["status"] == "OK":
            return json_dict
        elif json_dict["status"] == "OVER_QUERY_LIMIT":
            print("GEOCODE GoogleMapのアクセス制限に引っかかりました")
            return None
        else:
            print("GEOCODE 未確認のエラーが発生しました status:{}".format(json_dict["status"]))
            return None
    except:
        print("GEOCODE.py ERRER")
        return None
#getGeocode("野々市住吉")
