# General bot settings to use Pro settings you need to download Pro version from: www.automated-bots.com

browser = ["Chrome"]

# We advise logging in manually as opposed to saving it to a file.
# You can pass through 2FA and bot verification checks this way too.
email = " "
password = " "

headless = False

firefoxProfileRootDir = r""
# get Chrome profile path by typing following url: chrome://version/
chromeProfilePath = r""

# These settings are for running Linkedin job apply bot.
# location you want to search the jobs - ex : ["Poland", "Singapore", "New York City Metropolitan Area", "Monroe County"]
# continent locations:["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa", "Australia"]
# location = ["NorthAmerica"]
location = ["United States"]
# keywords related with your job search
# keywords = ["frontend", "react", "typescript","javascript", "vue", "python", "programming", "blockchain"]
keywords = [
    "developer python",
    "programmer python",
    "data engineer",
    "data scientist",
    "machine learning engineer",
    "artificial intelligence python",
    "software developer python",
    "machine learning",
    "junior data science",
    "junior data engineer",
    "junior data analyst",
    "junior software developer python",
    "junior python",
    "junior data",
    "python",
    "data",
    "data science",
    "developer python",
    "engineer python",
    "analyst python",
]
# job experience Level - ex:  ["Internship", "Entry level" , "Associate" , "Mid-Senior level" , "Director" , "Executive"]
experienceLevels = [
    "Entry level",
]

# experienceLevels = ["Entry level", "Associate", "Mid-Senior level"]
# job posted date - ex: ["Any Time", "Past Month" , "Past Week" , "Past 24 hours"] - select only one
datePosted = ["Past 24 hours"]
datePosted = ["Past Week"]
# job type - ex:  ["Full-time", "Part-time" , "Contract" , "Temporary", "Volunteer", "Intership", "Other"]
jobType = ["Full-time", "Part-time", "Contract"]
# remote  - ex: ["On-site" , "Remote" , "Hybrid"]
# remote = ["On-site" , "Remote" , "Hybrid"]
remote = ["Remote"]
# salary - ex:["$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", "$160,000+", "$180,000+", "$200,000+" ] - select only one
salary = ["$80,000+"]
# sort - ex:["Recent"] or ["Relevent"] - select only one
sort = ["Recent"]
# Blacklist companies you dont want to apply - ex: ["Apple","Google"]
blacklistCompanies = [
    "acs cons",
    "SnapTryAI",
    "CyberCoders",
    "Coders Data",
    "Akraya",
    "Mindrift",
]
# Blaclist keywords in title - ex:["manager", ".Net"]
blackListTitles = []
# Follow companies after sucessfull application True - yes, False - no
followCompanies = False

preferredCv = 1

# Testing & Debugging features
displayWarnings = False
