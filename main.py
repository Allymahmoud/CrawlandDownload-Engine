# Author: Ally Mahmoud
# Date: August 5th

# A python program to download all pdf files from
# an Active Server Page Extended file (".aspx")


import urllib2
import urllib
import re
import constants
import HTMLParser
from urlparse import urljoin
from collections import deque
import os
import  Queue


class LinkParser(HTMLParser.HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (key, value) in attrs:
                if key == "href":
                    newUrl = urljoin(self.baseurl, value)
                    self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseurl = url
        response = urllib.urlopen(url)

        if response.getheader('Content-Type') == 'text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            print self.links, htmlString
            return htmlString, self.links

        else:
            print "error 404"
            return "", []





# #connect to a URL
# website = urllib2.urlopen(constants.websiteUrl)
#
# #read html code
# html = website.read()
#
# #use re.findall to get all the links
# links = re.findall('"((http|ftp|url)s?://.*?)"', html)


sampleUrl ="http://mfma.treasury.gov.za/Documents/04.%20Service%20Delivery%20and%20Budget%20Implementation%20Plans/2015-16/02.%20Local%20Municipalities/EC106%20Sundays%20River%20Valley/EC106%20Sunday%20River%20Valley%20SDBIP%202015-16.PDF"

#method to construct a custom name out of a pdf link of
# this format "http://mfma.treasury.gov.za/Documents/04.%20Service%20Delivery%20and%20Budget%20Implementation%20Plans/2015-16/02.%20Local%20Municipalities/EC106%20Sundays%20River%20Valley/EC106%20Sunday%20River%20Valley%20SDBIP%202015-16.PDF"
def customUrlParser(url):
    extractedName = ""

    firstFilterdUrl = url.split("gov.za/Documents/")

    secondfilterdUrl = firstFilterdUrl[1].split("%20")

    n = 1
    while n < len(secondfilterdUrl):
        extractedName += secondfilterdUrl[n]
        n += 1

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


# i = 0
# for link in links:
#     if link[0].endswith(constants.fileExtension):
#         print (link)
#         longName = link[0].split("/")
#         filtername = longName[len(longName)-1]
#         print (filtername)
#
#         # urllib.urlretrieve(link[0],filtername)
#
#     if link[0].startswith(constants.baseURL):
#         i+=1
#         print (i, link[0])
#
# print customUrlParser(sampleUrl)

#method to convert list of tuples to a list of string
def listTuplesTolistStrings(listTuples):
    listStrings = []
    for tuple in listTuples:
        listStrings.append(tuple[0])

    return listStrings


def construct_custom_pdf_url(html, pdflinks, counter):
    parsed = html.split("HREF=\"/Documents/04.")

    for elements in parsed:
        filtered = elements.split("\"")

        newPdfUrl = "http://mfma.treasury.gov.za/Documents/04." + filtered[0]
        print str(counter) + " found pdf url: " + newPdfUrl
        if not newPdfUrl in pdflinks:
            pdflinks.append(newPdfUrl)


def crawler(depth=constants.depth, baseurl = constants.baseURL, seedUrl = constants.websiteUrl, fileExtension = constants.fileExtension):
    pagesToVisit = deque()
    pagesToVisit.append(seedUrl)

    visitedPages = {}
    pdflinks = []
    currentDepth = 0
    counter = 0
    while len(pagesToVisit) > 0:
        if len(pagesToVisit) < 400:
            print len(pagesToVisit)

        currentUrl = pagesToVisit.popleft()



        if not (currentUrl in visitedPages):
            # print "Visiting :" + currentUrl

            if currentUrl.startswith(baseurl):
                visitedPages[currentUrl]=1

                if currentUrl.endswith(fileExtension):
                    counter+=1
                    print str(counter) + " found pdf document: " + currentUrl
                else:
                    # connect to a URL
                    website = urllib2.urlopen(currentUrl)

                    # read html code
                    html = website.read()

                    parsed = html.split("HREF=\"/Documents")

                    for elements in parsed:
                        filtered = elements.split("\"")

                        newPdfUrl = "http://mfma.treasury.gov.za/Documents" + filtered[0]
                        if newPdfUrl.endswith(fileExtension):
                            counter+=1

                            if not newPdfUrl in pdflinks:
                                # print str(counter) + " found pdf url: " + newPdfUrl
                                # filepath = "/Users/Allymahmoud/desktop/downloadedpdf/"+customUrlParser(s)
                                if os.path.exists(customUrlParser(newPdfUrl)):
                                    if newPdfUrl == "IntegratedDevelopmentPlans>2017-18>01.Draft>03.Districtmunicipalities>DC20FezileDabi>DC20FezileDabiDraftIDP2017-18.pdf":
                                        print ("pdf file exist: " + newPdfUrl )

                                else:
                                    try:
                                        urllib.urlretrieve(newPdfUrl, customUrlParser(newPdfUrl))
                                        print "successfully downloaded :" + newPdfUrl
                                    except:
                                        print "failed to download :" + newPdfUrl

                                pdflinks.append(newPdfUrl)



                    # use re.findall to get all the links
                    links = re.findall('"((http|ftp)s?://.*?)"', html)

                    # add the new urls to pagesToVisit
                    newPagesTovisit = listTuplesTolistStrings(links)
                    for page in newPagesTovisit:
                        if not page in pagesToVisit:
                            if not page in visitedPages:
                                pagesToVisit.append(page)

                    # pagesToVisit.extend(listTuplesTolistStrings(links))
        # else:
        #     print "this has been visited already" + currentUrl
    print ("\\nn\n\nSUCCESS\n\n")


    out_file = open("output.txt", "w")  # open and write in the file
    # for loop to iterate over each line of the text file
    for link in pdflinks:
        out_file.write(link + "\n")

    out_file.close()  # close the file opened in out_file


os.chdir("/Users/Allymahmoud/desktop/downloadedpdf")
crawler()

def crawlernew(url, word, maxPages):
    pagesToVisit = [url]
    numberVisited = 0
    foundWord = False

    while numberVisited < maxPages and pagesToVisit !=[] and not foundWord:
        numberVisited += 1
        url = pagesToVisit[0]

        pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting: ", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            print links

            if data.find(word) > -1:
                foundWord = True

            pagesToVisit = pagesToVisit + links
            print("success..")
        except:
            print("Failed..")

    if foundWord:
        print("The word", word, "was found at", url)

    else:
        print("word never found")



# crawlernew(constants.websiteUrl, "ally", 30)




