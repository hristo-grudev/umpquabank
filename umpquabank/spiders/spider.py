import scrapy

from scrapy.loader import ItemLoader

from ..items import UmpquabankItem
from itemloaders.processors import TakeFirst


class UmpquabankSpider(scrapy.Spider):
	name = 'umpquabank'
	start_urls = ['https://www.umpquabank.com/newsroom/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="anchor"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="body-copy js-avoid-orphan"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="info text-2"]/span/text()').get().split('|')[0]

		item = ItemLoader(item=UmpquabankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
