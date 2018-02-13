# -*- coding: utf-8 -*-

from googlemaps import GoogleMaps
gmaps = GoogleMaps()
address = u'$B2,;3;T(B'
lat, lng = gmaps.address_to_latlng(address)
print(lat)
print(lng)

# GoogleMap Geocode
# $B[#Kf$JL>A0$G$O%(%i!<$,5/$3$j$d$9$$!#(B
# $B4A;z$,4V0c$C$F$$$k$H%(%i!<$,JV$C$F$/$k!#(B
# $B1Q8l$J$i$PDL$k$,!"F|K\8l$@$H8!:w$G$-$J$$!#%(%s%3!<%I$N$b$s$@$$!)!)!)(B
# urlencode$B;H$C$F$b(Bquote$B;H$C$F$b!"JQ49$O$G$-$k$,!"(Bapi$B$,FI$a$k$b$N$K$O$J$i$J$$(B
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

#get_geocode(u"$BLn!9;T=;5H(B")
