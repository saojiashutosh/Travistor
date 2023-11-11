
import base64
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'testing'
app.config['MONGO_DBNAME'] = 'user_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Travistor'



mongo = PyMongo(app)

@app.route("/")
@app.route("/main")
def main():
    return render_template('index.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    signup_user = None

    if request.method == 'POST':
        login = mongo.db.user
        existing_user = login.find_one({'username': request.form['username']})
        if existing_user:
            signup_user = 'Username is already in use. Please choose a different username.'
        else:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            login.insert_one({'username': request.form['username'], 'email': request.form['email'], 'password': hashed_password})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return render_template('signup.html', signup_user=signup_user)


@app.route("/signin", methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        login = mongo.db.user
        username = request.form['username']
        password = request.form['password']

        existing_user = login.find_one({'username': username})

        if existing_user:
            # Check if the provided password matches the stored hashed password
            if bcrypt.checkpw(password.encode('utf-8'), existing_user['password']):
                session['username'] = username
                flash('Successfully signed in!')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password. Please try again.')
        else:
            flash('Username not found. Please sign up first.')

    return render_template('signin.html')

posts = [
    {
        'title': 'Trip to Paris',
        'content': 'My recent Paris trip was a whirlwind of enchantment. The Eiffel Towers twinkling lights, the Louvres artistic treasures, and the aroma of freshly baked croissants on every corner made it a magical experience. Parisian streets held surprises at every turn, from charming cafes to hidden boutiques. Paris, with its timeless allure, exceeded all expectations.',
        'author': 'John Doe',
        'date_posted': 'October 1, 2023',
        'image': '../static/images/blog1.png'  
    },
    {
        'title': 'Exploring Tokyo',
        'content': 'Tokyo, a city of endless surprises. Skyscrapers meet shrines, and bustling streets are punctuated by serene gardens. Shibuya Crossings organized chaos is mesmerizing and Tsukiji Fish Markets sushi is a must-try. From cherry blossoms in Ueno Park to Akihabaras electronic paradise, Tokyo is a sensory adventure waiting to happen.',
        'author': 'Jane Smith',
        'date_posted': 'September 15, 2023',
        'image': '../static/images/blog2.png'
    },
]

@app.route('/blog')
def blog():
    if 'username' in session:
        return render_template('blog.html',posts=posts, username=session['username'])
    
    return render_template('blog.html', posts=posts)



@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])

    return render_template('index.html')

@app.route("/about")
def about():
       if 'username' in session:
            return render_template('about.html', username=session['username'])
        
       return render_template('about.html')
   
   
   
@app.route("/fampack")
def fampack():
    
    if 'username' in session:
            return render_template('fampack.html',username=session['username'])
        
    return render_template('fampack.html')

@app.route("/womenspecial")
def womenspecial():
    
    if 'username' in session:
            return render_template('womenspecial.html',username=session['username'])
        
    return render_template('womenspecial.html')

@app.route("/culture")
def culture():
    
    if 'username' in session:
            return render_template('cultural.html',username=session['username'])
        
    return render_template('cultural.html')

@app.route("/roadtrip")
def roadtrip():
    
    if 'username' in session:
            return render_template('roadtrip.html',username=session['username'])
        
    return render_template('roadtrip.html')

@app.route("/senior")
def senior():
    
    if 'username' in session:
            return render_template('senior.html',username=session['username'])
        
    return render_template('senior.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))



@app.route("/packages")
def packages():
    
    if 'username' in session:
            return render_template('packages.html',username=session['username'])
        
    return render_template('packages.html')

packages = mongo.db.package_details

@app.route('/package/<int:package_id>')
def package_details(package_id):
    package = mongo.db.package_details.find_one({'_id': package_id})
    if package:
        image_data = base64.b64encode(package['image']).decode('utf-8')
        package['image'] = image_data

        return render_template('package_details.html', package=package)
    else:
        return "Package not found."
    
@app.route("/book", methods=['POST', 'GET'])
def book():
    if 'username' in session:
        if request.method == 'POST':
            book = mongo.db.booking
            name = request.form['username']
            adult = request.form['adult']
            child = request.form['child']
            infant = request.form['infant']
            rooms = request.form['rooms']
            contact = request.form['contact']

            book.insert_one({'username': name, 'adult': adult, 'child': child, 'infant': infant, 'rooms': rooms, 'contact': contact})
            return redirect(url_for('success'))

        return render_template('book.html', username=session['username'])
    
    return redirect(url_for('signin'))
   
@app.route("/success")
def success():
    if 'username' in session:
            return render_template('success.html',username=session['username'])
        
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
 
    
if __name__ == "__main__":
    app.run(debug=True)
    app.run()
