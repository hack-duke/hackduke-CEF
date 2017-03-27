import requests
from bs4 import BeautifulSoup

class ZillowScraper:
	def __init__(self, url):
		self.url = url
		self.house_data = get_house_data(url)

	def getBedrooms(self):
		bedGroups = self.house_data.find_all("div", {"class": "bedroom-group-header"})
		housing_option = {}
		for group in bedGroups:
			name = group.find_all("strong")[0].text
			amount = group.find_all("span", {"class": "bedroom-group-price"})[0].text
			if amount != "":
				housing_option[str(name)] = str(amount)
		bedrooms = {}
		bedrooms["bedrooms"] = housing_option
		return bedrooms

	def getName(self):
		infoBlock = self.house_data.find_all("div", {"class": "bdp-info-container"})[0]
		return str(infoBlock.find_all("h1")[0].text)

	def getAddress(self):
		address = {}
		infoBlock = self.house_data.find_all("div", {"class": "bdp-info-container"})[0]
		address["address"] = str(infoBlock.find_all("h2")[0].text)
		return address

	def getURL(self):
		return {"url": self.url}

	def getInfo(self):
		info = dict()
		info[self.getName()] = [self.getAddress(), self.getBedrooms(), self.getURL()]
		print info
		return info

def get_house_data(url):
	r = requests.get(url)
	return BeautifulSoup(r.content, 'html.parser')

if __name__ == "__main__":

	# TEST CASES

	# scraper = ZillowScraper("https://www.zillow.com/homes/for_rent/Durham-NC-27708/house,condo,apartment_duplex,mobile,townhouse_type/5Xhykg_bldg/69492_rid/36.006791,-78.918872,35.968871,-78.973804_rect/13_zm/?")
	# scraper = ZillowScraper("https://www.zillow.com/homes/for_rent/Durham-NC-27708/house,condo,apartment_duplex,mobile,townhouse_type/5XhyWZ_bldg/69492_rid/35.997955,-78.938291,35.989032,-78.965757_rect/14_zm/")
	# scraper = ZillowScraper("https://www.zillow.com/homes/for_rent/Durham-NC-27708/house,condo,apartment_duplex,mobile,townhouse_type/5XhydN_bldg/69492_rid/36.001249,-78.95995,35.998936,-78.963384_rect/17_zm/")
	# scraper = ZillowScraper("https://www.zillow.com/homes/for_rent/Durham-NC-27708/house,condo,apartment_duplex,mobile,townhouse_type/5XhydN_bldg/69492_rid/36.000409,-78.960606,35.999253,-78.962323_rect/18_zm/")
	scraper = ZillowScraper("https://www.zillow.com/homes/for_rent/Durham-NC-27708/house,condo,apartment_duplex,mobile,townhouse_type/5Xqqtb_bldg/69492_rid/36.001974,-78.959089,35.997347,-78.965956_rect/16_zm/")
	scraper.getInfo()
