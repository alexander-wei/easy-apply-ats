import math, constants, config, time
from typing import List

from selenium import webdriver


class AlreadyAppliedException(Exception):
    pass


class BlacklistedJobException(Exception):
    pass


class SubmitButtonNotFoundException(Exception):
    pass


def chromeBrowserOptions():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    if config.headless:
        options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    if len(config.chromeProfilePath) > 0:
        initialPath = config.chromeProfilePath[0 : config.chromeProfilePath.rfind("/")]
        profileDir = config.chromeProfilePath[config.chromeProfilePath.rfind("/") + 1 :]
        options.add_argument("--user-data-dir=" + initialPath)
        options.add_argument("--profile-directory=" + profileDir)
    else:
        options.add_argument("--incognito")
    return options


def prRed(prt):
    print(f"\033[91m{prt}\033[00m")


def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")


def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")


def getUrlDataFile():
    urlData = ""
    try:
        file = open("data/urlData.txt", "r")
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./data folder exists and check config.py values of yours. Then run the bot again"
        prRed(text)
    return urlData


def jobsToPages(numOfJobs: str) -> int:
    number_of_pages = 1

    if " " in numOfJobs:
        spaceIndex = numOfJobs.index(" ")
        totalJobs = numOfJobs[0:spaceIndex]
        totalJobs_int = int(totalJobs.replace(",", ""))
        number_of_pages = math.ceil(totalJobs_int / constants.jobsPerPage)
        if number_of_pages > 40:
            number_of_pages = 40

    else:
        number_of_pages = int(numOfJobs)

    return number_of_pages


def urlToKeywords(url: str) -> List[str]:
    keywordUrl = url[url.index("keywords=") + 9 :]
    keyword = keywordUrl[0 : keywordUrl.index("&")]
    locationUrl = url[url.index("location=") + 9 :]
    location = locationUrl[0 : locationUrl.index("&")]
    return [keyword, location]


def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " + timeStr + ".txt"
    try:
        with open("data/" + fileName, encoding="utf-8") as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)

        with open("data/" + fileName, "w", encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + timeStr + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "
                + "\n"
            )
            for line in lines:
                f.write(line)
            f.write(text + "\n")

    except:
        with open("data/" + fileName, "w", encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + timeStr + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "
                + "\n"
            )

            f.write(text + "\n")


def click_button_in_containers(continue_buttons):
    for panel in continue_buttons:
        if len(panel) > 0:
            for button in panel:
                if button.is_displayed() and button.is_enabled():
                    try:
                        button.click()
                    except:
                        """pass"""
                        pass


def printInfoMes(bot: str):
    prYellow("ℹ️ " + bot + " is starting soon... ")


def donate(self):
    prYellow(
        "If you like the project, please support me so that i can make more such projects, thanks!"
    )
    try:
        self.driver.get("https://www.automated-bots.com/")
    except Exception as e:
        prRed("Error in donate: " + str(e))


class LinkedinUrlGenerate:
    def generateUrlLinks(self):
        path = []
        for location in config.location:
            for keyword in config.keywords:
                url = (
                    constants.linkJobUrl
                    + "?f_AL=true&keywords="
                    + keyword
                    + self.jobType()
                    + self.remote()
                    + self.checkJobLocation(location)
                    + self.jobExp()
                    + self.datePosted()
                    + self.salary()
                    + self.sortBy()
                )
                path.append(url)
        return path

    def checkJobLocation(self, job):
        jobLoc = "&location=" + job
        match job.casefold():
            case "asia":
                jobLoc += "&geoId=102393603"
            case "europe":
                jobLoc += "&geoId=100506914"
            case "northamerica":
                jobLoc += "&geoId=102221843&"
            case "southamerica":
                jobLoc += "&geoId=104514572"
            case "australia":
                jobLoc += "&geoId=101452733"
            case "africa":
                jobLoc += "&geoId=103537801"

        return jobLoc

    def jobExp(self):
        jobtExpArray = config.experienceLevels
        firstJobExp = jobtExpArray[0]
        _jobExp = ""
        match firstJobExp:
            case "Internship":
                _jobExp = "&f_E=1"
            case "Entry level":
                _jobExp = "&f_E=2"
            case "Associate":
                _jobExp = "&f_E=3"
            case "Mid-Senior level":
                _jobExp = "&f_E=4"
            case "Director":
                _jobExp = "&f_E=5"
            case "Executive":
                _jobExp = "&f_E=6"
        for index in range(1, len(jobtExpArray)):
            match jobtExpArray[index]:
                case "Internship":
                    _jobExp += "%2C1"
                case "Entry level":
                    _jobExp += "%2C2"
                case "Associate":
                    _jobExp += "%2C3"
                case "Mid-Senior level":
                    _jobExp += "%2C4"
                case "Director":
                    _jobExp += "%2C5"
                case "Executive":
                    _jobExp += "%2C6"

        return _jobExp

    def datePosted(self):
        _datePosted = ""
        match config.datePosted[0]:
            case "Any Time":
                _datePosted = ""
            case "Past Month":
                _datePosted = "&f_TPR=r2592000&"
            case "Past Week":
                _datePosted = "&f_TPR=r604800&"
            case "Past 24 hours":
                _datePosted = "&f_TPR=r86400&"
        return _datePosted

    def jobType(self):
        jobTypeArray = config.jobType
        firstjobType = jobTypeArray[0]
        _jobType = ""
        match firstjobType:
            case "Full-time":
                _jobType = "&f_JT=F"
            case "Part-time":
                _jobType = "&f_JT=P"
            case "Contract":
                _jobType = "&f_JT=C"
            case "Temporary":
                _jobType = "&f_JT=T"
            case "Volunteer":
                _jobType = "&f_JT=V"
            case "Intership":
                _jobType = "&f_JT=I"
            case "Other":
                _jobType = "&f_JT=O"
        for index in range(1, len(jobTypeArray)):
            match jobTypeArray[index]:
                case "Full-time":
                    _jobType += "%2CF"
                case "Part-time":
                    _jobType += "%2CP"
                case "Contract":
                    _jobType += "%2CC"
                case "Temporary":
                    _jobType += "%2CT"
                case "Volunteer":
                    _jobType += "%2CV"
                case "Intership":
                    _jobType += "%2CI"
                case "Other":
                    _jobType += "%2CO"
        _jobType += "&"
        return _jobType

    def remote(self):
        remoteArray = config.remote
        firstJobRemote = remoteArray[0]
        _jobRemote = ""
        match firstJobRemote:
            case "On-site":
                _jobRemote = "f_WT=1"
            case "Remote":
                _jobRemote = "f_WT=2"
            case "Hybrid":
                _jobRemote = "f_WT=3"
        for index in range(1, len(remoteArray)):
            match remoteArray[index]:
                case "On-site":
                    _jobRemote += "%2C1"
                case "Remote":
                    _jobRemote += "%2C2"
                case "Hybrid":
                    _jobRemote += "%2C3"

        return _jobRemote

    def salary(self):
        _salary = ""
        match config.salary[0]:
            case "$40,000+":
                _salary = "f_SB2=1&"
            case "$60,000+":
                _salary = "f_SB2=2&"
            case "$80,000+":
                _salary = "f_SB2=3&"
            case "$100,000+":
                _salary = "f_SB2=4&"
            case "$120,000+":
                _salary = "f_SB2=5&"
            case "$140,000+":
                _salary = "f_SB2=6&"
            case "$160,000+":
                _salary = "f_SB2=7&"
            case "$180,000+":
                _salary = "f_SB2=8&"
            case "$200,000+":
                _salary = "f_SB2=9&"
        return _salary

    def sortBy(self):
        _sortBy = ""
        match config.sort[0]:
            case "Recent":
                _sortBy = "_sortBy=DD"
            case "Relevent":
                _sortBy = "_sortBy=R"
        return _sortBy
