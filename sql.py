#import mysql.connector as sql
from datetime import datetime
from sd_parser import *
from random import sample
from time import time
from const import *
from helper import *
#import pandas as pd




class user_db:
    mydb = DATABASE

    @staticmethod
    def create(id):
        # ADDDING to users table---------------------------------------------------------------------------------------#
        cursor = user_db.mydb.cursor()
        cursor.execute(
            f"INSERT INTO users (id_telegram) VALUES ({id})")
        user_db.mydb.commit()
        # ADDDING to views table---------------------------------------------------------------------------------------#
        cursor = user_db.mydb.cursor()
        cursor.execute(
            f"INSERT INTO users_views (id_telegram) VALUES ({id})")
        user_db.mydb.commit()

    @staticmethod
    def get_users_id():
        cursor = user_db.mydb.cursor()
        request = cursor.execute("SELECT id_telegram FROM users")
        # turn into beautiful list
        return [i[0] for i in cursor.fetchall()]

    # ------------------------------------------------RATING-----------------------------------------------------------#
    @staticmethod
    def get_user_stats(id):
        mycursor = user_db.mydb.cursor()


        request = mycursor.execute(f"SELECT (%s, %s) FROM users WHERE id_telegram={id}")
        val = ("education_learning", "health_medicine", "business_industry", "science_society", "fossils_ruins","earth_climate", "plants_animals", "computers_math", "space_time", "matter_energy", "living_well", "mind_brain")
        mycursor.execute(request, val)

        # # turn into beautiful dict
        return dict(zip(val,[i[0] for i in mycursor.fetchall()]))

    @staticmethod
    def rate(id, theme, mark):
        mycursor = user_db.mydb.cursor()
        r = "UPDATE users " \
            f"SET {theme} = {theme} + {mark} WHERE id_telegram={id}"
        mycursor.execute(r)
        user_db.mydb.commit()

    # ------------------------------------------------RELATED-SENDED----------------------------------------------------#
    @staticmethod
    def get_user_related_sended(id):
        cursor = user_db.mydb.cursor()
        request = cursor.execute(f"SELECT id_article FROM users_related_sended WHERE id_telegram={id}")
        # turn into beautiful list
        return [i[0] for i in cursor.fetchall()]
    @staticmethod
    def add_related_sended(id, id_article):
        mycursor = user_db.mydb.cursor()
        if isinstance(id_article, list):
            for i in id_article:
                sql = "INSERT INTO users_related_sended (id_telegram, id_article) VALUES (%s, %s)"
                val = (id, i)
                mycursor.execute(sql, val)
                user_db.mydb.commit()
        else:#request = mycursor.execute(f"SELECT id_article FROM users_related_sended WHERE id_telegram={id}")
            sql = "INSERT INTO users_related_sended (id_telegram, id_article) VALUES (%s, %s)"
            val = (id, id_article)
            mycursor.execute(sql, val)
            user_db.mydb.commit()

    # includes fact checker
    @staticmethod
    def reboot_related_sended(id):
        mycursor = user_db.mydb.cursor()
        if len(user_db.get_user_related_sended(id)) > 25:
            mycursor.execute(f"DELETE FROM users_related_sended WHERE id_telegram = {id}")
            user_db.mydb.commit()
            # success!
            return 1
        return 0

    # ------------------------------------------------COUNTERS--------------------------------------------------------#

    @staticmethod
    def reboot_counters(id):
        mycursor = user_db.mydb.cursor()
        rows = ("count_viewed_today", "count_viewed_total", "count_likes", "count_dislikes", "count_neutral")
        for position in rows:
            r = f"UPDATE users " \
                f"SET {position}=0 " \
                f"WHERE id_telegram={id}"
            mycursor.execute(r)
            user_db.mydb.commit()

    @staticmethod
    def reboot_coefs(id):
        mycursor = user_db.mydb.cursor()
        rows =         row = ("health_medicine", "mind_brain", "living_well", "matter_energy", "space_time", "computers_math",
                  'plants_animals',
                  "earth_climate",
                  "fossils_ruins",
                  "science_society",
                  "business_industry",
                  "education_learning")
        for position in rows:
            r = f"UPDATE users " \
                f"SET {position}=0 " \
                f"WHERE id_telegram={id}"
            mycursor.execute(r)
            user_db.mydb.commit()

    @staticmethod
    def update_count_rated(id, mark):
        mycursor = user_db.mydb.cursor()

        if mark == 1:
            target = "count_likes"

        elif mark == 0.5:
            target = "count_neutral"
        else:
            target = "count_dislikes"

        mycursor.execute("UPDATE users " \
                         f"SET {target} = {target} + 1 WHERE id_telegram={id}")
        user_db.mydb.commit()

    @staticmethod
    def reboot_count_viewed_today(id):
        mycursor = user_db.mydb.cursor()
        r = "UPDATE users " \
            f"SET count_viewed_today = 0 WHERE id_telegram={id}"
        mycursor.execute(r)
        user_db.mydb.commit()



    @staticmethod
    def update_count_viewed(id):
        mycursor = user_db.mydb.cursor()
        rows = ["count_viewed_today", "count_viewed_total"]
        for position in rows:
            r = f"UPDATE users " \
                f"SET {position}={position}+1 " \
                f"WHERE id_telegram={id}"
            mycursor.execute(r)
            user_db.mydb.commit()


    #into csv file
    @staticmethod
    def add_view(id_tg, id_arc, rating):
        cursor = user_db.mydb.cursor()
        request = cursor.execute("SELECT * FROM users_views")
        VIEWS = [(int(i[0]), str(i[1]), int(i[2])) for i in cursor.fetchall()]
        NEW = (id_tg, id_arc, int(rating))
        if NEW not in VIEWS:
            mycursor = user_db.mydb.cursor()
            sql = "INSERT INTO users_views (id_telegram, id_article, rating) VALUES (%s, %s, %s)"
            val = (id_tg, id_arc, int(rating))
            print(id_arc)
            mycursor.execute(sql, val)
            user_db.mydb.commit()
        else:
            pass

    @staticmethod
    def reboot_view():
        mycursor = user_db.mydb.cursor()
        mycursor.execute("TRUNCATE TABLE users_views")
        user_db.mydb.commit()



class article_db:
    mydb = DATABASE

    @staticmethod
    def get_count_articles():
        mycursor = user_db.mydb.cursor()
        mycursor.execute('SELECT * FROM articles')
        return len(mycursor.fetchall())

    @staticmethod
    def update_content():
        start_time = time()
        count_added = 0
        mycursor = user_db.mydb.cursor()
        top = 'https://www.sciencedaily.com/news/top/science/'
        row = ("health_medicine", "mind_brain", "living_well", "matter_energy", "space_time", "computers_math",
                  'plants_animals',
                  "earth_climate",
                  "fossils_ruins",
                  "science_society",
                  "business_industry",
                  "education_learning")
        #----------------------BY-THEMES-------------------------------------------------------------------------------#
        for i in ("health_medicine", "mind_brain",):
            for obj in [article(j) for j in get_url(i)]:
                obj_text_new = obj['text'].replace("'", '').replace("<sub>", '').replace("</sub>", '')

                sql = "INSERT INTO articles (name,is_top, date, source, description, text, url, themes, telegraph_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (obj['name'], False, date_to_str(obj["date"]), obj["source"],
                       obj['summary'], obj_text_new, obj['url'], ' '.join(obj['themes']), get_telegraph(obj))
                mycursor.execute(sql, val)
                user_db.mydb.commit()
                count_added +=1
        # ----------------------BY-TOP---------------------------------------------------------------------------------#
        for obj in [article(j) for j in get_top_url()]:
            obj_text_new = obj['text'].replace("'", '').replace("<sub>", '').replace("</sub>", '')
            sql = "INSERT INTO articles (name,is_top, date, source, description, text, url, themes, telegraph_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (
                obj['name'], True, date_to_str(obj["date"]), obj["source"],
                obj['summary'], obj_text_new,
                obj['url'], ' '.join(obj['themes']), get_telegraph(obj))
            mycursor.execute(sql, val)
            user_db.mydb.commit()
            count_added += 1

        print(f'finished-{"%.2f" % time() - start_time}'
              f'\n{count_added} articles have been added')

    @staticmethod
    def decorate_article(id):
        mycursor = user_db.mydb.cursor()
        r = mycursor.execute(f"SELECT name, date, source, description, url, telegraph_url, rating FROM articles WHERE id={id}")
        obj = mycursor.fetchone()


        telegraph_url = '😢Недоступна для этой статьи' if obj[5] == None  else obj[5]
        return f"📬{obj[0]}\n\n🗓{obj[1]}\n🏫{obj[2]}\n\n💻Версия  для удобного чтения c компьютера:\n{telegraph_url}\n\n▪Description:\n{obj[3]}\n\n⭐Rating: {obj[6]}\n\n{obj[4]}",
    #add rating to current article
    @staticmethod
    def rate(id, mark):
        while True:
            try:
                mycursor = user_db.mydb.cursor()
                mycursor.execute("UPDATE articles " \
                                 f"SET rating = rating + {mark} WHERE id={id}")
                user_db.mydb.commit()

            except:
                print('------------------Cant update rating for that user--------------------\ntrying again')
            else:
                break

    @staticmethod
    def calibration(id):
        n = 5
        lst = []
        mycursor = user_db.mydb.cursor()
        mycursor.execute("SELECT id, theme FROM articles WHERE is_top=1")
        # select n random id of articles
        result = mycursor.fetchall()
        all_theme_of_top_articles = [i[1] for i in result]
        all_id_of_top_articles = [i[0] for i in result]
        selected_random_articles =  sample(list(set(all_id_of_top_articles) - set(user_db.get_user_related_sended(id))), n)
        for i in selected_random_articles:
            theme = all_theme_of_top_articles[all_id_of_top_articles.index(i)]
            lst.append([i, theme])
        # select N random NEW top articles for unique user
        #return sample(list(set(all_id_of_top_articles) - set(user_db.get_user_related_sended(id))), n)
        return lst
