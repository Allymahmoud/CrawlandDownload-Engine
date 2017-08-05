# Author: Ally Mahmoud
# Date: August 5th

# A python program to download all pdf files from
# an Active Server Page Extended file (".aspx")


import urllib2
import urllib
import re
import constants


#connect to a URL
website = urllib2.urlopen(constants.websiteUrl)

#read html code
html = website.read()

#use re.findall to get all the links
links = re.findall('"((http|ftp)s?://.*?)"', html)


sampleUrl ="http://mfma.treasury.gov.za/Documents/04.%20Service%20Delivery%20and%20Budget%20Implementation%20Plans/2015-16/02.%20Local%20Municipalities/EC106%20Sundays%20River%20Valley/EC106%20Sunday%20River%20Valley%20SDBIP%202015-16.PDF"

#method to construct a custom name out of a pdf link of
# this format "http://mfma.treasury.gov.za/Documents/04.%20Service%20Delivery%20and%20Budget%20Implementation%20Plans/2015-16/02.%20Local%20Municipalities/EC106%20Sundays%20River%20Valley/EC106%20Sunday%20River%20Valley%20SDBIP%202015-16.PDF"
def customUrlParser(url):
    extractedName = ""

    firstFilterdUrl = url.split("04.%20")
    secondfilterdUrl = firstFilterdUrl[1].split("%20")
    for urlComponent in secondfilterdUrl:
        extractedName+= urlComponent


    filterNames = extractedName.split("/")
    extractedName = ""

    i = 0
    for name in filterNames:
        extractedName += name
        if i < len(filterNames)-1:
            extractedName += ">"
        i+=1

    return extractedName


i = 0
for link in links:
    if link[0].endswith(constants.fileExtension):
        print (link)
        longName = link[0].split("/")
        filtername = longName[len(longName)-1]
        print (filtername)

        urllib.urlretrieve(link[0],filtername)

    if link[0].startswith(constants.websiteUrl):
        i+=1
        print (i, link[0])

print customUrlParser(sampleUrl)

