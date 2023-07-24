from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyBJWqokSyzdYaqUgQFLA1NJ7wRalptWJ7c",
  "authDomain": "cs-project-3b1b2.firebaseapp.com",
  "projectId": "cs-project-3b1b2",
  "storageBucket": "cs-project-3b1b2.appspot.com",
  "messagingSenderId": "795742576879",
  "appId": "1:795742576879:web:50c6eec968b35b0d42bb1a",
  "measurementId": "G-CHD1JCCDBQ","databaseURL": "https://cs-project-3b1b2-default-rtdb.europe-west1.firebasedatabase.app/"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('add_tweet'))
    except:
        error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name=request.form['full_name']
        username=request.form['username']
        bio=request.form['bio']

        try:
            user={"name":full_name, "email":email}
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        title=request.form['title']
        text=request.form['text']
        tweet={"title":title,"text":text,"UID":login_session['user']['localId']}
        try:
            db.child("Tweets").push(tweet)
        except:
            error="Can't add tweet"
    return render_template("add_tweet.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/all_tweets')
def allTweets():
    tweet=db.child("Tweets")
    
    return render_template('tweets.html',t=tweet)


if __name__ == '__main__':
    app.run(debug=True)