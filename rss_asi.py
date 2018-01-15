# python3
import urllib.request
import json
import codecs
import xml.etree.cElementTree as ET
import datetime
import time
import email.utils
import sys

def datetime_to_rfc822(dt):
    return email.utils.formatdate(time.mktime(dt.timetuple()))
def iso8601_to_rfc822(chain):
    dt = datetime.datetime.strptime(chain.replace(":", ""), "%Y-%m-%dT%H%M%S%z")
    return datetime_to_rfc822(dt)

def createRSS(numElts, out=sys.stdout.buffer):
    base_path = "https://www.arretsurimages.net"
    base_api = "https://api.arretsurimages.net/api/public"
    url = base_api + "/search?q="

    req = urllib.request.Request(url, headers={"range": "objects 0-%d" % (numElts-1)})
    with urllib.request.urlopen(req) as f:
        obj = json.load(codecs.getreader("utf-8")(f))
        hits = obj["hits"]["hits"]

    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")
    ET.SubElement(channel, "title").text = "Arrêt sur Images"
    ET.SubElement(channel, "link").text = base_path
    ET.SubElement(channel, "lastBuildDate").text = datetime_to_rfc822(datetime.datetime.now())

    for hit in hits:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = hit["title"]
        ET.SubElement(item, "pubDate").text = iso8601_to_rfc822(hit["updated_at"]) # "published_at"?
        ET.SubElement(item, "link").text = "%s/%s" % (base_path, hit["path"])
        img = '<br><img src="%s/media/%s/action/show?format=thumbnail">' % (base_api, hit["thumbnail"]["slug"])
        ET.SubElement(item, "description").text = '%s<br>%s%s' % (hit["lead"], hit["tease"], img)

    ET.ElementTree(root).write(out)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        createRSS(30)
    else:
        createRSS(30, out=sys.argv[1])
