# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import sqlite3
import csv

conn = sqlite3.connect("anime.db")
cur = conn.cursor()
conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')


def createTable():
    cur.execute(""" CREATE TABLE IF NOT EXISTS AnimeTable(
                anime_id INTEGER unique,
                anime_name TEXT,
                genre TEXT,
                anime_type TEXT, 
                episodes REAL,
                rating REAL,
                members INTEGER)""")

    conn.commit()
    print("executed")
    with open('anime.csv', 'r') as csvfile:
        no_records = 0
        reader = csv.reader(csvfile)
        i = 0
        while i < 12294:
            row = list()
            row.extend(reader.next())
            # print unit #prints a whole row, confirming that reader.next() is a list
            if row[5] and (int(row[6]) > 1000):  # requirements: has to have rating & min. of 1000 reviews
                cur.execute("INSERT OR IGNORE INTO AnimeTable VALUES (?,?,?,?,?,?,?)", row)
                conn.commit()
                no_records += 1
            i += 1
    print("\n{} built".format(no_records))


def getRatingList():  # kinda useless now
    cur.execute("SELECT rating FROM AnimeTable")
    conn.commit()
    rating_list = list()
    f_rating_list = list()
    rating_list.extend(cur.fetchall())
    i = 0
    while i < 6791:  # removes the coma at end from every number
        f_rating_list.extend(rating_list[i])
        i += 1
    return f_rating_list


def getGenreList():
    cur.execute("SELECT genre FROM AnimeTable")
    conn.commit()
    genre_list = list()
    genre_list.extend(cur.fetchall())
    return [genre.translate(None, ",") for genre in genre_list]


def getAnimeID(index):  # gets the AnimeID of specified index in the sorted AnimeID LIst
    id_list = sortAnimeID()
    return id_list[index][0]  # for some reason treats the id/# as one element & the comma as the 2nd


def sortRating():  # sort table by rating = useless
    totalCount = 6790
    ratingList = getRatingList()
    for i in range(totalCount):
        top = ratingList[i]
        indexOfTop = i
        i_compare = i+1
        while i_compare < totalCount-1:
            compareTo = ratingList[i_compare]
            if top <= compareTo:
                top = compareTo
                indexOfTop = i_compare
            i_compare += 1
        ratingList.pop(indexOfTop)
        ratingList.insert(i, top)
    return ratingList

def sortAnimeID(): #works
    animeIDList = list()
    #ratingList = sortRating()
    #for i in range(6790): #have to remove repeats
        #cur.execute("SELECT anime_id FROM AnimeTable WHERE rating == ? ORDER BY rating DESC", (ratingList[i],))
    cur.execute("SELECT DISTINCT anime_id FROM AnimeTable ORDER BY rating DESC")
    conn.commit()
    animeIDList.extend(cur.fetchall())
    return animeIDList

def searchAnime(): #use filters of genre to search for the top anime
    """need to change this to fit flask/website"""
    allNeedToMatch = False #option where all the genres need to match or one of them #need to change this
    wantGenre = ["Action", "Drama"] #need to change this
    print wantGenre[1]
    f_anime_list = list()
    animeList = sortAnimeID()
    for x in animeList:
        cur.execute("SELECT DISTINCT genre from AnimeTable WHERE anime_id == ?", (x))
        conn.commit()
        genre_list = cur.fetchall() #stores the genre of the specific anime
        #print genre_list[0][0] #prints this: Drama, Romance, School, Supernatural
        #print genre_list & genre_list[0] prints this: [(u'Comedy, Drama, Mystery, Psychological',)]
        if allNeedToMatch:
            if wantGenre == genre_list[0][0]:
                f_anime_list.extend(x)
        else:
            for i in wantGenre:
                if i in genre_list[0][0]: #if wanted genre matches anime's genre, works
                    #print("searching")
                    f_anime_list.extend(x)
                    break
    return f_anime_list

def getAnimeInfo(anime_list): #returns the anime info you want
    """need to change this to fit flask/website"""
    animeInfoList = list()
    for x in anime_list:
        cur.execute("SELECT anime_name, genre, anime_type, episodes, rating from AnimeTable WHERE anime_id == ?", (x))
        conn.commit()
        animeInfoList.append(cur.fetchall())
    return animeInfoList


def main():
    #cur.execute("DELETE FROM AnimeTable;") to reset table
    createTable()
    print searchAnime()
    conn.close()



if __name__ == "__main__":
    main()
