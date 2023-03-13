from flask import Flask, render_template, request, redirect, session, url_for
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdrivermanager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

from helper import login_instagram, naviagate_to_followers

#credit to https://github.com/JasonLeviGoodison/InstagramScripts/blob/master/UserInfo.py
# on how to acess instagram's data

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #request for the users instagrams log in and password
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            error_msg = "Please provide both a username and a password."
            return render_template('login.html', error_msg=error_msg)
        else:
            #start a browser that logs into their instagram
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
            login_instagram(driver, username, password)   
            naviagate_to_followers(driver, username)         
    return render_template('login.html')



@app.route('/home', methods=['GET'])
def main():
    return render_template("home.html")


@app.route('/followers', methods=['GET'])
def followers():

    # Render the followers template and pass in the list of followers
    return render_template("followers.html", followers=followers)


@app.route('/following', methods=['GET'])
def following():
    return render_template("follow_back.html", back=back)

@app.route('/unfollowers', methods=['GET'])
def unfollowers():
    return render_template("unfollowers.html", unfollowers=unfollowers)

@app.route('/admires', methods=['GET'])
def admires():            
    return render_template("admires.html", admires=admires)

if __name__ == '__main__':
    app.run(debug=True)