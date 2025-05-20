from playwright.sync_api import sync_playwright
import time
import requests
def scrape_website(url,emailAddress,password):
    with sync_playwright() as p:
        # open browser session
        browser = p.chromium.launch(headless=False)
        # open the webpage
        page = browser.new_page()
        print(f"Opeing URL : {url}")
        # go to the specified URL
        page.goto(url)
        # wait to load the page completely
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        # Locate email and password by placeholder
        #page.get_by_role('textbox', name='Email Address').fill(emailAddress)
        page.get_by_placeholder('Email Address').fill(emailAddress)
        time.sleep(1)
        page.get_by_role('textbox', name='Password').fill(password)
        # Unchecking the check box
        page.get_by_role('checkbox', name='Keep me signed in').uncheck()
        time.sleep(1)
        # Locate by role and click the Sign in button
        page.get_by_role('button', name='Sign in').click()
        time.sleep(2)
        # Loading the page
        page.wait_for_load_state('domcontentloaded')
        time.sleep(2)
        # Locate by html lable and select the option
        page.get_by_label('Profession').select_option(value='1501')
        time.sleep(1)
        # Locate the download file by link
        metadataLink = page.get_by_role("link", name='Click here to download metadata file').get_attribute('href')
        allStatusLink = page.get_by_role("link", name='All Statuses').get_attribute('href')
        page.click(metadataLink)
        page.click(allStatusLink)
        # funtion to open a file
        def file_open(url):
            absolute_url = f"https://mqadatadownload.azurewebsites.net/{url}"
            file = requests.get(absolute_url)
            with open('arl.txt', 'wb') as f:
                f.write(file.content)
        # Calling the function
        file_open(metadataLink)
        file_open(allStatusLink)
        time.sleep(2)
        
        try:
            page.wait_for_selector("h1", timeout=5000)
            title = page.query_selector("h1").inner_text()
            print("Title:", title)
            paragraphs = page.query_selector_all("p")
            for p in paragraphs:
                print("Paragraph:", p.inner_text())
        except Exception as e:
            print("An error occurred:", e)
        # Closing Browser
        browser.close()

scrape_website("https://mqadatadownload.azurewebsites.net/LicensureData","chris24092004@gmail.com", "Cyrino@2024")