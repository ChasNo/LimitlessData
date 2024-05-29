import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Crawler.items import CrawlerItem


class teamCrawler(CrawlSpider):
    name = "team"
    #only follow links on this sight
    allowed_domains = ['play.limitlesstcg.com']
    #tells the crawler to only access urls containing teamlist and to call parse_item when one is found
    rules = (
        Rule(LinkExtractor(allow='teamlist'), callback= 'parse_item', follow=True),
    )

    def parse_item(self, response):
        #call function to store data
        team_item = CrawlerItem()
        for pokemon in response.css("div.pkmn"):
            team_item["pkmn"]= pokemon.css("span::text").get()
            team_item["ability"]= pokemon.css("div.ability::text").get()
            team_item["item"]= pokemon.css("div.item::text").get()
            team_item["tera"]= pokemon.css("div.tera::text").get()
            team_item["attacks"]= pokemon.css("li::text").getall()
            team_item["points"]= response.css("div.details::text").get()
            team_item["url"]= response.url
            #outputs all scraped data
            yield team_item