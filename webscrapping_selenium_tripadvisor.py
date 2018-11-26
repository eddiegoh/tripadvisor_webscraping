# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 20:30:53 2018
a
@author: Eddie
1)Do go through the whole script to understand the flow of the application before 
running it.
2)Some of the parameters do require manual input from user and they are indicated 
at the specific line.
3)Trip advisor website structure might change from time to time, hence affect the 
usability of the script
4) Usable as of 7 Nov 2018
5) things to configure - url, ending page number of reviews, traveller type & xpath
"""

from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup


# function to scrap reviews, country, rating and date of reviews

def extract_reviews(driver):
    time.sleep(5)
    try:
        driver.find_element_by_css_selector(".taLnk.ulBlueLinks").click()  # click on More
    except Exception as error:
        print(error)
        print("Clicking MORE on review has error")
    time.sleep(5)
    # by scrolling through all the reviews allows google translate to take place 
    for i in range(300, 1800, 300):
        driver.execute_script("window.scrollTo(0, window.pageYOffset+{});".format(i))
        time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
    
    # capture the source of the website
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")
    
    # each review in kept in review container so we will loop through all container to extract data out
    for link in soup.find_all("div", {"class": "review-container"}):

        # use reviews.append(link.find('p').text) if only one specific language you are interest
        # Below approach is to extract reviews from all languages
        # it also required user to manually configure chrome to always translate to english
        # Upon web page loaded right click and select google translate and option put always translate
        # scrapping review
        review = ''
        p = link.find('p')
        for font in p.findAll('font'):
            for sub_font in font.findAll('font'):
                review += sub_font.text
        if len(review) == 0:
            print('no google translation')
            reviews.append(p.text)
        else:
            print(review)
            reviews.append(review)
            
        # scrapping date of review
        date_of_review.append(link.find("span", {"class": "ratingDate"}).get("title"))
        
        # scrapping reviewer nationalities
        try:
            country.append(link.find("div", {"class": "userLoc"}).text)
        except Exception as error:
            print(error)
            print('country not indicated')
            country.append("N.A.")
            
        # scrapping rating
        rating.append(link.find("div", {"class": "ui_column is-9"}).find("span", recursive=False)["class"][1])
       
        # scrapping reviewer name
        try:
            name.append(link.find("div", {"class": "info_text"}).find("div", class_=False, id=False).text)
        except Exception as error:
            print(error)
            print('Name not indicated')
            name.append("N.A.")
            
        # traveller type got to indicate manually
        traveller_type.append('Friends')
    return [len(soup.find_all("div", {"class": "review-container"})), reviews, date_of_review, country, rating, name, traveller_type]


# open the url in chrome browser and set the default language to english
options = webdriver.ChromeOptions()
options.add_argument('--lang=en')
drive = webdriver.Chrome(".\\chromedriver.exe", chrome_options=options)
drive.set_page_load_timeout(10)

# MBS casino
drive.get('https://www.tripadvisor.com.sg/Attraction_Review-g294265-d1062119-Reviews-Marina_Bay_Sands_Casino-Singapore.html')
# RWS casino
# drive.get('https://www.tripadvisor.com.sg/Attraction_Review-g294265-d1994850-Reviews-Resorts_World_Sentosa_Casino-Singapore.html')
# MBS
# drive.get("https://www.tripadvisor.com.sg/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html")
time.sleep(15)  # this 15 second is meant for user to set the google translation in the chrome manually

# pg_num and pg_to_review need to set manually
pg_num = 1  # starting page of reviews
pg_to_review = 28 # ending page of reviews - page+1

# initialise variables
num_of_reviews = 0
reviews = []
date_of_review = []
country = []
rating = []
traveller_type = []
name = []

# name of the json file to be set accordingly
fp = open(".\\Trip_Advisor_Reviews_MBS_Casino_Friends.json", mode="w")
try:
    for pg_num in list(range(pg_num, pg_to_review)):
        if pg_num == 1:
            try:
                # click on the option all languages
                drive.find_element_by_xpath(
                    "//*[@id='taplc_detail_filters_ar_responsive_0']/div/div[1]/div/div[2]/div[4]/div/div[2]/div[1]/div[1]/label"
                ).click()
                time.sleep(2)
                
                # The following are the XPATHS for the 5 checkboxes associate with traveller type
                # The xpath belong to the checkboxes of different reviews
                # Suggest to reconfirm the xpath from chrome inspect console from time to time
                ''' click traveller type checkbox - families
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/label").click() # MBS
                '''
                # RWS Casino
                # drive.find_element_by_xpath('//*[@id="taplc_detail_filters_ar_responsive_0"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/label').click()
                # drive.find_element_by_xpath('//*[@id="taplc_detail_filters_ar_responsive_0"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/label).click()
                
                # click traveller type couple
                '''
                drive.find_element_by_xpath(
                    "// *[ @ id = 'taplc_detail_filters_ar_responsive_0'] / div / div[1] / div / div[2] / div[2] / div / div[2] / div / div[2] / label"
                ).click()  # RWS/MBS Casino '''
                # drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[2]/label").click()
                
                '''
                # click solo traveller type
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[3]/label").click()
                '''
                # drive.find_element_by_xpath('//*[@id="taplc_detail_filters_ar_responsive_0"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[3]/label/font/font').click()
                '''
                # click friend traveller type
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[5]/label").click()
                '''
                drive.find_element_by_xpath('//*[@id="taplc_detail_filters_ar_responsive_0"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[5]/label/font/font').click()
                
                '''
                # click Business traveller type
                drive.find_element_by_xpath(" //*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[4]/label").click()
                '''
                # drive.find_element_by_xpath('//*[@id="taplc_detail_filters_ar_responsive_0"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[4]/label/font/font').click()
                time.sleep(2)
                print("In first page...")
            except Exception as e:
                print(e)
                print("Clicking traveler type checkbox has error")
        else:
            try:
                print("\n\nClicked Page " + str(pg_num))
                el = drive.find_element_by_css_selector(".unified.ui_pagination .nav.next")
                el.click()
                time.sleep(10)
            except Exception as e:
                print(e)
                print("Clicking next page of review element has error")
        [reviews_in_page, reviews, date_of_review, country, rating, name, traveller_type] = extract_reviews(drive)
        num_of_reviews += reviews_in_page
except Exception as e:
    print(e)
    print("program run into error, proceed with json dump")

json.dump({"review": reviews,
           "date": date_of_review,
           "country": country,
           "rating": rating,
           "name": name,
           "type": traveller_type}, fp)
print('Total review:' + str(num_of_reviews))
fp.close()
drive.close()

