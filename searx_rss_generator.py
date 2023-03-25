import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from dateutil.parser import parse
from datetime import datetime, timedelta
import schedule
import time
import xml.etree.ElementTree as ET
import feedparser

def age_within_hours(date_string, hours):
    date = parse(date_string)
    now = datetime.utcnow()
    return (now - date) <= timedelta(hours=hours)

def generate_opml(feed_info):
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = "Searx OPML Feed for {}".format(feed_info["search_query"])

    body = ET.SubElement(opml, "body")
    outline = ET.SubElement(body, "outline", text=feed_info["title"], title=feed_info["title"], type="rss", xmlUrl=feed_info["rss_url"])

    opml_string = ET.tostring(opml, encoding="utf-8", method="xml").decode("utf-8")
    
    with open("searx_opml_feed.xml", "w") as f:
        f.write(opml_string)

    print("OPML feed generated at", datetime.utcnow())
    
def validate_feed(feed_path):
    result = feedparser.parse(feed_path)

    if result.bozo == 0:
        print(f"{feed_path} is valid.")
    else:
        print(f"{feed_path} is not valid.")
        print(f"Error: {result.bozo_exception}")

def generate_rss_feed():
    search_query = "prova"
    searx_instance_url = "https://freesearch.club"
    prefs_url = "https://freesearch.club/preferences?preferences=eJx1V02T2zYM_TX1RRNP2xw6PfjUmV7bmaRnDkTBEiKS4PLDsvbXF7Qki1pvDlFMkATAB-ABqyFhz4EwXnp0GMCcDLg-Q48XdF_--3YyrMHghdIJcmLN1htMeDmRlTPKB77Pl-8h48liGri7_PvPt--nCFeMCEEPl19PaUCLl0jl5ilgzCZFxU45nFSCdrndMSnZY3PDcGGQ5ZlDf1puqZhm8aE4cNLoEgYFhnpn5fdyHbobOI2dWq3-DSbi6S1jmBU5lSjJ_UVI7kqOkijVgY1ZzVOE1sh9dD05QePPHnqlImsC01jsCH75_S_wY2MpBA5KXclgfMjEwUa-TUwcsNoQP-iGDUWlVmxF2lJqsx4xKUVJ1lrrL-mm1I065HJNnIox4FWMa0J5k8hm9LUOnYMh_CAJcnauZR3iuwClbI6ky7rrmw4fbyd2B6cw8ESdUiyhCrKeaKQOEhzUidflX8-fS5tHQoja5f_j3oRQVO8WFtQseLkg3-KD5R_kC9D7qSShmA8P_e1eGbh2gYvbG-LXgNhEvqYJAjYdBdQSknlF-hrIjQS6UtBTL1GHmGoTveQKtFt4uMMWQ78ue-Ze_PYG5hLyuNuudyzfqCDxjGnvuevqWAzQBiifVS_Zrt2fTQ6qy-TkJ3GOn8s2lT8oDrzrGEmPECsHDYnJMDfloZEOG66_HUJtuI0JzyGu3sG7mQPpypjUOmgPbj3gvN1-zQC7avboAnqurHkQv3qKW_773J47vK2rpXoL6E35PCMHFor_-DxmwSXSTdQDGwh1rSQeZ04sYIzFv81umigV3vhY0jMMfMjoidpDGVkIwghi_gCRUOIdXBeO0lI3LfMYPwqF6kRWvqvgLXPCj6ci56BfpEKIkdL8Iua5EHBdi6TTO7tjvXz9-sd9R6HLHbo9SSK-O7D1eQe3AtIuCLmde7RbKnjEkHKLVS4-kBSFoyT9NGFbbYVshVQrwcR3GtlJxJs4O3azxcqbH_7sJ3ekISt8VfvjJfPMkiY_Eb8SkaTOnswLyENOe0k_FZ3QHbvAQ58USL43xZmtHoLkXqUfwp1udQ62khoarN8Lptxeya3uBa7_uH71_iE9JNBDsmBaYdumjvr-WHwld7CmZLyRVI48oBay9KPQDHkjPUyzZSfProJzNUIooeZOdFTzj6xTgXIBldKubqHGA8UuZPny1FV-eOwqe3nuKv-EAYbV3sP4Rnt8FUZxvYwYtUFLd204dxWzgTQJ3Hi5YAjSR0ozjChjS2Vm2xMGE2xgbarH_ZikJSVpcFuX812pnf2QH4Sr3HOXgsxjLcwVX-ZWCuxwZfZbIr5NEswa2IfgiN8ieoF6Eb-gKk_tKL2wZERPsFXd87CUkuT5Eb8ojWFkybur4WmrlzjmNruUtxLMHkOOT5RjSUj_gc1kFKRO2rfMNanqH9lF6bFxqJ7yoPDjo2fOH1jqKXmOQ0BG0ryErTp2I4tcExaN5QSUKeJJS2yWjuSHalaxwmVWpo0mBXDRSByrgUpmG8TxQOEcOkdjpTWlcKaK_SRvbzsi-4TqTRZyipcSjvt5XZ0Hjkm4HGWIFnweiXI8YIRK08r6tVxerCQJR5zjk_5-YqLAvixetDCoZYKfglh52V5TR6DWyx8cswzqRsazT06aq0zsV37ZkVxQekA9vu4EKAymZCwWD2zJvpOMAVJ-l_8BjlbdhA==&save=1"
    params = {"q": search_query, "format": "html"}

    prefs_response = requests.get(prefs_url)
    prefs_soup = BeautifulSoup(prefs_response.text, "html.parser")
    prefs_input = prefs_soup.find("input", {"name": "settings"})

    if prefs_input:
        prefs_value = prefs_input["value"]
        params["settings"] = prefs_value

    response = requests.get(f"{searx_instance_url}/search", params=params)

    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", class_="result")

    fg = FeedGenerator()
    fg.title("Searx RSS Feed for {}".format(search_query))
    fg.link(href=searx_instance_url, rel="alternate")
    fg.description("An RSS feed for the search query '{}' on Searx.".format(search_query))

    for result in results:
        title = result.find("a", class_="result_title").get_text()
        link = result.find("a", class_="result_title")["href"]
        content = result.find("p", class_="content").get_text()
        date_string = result.find("span", class_="label").get_text()

        if age_within_hours(date_string, 4):
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=link)
            fe.description(content)

    rss_feed = fg.rss_str(pretty=True).decode("utf-8")

    with open("searx_rss_feed.xml", "w") as f:
        f.write(rss_feed)

    print("RSS feed generated at", datetime.utcnow())
    
    feed_info = {
        "search_query": search_query,
        "title": "Searx RSS Feed for {}".format(search_query),
        "rss_url": "http://localhost:8000/rss"
    }
    
    generate_opml(feed_info)
    validate_feed("searx_rss_feed.xml")

schedule.every(4).hours.do(generate_rss_feed)

generate_rss_feed()

while True:
    schedule.run_pending()
    time.sleep(60)
