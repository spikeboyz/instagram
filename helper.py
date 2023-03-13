from flask import Flask, render_template, request, redirect, session, url_for
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdrivermanager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

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

def naviagate_to_followers(driver, username):
    #clicks the profile button
    profile_css = "[href*=\"" + username + "\"]"
    click_button_with_css(driver, profile_css)