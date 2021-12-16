# Purpose
Intended for anyone who obtains the majority of their trainings from one vendor/company and can generate a CSV report. I personally did not want to manually enter each one into ISC2's website. This script helps automate that process.

# Initial Setup
```
virtualenv cissp
source cissp/bin/activate
pip3 install selenium
pip3 install python-dateutil
```

# Getting Started
- Download chromedriver from  http://chromedriver.chromium.org/downloads
  - Download the version that matches the main version of Chrome you have installed (Click Chrome --> "About Google Chrome")
- Download CSV report from your vendor/company
- Ensure `Duration` (minutes), `Learner Completion Date` (ISO 27 date), and `Learning Activity Title` are CSV header titles. If not change the code (or your CSV headers)
- Add a column called `Domain` to CSV file and tag them (Security and Risk Management, Asset Security, Security Architecture and Engineering, Communication and Network Security, Identity and Access Management, Security Assessment and Testing, Security Operations, Software Development Security, or Group B)
- Replace `USERNAME` and `PASSWORD` with your creds
- Replace `CSVFILENAME` with the name and location of your CSV file. Store the CSV file in the same directory as the script for ease of use
- Comment out the last submit click action before running. Do a test run and watch selenium process your data. If your comfortable with how it went then you can uncomment it out and go for real.
- `python3 CISSP.py` to start the script

# Caveats
- This script can break very easily if ISC2 makes any changes to their HTML
- This script is not idempotent. Meaning if you get halfway through the script and only 15 of your 30 trainings made it into ISC2 website, then you can't just run the script again. You'll need to update your CSV file with the remaining trainings you want to add.

# Issues
- "chromedriver” cannot be opened because the developer cannot be verified.
  - `xattr -d com.apple.quarantine ~/Downloads/chromedriver`
  - Source: https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de
- `element not interactable: element has zero size`
  - Not sure on this one still. Tried some execute javascript to scroll to the element but then ran into a conflict with another element blocking the click. For now I put a timeout of 2 seconds which for the most part seems to have solved it.

# XPath Tips
- Inspect element in chrome --> right click on element --> copy --> copy XPath 

# References
- Methods that are deprecated: https://stackoverflow.com/questions/69875125/find-element-by-commands-are-deprecated-in-selenium/69875984
- Official Documentation: https://www.selenium.dev/selenium/docs/api/py/
- No such element (great list of reasons why your element can't be found): https://stackoverflow.com/questions/48471321/nosuchelementexception-selenium-unable-to-locate-element
