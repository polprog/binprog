#!/usr/bin/env python3

# Whee for PAA for not having an api... I hope they don't change the site
# layout.

from urllib.request import urlopen
from urllib.error import URLError
import re
import simplejson

url = 'https://mapa.paa.gov.pl/'


def checkRadiation(city):
    city = city.casefold()
    try:
        sitepayload = urlopen(url).read().decode('utf-8')
    except URLError as e:
            return "E005: " + str(e.reason)
        
    find = re.findall("data_object = ({.*});", sitepayload)
    #print(find)
    if find == []:
        return "E005 Cannot find data_object in site code"

    #print(type(find[0]))
    jsondata = simplejson.loads(find[0])
    for key,record in jsondata.items():
        #print(key, "--->", record['nazwa'])
        if record['nazwa'].casefold() == city:
            return "I003 " + record['nazwa'] + ": " + record['wartosc'] + " µSv/h [pomiar z " \
                + record['data'] + " " + record['godzina'] + "]"
        
    return "E006 Cannot find city, try nearest larger city."

if __name__ == "__main__":
    print(checkRadiation("Rzeszow"))
    print(checkRadiation("Kraków"))
    print(checkRadiation("Warszawa"))
    print(checkRadiation("ZiElOnA GoRa"))
    print(checkRadiation("NOWHERE "))
