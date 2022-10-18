import json
import shutil
import duckdb
import sqlite3


def create_common_drawl():
    '''
    Creates common_drawl.duckdb based on common_drawl.db
    '''
    sql = sqlite3.connect('common_drawl.db')
    cursor_sql = sql.cursor()

    duck = duckdb.connect(database='commmon_drawl.duckdb', read_only=False)
    cursor_duck = duck.cursor()

    cursor_duck.execute("PRAGMA memory_limit='2GB'")

    print("embeddings is starting")
    cursor_sql.execute("SELECT * FROM embeddings")
    cursor_duck.execute("CREATE TABLE embeddings(word text primary key, emb blob)")
    b=0
    array = cursor_sql.fetchmany(1000)

    while (len(array) != 0):
        cursor_duck.execute("BEGIN TRANSACTION")
        print(b)
        b= b+1
        for line in array:
            
            word = line[0]
            emb = line[1]    
            cursor_duck.execute("INSERT INTO embeddings VALUES(?,?)", (word, emb))
        array = cursor_sql.fetchmany(1000)    
        cursor_duck.execute("COMMIT")
    print("embeddings is done")

    duck.close()
    sql.close()


def create_entity_word_embedding():

    '''
    Creates entity_word_embedding.duckdb based on entity_word_embedding.db
    '''

    sql = sqlite3.connect('entity_word_embedding.db')
    cursor_sql = sql.cursor()

    duck = duckdb.connect(database='entity_word_embedding.duckdb', read_only=False)
    cursor_duck = duck.cursor()

    cursor_duck.execute("PRAGMA memory_limit='2GB'")

    print("glove is starting")
    cursor_sql.execute("SELECT * FROM glove")
    cursor_duck.execute("CREATE TABLE glove(word TEXT primary key, emb blob)")
    cursor_duck.execute("BEGIN TRANSACTION")
    b=0

    for line in cursor_sql.fetchall():
        print(b)
        b= b+1
        word = line[0]
        emb = line[1]
        
        cursor_duck.execute("INSERT INTO glove VALUES(?,?)", (word, emb))    
    cursor_duck.execute("COMMIT")
    print("glove is done")

    print("embeddings is starting")
    cursor_sql.execute("SELECT * FROM embeddings")
    cursor_duck.execute("CREATE TABLE embeddings(word TEXT primary key, emb blob)")
    b=0
    array = cursor_sql.fetchmany(10000)

    while (len(array) != 0):
        cursor_duck.execute("BEGIN TRANSACTION")
        print(b)    
        b= b+1
        for line in array:
            
            word = line[0]
            emb = line[1]
        
            cursor_duck.execute("INSERT INTO embeddings VALUES(?,?)", (word, emb))
        
        array = cursor_sql.fetchmany(10000)    
        cursor_duck.execute("COMMIT")    
    print("embeddings is done")

    print("wiki is starting")
    cursor_sql.execute("SELECT * FROM wiki")
    cursor_duck.execute("CREATE TABLE wiki(word text primary key, p_e_m blob, lower text, freq INTEGER)")

    b=0
    array = cursor_sql.fetchmany(10000)

    while (len(array) != 0):
        cursor_duck.execute("BEGIN TRANSACTION")
        print(b)
        b= b+1
        for line in array:
            
            word = line[0].encode(encoding = 'UTF-8', errors = 'strict')
            p_e_m = line[1]
            lower= line[2].encode(encoding = 'UTF-8', errors = 'strict')
            freq = line[3]
            cursor_duck.execute("INSERT INTO wiki VALUES(?,?,?,?)", (word, p_e_m, lower, freq))
        array = cursor_sql.fetchmany(10000)    
        cursor_duck.execute("COMMIT")
    print("wiki is done")



    duck.close()
    sql.close()