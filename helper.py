from flask import Flask, render_template, request, redirect, session, url_for
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdrivermanager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

count = 0 

def login_instagram(driver, username, password):
    #waits for the log in page to pop up
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "username")))
    #plugs in the username and passwords that the user put in my website
    #into the instagram log in
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password) 
    driver.find_element_by_name("password").send_keys(u'\ue007')

def click_button_with_css(driver, css_selector):
    #waits for the css button to appear and then clicks it
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
    element.click()

def naviagate_to_profile(driver, username):
    #clicks the profile button
    profile_css = "[href*=\"" + username + "\"]"
    click_button_with_css(driver, profile_css)

def get_followers(driver, username):
    followers = list()
    css_select_close = '[aria-label="Close"]'
    click_button_with_css(driver, "[href*=\"" + username + "/followers/\"]")
    followers = get_list_from_dialog(driver)
    click_button_with_css(driver, css_select_close)
    return followers

def get_following(driver, username):
    following = list()
    css_select_close = '[aria-label="Close"]'
    click_button_with_css(driver, "[href*=\"" + username + "/following/\"]")
    following = get_list_from_dialog(driver)
    click_button_with_css(driver, css_select_close)
    return following 

def click_button_with_xpath(driver, xpath):
    element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()

def get_list_from_dialog(driver):
    list_xpath ="//div[@role='dialog']//li"
    WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, list_xpath)))

    scroll_down(driver)

    list_elems = driver.find_elements_by_xpath(list_xpath)
    users = []

    for i in range(len(list_elems)):
        try:
            row_text = list_elems[i].text
            if ("Follow" in row_text):
                username = row_text[:row_text.index("\n")]
                users += [username]
        except:
            continue
    return users

def scroll_down(driver):
    global count
    iter = 1
    while 1:
        scroll_top_num = str(iter * 1000)
        iter += 1
        # scroll down
        driver.execute_script("document.querySelector('div[role=dialog] ul').parentNode.scrollTop=" + scroll_top_num)
        try:
            WebDriverWait(driver, 1).until(check_difference_in_count)
        except:
            count = 0
            break

def check_difference_in_count(driver):
    global count

    new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))

    if count != new_count:
        count = new_count
        return True
    else:
        return False

