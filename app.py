from datetime import datetime  # Imports the datetime module for working with dates and times

from flask import Flask, render_template, request, flash  # Imports necessary Flask modules
from flask_sqlalchemy import SQLAlchemy  # Imports SQLAlchemy for database interaction
from flask_mail import Mail, Message  # Imports modules for sending emails

app = Flask(__name__)  # Creates a Flask application instance

app.config["SECRET_KEY"] = "myapplication123"  # Sets the secret key for the application
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"  # Configures the database URI
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # Sets the mail server to Gmail
app.config["MAIL_PORT"] = 465   # Sets the mail port to 465 for SSL
app.config["MAIL_USE_SSL"] = True  # Enables SSL for secure email communication
app.config["MAIL_USERNAME"] = "YOUR EMAIL TO CAN SEND THE EMAIL FROM WEB APP"  # Sets your Gmail address as the username
app.config["MAIL_PASSWORD"] = "YOUR UNIQ PASSWORD"  # Sets your Gmail password

db = SQLAlchemy(app)  # Creates a SQLAlchemy database instance

mail = Mail(app)  # Creates a Mail instance for sending emails

class Form(db.Model):  # Defines a database model named Form
    id = db.Column(db.Integer, primary_key=True)  # Defines an integer primary key column named id
    first_name = db.Column(db.String(80))  # Defines a string column named first_name with max length 80
    last_name = db.Column(db.String(80))  # Defines a string column named last_name with max length 80
    email = db.Column(db.String(80))  # Defines a string column named email with max length 80
    date = db.Column(db.Date)  # Defines a date column named date
    occupation = db.Column(db.String(80))  # Defines a string column named occupation with max length 80


@app.route("/", methods=["GET", "POST"])  # Defines a route for the home page that accepts GET and POST requests
def index():  # Defines the view function for the home page
    if request.method == "POST":  # Checks if the request method is POST
        first_name = request.form["first_name"]  # Retrieves the first_name value from the form data
        last_name = request.form["last_name"]  # Retrieves the last_name value from the form data
        email = request.form["email"]  # Retrieves the email value from the form data
        date = request.form["date"]  # Retrieves the date value from the form data
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Converts the date string to a datetime object
        occupation = request.form["occupation"]  # Retrieves the occupation value from the form data

        form = Form(first_name=first_name, last_name=last_name,  # Creates a new Form object with the retrieved data
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)  # Adds the new Form object to the database session
        db.session.commit()  # Commits the changes to the database

        # Creates the email body
        message_body = f"Thank you for your submission, {first_name}." \
                       f"Here are your data:\n{first_name}\n{last_name}\n{date}\n" \
                       f"Thank you!"

        # Creates an email message
        message = Message(subject="New form submission",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        mail.send(message)  # Sends the email

        flash(f"{first_name}, your form was submitted successfully!", "success")  # Flashes a success message

    # Renders the index.html template
    return render_template("index.html")


if __name__ == "__main__":  # Checks if the script is being run directly
    with app.app_context():  # Creates an application context
        db.create_all()  # Creates all the tables in the database
        app.run(debug=True, port=5001)  # Runs the Flask application in debug mode on port 5001
