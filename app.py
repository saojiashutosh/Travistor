import base64
import re
from bson import ObjectId
from flask import (
    Flask,
    make_response,
    render_template,
    url_for,
    request,
    session,
    redirect,
    flash,
)
from flask_pymongo import PyMongo
import bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["MONGO_DBNAME"] = "user_database"
app.config["MONGO_URI"] = "mongodb://localhost:27017/Travistor"

mongo = PyMongo(app)


def is_valid_username(username):
    username_regex = "^[A-Za-z][A-Za-z0-9_]*$"
    return bool(re.match(username_regex, username))


@app.route("/")
@app.route("/main")
def main():
    return render_template("index.html")


# Signup logic


@app.route("/signup", methods=["POST", "GET"])
def signup():
    signup_user = None

    if request.method == "POST":
        login = mongo.db.user
        existing_user = login.find_one({"username": request.form["username"]})

        if existing_user:
            signup_user = (
                "Username is already in use. Please choose a different username."
            )
        elif not is_valid_username(request.form["username"]):
            signup_user = "Invalid username format. Please use only letters, numbers, and underscores."
        else:
            hashed_password = bcrypt.hashpw(
                request.form["password"].encode("utf-8"), bcrypt.gensalt()
            )
            login.insert_one(
                {
                    "username": request.form["username"],
                    "email": request.form["email"],
                    "password": hashed_password,
                }
            )
            session["username"] = request.form["username"]
            flash("Successfully signed up!", "success")
            return redirect(url_for("index"))

    return render_template("signup.html", signup_user=signup_user)


# Signin logic


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        login = mongo.db.user
        username = request.form["username"]
        password = request.form["password"]

        if not is_valid_username(username):
            flash(
                "Invalid username format. Please use only letters, numbers, and underscores."
            )
        else:
            existing_user = login.find_one({"username": username})

            if existing_user:
                if bcrypt.checkpw(password.encode("utf-8"), existing_user["password"]):
                    session["username"] = username
                    flash("Successfully signed in!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Incorrect password. Please try again.", "error")
            else:
                flash("Username not found. Please sign up first.", "error")

    return render_template("signin.html")


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        username = session["username"]
        response = make_response(render_template("dashboard.html", username=username))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    else:
        flash("Please sign in to access the dashboard.", "error")
        return redirect(url_for("signin"))


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response


# for logout and session handling


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.clear()
    flash("Successfully logged out!", "success")
    return redirect(url_for("main"))


# used dictionary for blogs

posts = [
    {
        "title": "A Whirlwind Tour of Gujarats Rich Heritage and Natural Beauty",
        "content": "Embarking on an eight-day whirlwind tour of Gujarat, my journey unfolded amidst the untamed wilderness of Gir, where a night among Asiatic lions set the stage for adventure. Moving to the spiritual enclave of Somnath, a tranquil night by the Arabian Sea offered cultural immersion. Dwarka, steeped in mythology, captivated with its sacred tales during a two-night stay. Ahmedabad, a blend of history and modernity, showcased bustling markets and architectural marvels over two nights. A final day in Patan unveiled Gujarats architectural brilliance at the UNESCO-listed Rani Ki Vav stepwell. In this brief span, Gujarat revealed a tapestry of experiences, from the regal roars of Gir to the tranquil shores of Somnath, the spiritual aura of Dwarka, the vibrant charm of Ahmedabad, and the historical allure of Patan, leaving indelible memories of cultural richness and natural wonders.",
        "author": "Ashwin Jha",
        "date_posted": "October 1, 2023",
        "image": "../static/images/blog1.jpg",
    },
    {
        "title": " A Blissful Journey through Bangalore, Coorg, and Mysore",
        "content": "Embarking on an enchanting journey, my exploration unfolded across Bangalore, Coorg, and Mysore, encapsulating the diverse tapestry of Karnatakas beauty. Starting in Bangalore for a night, I immersed myself in its modern allure before heading to Coorg, where two serene nights amidst mist-covered hills and coffee plantations rejuvenated my soul. The historic charm of Mysore beckoned next, with two nights spent exploring majestic palaces and vibrant markets. The grandeur of Mysore Palace lingered in my memories, making the two-night stay truly captivating. Returning to Bangalore, the seamless blend of technology and tradition in the bustling city marked the perfect finale to an eight-day odyssey, leaving me with a mosaic of unforgettable experiences.",
        "author": "Kalpesh Mahajan",
        "date_posted": "September 15, 2023",
        "image": "../static/images/blog2.jpg",
    },
]


@app.route("/blog")
def blog():
    if "username" in session:
        return render_template("blog.html", posts=posts, username=session["username"])

    return render_template("blog.html", posts=posts)


@app.route("/index")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])

    return render_template("index.html")


@app.route("/about")
def about():
    if "username" in session:
        return render_template("about.html", username=session["username"])

    return render_template("about.html")


@app.route("/fampack")
def fampack():

    if "username" in session:
        return render_template("fampack.html", username=session["username"])

    return render_template("fampack.html")


@app.route("/womenspecial")
def womenspecial():

    if "username" in session:
        return render_template("womenspecial.html", username=session["username"])

    return render_template("womenspecial.html")


@app.route("/culture")
def culture():

    if "username" in session:
        return render_template("cultural.html", username=session["username"])

    return render_template("cultural.html")


@app.route("/roadtrip")
def roadtrip():

    if "username" in session:
        return render_template("roadtrip.html", username=session["username"])

    return render_template("roadtrip.html")


@app.route("/senior")
def senior():

    if "username" in session:
        return render_template("senior.html", username=session["username"])

    return render_template("senior.html")


@app.route("/packages")
def packages():

    if "username" in session:
        return render_template("packages.html", username=session["username"])

    return render_template("packages.html")


packages = mongo.db.package_details

# packages details


@app.route("/package/<int:package_id>")
def package_details(package_id):
    package = mongo.db.package_details.find_one({"_id": package_id})
    if package:
        image_data = base64.b64encode(package["image"]).decode("utf-8")
        package["image"] = image_data

        return render_template("package_details.html", package=package)
    else:
        return "Package not found."


# booking of packages


@app.route("/book", methods=["POST", "GET"])
def book():

    if "username" not in session:
        flash("You need to sign in to book a package", "warning")
        return redirect(url_for("signin"))

    if request.method == "POST":
        print("Inside POST request")
        package_name = request.args.get("package_name")
        package_price_str = request.form.get("package_price")

        if package_price_str is None:
            flash("Package price is missing in the form", "error")
            return redirect(url_for("book"))

        try:
            package_price = float(package_price_str)
        except ValueError:
            flash("Invalid package price format", "error")
            return redirect(url_for("book"))

        print(f"Package Name: {package_name}")

        try:
            book = mongo.db.booking

            username = session["username"]
            name = request.form["username"]
            person = request.form["persons"]
            contact = request.form["contact"]

            total_price = package_price * int(person)
            print("Inserting data into the database...")

            book.insert_one(
                {
                    "package_name": package_name,
                    "username": username,
                    "name": name,
                    "person": person,
                    "contact": contact,
                    "total_price": total_price,
                }
            )

            return redirect(url_for("success"))
        except Exception as e:
            print(f"Error during insertion: {e}")
            flash("Error during booking. Please try again.", "error")
            return redirect(url_for("book"))

    package_name = request.args.get("package_name")
    package_price = float(request.args.get("package_price"))
    return render_template(
        "book.html", package_name=package_name, package_price=package_price
    )


# bookings page logic


@app.route("/bookings")
def bookings():
    app.logger.info("Rendering bookings.html")
    if "username" not in session:
        flash("You need to sign in to view your bookings", "warning")
        return redirect(url_for("signin"))

    try:
        bookings = mongo.db.booking.find({"username": session["username"]})
        return render_template("bookings.html", bookings=bookings)
    except Exception as e:
        flash(f"Error fetching bookings: {e}", "error")
        return render_template("bookings.html", bookings=[])


# package should get cancle after clicking on cancle booking button


@app.route("/cancel_booking/<booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    if "username" not in session:
        flash("You need to sign in to cancel your booking", "warning")
        return redirect(url_for("signin"))

    try:

        booking = mongo.db.booking.find_one(
            {"_id": ObjectId(booking_id), "username": session["username"]}
        )
        if not booking:
            flash("Invalid booking or you do not have permission to cancel it", "error")
            return redirect(url_for("bookings"))

        # Remove the booking from the database
        mongo.db.booking.delete_one({"_id": ObjectId(booking_id)})

        flash("Booking canceled successfully", "success")
        return redirect(url_for("bookings"))
    except Exception as e:
        flash(f"Error canceling booking: {e}", "error")
        return redirect(url_for("bookings"))


# success should be called after the successfull booking of package


@app.route("/success")
def success():
    if "username" in session:
        return render_template("success.html", username=session["username"])

    return render_template("success.html")


@app.route("/addwishlist/<int:package_id>")
def addwishlist(package_id):
    if "username" not in session:
        flash("You need to sign in to view your wishlist", "warning")
        return redirect(url_for("signin"))

    package = mongo.db.package_details.find_one({"_id": package_id})
    if package:
        wishlist_item = {
            "username": session["username"],
            "package_name": package["title"],
            "package_price": package["price"],
            "package_details": {"image": package["image"], "route": package["route"]},
        }
        mongo.db.addwishlist.insert_one(wishlist_item)
        flash("Package added to wishlist successfully", "success")
        return redirect(request.referrer)
    else:
        flash("Package not found", "error")
        return redirect(request.referrer)


@app.route("/wishlist")
def wishlist():
    app.logger.info("Rendering wishlist.html")
    if "username" not in session:
        flash("You need to sign in to view your wishlist", "warning")
        return redirect(url_for("signin"))

    try:
        wishlist = mongo.db.addwishlist.find({"username": session["username"]})
        return render_template("wishlist.html", wishlist=wishlist)
    except Exception as e:
        flash(f"Error fetching wishlist: {e}", "error")
        return render_template("wishlist.html", wishlist=[])


@app.route("/package/<int:package_id>")
def package_details(package_id):
    package = mongo.db.package_details.find_one({"_id": package_id})
    if package:
        image_data = base64.b64encode(package["image"]).decode("utf-8")
        package["image"] = image_data

        return render_template("package_details.html", package=package)
    else:
        return "Package not found."


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
    app.run()
