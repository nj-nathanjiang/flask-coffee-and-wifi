from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Bootstrap(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    location = StringField("Cafe Location", validators=[DataRequired()])
    map_url = StringField("Cafe URL On Google Maps", validators=[DataRequired(), URL()])
    img_url = StringField("Image Of Cafe URL", validators=[DataRequired(), URL()])
    has_wifi = StringField("Has Wifi True/False", validators=[DataRequired()])
    has_sockets = StringField("Has Power Sockets True/False", validators=[DataRequired()])
    has_toilets = StringField("Has Toilet True/False", validators=[DataRequired()])
    can_take_calls = StringField("You Can Take Calls There True/False", validators=[DataRequired()])
    coffee_price = StringField("Price Of Black Coffee", validators=[DataRequired()])
    seats = StringField("Approximate Number of Seats", validators=[DataRequired()])
    submit = SubmitField('Submit')


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


db.create_all()
db.session.commit()

@app.route("/")
def home():
    return render_template("cafe_main_page.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=request.form["name"],
            map_url=request.form["map_url"],
            img_url=request.form["img_url"],
            location=request.form["location"],
            seats=request.form["seats"],
            has_toilet=bool(request.form["has_toilets"]),
            has_wifi=bool(request.form["has_wifi"]),
            has_sockets=bool(request.form["has_sockets"]),
            can_take_calls=bool(request.form["can_take_calls"]),
            coffee_price=request.form["coffee_price"]
        )
        db.session.add(new_cafe)
        db.session.commit()
        db.create_all()
    return render_template('add_cafe.html', form=form)


@app.route('/cafes')
def cafes():
    list_of_rows = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
