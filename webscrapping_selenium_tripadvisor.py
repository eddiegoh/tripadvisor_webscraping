# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 20:30:53 2018
a
@author: Eddie
"""

from selenium import webdriver
import time
import json
from bs4 import BeautifulSoup

# function to scrap reviews, country, rating and date of reviews


def extract_reviews(driver):
    try:
        driver.find_element_by_css_selector(".taLnk.ulBlueLinks").click()  # click on More
    except Exception as error:
        print(error)
        print("Clicking MORE on review has error")
    time.sleep(5)
    data = driver.page_source
    soup = BeautifulSoup(data, "html.parser")
    # i=1
    for link in soup.find_all("div", {"class": "review-container"}):
        # scrapping review
        reviews.append(link.find('p').text)
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
        # i=i+1
    return [len(soup.find_all("div", {"class": "review-container"})), reviews, date_of_review, country, rating]


drive = webdriver.Chrome(".\\chromedriver.exe")
drive.set_page_load_timeout(10)
drive.get("https://www.tripadvisor.com.sg/Hotel_Review-g294265-d1770798-Reviews-Marina_Bay_Sands-Singapore.html")
time.sleep(5)
pgNum = 1  # starting page of reviews
pgToReview = 1226  # ending page of reviews
numOfReviews = 0
reviewsInPage = 0
reviews = []
date_of_review = []
country = []
rating = []
fp = open(".\\TripAdvisorReviewstesting.json", mode="w")
try:
    for pgNum in list(range(pgNum, pgToReview)):
        if pgNum == 1:
            try:
                ''' click traveller type families
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/label").click()
                '''
                # click traveller type couple
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[2]/label").click()
                '''
                # click solo traveller type
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[3]/label").click()
                '''
                '''
                # click friend traveller type
                drive.find_element_by_xpath("//*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[5]/label").click()
                '''
                '''
                # click Business traveller type
                drive.find_element_by_xpath(" //*[@id='taplc_detail_filters_hr_resp_0']/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[4]/label").click()
                '''
                time.sleep(5)
                print("In first page...")
            except Exception as e:
                print(e)
                print("Clicking traveler type checkbox has error")
        else:
            try:
                print("\n\nClicked Page " + str(pgNum))
                el = drive.find_element_by_css_selector(".unified.ui_pagination .nav.next")
                el.click()
                time.sleep(5)
            except Exception as e:
                print(e)
                print("Clicking next page of review element has error")
        [reviewsInPage, reviews, date_of_review, country, rating] = extract_reviews(drive)
        numOfReviews += reviewsInPage
except Exception as e:
    print(e)
    print("program run into error, proceed with json dump")

json.dump({"review": reviews, "date": date_of_review, "country": country, "rating": rating}, fp)
print('Total review:' + str(numOfReviews))
fp.close()
drive.close()
