# HousingScraper

## Demo

Download the .mov of the demo here <img src="lib/Demo.mov" alt="Housing GUI Demo" width="40%" height="40%">

## Origins of Project

This project was started after [Durham Community Engagement Fund (CEF)](https://communityempowermentfund.org/) reached out to HackDuke to have their housing data generation automated. Following their request, meetings were scheduled and carried out, web scrapers were built, and a destop application was made.

## How It Was Built

All of the web scraping was done using [Scrapy](https://scrapy.org/), a python web scraping library. "Spiders", or site specific scapers were built for [Zillow](https://www.zillow.com/), [ShowMeTheRent](https://www.showmetherent.com/), and [CheapApartmentsLocator](http://www.cheapapartmentslocator.com/) via the request of the CEF.

The desktop app was built in Java using JavaFX and it made all of the scraped data avaliable to the user. Queries could be put into the desktop app after specifying the City, State, and price limit. The spiders re-ran everytime a new query was put in. 

## Future Steps

Set up a web application which re-runs the Durham scraper every 30 minutes. The web app would allow for users to specify their price range and see the results. There are some web app frameworks and libraries which have built in GET request functionalities in place for Scrapy spiders. For example [Arachne](http://arachne.readthedocs.io/en/latest/) can be used to run spiders on a Flask app. Our Flask app is already written, Arachne just needs to be integrated.
