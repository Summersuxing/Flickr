#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      simon
#
# Created:     03/04/2017
# Copyright:   (c) simon 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import weibo
import json
import datetime
from dateutil import parser
import pprint
import csv



# Your own App Information
APP_KEY = '2380632977'
APP_SECRET = '7013e4c8bb05fa5912b1b81d556e8d16'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'

class Stay():
     def __init__(self, init_time):
        self.inittime =init_time
        self.checkins = []

     def end(self,end_time):
        self.endtime =end_time
        self.innerduration =self.endtime-self.inittime
        self.isdaytripper = (True if self.innerduration <= datetime.timedelta(days=1) else False)
        self.issuredaytripper = (True if self.innerduration <= datetime.timedelta(days=1) and self.innerduration > datetime.timedelta(0) else False)

     def checkin(self,checkin):
        self.checkins.append(checkin)

     def beforeStay(self,bs_time):
        self.beforestaytime = bs_time

     def afterStay(self,as_time):
        self.afterstaytime = as_time


     def __str__(self):
        from pprint import pprint
        return str(pprint(vars(self)))

#This method reads a list of pois (hongkong) and generates stayevents for lists of pois check-in by some user.
def findStays(user_id, user_pois):
    lines = []
    #List of pois (in hongkong)
    with open('poiid.csv') as file:
        for line in file:
            line = line.strip() #or someother preprocessing
            lines.append(line)
    stay = None
    listofStays = []
    user_pois.reverse()
    for idx,j in enumerate(user_pois):
        #checkinlist[index-1]
        j_before = None
        #Selects predecessors ...
        if idx != 0:
            lastidx = idx-1
            j_before = user_pois[lastidx]
        if idx != len(user_pois)-1:
            comingidx = idx+1
            j_after = user_pois[comingidx]
            #before_d = j[3] - j_after[3]

        if j[0] in lines:
            if stay == None:
                print "new stay in Hongkong"
                stay = Stay(j[3])
                stay.checkins.append(j)
                stay.end(j[3])
                if j_before != None:
                    stay.beforeStay(j_before[3])
            else:
                if stay.inittime != None:
                    before_d = j[3] - stay.inittime #j_before[3]
                    #print before_d
                    #Stay can never be longer than 7 days
                    if before_d >= datetime.timedelta(days=7):
                        print "stay ends in Hongkong"
                        stay.afterStay(j[3])
                        listofStays.append(stay)
                        print "new stay in Hongkong"
                        stay = Stay(j[3])
                        stay.checkins.append(j)
                        stay.end(j[3])
                        if j_before != None:
                            stay.beforeStay(j_before[3])
                    else:
                        print "continue stay in Hongkong"
                        stay.checkins.append(j)
                        stay.end(j[3])

        else:
            if stay == None:
                pass
            else:
                print "stay ends in Hongkong"
                stay.afterStay(j[3])
                listofStays.append(stay)
                stay = None
            print "stay outside Hongkong"

    with open(str(user_id)+".csv",'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['innerduration', 'isdaytripper', 'issuredaytripper', 'endtime','inittime'])
        for i in listofStays:
            if i != None:
                writer.writerow([str(i.innerduration), str(i.isdaytripper), str(i.issuredaytripper), str(i.endtime),str(i.inittime) ])





    return listofStays


def run():
        #client = weibo.Client(APP_KEY, APP_SECRET, CALLBACK_URL, username='jiayousuxing@163.com', password='13956413801')
        #url = client.authorize_url #'https://api.weibo.com/oauth2/authorize?redirect_uri=https%3A%2F%2Fapi.weibo.com%2Foauth2%2Fdefault.html&client_id=2380632977'
        #print url
        token = {}
        token['uid'] =''
        token['access_token'] = '2.00JhHijFF5tGbCe2bfdb1a1fr5sy7C'
        token['expires_at'] =''

        c2 = weibo.Client(APP_KEY, APP_SECRET, CALLBACK_URL, token)

        #print c2.get('users/show', uid=2441081134)
        ##print c2.get('statuses/user_timeline', access_token='2.00JhHijFF5tGbCe2bfdb1a1fr5sy7C' , uid=2441081134)
        #print c2.get('statuses/friends_timeline', uid=2441081134)
        ##print c2.get('statuses/timeline_batch', uids='2441081134')
        pois = c2.get('place/users/checkins', uid=1996524755)['pois']



        #poiinfo = c2.get('place/pois/show', poiid='B2094750D36AA2FD4193')
        #print poiinfo
        user_pois =[]
        #print pois
        for i in pois:
            poi_id =i['poiid']
            #print c2.get('place/poi_timeline', poiid=poi_id)
            poi_lat =i['lat']
            poi_lng =i['lon']
            poi_time =i['checkin_time']
            user_pois.append([poi_id, poi_lat, poi_lng,parser.parse(poi_time)])

        #print user_pois

        listofstays = findStays(1996524755, user_pois)




        #lat_long_file = open("poi.txt", "r")






if __name__ == '__main__':
    run()
