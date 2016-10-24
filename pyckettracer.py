#! /usr/bin/env python


import sys
from scapy.all import sr,sr1,IP,ICMP,TCP,UDP,conf
from datetime import datetime, time
from socket import gethostbyname
import logging
import geoip2.database

def get_times(ans):
    for pack in ans:
        yield pack[1].time - pack[0].sent_time

if __name__ == '__main__':
    # sssssh
    conf.verb=0
    dest = sys.argv[1] if len(sys.argv) > 1 else 'google.com'
    try:
        dest_ip = gethostbyname(dest)
    except:
        dest_ip = dest

    georeader = geoip2.database.Reader('GeoLite2-City.mmdb')
    for i in range(1,100):
        p=IP(dst=dest,ttl=i)/ICMP()
        ans = sr1(p, retry=0, timeout=1)
        # ans.show()
        print i,
        if not ans:
            print '?'
            continue

        try:
            georesp = georeader.city(ans.src)
            geocity = (georesp.city.name, \
                       georesp.country.name, \
                       [georesp.location.latitude, \
                       georesp.location.longitude])
        except geoip2.errors.AddressNotFoundError:
            geocity = None

        print ans.type, ans.src, geocity

        if ans.type == 0 or ans.src == dest_ip:
            print "stop"
            break
        # if len(ans):
        #     snd,rcv = ans[0]
        #     print snd
        #     print rcv
