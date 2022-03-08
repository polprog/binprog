#!/usr/bin/env python3

from urllib.request import urlopen
from urllib.error import URLError

import simplejson

ukeurl_base = 'https://numeracja.uke.gov.pl/pl/%s?draw=2&columns[0][data]=id&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][regex]=false&columns[1][data]=scope&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][regex]=false&order[0][column]=1&order[0][dir]=asc&start=0&length=10&search[value]=%s&search[regex]=false'

def print_pstn(numer):
    return "PSTN: %s: [%s] %s, AB=%s (%s, %s)" % (
    numer['scope'], numer['provider_id'], numer['provider_name'], numer['zone_ab'], numer['zone_name'], numer['zone_symbol'])

def print_plmn(numer):
    return "PLMN: %s: [%s] %s" % (
    numer['scope'], numer['provider_id'], numer['provider_name'])

def print_ndsi(numer):
    return "NDSI: %s: [%s] %s" % (
    numer['scope'], numer['provider_id'], numer['provider_name'])

def print_aus(numer):
    return "AUS: %s: [%s] %s, AB=%s (%s, %s)" % (
    numer['scope'], numer['provider_id'], numer['provider_name'], numer['zone_ab'], numer['zone_name'], numer['zone_symbol'])

def print_ndin(numer):
    return "AUS: %s: [%s] %s, %s" % (
    numer['scope'], numer['provider_id'], numer['provider_name'], numer['service_type_name'])

def print_voip(numer):
    return "VOIP: %s: [%s] %s" % (
    numer['scope'], numer['provider_id'], numer['provider_name'])
    


ukeurls = {'plmn_tables.json':print_plmn, 'pstn_tables.json':print_pstn, 'aus_tables.json':print_aus, 'ndin_tables.json':print_ndin, 'ndsi_tables.json':print_ndsi, 'voip_tables.json':print_voip}


def abspqmcdu(x):
    json = {}
    for url, method in ukeurls.items():
        print("M=", method)
        try:
            json = simplejson.load(urlopen(ukeurl_base  % (url, x)))
            if json['data'] == []:
                print("Not in", url)
            else:
                msg = method(json['data'][0])
                if(len(json['data']) > 1):
                    msg = msg + "  [+" +str(len(json['data']) - 1) + " records]"
                return msg+"\r\n"
        except URLError as e:
            print(str(e.reason))
            
    return "E005 not found in any table\r\n"

if __name__ == "__main__":
    print(abspqmcdu("700"))
    print(abspqmcdu("70"))
    print(abspqmcdu("22"))
    print(abspqmcdu("50"))
    print(abspqmcdu("48"))
    print(abspqmcdu("3911"))

