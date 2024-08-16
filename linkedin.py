from random import randint
import argparse
import ast
import pickle, hashlib
import re
import time, random, os
import traceback

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchWindowException,
    ElementClickInterceptedException,
)
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session
from webdriver_manager.chrome import ChromeDriverManager

import db
import db.query as dbquery
import utils, constants, config


countApplied = 0


class Linkedin:

    def __init__(
        self,
        session_id=None,
        hands_free=None,
        url_list=None,
        retry=None,
        recommended_jobs=None,
    ):
        self.session_id = session_id
        self.hands_free = hands_free
        self.url_list = url_list
        self.retry_mode = retry
        self.recommended_jobs = recommended_jobs
        utils.prYellow(
            "🤖 Thanks for using Easy Apply Jobs bot, for more information you can visit our site - www.automated-bots.com"
        )
        utils.prYellow("🌐 Bot will run in Chrome browser and log in Linkedin for you.")
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=utils.chromeBrowserOptions(),
        )
        self.cookies_path = (
            f"{os.path.join(os.getcwd(),'cookies')}/{self.getHash(config.email)}.pkl"
        )
        self.driver.get("https://www.linkedin.com")
        self.loadCookies()

        if not self.isLoggedIn():
            self.driver.get(
                "https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin"
            )
            utils.prYellow("🔄 Ensure that you are logged in.")
            try:
                self.driver.find_element("id", "username").send_keys(config.email)
                time.sleep(2)
                self.driver.find_element("id", "password").send_keys(config.password)
                time.sleep(30)
            except:
                utils.prRed(
                    "❌ Couldn't log in Linkedin by using Chrome. Ensure that you are logged in."
                )

            self.saveCookies()

        self.linkJobApply()

    def getHash(self, string):
        return hashlib.md5(string.encode("utf-8")).hexdigest()

    def loadCookies(self):
        if os.path.exists(self.cookies_path):
            cookies = pickle.load(open(self.cookies_path, "rb"))
            self.driver.delete_all_cookies()
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def saveCookies(self):
        pickle.dump(self.driver.get_cookies(), open(self.cookies_path, "wb"))

    def isLoggedIn(self):
        self.driver.get("https://www.linkedin.com/feed")
        try:
            self.driver.find_element(By.XPATH, '//*[@id="ember14"]')
            return True
        except:
            pass
        return False

    def generateUrls(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        try:
            with open("data/urlData.txt", "w", encoding="utf-8") as file:
                linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedinJobLinks:
                    file.write(url + "\n")
            utils.prGreen(
                "✅ Apply urls are created successfully, now the bot will visit those urls."
            )
        except:
            utils.prRed(
                "❌ Couldn't generate urls, make sure you have editted config file line 25-39"
            )

    def dialogue_post_resume(
        self,
        __posting_id,
        offerPage,
        jobProperties,
        continue_buttons,
        comPercentage_list,
    ):
        j = 6
        while len(comPercentage_list) == 0 and j > 0:
            continue_buttons = [
                self.driver.find_elements(
                    By.CSS_SELECTOR, "button[aria-label='Continue to next step']"
                ),
                self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'artdeco-modal__content jobs-easy-apply-modal__content')]//button[contains(@class,'jobs-apply-button artdeco-button')]",
                ),
                self.driver.find_elements(
                    By.XPATH,
                    "//button[contains(@class,'jobs-apply-button artdeco-button')]",
                ),
            ]
            utils.click_button_in_containers(continue_buttons)

            if not self.hands_free:
                time.sleep(4)
            j -= 1
            comPercentage_list = self.driver.find_elements(
                By.XPATH, "html/body/div[3]/div/div/div[2]/div/div/span"
            )
            if len(comPercentage_list) < 1:
                """continue"""
                continue

        result = self.applyProcess(offerPage)
        lineToWrite = jobProperties + " | " + result
        self.displayWriteResults(lineToWrite)

        with Session(db.engine) as session:
            __user_application = db.models.UserApplication(
                posting_id=__posting_id, session_id=self.session_id
            )
            session.add(__user_application)
            session.commit()
        return lineToWrite

    def begin_dialog_manypage(
        self,
        __posting_id,
        offerPage,
        jobProperties,
    ):
        try:
            continue_buttons = [
                self.driver.find_elements(
                    By.CSS_SELECTOR, "button[aria-label='Continue to next step']"
                ),
                self.driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'artdeco-modal__content jobs-easy-apply-modal__content')]//button[contains(@class,'jobs-apply-button artdeco-button')]",
                ),
            ]
            utils.click_button_in_containers(continue_buttons)
        except:
            raise Exception

        time.sleep(random.uniform(1, constants.botSpeed))
        self.chooseResume()
        comPercentage_list = []
        lineToWrite = self.dialogue_post_resume(
            __posting_id,
            offerPage,
            jobProperties,
            continue_buttons,
            comPercentage_list,
        )
        return lineToWrite

    def dialog_begin_singlepage(self, __posting_id, offerPage, jobProperties):
        global countApplied
        self.chooseResume()
        if config.followCompanies is False:
            try:
                unfollow_button = self.driver.find_elements(
                    By.CSS_SELECTOR, "label[for='follow-company-checkbox']"
                )
                if len(unfollow_button) > 0:
                    unfollow_button[0].click()
            except:
                """pass"""
                pass

        try:
            self.driver.find_element(
                By.CSS_SELECTOR, "button[aria-label='Submit application']"
            ).click()
        except:
            raise utils.SubmitButtonNotFoundException

        time.sleep(random.uniform(1, constants.botSpeed))
        lineToWrite = (
            jobProperties
            + " | "
            + "* 🥳 Just Applied to this job: "
            + str(offerPage)
            + " | SKIPPED (DEBUG)"
        )

        with Session(db.engine) as session:
            __user_application = db.models.UserApplication(
                posting_id=__posting_id, session_id=self.session_id
            )
            session.add(__user_application)
            session.commit()
        self.displayWriteResults(lineToWrite)
        countApplied += 1
        return lineToWrite, session

    def job_posting_main(self, countJobs, __posting_id, offerPage):
        self.driver.get(offerPage)
        time.sleep(random.uniform(1, constants.botSpeed))
        countJobs += 1
        jobProperties, __jobProperties = self.getJobProperties(countJobs)

        with Session(db.engine) as session:
            __posting = db.models.Posting(url=str(offerPage), **__jobProperties)
            session.add(__posting)
            session.commit()
            __posting_id = __posting.id

        try:
            easyApplybutton = self.easyApplyButton()
            if not easyApplybutton:
                raise utils.AlreadyAppliedException
            easyApplybutton.click()
            time.sleep(random.uniform(1, constants.botSpeed))
            try:
                lineToWrite, session = self.dialog_begin_singlepage(
                    __posting_id, offerPage, jobProperties
                )

            except utils.SubmitButtonNotFoundException:
                lineToWrite = self.begin_dialog_manypage(
                    __posting_id,
                    offerPage,
                    jobProperties,
                )
        except utils.AlreadyAppliedException:
            lineToWrite = (
                jobProperties + " | " + "* 🥳 Already applied! Job: " + str(offerPage)
            )
            self.displayWriteResults(lineToWrite)

        except (Exception, NoSuchWindowException, ElementClickInterceptedException):
            # catchall begin_dialog_manypage
            print(traceback.format_exc())
            self.chooseResume()
            lineToWrite = (
                jobProperties
                + " | "
                + "* 🥵 Cannot apply to this Job! "
                + str(offerPage)
            )
            self.displayWriteResults(lineToWrite)

        return countJobs

    def linkJobApply(self):
        global countApplied
        self.generateUrls()
        countApplied = 0
        countJobs = 0

        urlData = utils.getUrlDataFile()

        __posting_id = -1

        if self.recommended_jobs:
            urlData = [
                "https://www.linkedin.com/jobs/collections/recommended?discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII&lipi=urn%3Ali%3Apage%3Ad_flagship3_job_home%3BybeZvyRYR527XzcbZ45%2BhA%3D%3D"
            ]
        for url in urlData:
            url = re.sub("\n", "", url)
            self.driver.get(url)
            time.sleep(random.uniform(1, constants.botSpeed))

            try:
                totalJobs = self.driver.find_element(By.XPATH, "//small").text
                totalPages = utils.jobsToPages(totalJobs)
            except:
                continue

            try:
                urlWords = utils.urlToKeywords(url)
                lineToWrite = (
                    "\n Category: "
                    + urlWords[0]
                    + ", Location: "
                    + urlWords[1]
                    + ", Applying "
                    + str(totalJobs)
                    + " jobs."
                )
                self.displayWriteResults(lineToWrite)
            except:
                pass
            for page in range(totalPages):
                currentPageJobs = constants.jobsPerPage * page
                url = url + "&start=" + str(currentPageJobs)
                self.driver.get(url)
                time.sleep(random.uniform(1, constants.botSpeed))

                offersPerPage = self.driver.find_elements(
                    By.XPATH, "//li[@data-occludable-job-id]"
                )
                offerIds = [
                    (offer.get_attribute("data-occludable-job-id").split(":")[-1])
                    for offer in offersPerPage
                ]
                time.sleep(random.uniform(1, constants.botSpeed))

                for offer in offersPerPage:
                    if not self.element_exists(
                        offer, By.XPATH, ".//*[contains(text(), 'Applied')]"
                    ):
                        offerId = offer.get_attribute("data-occludable-job-id")
                        offerIds.append(int(offerId.split(":")[-1]))

                __mapper = lambda jobID: "https://www.linkedin.com/jobs/view/" + str(
                    jobID
                )
                make_url = map(__mapper, offerIds)

                offerPages = iter(make_url)
                if not self.url_list is None:
                    offerPages = open(self.url_list, "r").readlines(9999)
                if self.retry_mode:
                    assert not self.hands_free
                    offerPages = dbquery.DBQuery.get_incomplete_urls(db)

                for offerPage in offerPages:
                    countJobs = self.job_posting_main(
                        countJobs, __posting_id, offerPage
                    )

            utils.prYellow(
                "Category: "
                + urlWords[0]
                + ","
                + urlWords[1]
                + " applied: "
                + str(countApplied)
                + " jobs out of "
                + str(countJobs)
                + "."
            )

        utils.donate(self)

    def chooseResume(self):
        try:
            self.driver.find_element(
                By.CLASS_NAME, "jobs-document-upload__title--is-required"
            )
            resumes = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'ui-attachment--pdf')]"
            )
            if (
                len(resumes) == 1
                and resumes[0].get_attribute("aria-label") == "Select this resume"
            ):
                resumes[0].click()
            elif (
                len(resumes) > 1
                and resumes[config.preferredCv - 1].get_attribute("aria-label")
                == "Select this resume"
            ):
                resumes[config.preferredCv - 1].click()
            elif type(len(resumes)) != int:
                utils.prRed(
                    "❌ No resume has been selected please add at least one resume to your Linkedin account."
                )
        except:
            pass

    def getJobProperties(self, count):
        jobTitle = ""
        jobLocation = ""
        jobDescription = ""
        jobCompanyName = ""
        jobDetail = ""

        time.sleep(5)
        try:
            # t-24 t-bold inline
            # jobTitle = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            jobTitle = (
                self.driver.find_element(
                    By.XPATH, "//h1[contains(@class, 't-24 t-bold inline')]"
                )
                .get_attribute("innerHTML")
                .strip()
            )
            res = [
                blItem
                for blItem in config.blackListTitles
                if (blItem.lower() in jobTitle.lower())
            ]
            if len(res) > 0:
                jobTitle += "(blacklisted title: " + " ".join(res) + ")"
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow("⚠️ Warning in getting jobTitle: " + str(e)[0:50])
            jobTitle = ""

        try:
            jobWorkStatusSpans = self.driver.find_elements(
                By.XPATH,
                "//span[contains(@class,'ui-label ui-label--accent-3 text-body-small')]//span[contains(@aria-hidden,'true')]",
            )
            for span in jobWorkStatusSpans:
                jobLocation = jobLocation + " | " + span.text

        except Exception as e:
            if config.displayWarnings:
                print(e)
                utils.prYellow("⚠️ Warning in getting jobLocation: " + str(e)[0:100])
            jobLocation = ""

        try:
            jobDescriptionSpans = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'jobs-description__content jobs-description-content')]//div",
            )
            for span in jobDescriptionSpans:
                jobDescription = jobDescription + "\n\n" + span.text

        except Exception as e:
            if config.displayWarnings:
                print(e)
                utils.prYellow("⚠️ Warning in getting JOBDESSCRIPTION: " + str(e)[0:100])

        try:
            jobCompanyNameSpans = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class,'job-details-jobs-unified-top-card__company-name')]//a",
            )
            for span in jobCompanyNameSpans:
                jobCompanyName = jobCompanyName + " " + span.text

            for matcher in config.blacklistCompanies:
                if matcher.lower() in jobCompanyName.lower():
                    jobDetail += " | blacklisted "

        except Exception as e:
            if config.displayWarnings:
                print(e)
                utils.prYellow("⚠️ Warning in getting COMPANYNAME: " + str(e)[0:100])

        textToWrite = str(count) + " | " + jobTitle + " | " + jobDetail + jobLocation
        return textToWrite, {
            "title": jobTitle[:64],
            "company_name": jobCompanyName[:128],
            "detail": str(jobDetail + jobLocation)[:128],
            "description": re.sub(r"[^a-zA-Z0-9.-;,\n–— ]", "", jobDescription),
            "session_id": self.session_id,
        }

    def easyApplyButton(self):
        try:
            time.sleep(random.uniform(1, constants.botSpeed))
            button = self.driver.find_element(
                By.XPATH,
                "//div[contains(@class,'jobs-apply-button--top-card')]//button[contains(@class, 'jobs-apply-button')]",
            )
            EasyApplyButton = button
        except:
            EasyApplyButton = False

        return EasyApplyButton

    def applyProcess(self, offerPage):
        global countApplied

        comPercentage_list = self.driver.find_elements(
            By.XPATH,
            "html/body/div[3]/div/div/div[2]/div/div/span",
        )
        percenNumber = 111
        if len(comPercentage_list) > 0:
            comPercentage = comPercentage_list[0].text
            percenNumber = int(comPercentage[0 : comPercentage.index("%")])

        try_limit = 10e3
        if self.hands_free:
            try_limit = 60

        while percenNumber < 100 and try_limit > 0:
            try_limit -= 1
            comPercentage = self.driver.find_element(
                By.XPATH,
                "html/body/div[3]/div/div/div[2]/div/div/span",
            ).text
            percenNumber = int(comPercentage[0 : comPercentage.index("%")])
            buttons = [
                self.driver.find_elements(
                    By.CSS_SELECTOR, "button[aria-label='Continue to next step']"
                ),
                self.driver.find_elements(
                    By.CSS_SELECTOR, "button[aria-label='Review your application']"
                ),
            ]
            utils.click_button_in_containers(buttons)
            if not self.hands_free:
                time.sleep(1)

        if config.followCompanies is False:
            try:
                unfollow_button = self.driver.find_element(
                    By.CSS_SELECTOR, "label[for='follow-company-checkbox']"
                )
                unfollow_button.click()
            except:
                pass

        try:
            self.driver.find_element(
                By.CSS_SELECTOR, "button[aria-label='Submit application']"
            ).click()
        except:
            raise Exception
        time.sleep(random.uniform(1, constants.botSpeed))
        countApplied += 1
        result = "* 🥳 Just Applied to this job: " + str(offerPage)

        return result

    def displayWriteResults(self, lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            utils.prRed("❌ Error in DisplayWriteResults: " + str(e))

    def element_exists(self, parent, by, selector):
        return len(parent.find_elements(by, selector)) > 0


parser = argparse.ArgumentParser()
parser.add_argument("--session-id", default=randint(1000, 9999))
parser.add_argument("--hands-free", default=False, action=argparse._StoreTrueAction)
parser.add_argument("--url-list", default=None, type=str)
parser.add_argument("--retry", default=False, action=argparse._StoreTrueAction)
parser.add_argument(
    "--recommended-jobs", default=False, action=argparse._StoreTrueAction
)
args = vars(parser.parse_args())

print(args)


start = time.time()
Linkedin(**args).linkJobApply()
end = time.time()
utils.prYellow("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
