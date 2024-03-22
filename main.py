
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC



class DOLPHIN_WEBDRIVER:
    def __init__(self) -> None:
        pass

    def getDriver(self, antyID):
        import selenium_dolphin as dolphin
        response = dolphin.run_profile(antyID)
        port = response['automation']['port']
        driver = dolphin.get_driver(options=self.testDriver_cap(), port=port)
        return driver

    def testDriver_cap(self):
        chrome_options = Options()
        chrome_options.headless = False
        chrome_options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"])
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        chrome_options.add_argument('--disable-application-cache')
        chrome_options.add_argument('--disable-cache')
        chrome_options.add_argument('--disable-component-update')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--start-minimized")
        chrome_options.add_argument('--disable-features=OptimizationGuideModelDownloading,OptimizationHintsFetching,OptimizationTargetPrediction,OptimizationHints')
        return chrome_options

class JOB:
    def __init__(self, driver) -> None:
        self.driver = driver
        self.RESULTS = {}
        self.XPATHS()

    def XPATHS(self):
        self.URL = "https://www.cv-library.co.uk/"
        self.KEYWORD_ = "//input[contains(@placeholder, 'Keywords')]"
        self.LOCATION_ = "//input[contains(@placeholder, 'Location')]"
        self.FIND_BTN = "//input[contains(@type, 'submit')]"
        self.JOBS = "//div[@class='page-main']//ol[@id='searchResults']/li[@class='results__item']"
        self.LINKS = "//h2[@class='job__title']//a"
        self.ApplyLink = "//*[contains(text(), 'Apply Now')]"
        self.SALARY = "//dl[@class='job__details l-flex-row']//dd[@class='job__details-value salary']"
        self.JobType = "//dl[@class='job__details l-flex-row']//dd[@class='job__details-value']"

    def scrap(self, keyword, loc=False ):
        urls = "https://www.cv-library.co.uk/{}-jobs"

        if loc: urls = urls + "-in-" + '-'.join(loc.split(' ')).lower()
        urls = urls.format('-'.join(keyword.lower().split(' '))) + "?page={}&perpage=100"
        urls = [urls.format(i) for i in range(1,6)]

        JOB_salary = []
        JOB_Titles = []
        JOB_TYPES = []
        JOB_applyLinks = []
        JOB_DetailsLink = []
        lastURL = None
        
        for url in urls:
            print(url)
            lastURL = url
            self.driver.get(url)

            myURl = self.driver.current_url
            print("Current URL: ", myURl)
            if myURl in urls[:urls.index(myURl)]: break

            WebDriverWait(self.driver, timeout=15).until(EC.presence_of_all_elements_located((By.XPATH, self.JOBS)))
            jobs = self.driver.find_elements(By.XPATH, self.JOBS)

            for job in jobs:
                try: title = job.find_element(By.XPATH, self.LINKS).text
                except: title = "N/A"

                try: salary = job.find_element(By.XPATH, self.SALARY).text
                except: salary = "N/A"

                try: jobType = job.find_element(By.XPATH, self.JobType)
                except: jobType = "N/A"

                try: link1 = job.find_element(By.XPATH, self.LINKS).get_attribute('href')
                except: link1 = "N/A"
                try: link2 = job.find_element(By.XPATH, self.ApplyLink).get_attribute('href')
                except: link2 = "N/A"

                JOB_Titles.append(title)
                JOB_salary.append(salary)
                JOB_TYPES.append(jobType)
                JOB_applyLinks.append(link1)
                JOB_DetailsLink.append(link2)
            
        return JOB_Titles, JOB_salary, JOB_TYPES, JOB_applyLinks, JOB_DetailsLink
        

keyword = "Python Developer"
Location = "London"

# dolphin = DOLPHIN_WEBDRIVER()
# driver = dolphin.getDriver(antyID=277017922)

import selenium_dolphin as dolphin

response = dolphin.run_profile(277017922)
port = response['automation']['port']
driver = dolphin.get_driver(port=port)

job = JOB(driver=driver)
results = job.scrap(keyword=keyword, loc=Location)
print(results)



# # loc = False
# loc = "United Kingdom"
# keyword = "Python Developer"
# # loc = "London"

# url = "https://www.cv-library.co.uk/{}-jobs"

# if loc: url = url + "-in-" + '-'.join(loc.split(' ')).lower()
# url = url.format('-'.join(keyword.lower().split(' '))) + "?page={}&perpage=100"
# url = [url.format(i) for i in range(1,6)]
# print(url)

# "https://www.cv-library.co.uk/python-jobs-in-london?us=1"


# "https://www.cv-library.co.uk/python-developer-jobs-in-united-kingdom?page=3&perpage=100"
# 'https://www.cv-library.co.uk/python-developer-jobs-in-united-kingdom?perpage=100&page=5'