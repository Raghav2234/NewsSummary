from dbconfig import dbconfig
import requests
import scrapy
import json

db, dbconnected = dbconfig('newsum', 'mongodb://sarwar:sarwar123@ds255577.mlab.com:55577/newsum?retryWrites=false', 55577, 'sarwar', 'sarwar123')

if(dbconnected):
    print("connected to database")
else:
    print("not connected to database, no caching of result")   

data = []
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
    print("Hello")  
    main_url = "https://eventregistry.org/api/v1/article/getArticles?query=%7B%22%24query%22%3A%7B%22%24and%22%3A%5B%7B%22%24or%22%3A%5B%7B%22categoryUri%22%3A%22dmoz%2FBusiness%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FScience%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FHealth%22%7D%2C%7B%22categoryUri%22%3A%22dmoz%2FSports%22%7D%5D%7D%2C%7B%22lang%22%3A%22eng%22%7D%5D%7D%7D&dataType=news&resultType=articles&articlesSortBy=date&articlesCount=10&includeArticleCategories=true&articleBodyLen=-1&includeConceptLabel=false&includeConceptDescription=true&includeSourceTitle=false&includeSourceLocation=true&apiKey=7a0f2d98-d08b-4b08-b1f2-830bd7ae6883"
  
    # fetching data in json format 
    fetchHeadlines = requests.get(main_url).json()
  
    # getting all articles in a string article 
    article = fetchHeadlines["articles"]["results"] 
  
    # contain all trending news 
    results = [] 
    i = 1	
    for ar in article: 
        val = {
                 "id" : i,
                 "head_line" : ar["title"],
                 "content" : ar["body"], 
                 "tag" : getTag(ar["categories"][0]["label"]),
                 "img" : ar["image"]
        }
        i = i+1
        print(val)
        print(json.dumps(val, indent=4, sort_keys=True))

    for i in range(len(results)): 
        print(i + 1, results[i])  
	

HeadLines()
#for i in range(len(data)):
 #   print(db.News.insert_one(data[i]).inserted_id)
