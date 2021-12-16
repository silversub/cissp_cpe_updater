import time
import csv
import json
import sys
import math
import dateutil.parser 
#from secrets import secrets #custom file made to store creds so they aren't in this main file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

#Location of Chrome Driver after downloading from http://chromedriver.chromium.org/downloads
#Download the version that matches the main version of Chrome you have installed (Click Chrome --> "About Google Chrome")
#Windows Example: r"C:\Users\USERNAME\Downloads\chromedriver.exe"
#MAC Example: r"/Users/USERNAME/Downloads/chromedriver"
ser = Service(r"/Users/USERNAME/Downloads/chromedriver")

driver = webdriver.Chrome(service=ser)
driver.get('https://cpe.isc2.org/s/') 

##Default maximum waiting time for an element/page to load
delay = 60

##Hard coded list of security domains
listDomains = ["Security and Risk Management", "Asset Security", "Security Architecture and Engineering", "Communication and Network Security", "Identity and Access Management", "Security Assessment and Testing", "Security Operations", "Software Development Security", "Group B"]

### Login ###
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'signIn__inputForEmail')))
    print ("Login Page is ready")
except TimeoutException:
    print ("Login Page - Loading took too much time!")

## You can automate your creds by uncommenting the following lines and storing them in a separate protected file... or just login manually. The script will wait 60 seconds before timing out
#creds = secrets()
username_box = driver.find_element(By.ID, 'signIn__inputForEmail')
username_box.send_keys("USERNAME")

passwd_box = driver.find_element(By.ID, 'signIn__inputForPassword')
passwd_box.send_keys("PASSWORD")

driver.find_element(By.ID, 'signIn__userSignIn').click()

counter = 0

with open('CSVFILENAME.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        flDuration = float(row['Duration'])

        #60 minutes = 1 CPE. Let's convert duration minutes to CPEs
        flDuration = flDuration / 60

        #Only accepts nearest .25. Round down to nearest .25
        flDuration = math.floor(flDuration*4)/4

        if flDuration >= .25:
                       
            # Pound sign (windows) or hyphen (unix/linux/osx) will remove leading zeros https://stackoverflow.com/questions/904928/python-strftime-date-without-leading-0
            dtCompletion = dateutil.parser.parse(row['Learner Completion Date'])
            strCompletion = dtCompletion.strftime("%-m/%-d/%Y")
            #strCompletion = dtCompletion.strftime("%#m/%#d/%Y")
            strTitle = (row['Learning Activity Title'])
            strDomain = (row['Domain'])
            if strDomain not in listDomains:
                raise NameError('Security domain name {0} is invalid'.format(strDomain))
            print(strCompletion)
            print(strTitle)

            # We only want to hit this on subsequent runs or it won't fully authenticate the first time
            if counter > 0:
                driver.get('https://cpe.isc2.org/s/') 

            ## Main CPE page ###
            strStartDateXPath = '//input[contains(@name,"start-date")]'
            strEndDateXPath = '//input[contains(@name,"end-date")]'
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strStartDateXPath)))
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, strStartDateXPath)))
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strEndDateXPath)))
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, strEndDateXPath)))
                print ("Main CPE page is ready")
            except TimeoutException:
                print ("Main CPE page - Loading took too much time!")

             
            start_date_box = driver.find_element(By.XPATH, strStartDateXPath)
            start_date_box.send_keys(strCompletion)

            end_date_box= driver.find_element(By.XPATH, strEndDateXPath)
            end_date_box.send_keys(strCompletion)
            end_date_box.send_keys(Keys.RETURN)

            ### Continue Button Clickable ###
            try:
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="continueButton"]')))
                print ("Continue button is clickable")
            except TimeoutException:
                print ("Continue button is clickable - Loading took too much time!")

            driver.find_element(By.XPATH, '//*[@id="continueButton"]').click()

            ### Category Radio Button ###
            strRadioBtnXPath='//span[text() = "Courses and Seminars - Other"]'
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strRadioBtnXPath)))
                WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, strRadioBtnXPath)))
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, strRadioBtnXPath)))
# element not interactable: element has zero size bug - using sleep for now
# I tried scrolling it into view but then ran into an issue with another element blocking it.
#                elem = driver.find_element(By.XPATH, strRadioBtnXPath)
#                driver.execute_script("arguments[0].scrollIntoView();", elem);
# move_to_element in selenium?

                print ("Category radio button is ready")
            except TimeoutException:
                print ("Category radio button - Loading took too much time!")

            time.sleep(2)
            driver.find_element(By.XPATH, strRadioBtnXPath).click()

            ### Course Details ###
            course_detail_elements=driver.find_elements(By.XPATH, '//*[@id="detailElement"]//input')
            # Title
            course_detail_elements[0].send_keys(strTitle)
            # Training Provider
            course_detail_elements[1].send_keys("IBM")
            # Credits - Enter a value from 0.25 to 40 in increments of 0.25.
            course_detail_elements[2].send_keys(flDuration)

            driver.find_element(By.CLASS_NAME, 'button-primary').click()

            ### Domain ###
            #strRadioBtnXPath='//span[text() = "Security Architecture and Engineering"]'
            strRadioBtnXPath='//span[text() = "{0}"]'.format(strDomain)
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strRadioBtnXPath)))
                WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, strRadioBtnXPath)))
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, strRadioBtnXPath)))
                print ("Domain radio button is ready")
            except TimeoutException:
                print ("Domain radio button - Loading took too much time!")
            driver.find_element(By.XPATH, strRadioBtnXPath).click()

            driver.find_element(By.CLASS_NAME, 'button-primary').click()

            ### Submit CPE ###
            strPageReadyXPath = "//h2[text()='Category & Detail']"
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, strPageReadyXPath)))
                WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, strPageReadyXPath)))
                WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, strPageReadyXPath)))
                print ("Submit CPE page is ready")
            except TimeoutException:
                print ("Submit CPE page - Loading took too much time!")
        
            #Comment the button click line out below if you want to run a test without submitting anything 
            driver.find_element(By.CLASS_NAME, 'button-primary').click()

            counter = counter + 1
