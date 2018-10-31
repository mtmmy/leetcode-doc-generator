from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import time
import os
import re
import tkinter as tk

TIME_DELAY = 10

CODE_DRIVER = webdriver.Chrome("./chromedriver")
WAIT = WebDriverWait(CODE_DRIVER,10)

LEETCODE_PROBLEMS = []

LEETCODE_URL = "https://leetcode.com"
GITHUB_URL = "https://github.com/mtmmy/Leetcode/tree/master/"
GITHUB_URL_CSHARP = GITHUB_URL + "Csharp/Leetcode/"
GITHUB_URL_JAVA = GITHUB_URL + "Java/Leetcode/src/main/java/com/leetcode/"
GITHUB_URL_PYTHON = GITHUB_URL + "Python/"

LOCAL_PATH_LEETCODE = "/Users/mtmmy/Projects/Leetcode/"
LOCAL_PATH_CSHARP = LOCAL_PATH_LEETCODE + "Csharp/Leetcode/"
LOCAL_PATH_JAVA = LOCAL_PATH_LEETCODE + "Java/Leetcode/src/main/java/com/leetcode/"
LOCAL_PATH_PYTHON = LOCAL_PATH_LEETCODE + "Python/"

class Problem (object):
    def __init__ (self, number, title, href, acceptance, difficulty ):
        self.number = number
        self.title = title
        self.href = href
        self.acceptance = acceptance
        self.difficulty = difficulty
        self.language = []
        self.github_url = []
    def add_language (self, language):
        self.language.append(language)
    def add_github_url (self, url):
        self.github_url.append(url)

def get_folders(type, path):
    """
    get folders form local, need to be change to fit your folder structure
    """
    folders_dictionary = {}
    for p in os.listdir(path):
        if type == "CSHARP":
            if str(p).startswith("0"):
                num = p[0:4]
                folders_dictionary[int(num)] = p
        if type == "JAVA":
            if str(p).startswith("_0"):
                num = p[1:5]
                folders_dictionary[int(num)] = p
        if type == "PYTHON":
            if str(p).startswith("0"):
                num = p[0:4]
                folders_dictionary[int(num)] = p
    return folders_dictionary

def sign_into_leetcode():

    CODE_DRIVER.implicitly_wait(TIME_DELAY)

    CODE_DRIVER.get("https://leetcode.com/accounts/logout")

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    CODE_DRIVER.get("https://leetcode.com/accounts/login/")
    loginBtn = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, "btn__2FMG")))
    CODE_DRIVER.find_element_by_name("login").send_keys(username)
    CODE_DRIVER.find_element_by_name("password").send_keys(password)
    loginBtn.send_keys(Keys.ENTER)

    time.sleep(5)

def go_to_next_page(class_name):
    """
    go to the next page of the list of problems
    if there is no next page, return false
    """
    try:
        element = CODE_DRIVER.find_element_by_class_name(class_name)
        element.click()        
        return True
    except NoSuchElementException:
        return False

def get_problem_rows(table):
    problems = []

    for row in table.find_elements_by_css_selector("tbody:nth-of-type(1)>tr"):
        number = row.find_element_by_css_selector("td:nth-of-type(2)").text
        title = row.find_element_by_css_selector("td:nth-of-type(3) a").text
        href = row.find_element_by_css_selector("td:nth-of-type(3) a").get_attribute('href')
        acceptance = row.find_element_by_css_selector("td:nth-of-type(5)").text
        difficulty = row.find_element_by_css_selector("td:nth-of-type(6) span").text
        problem = Problem(int(number), title, href, acceptance, difficulty)
        problems.append(problem)
    return problems

def create_read_me(type):
    """
    create README.md for each problem under its folder
    """

    local_path = ""
    
    if type == "CSHARP":
        local_path = LOCAL_PATH_CSHARP
    elif type == "JAVA":
        local_path = LOCAL_PATH_JAVA
    elif type == "PYTHON":
        local_path = LOCAL_PATH_PYTHON

    folders = get_folders(type, local_path)
    
    for problem in LEETCODE_PROBLEMS:
        if problem.number in folders:
            file_path = local_path + folders[problem.number] + "/README.md"
            
            CODE_DRIVER.get(problem.href)
            allDesc = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, "description__3vkv")))
            # description = allDesc.find_element_by_class_name("content__1c40")
            description = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, "content__1c40")))

            # btnClickable = False
            

            
            # while not btnClickable and btns:
            #     try:
            #         btns[0].click()
            #         btnClickable = True
            #     except WebDriverException:
            #         print("Still not clickable. Keep waiting")
            #         time.sleep(0.1)

            # for btn in btns[0:]:
            #     btn.click()        

            topics = allDesc.find_elements_by_class_name("topic-tag__Hn49")
            simQs = allDesc.find_elements_by_class_name("title__3BnH")

            btns = allDesc.find_elements_by_class_name("css-1dhf2dg-baseHeaderStyle")
            
            for btn in btns:
                while 1:
                    try:
                        btn.click()
                        time.sleep(0.5)
                        break
                    except WebDriverException:
                        time.sleep(0.5)

            if not os.path.isfile(file_path):
                            
                children = description.find_element_by_tag_name("div").find_elements_by_xpath("*")

                file = open(file_path, 'w')
                file.write("# [" + str(problem.number) + ". " + problem.title + "](" + problem.href + ")\n\n")
                file.write("## Description\n")
                for child in children:
                    if child.tag_name == "p":
                        try:
                            CODE_DRIVER.implicitly_wait(0)
                            image = child.find_element_by_tag_name("img")
                            CODE_DRIVER.implicitly_wait(TIME_DELAY)
                            file.write("\n")
                            file.write("![image](" + image.get_attribute("src") + ")")
                            file.write("\n")
                        except NoSuchElementException:
                            CODE_DRIVER.implicitly_wait(TIME_DELAY)
                        file.write("\n")
                        file.write(child.text)
                        file.write("\n")
                    if child.tag_name == "pre":
                        file.write("\n")
                        file.write("```")
                        file.write("\n")
                        file.write(child.text)
                        file.write("\n")
                        file.write("```")
                        file.write("\n")
                        
                file.write("\n## Solution\n\n")

                file.write("## Related Topics")
                topicsLine = ""
                for topic in topics:
                    topiscUrl = LEETCODE_URL + topic.get_attribute("href")
                    topicTxt = topic.find_element_by_class_name("tag__2PqS").text
                    topicsLine += "[" + topicTxt + "](" + topiscUrl + "), "

                file.write("## Similar Questions")
                simQsLine = ""
                for q in simQs:
                    topiscUrl = LEETCODE_URL + q.get_attribute("href")
                    topicTxt = q.text
                    topicsLine += "[" + topicTxt + "](" + topiscUrl + "), "
                file.write(simQsLine)
                file.close()
            else:
                loadFile = open(file_path).read()

                with open(file_path, 'a') as myfile:
                    if "Related Topics" not in loadFile:
                        # myfile.write("\n## Related Topics\n\n")
                        topicsLine = ""
                        for topic in topics:
                            tipicUrl = LEETCODE_URL + topic.get_attribute("href")
                            topicTxt = topic.find_element_by_class_name("tag__2PqS").text
                            topicsLine += "[" + topicTxt + "](" + tipicUrl + "), "
                        # file.write(topicsLine)
                        # myfile.write("\n")
                    
                    if "Similar Questions" not in loadFile:
                        # myfile.write("\n## Similar Questions\n\n")
                        simQsLine = ""
                        for q in simQs:
                            simQsLine += "[" + q.text + "](" + LEETCODE_URL + q.get_attribute("href") + "), "
                        # file.write(simQsLine)
                        # myfile.write("\n")
                        
                print("")
            # file.close()


def scrap_description():
    
    CODE_DRIVER.implicitly_wait(TIME_DELAY)

    CODE_DRIVER.get("https://leetcode.com/problemset/algorithms/?status=Solved")

    table = CODE_DRIVER.find_element_by_css_selector(".question-list-table>table")

    global LEETCODE_PROBLEMS
    LEETCODE_PROBLEMS += get_problem_rows(table)

    while go_to_next_page("reactable-next-page"):        
        LEETCODE_PROBLEMS += get_problem_rows(table)

    create_read_me("CSHARP")
    create_read_me("JAVA")
    create_read_me("PYTHON")
    
def write_problem_row(p):
    language_list = []

    for i in range(len(p.language)):
        language_list.append("[" + p.language[i] + "](" + p.github_url[i] + ")")

    data = {
        'num': p.number,
        'title': '[' + p.title + "](" + p.href + ")",
        'acceptance': p.acceptance,
        'difficulty': p.difficulty,
        'language': ", ".join(language_list)
    }
    line = "|{num}|{title}|{acceptance}|{difficulty}|{language}|\n".format(**data)
    return line
    
def create_sum_file():
    """
    create summary README.md for all problmes and organize them in a table
    """
    global LEETCODE_PROBLEMS
    
    folders_csharp = get_folders("CSHARP", LOCAL_PATH_CSHARP)
    folders_java = get_folders("JAVA", LOCAL_PATH_JAVA)
    folders_python = get_folders("PYTHON", LOCAL_PATH_PYTHON)
    sum_file_path = LOCAL_PATH_LEETCODE + "README.md"

    LEETCODE_PROBLEMS.sort(key=lambda x: x.number, reverse=False)

    file = open(sum_file_path, 'w')
    file.write("# Leetcode Solutions\n\n")
    file.write("This repository shows all of leetcode problems I'd accomplished. I use C# as my primary language to solve problems because I want to get familiar with it by utilizing it more but sometimes I use Java as well.\n\n")
    file.write("| # | Title | Acceptance | Difficulty | Language | \n")
    file.write("|:---:|:---|:---:|:---:|:---:|\n")

    for p in LEETCODE_PROBLEMS:
        line = ""
        if p.number in folders_csharp:
            folder_name = folders_csharp[p.number]
            p.add_language("C#")
            p.add_github_url(GITHUB_URL_CSHARP + folder_name)
            
        if p.number in folders_java:
            folder_name = folders_java[p.number]
            p.add_language("Java")
            p.add_github_url(GITHUB_URL_JAVA + folder_name)
            
        if p.number in folders_python:
            folder_name = folders_python[p.number]
            p.add_language("Python")
            p.add_github_url(GITHUB_URL_PYTHON + folder_name)
            
        line = write_problem_row(p)
        file.write(line)
            
if __name__ == "__main__":
    sign_into_leetcode()
    scrap_description()
    CODE_DRIVER.close()
    create_sum_file()
    # ----------------------------------
    # remove all files under the path. If you need to regenerate all files, run this
    # 
    # folders = get_folders("CSHARP", LOCAL_PATH_CSHARP)
    # for key in folders:
    #     file_name = LOCAL_PATH_CSHARP + folders[key] + "/README.md"
    #     try:
    #         os.remove(file_name)
    #     except OSError:
    #         pass