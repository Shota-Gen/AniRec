# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import sqlite3
import csv

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


def createTable():
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    cur.execute(""" CREATE TABLE IF NOT EXISTS AnimeTable(
                anime_id INTEGER PRIMARY KEY,
                anime_name TEXT,
                genre TEXT,
                anime_type TEXT, 
                episodes REAL,
                rating REAL,
                members INTEGER)""")
    #cur.execute(""" CREATE INDEX IndexID ON AnimeTable""")
    conn.commit()
    print("table created")
    with open('anime.csv', 'r') as csvfile:
        no_records = 0
        reader = csv.reader(csvfile)
        i = 0
        while i < 12294:  # should probably adjust this, make it a variable & find an updated database
            row = list()
            row.extend(reader.next())
            # prints a whole row, confirming that reader.next() is a list
            # adds each anime into the table
            if row[5] and (int(row[6]) > 1000):  # requirements: has to have rating & min. of 1000 reviews
                cur.execute("INSERT OR IGNORE INTO AnimeTable VALUES (?,?,?,?,?,?,?)", row)
                conn.commit()
                no_records += 1
            i += 1
    conn.close()
    print("\n{} built".format(no_records))  # prints how many anime were actually inserted into table


def getRatingList():  # USELESS
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    cur.execute("SELECT rating FROM AnimeTable")
    conn.commit()
    rating_list = list()
    f_rating_list = list()
    rating_list.extend(cur.fetchall())
    conn.close()
    i = 0
    while i < 6791:  # removes the coma at end from every number
        f_rating_list.extend(rating_list[i])
        i += 1
    return f_rating_list


def getGenreList():  # returns list of all genres in table
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    cur.execute("SELECT genre FROM AnimeTable")
    conn.commit()
    genre_list = list()
    genre_list.extend(cur.fetchall())
    conn.close()
    return [genre.translate(None, ",") for genre in genre_list]


def getAnimeID(index):  # gets the AnimeID of specified index in the sorted AnimeID LIst
    # so I can use this to get like the 10th most popular anime
    # CHANGE this so I sort list by other parameter first then I can choose like the 10th most popular anime in a genre
    id_list = sortAnimeID()
    return id_list[index][0]  # for some reason treats the id/# as one element & the comma as the 2nd ***


def sortRating():  # sort table by rating = USELESS
    totalCount = 6790
    ratingList = getRatingList()
    for i in range(totalCount):
        top = ratingList[i]
        indexOfTop = i
        i_compare = i + 1
        while i_compare < totalCount - 1:
            compareTo = ratingList[i_compare]
            if top <= compareTo:
                top = compareTo
                indexOfTop = i_compare
            i_compare += 1
        ratingList.pop(indexOfTop)
        ratingList.insert(i, top)
    return ratingList


def sortAnimeID():  # works, creates a sorted list of animeID by descending rating order
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    animeIDList = list()
    # ratingList = sortRating()
    # for i in range(6790): #have to remove repeats
    # cur.execute("SELECT anime_id FROM AnimeTable WHERE rating == ? ORDER BY rating DESC", (ratingList[i],))
    cur.execute("SELECT DISTINCT anime_id FROM AnimeTable ORDER BY rating DESC LIMIT 10") # can change l8r
    # DISTINCT fixed the error of an anime appearing multiple times in sorted list
    conn.commit()
    animeIDList.extend(cur.fetchall())
    conn.close()
    return animeIDList


def searchAnime(fGenre):  # use filters of genre to search for the top anime, returns an animeIDlist
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    """need to change this to fit flask/website"""
    allNeedToMatch = False  # option where all the genres need to match or one of them #need to change/apply this
    wantGenre = fGenre  # ["Action", "Drama"], need to change this, the genre wanted #needs to be a list
    f_anime_list = list()  # final anime list to return
    animeList = sortAnimeID()
    for x in animeList:
        #print x # prints this (32281,) a tuple
        cur.execute("SELECT DISTINCT genre from AnimeTable WHERE anime_id == ?", (x))  # works
        conn.commit()
        genre_list = cur.fetchall()  # stores the genre of the specific anime
        # print genre_list[0][0] #prints this: Drama, Romance, School, Supernatural *****
        # print genre_list & genre_list[0] prints this: [(u'Comedy, Drama, Mystery, Psychological',)]
        if allNeedToMatch:
            if wantGenre == genre_list[0][0]:  # need to test if wantGenre format would ever equal this, look above
                f_anime_list.extend(x)
        else:
            for i in wantGenre:  # i is each genre wanted
                if i in genre_list[0][0]:  # if wanted genre is part of anime's genres, works
                    f_anime_list.extend(x)
                    break
    conn.close()
    return f_anime_list


def getAnimeInfo(anime_list):  # returns all the anime info in a given animeID list, can input searchAnime output
    conn = sqlite3.connect("anime.db")
    cur = conn.cursor()
    conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    """need to change this to fit flask/website"""
    animeInfoList = list()
    for x in anime_list:
        a = (x,) #reformats it to a tuple? so it actually works
        cur.execute("SELECT anime_name, genre, anime_type, episodes, rating from AnimeTable WHERE anime_id == ? LIMIT 1", (a))
        conn.commit()
        animeInfoList.append(cur.fetchall()[0])  # use append b/c want all anime info of 1 anime to be 1 element
    conn.close()
    return animeInfoList


app = Flask(__name__, template_folder='templates', static_url_path='', static_folder='static')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.db' #have to fix this, have to make own db from csv
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route('/my.html')
def my():
    return render_template("my.html")


@app.route('/about.html')
def about():
    return render_template("about.html")


@app.route('/rec.html', methods=['POST', 'GET'])
def rec():
    if request.method == 'POST':
        conn = sqlite3.connect("anime.db")
        genreList, submitList = list(), list()
        genres = request.form['submit']
        print genres
        genreList.extend(genres.split(","))
        print genreList
        for x in genreList:  # this is to fix issue where anime not matching genre got recommended b/c had a blank genre at the end so deleted it
            x = x.encode('ascii')
            x = x.replace(" ", "")
            submitList.append(x)
        submitList = submitList[:-1]  # deletes last blank genre here
        recommend = getAnimeInfo(searchAnime(submitList))
        print recommend
        conn.commit()
        conn.close()
        if not recommend:
            return redirect(url_for("searcherror"))  # change here for if nothing submitted or no results, put like a page where it says that
        else:
            return render_template("rec.html", recommend=recommend)
    else:
        return redirect(url_for("index"))


@app.route('/searcherror.html')
def searcherror():
    return render_template("searcherror.html")


def main():
    # cur.execute("DELETE FROM AnimeTable;") to reset table
    createTable()
    #print searchAnime(["Action", "Adventure"]) #prints [id, id ...] then use getAnimeInfo with this


if __name__ == "__main__":
    # main()
    app.run(debug=True)
