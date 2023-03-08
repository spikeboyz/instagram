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
            'response_type': 'code',
            'scope': 'user_profile,user_media'
        }
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
    pass
