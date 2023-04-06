from flask import Flask, render_template, request, redirect, session, url_for
from igramscraper.instagram import Instagram
from time import sleep


app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'

following_list = list()
followers_list = list()

@app.route('/', methods=['GET', 'POST'])
def login():
    global following_list, followers_list
    if request.method == 'POST':
        #request for the users instagrams log in and password
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            error_msg = "Please provide both a username and a password."
            return render_template('login.html', error_msg=error_msg)
        else:
            instagram = Instagram()
            instagram.with_credentials(username, password)
            instagram.login(force=False,two_step_verificator=True)
            #delay to mimic the user 
            sleep(3)
            account = instagram.get_account(username)
            followers_list = instagram.get_followers(account.identifier, 100, delayed=True) 
            following_list = instagram.get_following(account.identifier, 100, delayed=True)
            return redirect(url_for("home"))
    return render_template('login.html')


@app.route('/home', methods=['GET'])
def main():
    return render_template("home.html")


@app.route('/followers', methods=['GET'])
def followers():
    global followers_list
    return render_template("followers.html", followers=followers_list)


@app.route('/following', methods=['GET'])
def following():
    global following_list
    return render_template("follow_back.html", following=following_list)

@app.route('/unfollowers', methods=['GET'])
def unfollowers():
    global following_list, followers_list
    unfollowers = list()
    for follow in following_list:
        if follow not in followers_list:
            unfollowers.append(follow)
    return render_template("unfollowers.html", unfollowers=unfollowers)

@app.route('/admires', methods=['GET'])
def admires():
    global followers_list, followers_list
    admires = list()
    for follow in followers_list:
        if follow not in following_list:
            admires.append(follow)            
    return render_template("admires.html", admires=admires)

if __name__ == '__main__':
    app.run(debug=True)