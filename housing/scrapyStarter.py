from scrapy import cmdline
import os

class scrapyStarter:
	def __init__(self, city='Durham', state='NC', limit=int(10000), spider = 'zillow'):
		self.city = city
		self.state = state
		self.limit = limit
		self.spider = spider

	def makeJSON(self, filename):
		s = 'scrapy crawl "%s" -a city="%s" -a state="%s" -a limit="%s" -o %s.json'
		updatedS = s % (self.spider, self.city, self.state, str(self.limit), str(filename))
		print(updatedS)
		status = os.system(updatedS)
		return status