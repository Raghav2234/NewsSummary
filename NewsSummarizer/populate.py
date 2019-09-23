from .dbconfig import dbconfig
import time
import requests
import scrapy
import json
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def Summarizer(arg):
    parser = PlaintextParser.from_string(arg,Tokenizer("english"))
    summarizer = LexRankSummarizer()
    #Summarize the document with 2 sentences
    summary = summarizer(parser.document, 4)
    string_summary = ""
    for sentence in summary:
       string_summary += str(sentence) 
    return string_summary


def getTag(arg):
    s = ""
    f = 0
    for i in range(len(arg)):
        if(f == 1 and arg[i] == '/'):
            break
        if(f == 1) :
            s += arg[i]
        if(arg[i] == '/' and f == 0):
            f = 1
            continue
    return s


def HeadLines(): 
    main_url = "https://www.google.com/url?q=https://eventregistry.org/api/v1/article/getArticles?query%3D%257B%2522%2524query%2522%253A%257B%2522%2524and%2522%253A%255B%257B%2522%2524or%2522%253A%255B%257B%2522categoryUri%2522%253A%2522dmoz%252FBusiness%2522%257D%252C%257B%2522categoryUri%2522%253A%2522dmoz%252FHealth%2522%257D%252C%257B%2522categoryUri%2522%253A%2522dmoz%252FSociety%2522%257D%252C%257B%2522categoryUri%2522%253A%2522dmoz%252FScience%2522%257D%252C%257B%2522categoryUri%2522%253A%2522dmoz%252FSports%2522%257D%255D%257D%252C%257B%2522lang%2522%253A%2522eng%2522%257D%255D%257D%257D%26dataType%3Dnews%26resultType%3Darticles%26articlesSortBy%3Ddate%26articlesCount%3D50%26includeArticleCategories%3Dtrue%26includeArticleLocation%3Dtrue%26includeArticleImage%3Dtrue%26articleBodyLen%3D-1%26includeConceptImage%3Dtrue%26apiKey%3D7a0f2d98-d08b-4b08-b1f2-830bd7ae6883&source=gmail&ust=1569321839220000&usg=AFQjCNEdvkbM0CHoUY6avYwySs3smT7JDw"
    fetchHeadlines = requests.get(main_url).json()
    article = fetchHeadlines["articles"]["results"] 
    data = []
    for ar in article: 
        val = {
                 "head_line" : ar["title"],
                 "content" : Summarizer(ar["body"]), 
                 "tag" : getTag(ar["categories"][0]["label"]),
#                  "tag" : sports,
                 "img" : ar["image"],
                 "dateTime" : ar["dateTime"],
                 "src" : ar["source"]["uri"],
                 "url" : ar["url"]
        }
        data.append(val)
    return data


def update_news():
    global db, dbconnected
    if not dbconnected:
        print("not connected  to database, no caching of result")
        return
    db.News.drop()
    datas = HeadLines()
    for data in datas:
        db.News.insert_one(data).inserted_id
    print ("News successfully updated.")


def schedule():
    print("Scheduler started")
    global db, dbconnected, data
    while True:
        time.sleep(60*60*24)
        update_news()


def retrieve_data():
    global db, dbconnected
    if not dbconnected:
        print("not connected to database, no caching of result")
        return None, False

    cursor = db.News.find({})
    collections = {}
    for document in cursor:
        pid = str(document['_id'])
        collection = {}
        for key, value in document.items():
            if key == '_id':
                continue
            collection[key] = str(value)
        collections[pid] = collection
    return collections, dbconnected


db, dbconnected = dbconfig('newsum', 'mongodb://sarwar:sarwar123@ds255577.mlab.com:55577/newsum?retryWrites=false', 55577, 'sarwar', 'sarwar123')
