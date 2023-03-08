from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, URL


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes_restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#DB Cafe TABLE Configuration
class Cafe(db.Model):
    __tablename__ = "cafe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    open = db.Column(db.String(250), nullable=False)
    signature_coffee = db.Column(db.Boolean, nullable=False)
    dessert_menu = db.Column(db.Boolean, nullable=False)
    parking = db.Column(db.Boolean, nullable=False)
    smoking = db.Column(db.Boolean, nullable=False)
    close = db.Column(db.String(250), nullable=True)

#DB Restaurant TABLE Configuration
class Restaurant(db.Model):
    __tablename__ = "restaurant"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    open = db.Column(db.String(250), nullable=False)
    menu = db.Column(db.String(250), nullable=False)
    parking = db.Column(db.Boolean, nullable=False)
    close = db.Column(db.String(250), nullable=True)

with app.app_context():
    db.create_all()

# WTForms Configuration
choices = ['✅', '❌']

class Form(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = URLField('Map Link', validators=[DataRequired(), URL()])
    img_url = URLField('Image Link', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    signature_coffee = SelectField('Signature Coffee', choices=choices, validators=[DataRequired()])
    dessert_menu = SelectField('Dessert Menu Quality', choices=choices, validators=[DataRequired()])
    parking = SelectField('Parking Efficiency', choices=choices,validators=[DataRequired()])
    smoking = SelectField('Smoking Area', choices=choices, validators=[DataRequired()])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    submit = SubmitField("Add")

class RestaurantForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = URLField('Map Link', validators=[DataRequired(), URL()])
    img_url = URLField('Image Link', validators=[DataRequired(), URL()])
    location = StringField('Location', validators=[DataRequired()])
    menu = StringField('Menu', validators=[DataRequired()])
    parking = SelectField('Parking Efficiency', choices=choices,validators=[DataRequired()])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    submit = SubmitField("Add")


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafes')
def cafes():
    all_cafes = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=all_cafes)


@app.route('/restaurants')
def restaurants():
    all_restaurants = db.session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=all_restaurants)


@app.route("/add-cafe", methods=['GET', 'POST'])
def add_cafe():
    form = Form()
    if form.validate_on_submit():
        new_cafe = Cafe(name=form.name.data,
                        map_url=form.map_url.data,
                        img_url=form.img_url.data,
                        location=form.location.data,
                        signature_coffee=bool(1 if form.signature_coffee.data == '✅' else 0),
                        dessert_menu=bool(1 if form.dessert_menu.data == '✅' else 0),
                        parking=bool(1 if form.parking.data == '✅' else 0),
                        smoking=bool(1 if form.smoking.data == '✅' else 0),
                        open=form.open.data,
                        close=form.close.data,)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route("/add-restaurant", methods=['GET', 'POST'])
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        new_restaurant = Restaurant(name=form.name.data,
                        map_url=form.map_url.data,
                        img_url=form.img_url.data,
                        location=form.location.data,
                        menu=form.menu.data,
                        parking=bool(1 if form.parking.data == '✅' else 0),
                        open=form.open.data,
                        close=form.close.data,)
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect(url_for('restaurants'))
    return render_template('add.html', form=form)


@app.route('/update', methods=['POST', 'GET'])
def update():
    cafe_id = request.args.get('id')
    selected_cafe = Cafe.query.get(cafe_id)
    form = Form(
        name=selected_cafe.name,
        map_url=selected_cafe.map_url,
        img_url=selected_cafe.img_url,
        location=selected_cafe.location,
        open=selected_cafe.open,
        close=selected_cafe.close,
        signature_coffee='✅' if selected_cafe.signature_coffee else '❌',
        dessert_menu='✅' if selected_cafe.dessert_menu else '❌',
        parking='✅' if selected_cafe.parking else '❌',
        smoking='✅' if selected_cafe.smoking else '❌'
    )
    if form.validate_on_submit():
        selected_cafe.name = form.name.data
        selected_cafe.map_url = form.map_url.data
        selected_cafe.img_url = form.img_url.data
        selected_cafe.location = form.location.data
        selected_cafe.signature_coffee = True if form.signature_coffee.data == '✅' else False
        selected_cafe.dessert_menu = True if form.dessert_menu.data == '✅' else False
        selected_cafe.parking = True if form.parking.data == '✅' else False
        selected_cafe.smoking = True if form.smoking.data == '✅' else False
        selected_cafe.open = form.open.data
        selected_cafe.close = form.close.data
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('update.html', form=form)

@app.route('/restaurant-update', methods=['POST', 'GET'])
def restaurant_update():
    restaurant_id = request.args.get('id')
    selected_restaurant = Restaurant.query.get(restaurant_id)
    form = Form(
        name=selected_restaurant.name,
        map_url=selected_restaurant.map_url,
        img_url=selected_restaurant.img_url,
        location=selected_restaurant.location,
        open=selected_restaurant.open,
        close=selected_restaurant.close,
        menu=selected_restaurant.menu,
        parking='✅' if selected_restaurant.parking else '❌',
    )
    if form.validate_on_submit():
        selected_restaurant.name = form.name.data
        selected_restaurant.map_url = form.map_url.data
        selected_restaurant.img_url = form.img_url.data
        selected_restaurant.location = form.location.data
        selected_restaurant.menu = form.menu.data
        selected_restaurant.parking = True if form.parking.data == '✅' else False
        selected_restaurant.open = form.open.data
        selected_restaurant.close = form.close.data
        db.session.commit()
        return redirect(url_for('restaurants'))
    return render_template('update.html', form=form)


@app.route('/delete')
def delete():
    cafe_id = request.args.get('id')
    selected_cafe = Cafe.query.get(cafe_id)
    db.session.delete(selected_cafe)
    db.session.commit()
    return redirect(url_for('cafes'))

@app.route('/delete-restaurant')
def delete_restaurant():
    restaurant_id = request.args.get('id')
    selected_restaurant = Restaurant.query.get(restaurant_id)
    db.session.delete(selected_restaurant)
    db.session.commit()
    return redirect(url_for('restaurants'))


if __name__ == "__main__":
    app.run(debug=True, port=5001)