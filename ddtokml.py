### Takes a local CSV and generates KML from LAT LON.
### Include arguments in command line or  the 'myOrder' variable below to name and specify column order.
### Include any relevant attributes or HTML link tags in the CSV. 
###Adapted from the sample found here: https://developers.google.com/kml/articles/csvtokml

import csv
import xml.dom.minidom
import sys

myCSV = r"file.csv"

myOrder = ['Latitude','Longitude', 'Name'] ### Must have columns named 'Latitude','Longitude'

myKML = 'localpoints.kml'

def createPlacemark(kmlDoc, row, order):
  # This creates a <Placemark> element for a row of data.
  # A row is a dict.
  placemarkElement = kmlDoc.createElement('Placemark')
  extElement = kmlDoc.createElement('ExtendedData')
  placemarkElement.appendChild(extElement)
  
  # Loop through the columns and create a <Data> element for every field that has a value.
  for key in order:
    if row[key]:
      dataElement = kmlDoc.createElement('Data')
      dataElement.setAttribute('name', key)
      valueElement = kmlDoc.createElement('value')
      dataElement.appendChild(valueElement)
      valueText = kmlDoc.createTextNode(row[key])
      valueElement.appendChild(valueText)
      extElement.appendChild(dataElement)
  
  pointElement = kmlDoc.createElement('Point')
  placemarkElement.appendChild(pointElement)
  coordinates = row['Longitude'] + "," + row['Latitude'] + ",0"
  coorElement = kmlDoc.createElement('coordinates')
  coorElement.appendChild(kmlDoc.createTextNode(str(coordinates)))
  pointElement.appendChild(coorElement)
  return placemarkElement

def createKML(csvReader, fileName, order):
  # This constructs the KML document from the CSV file.
  kmlDoc = xml.dom.minidom.Document()
  
  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
  kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
  kmlElement = kmlDoc.appendChild(kmlElement)
  documentElement = kmlDoc.createElement('Document')
  documentElement = kmlElement.appendChild(documentElement)

  # Skip the header line.
  next(csvReader)
  
  for row in csvReader:
    placemarkElement = createPlacemark(kmlDoc, row, order)
    documentElement.appendChild(placemarkElement)
  kmlFile = open(fileName, 'wb')
  kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def main():
  # This reader opens up a .csv file defined by the variable, 'myCSV'.
  # It creates a KML file defined by the variable, 'myKML'.
  
  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the order defined.
  
  if len(sys.argv) >1: order = sys.argv[1].split(',')
  else: order = myOrder
  csvreader = csv.DictReader(open(myCSV))
  kml = createKML(csvreader, myKML, order)

if __name__ == '__main__':
  main()