from Crawler.spiders.teamCrawler import teamCrawler
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Crawler import settings as my_settings
import mysql.connector
from itemadapter import ItemAdapter
import sys


def main():

    #take start url from user
    url = input("Enter URL: ")
    domain = "https://play.limitlesstcg.com/tournament/"
    if url.find(domain) == -1:
        sys.exit("Invalid Domain must be from https://play.limitlesstcg.com/tournament/")
    uuid = url.replace(domain, "")
    uuid = uuid.replace("/standings", "")
    url_check(uuid)

    #start crawler instance in main
    crawler_settings = Settings()
    crawler_settings.setmodule(my_settings)
    crawler = CrawlerProcess(settings=crawler_settings)
    crawler.crawl(teamCrawler, start_urls=[url])
    crawler.start()
    crawler.stop()


    conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '576241',
            database = 'limitless'
        )

    cur = conn.cursor()

    cur.execute("""alter table pokemon order by url""")
    cur.execute("""select distinct url from pokemon where url like %s """, ('%' + uuid + '%',))
    result = cur.fetchall()
    for row in result:
        query = "select pkmn from pokemon where url = %s"
        cur.execute(query, row)
        team = cur.fetchall()

        team_values = [x[0] for x in team]
        team_values.extend([None] * (6 - len(team_values)))
        team_values = team_values[:6]

        teamQuery = "insert into teams (url, pkmn1, pkmn2, pkmn3, pkmn4, pkmn5, pkmn6) values (%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(teamQuery, (row[0],) + tuple(team_values))
        

    conn.commit()
    cur.close()
    conn.close()

def url_check(x):
    conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '576241',
            database = 'limitless'
        )

    cur = conn.cursor()
    try: 
        sql = "insert into tourneys (urls) VALUES (%s)"
        cur.execute(sql,(x,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        sys.exit("Tournament Data has already been Uploaded")


if __name__ == '__main__':
    main()

