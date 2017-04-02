import json
from sys import argv
import csv

def main(argv):
	json_data=open(argv[1]).read()

	data = json.loads(json_data)

	# open a file for writing

	house_data = open(argv[2], 'w')

	# create the csv writer object

	csvwriter = csv.writer(house_data)

	newData = sorted(data, key=lambda k: int(k['pricePerMonth'])) 

	for i in range(len(newData)):
	    if i == 0:
	        header = newData[0].keys()
	        csvwriter.writerow(header)
	    csvwriter.writerow(newData[i].values())

	house_data.close()

if __name__ == "__main__":
	main(argv)
