import xmltodict
import json
import os

def xml2Json(xmlPath,savePath):
    xmlFiles = os.listdir(xmlPath)
    for i in range(len(xmlFiles)):
        xml = open(os.path.join(xmlPath,xmlFiles[i]),'r')
        xmlString = xml.read()
        jsonString = xmltodict.parse(xmlString)
        result = json.dumps(jsonString,indent=4)
        jsonName = xmlFiles[i].split('.')[0]
        tempfile = os.path.join(savePath,jsonName+'.json')
        with open(tempfile,'w') as f:
            f.write(result)

if __name__ == '__main__':
    xmlPath = r"D:\SampleML\sampleMLV2\xml"
    jsonPath = r"D:\SampleML\sampleMLV2\SampleJson"
    xml2Json(xmlPath,savePath = jsonPath)
