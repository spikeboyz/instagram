from flask import Flask, render_template, request, redirect, session, url_for
import os
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':
        # Ensure username was submitted
        if not request.form.get('username'):
            error = 'must provide username'
            return render_template('/', error=error)

        # Ensure password was submitted
        elif not request.form.get('password'):
            error = 'must provide password'
            return render_template('/', error=error)

        # Authenticate the user and obtain an access token
        auth_url = 'https://api.instagram.com/oauth/authorize'
        token_url = 'https://api.instagram.com/oauth/access_token'
        client_id = os.environ.get('INSTAGRAM_CLIENT_ID')
        client_secret = os.environ.get('INSTAGRAM_CLIENT_SECRET')
        redirect_uri = url_for('callback', _external=True)
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            #the code im getting back from the instagram verification page
            'response_type': 'code',
            #what acess im asking for 
            'scope': 'user_profile,user_media'
        }
        #sends the user to the verification page 
        auth_url = requests.Request('GET', auth_url, params=params).prepare().url
        return redirect(auth_url)

    return render_template('index.html')

@app.route('/callback', methods=['GET'])
def callback():
    # Get the authorization code from the query parameters
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://api.instagram.com/oauth/access_token'
    client_id = os.environ.get('INSTAGRAM_CLIENT_ID')
    client_secret = os.environ.get('INSTAGRAM_CLIENT_SECRET')
    redirect_uri = url_for('callback', _external=True)
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': code
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get('access_token')

    # Save the access token to the user's session
    session['access_token'] = access_token

    # Redirect the user to the home page
    return redirect(url_for('home'))


@app.route('/home', methods=['GET'])
def main():
    return render_template("home.html")

@app.route('/followers', methods=['GET'])
def followers():

    followers = []

    # Get the user's access token from the session
    access_token = session.get('access_token')

    # If the user is not logged in, redirect them to the login page
    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to make an API request to fetch the user's followers
    api_url = f'https://graph.instagram.com/me/followers?access_token={access_token}'
    response = requests.get(api_url)
    followers_json = response.json().get('data')

    #make a list of the followers from the json file
    for follower in followers_json:
        followers.append(follower['username'])

    # Render the followers template and pass in the list of followers
    return render_template("followers.html", followers=followers)


@app.route('/following', methods=['GET'])
def following():
    following = []

    # Get the user's access token from the session
    access_token = session.get('access_token')

    # If the user is not logged in, redirect them to the login page
    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to make an API request to fetch the user's followers
    api_url = f'https://graph.instagram.com/me/following?access_token={access_token}'
    response = requests.get(api_url)
    following_json = response.json().get('data')

    #make a list of the followers from the json file
    for follower in following_json:
        following.append(follower['username'])

    return render_template("following.html", following=following)

@app.route('/follow_back', methods=['GET'])
def follow_back():
    followers = []
    following = []
    back = []

    # Get the user's access token from the session
    access_token = session.get('access_token')

    # If the user is not logged in, redirect them to the login page
    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to make an API request to fetch the user's followers
    followers_url = f'https://graph.instagram.com/me/followers?access_token={access_token}'
    followers_response = requests.get(followers_url)
    followers_json = followers_response.json().get('data')

    # Make a list of the followers from the JSON file
    for follower in followers_json:
        followers.append(follower['username'])

    # Use the access token to make an API request to fetch the users that the authenticated user is following
    following_url = f'https://graph.instagram.com/me/following?access_token={access_token}'
    following_response = requests.get(following_url)
    following_json = following_response.json().get('data')

    # Make a list of the users that the authenticated user is following from the JSON file
    for user in following_json:
        following.append(user['username'])

    for follow in following:
        if follow in followers:
            back.append(follow)

    return render_template("follow_back.html", back=back)

@app.route('/unfollowers', methods=['GET'])
def unfollowers():
    followers = []
    following = []
    unfollowers = []

    # Get the user's access token from the session
    access_token = session.get('access_token')

    # If the user is not logged in, redirect them to the login page
    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to make an API request to fetch the user's followers
    followers_url = f'https://graph.instagram.com/me/followers?access_token={access_token}'
    followers_response = requests.get(followers_url)
    followers_json = followers_response.json().get('data')

    # Make a list of the followers from the JSON file
    for follower in followers_json:
        followers.append(follower['username'])

    # Use the access token to make an API request to fetch the users that the authenticated user is following
    following_url = f'https://graph.instagram.com/me/following?access_token={access_token}'
    following_response = requests.get(following_url)
    following_json = following_response.json().get('data')

    # Make a list of the users that the authenticated user is following from the JSON file
    for user in following_json:
        following.append(user['username'])

    for follow in following:
        if follow not in followers:
            unfollowers.append(follow)
    return render_template("unfollowers.html", unfollowers=unfollowers)

@app.route('/admires', methods=['GET'])
def admires():
    followers = []
    following = []
    admires = []

    # Get the user's access token from the session
    access_token = session.get('access_token')

    # If the user is not logged in, redirect them to the login page
    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to make an API request to fetch the user's followers
    followers_url = f'https://graph.instagram.com/me/followers?access_token={access_token}'
    followers_response = requests.get(followers_url)
    followers_json = followers_response.json().get('data')

    # Make a list of the followers from the JSON file
    for follower in followers_json:
        followers.append(follower['username'])

    # Use the access token to make an API request to fetch the users that the authenticated user is following
    following_url = f'https://graph.instagram.com/me/following?access_token={access_token}'
    following_response = requests.get(following_url)
    following_json = following_response.json().get('data')

    # Make a list of the users that the authenticated user is following from the JSON file
    for user in following_json:
        following.append(user['username'])

    for follower in followers:
        if follower not in following:
            admires.append(follower)
            
    return render_template("admires.html", admires=admires)