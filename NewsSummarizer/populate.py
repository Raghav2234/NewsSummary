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
    main_url = "https://eventregistry.org/api/v1/article/getArticles?query=%7B%22%24query%22%3A%7B%22%24and%22%3A%5B%7B%22%24or%22%3A%5B%7B%22categoryUri%22%3A%22dmoz%2FBusiness%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FHealth%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FSociety%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FScience%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FSports%22%7D%5D%7D%2C%7B%22lang%22%3A%22eng%22%7D%5D%7D%7D&dataType=news&resultType=articles&articlesSortBy=date&articlesCount=50&includeArticleCategories=true&includeArticleLocation=true&includeArticleImage=true&articleBodyLen=-1&includeConceptImage=true&apiKey=7a0f2d98-d08b-4b08-b1f2-830bd7ae6883"
    fetchHeadlines = requests.get(main_url).json()
    article = fetchHeadlines["articles"]["results"] 
    data = []
    for ar in article: 
        val = {
                 "head_line" : ar["title"],
                 "content" : Summarizer(ar["body"]), 
                 "tag" : getTag(ar["categories"][0]["label"]),
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
        print("not connected to database, no caching of result")
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
