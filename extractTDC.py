import xml.etree.ElementTree as ET
import os
import csv
import itertools

#Set working Directory
path = '/Users/arthurg/Documents/My Tableau Repository (Beta)/Datasources'
os.chdir(path)


#Print Files in working directory
#import os
#for subdir, dirs, files in os.walk('./'):
#    for file in files:
#      print file


for files in os.walk('./'):
    for file in files:
        print file

#Helper Functions to extract specific elements
def getDbClass(tdc):
    for header in tdc.iter('connection-customization'):
        dbclass = header.attrib['class']
        return dbclass        

def getEnabled(tdc):
    for header in tdc.iter('connection-customization'):
        enabled = header.attrib['enabled']
        return enabled      

def getCustomizations(tdc):
    dbclass = getDbClass(tdc)
    enabled = getEnabled(tdc)
    customization_values = []
    for customization in tdc.iter('customization'):
        name = customization.attrib['name']
        value = customization.attrib['value']
        row = dict({'dbclass': dbclass, 'enabled': enabled, 'name': name, 'value': value})
        customization_values.append(row)
        #customization_values.update({'dbclass': dbclass, 'enabled': enabled, 'name': name, 'value': value})
    return customization_values


def getCustomizationsFromTDC(tdc_path):
    tree = ET.parse(tdc_path)
    root = tree.getroot()
    return getCustomizations(root)


def getTDCFiles(directory = os.getcwd()):
    tdc_files = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".tdc"):
            tdc_files.append(file)
    return tdc_files

def writeResults(fileName):
    with open(fileName, 'w') as csvfile:
        fieldnames = ['dbclass', 'enabled', 'name', 'value']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for customization in cleanCustomizations:
            writer.writerow(customization)

#Get all TDC files in the directory
myTDC = getTDCFiles()    

#extract customizations from the TDC files
myCustomizations = map(getCustomizationsFromTDC, myTDC)

#Combine customizations into a single list
cleanCustomizations =  list(itertools.chain.from_iterable(myCustomizations))

#Write out File Results
writeResults("mycsv.csv")

    