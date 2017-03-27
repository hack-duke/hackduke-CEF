import json

import csv

json_data=open('test.json').read()

data = json.loads(json_data)

# open a file for writing

house_data = open('test.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(house_data)

for i in range(len(data)):
    if i == 0:
        header = data[0].keys()
        csvwriter.writerow(header)

    csvwriter.writerow(data[i].values())

house_data.close()
