
import base64
import re
from flask import Flask, make_response, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MONGO_DBNAME'] = 'user_database'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Travistor'

mongo = PyMongo(app)

def is_valid_username(username):
    username_regex ="^[A-Za-z][A-Za-z0-9_]*$"
    return bool(re.match(username_regex, username))

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
        elif not is_valid_username(request.form['username']):
            signup_user = 'Invalid username format. Please use only letters, numbers, and underscores.'
        else:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            login.insert_one({'username': request.form['username'], 'email': request.form['email'], 'password': hashed_password})
            session['username'] = request.form['username']
            flash('Successfully signed up!', 'success')
            return redirect(url_for('index'))

    return render_template('signup.html', signup_user=signup_user)

@app.route("/signin", methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        login = mongo.db.user
        username = request.form['username']
        password = request.form['password']

        if not is_valid_username(username):
            flash('Invalid username format. Please use only letters, numbers, and underscores.')
        else:
            existing_user = login.find_one({'username': username})

            if existing_user:
                if bcrypt.checkpw(password.encode('utf-8'), existing_user['password']):
                    session['username'] = username
                    flash('Successfully signed in!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Incorrect password. Please try again.', 'error')
            else:
                flash('Username not found. Please sign up first.', 'error')

    return render_template('signin.html')

@app.route("/dashboard")
def dashboard():
    if 'username' in session:
        username = session['username']
        response = make_response(render_template('dashboard.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        flash('Please sign in to access the dashboard.', 'error')
        return redirect(url_for('signin'))

@app.route("/logout")
def logout():
    session.clear()
    flash('Successfully logged out!', 'success')
    return redirect(url_for('main'))

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
    
    if 'username' not in session:
        flash('You need to sign in to book a package', 'warning')
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        print("Inside POST request")
        package_name = request.args.get('package_name')
        package_price = float(request.form.get('package_price'))
        print(f"Package Name: {package_name}")
        
        try:
             book = mongo.db.booking
             
             name = request.form['username']
             person = request.form['persons']
             contact = request.form['contact']
             
             total_price = package_price * int(person)  # Convert 'person' to an integer
             print("Inserting data into the database...")
             
             book.insert_one({
                 'package_name': package_name,
                 'name': name,
                 'person': person,
                 'contact': contact,
                 'total_price': total_price
                 })
             
             flash('Booking successful!', 'success')
             return redirect(url_for('success'))
        except Exception as e:
            print(f"Error during insertion: {e}")
            flash('Error during booking. Please try again.', 'error')
            if e is True:
                return redirect(url_for('book'))
        return redirect(url_for('success'))


    package_name = request.args.get('package_name')
    package_price = float(request.args.get('package_price'))
    return render_template('book.html', package_name=package_name, package_price=package_price)
    

   
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
