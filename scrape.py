#-*- coding: utf-8 -*-
import urllib2
import urllib
import csv
from bs4 import BeautifulSoup

#Get list of MP webpages
MPList = "https://www.parliament.uk/mps-lords-and-offices/mps/"
page = urllib2.urlopen(MPList)
soup = BeautifulSoup(page, "html.parser")

# 'data' is the list of MP Url's
data = []

for i in range (1, 651):
    if i<10:
        rowId = "ctl00_ctl00_FormContent_SiteSpecificPlaceholder_PageContent_rptMembers_ctl"+ str(0) + str(i) +"_hypName"
    else:
        rowId = "ctl00_ctl00_FormContent_SiteSpecificPlaceholder_PageContent_rptMembers_ctl"+ str(i) +"_hypName"
    row = soup.find("a", {"id":rowId})
    wholeUrl = row.attrs['href'] #whole url
    MP = wholeUrl[45:] # MP specific end of URL
    MPUrl = "http://www.parliament.uk/biographies/commons/" + MP
    data.append(MPUrl)



for i in range (0, 650):
    #Go to specific page
    page = urllib2.urlopen(data[i])
    soup = BeautifulSoup(page, "html.parser")

    #Get the information from the page
    name_box = soup.findAll(id="commons-biography-header")
    name = name_box[0].get_text().strip()
    name1 = name.encode('ascii', 'ignore')
    # def myfunction(name):
    #     try:
    #         name = unicode(name, 'utf-8').decode('utf-8')
    #     except UnicodeEncodeError:
    #         name = "error"
    # split_name = name.split()
    # first_name = split_name[0]
    # last_name = split_name[1]

    interests = soup.find_all(id="biography-entry-body")
    try:
        interestsP = interests[0].get_text().strip()
    except IndexError:
        interestsP = ""
    try:
        interestsG = interests[1].get_text().strip()
    except IndexError:
        interestsG = ""

    #Save data to csv file
    with open('index.csv', 'a') as csv_file:
     writer = csv.writer(csv_file)
     writer.writerow([name1, interestsP, interestsG])
