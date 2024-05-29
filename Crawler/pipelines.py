# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector


class CrawlerPipeline:
    #how to access the database
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '576241',
            database = 'limitless'
        )

        #allows to make commands to mysql
        self.cur = self.conn.cursor(buffered=True)

    
    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute(""" insert into pokemon (pkmn, item, ability, tera, attacks, points, url) values (%s,%s,%s,%s,%s,%s,%s)""", (
            item["pkmn"],
            item["item"],
            item["ability"],
            item["tera"],
            str(item["attacks"]),
            item["points"],
            str(item["url"])
        ))
        self
        
        #clean data in points, tera and ability
        self.cur.execute(""" update pokemon set points = substring_index(points, ' ', 1);""")
        self.cur.execute(""" update pokemon set tera = trim(leading 'Tera Type:' from tera);""")
        self.cur.execute(""" update pokemon set ability = trim(leading 'Ability:' from ability);""")
        self.cur.execute(""" update pokemon set url = trim(leading 'https://play.limitlesstcg.com/tournament/' from url);""")
        #break attacks into seperate columns
        self.cur.execute("""update pokemon set attack1 = substring_index(attacks, ',', 1);""")
        self.cur.execute("""update pokemon set attack2 = substring_index(substring_index(attacks, ',', 2), ',', -1);""")
        self.cur.execute("""update pokemon set attack3 = substring_index(substring_index(attacks, ',', 3), ',',-1);""")
        self.cur.execute("""update pokemon set attack4 = substring_index(attacks, ',', -1);""")

        ## Execute insert of data into database
        self.conn.commit()

    


    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

