import sys
import feedparser

etag=sys.argv[1] #a tag used to verify if the feed changed since the last check

feedURL='http://s3.spotcrime.com/cache/rss/chicago.xml'
feed=feedparser.parse(feedURL,etag=etag) #open the feed

#the feed hasn't changed since the last time we checked
if feed.status == 304:
    print "The feed has not changed since the last time you checked"
#we have new entries in the feed
elif feed.status == 200:
    print "New etag: %s" %feed.etag
    for entry in feed.entries:
        content = entry.summary
        lat,lon = '0','0'
        if 'geo_lat' in entry: lat = entry['geo_lat']
        if 'geo_long' in entry: lon = entry['geo_long']
        print "%s,%s,%s" %(content,lat,lon)
else:
    print "Feed returned status code %d" %feed.status
