import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BbancocredicoopItem
from itemloaders.processors import TakeFirst
import json
from w3lib.html import remove_tags
pattern = r'(\xa0)?(Click aqu&iacute;)?(&nbsp;)?'

class BbancocredicoopSpider(scrapy.Spider):
	name = 'bancocredicoop'
	start_urls = ['https://www.bancocredicoop.coop/api/noticias/NoticiasPrensa']

	def parse(self, response):
		data = json.loads(response.text)
		for index in range(len(data['noticias'])):
			item = ItemLoader(item=BbancocredicoopItem(), response=response)
			item.default_output_processor = TakeFirst()

			title = data['noticias'][index]['titulo']
			content = remove_tags(data['noticias'][index]['contenido'])
			content = re.sub(pattern, "", content)
			date = "Not published in article"


			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)

			yield item.load_item()
