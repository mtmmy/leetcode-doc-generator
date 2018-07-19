from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import os
import re
import tkinter as tk

TIME_DELAY = 10

CODE_DRIVER = webdriver.Chrome("./chromedriver")
WAIT = WebDriverWait(CODE_DRIVER,10)

LEETCODE_PROBLEMS = []

GITHUB_URL_CSHARP = "https://github.com/mtmmy/Leetcode/tree/master/Csharp/Leetcode/"

LOCAL_PATH_LEETCODE = "/Users/mtmmy/Projects/Leetcode/"
LOCAL_PATH_CSHARP = LOCAL_PATH_LEETCODE + "Csharp/Leetcode/"


class Problem (object):
    def __init__ (self, number, title, href, acceptance, difficulty ):
        self.number = number
        self.title = title
        self.href = href
        self.acceptance = acceptance
        self.difficulty = difficulty

def get_folders(path):    
    folders_dictionary = {}
    for p in os.listdir(path):
        if str(p).startswith('0'):
            num = p[0:4]
            folders_dictionary[int(num)] = p
    return folders_dictionary

def sign_into_leetcode():

    CODE_DRIVER.implicitly_wait(TIME_DELAY)

    CODE_DRIVER.get("https://leetcode.com/accounts/logout")

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    CODE_DRIVER.get("https://leetcode.com/accounts/login/")
    CODE_DRIVER.find_element_by_css_selector("#id_login").send_keys(username)
    CODE_DRIVER.find_element_by_css_selector("#id_password").send_keys(password)
    CODE_DRIVER.find_element_by_css_selector("#id_password").send_keys(Keys.ENTER)
        
    CODE_DRIVER.implicitly_wait(0)
    time.sleep(5)

def go_to_next_page(class_name):
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

def scrap_description():
    
    CODE_DRIVER.implicitly_wait(TIME_DELAY)

    CODE_DRIVER.get("https://leetcode.com/problemset/algorithms/?status=Solved")

    table = CODE_DRIVER.find_element_by_css_selector(".question-list-table>table")

    global LEETCODE_PROBLEMS
    LEETCODE_PROBLEMS += get_problem_rows(table)

    while go_to_next_page("reactable-next-page"):        
        LEETCODE_PROBLEMS += get_problem_rows(table)    

    folders = get_folders(LOCAL_PATH_CSHARP)
    
    for problem in LEETCODE_PROBLEMS:
        if problem.number in folders:
            file_path = LOCAL_PATH_CSHARP + folders[problem.number] + "/README.md"
            
            if not os.path.isfile(file_path):
                CODE_DRIVER.get(problem.href)
                description = WAIT.until(EC.presence_of_element_located((By.CLASS_NAME, "question-description__3U1T")))
                children = description.find_element_by_tag_name("div").find_elements_by_xpath("*")            
            
                file = open(file_path, 'w')
                file.write("# [" + str(problem.number) + ". " + problem.title + "](" + problem.href + ")\n\n")
                file.write("## Description\n")
                for child in children:
                    if child.tag_name == "p":
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
                file.close()

def create_sum_file():
    global LEETCODE_PROBLEMS
    
    folders = get_folders(LOCAL_PATH_CSHARP)    
    sum_file_path = LOCAL_PATH_LEETCODE + "README.md"

    LEETCODE_PROBLEMS.sort(key=lambda x: x.number, reverse=False)

    file = open(sum_file_path, 'w')
    file.write("# Leetcode Solutions\n\n")
    file.write("This repository shows all of leetcode problems I'd accomplished. I use C# as my primary language to solve problems because I want to get familiar with it by utilizing it more but sometimes I use Java as well.\n\n")
    file.write("| # | Title | Acceptance | Difficulty | Language | \n")
    file.write("|:---:|:---|:---:|:---:|:---:|\n")

    for p in LEETCODE_PROBLEMS:
        if p.number in folders:
            folder_name = folders[p.number]
            data = {
                'num': p.number,
                'title': '[' + p.title + "](" + GITHUB_URL_CSHARP + folder_name + ")",
                'acceptance': p.acceptance,
                'difficulty': p.difficulty,
                'language': "C#"
            }
            line = "|{num}|{title}|{acceptance}|{difficulty}|{language}|\n".format(**data)
            file.write(line)
            
    
            
if __name__ == "__main__":
    sign_into_leetcode()
    scrap_description()
    CODE_DRIVER.close()
    create_sum_file()
    # folders = get_folders(LOCAL_PATH_CSHARP)
    # for key in folders:
    #     file_name = LOCAL_PATH_CSHARP + folders[key] + "/README.md"
    #     try:
    #         os.remove(file_name)
    #     except OSError:
    #         pass