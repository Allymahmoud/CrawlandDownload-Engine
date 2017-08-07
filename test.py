from HTMLParser import HTMLParser
import urllib2
import constants
import os
import urllib
from time import sleep
import distutils.dir_util


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')

response = urllib2.urlopen(constants.websiteUrl)
html = response.read()
parser.feed(html)






def construct_custom_pdf_url(html,pdflinks, counter):
    parsed = html.split("HREF=\"/Documents/04.")


    for elements in parsed:
        filtered = elements.split("\"")

        newPdfUrl = "http://mfma.treasury.gov.za/Documents/04." + filtered[0]
        print str(counter) + " found pdf url: " + newPdfUrl
        if not newPdfUrl in pdflinks:
            pdflinks.append(newPdfUrl)



def constructDirectoryTree(baseFilePath1, baseFilePath2, filename):
    splittedFileName = filename.split(">")
    i = 0
    newFilePath = ""
    for i in range(0,len(splittedFileName)-1):
        newFilePath += splittedFileName[i]

        # if i != len(splittedFileName)-1:
        newFilePath += "/"

    if os.path.exists(baseFilePath2+newFilePath):
        os.rename((baseFilePath1+filename), (baseFilePath2+newFilePath+splittedFileName[len(splittedFileName)-1]))
    else:
        # sleep(0.3)
        # os.mkdirs(baseFilePath2+newFilePath)
        distutils.dir_util.mkpath(baseFilePath2+newFilePath)
        os.rename((baseFilePath1 + filename),
                  (baseFilePath2 + newFilePath + splittedFileName[len(splittedFileName) - 1]))

def itearateOverAllPdfFiles(directory,dest):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            constructDirectoryTree(directory, dest, filename )
            print "Success in moving file"
        else:
            print "error: file not pdf: " + filename
        # sleep(01)


origin = "/Users/Allymahmoud/desktop/Sample 1/"
dest = "/Users/Allymahmoud/desktop/Sample 2/"
itearateOverAllPdfFiles(origin,dest)


# filepath = "IntegratedDevelopmentPlans>2017-18>01.Draft>03.Districtmunicipalities>DC20FezileDabi>DC20FezileDabiDraftIDP2017-18.pdf"

sampleUrl = "http://mfma.treasury.gov.za/Documents/01.%20Integrated%20Development%20Plans/2017-18/01.%20Draft/03.%20District%20municipalities/DC20%20Fezile%20Dabi/DC20%20Fezile%20Dabi%20Draft%20IDP%202017-18.pdf"

# method to construct a custom name out of a pdf link of
# this format "http://mfma.treasury.gov.za/Documents/04.%20Service%20Delivery%20and%20Budget%20Implementation%20Plans/2015-16/02.%20Local%20Municipalities/EC106%20Sundays%20River%20Valley/EC106%20Sunday%20River%20Valley%20SDBIP%202015-16.PDF"
def customUrlParser(url):
    extractedName = ""

    firstFilterdUrl = url.split("gov.za/Documents/")

    secondfilterdUrl = firstFilterdUrl[1].split("%20")

    n = 1
    while n < len(secondfilterdUrl):
        extractedName += secondfilterdUrl[n]
        n += 1
    print "url: " + extractedName
    filterNames = extractedName.split("/")
    extractedName = ""

    i = 0
    for name in filterNames:
        extractedName += name
        if i < len(filterNames) - 1:
            extractedName += ">"
        i += 1

    return extractedName

print customUrlParser(sampleUrl)