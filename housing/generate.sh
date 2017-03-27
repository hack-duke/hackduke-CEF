#!/bin/sh
rm info.json
scrapy crawl zillow -o info.json
python3 csv_generator.py info.json ~/Desktop/info.csv
done
