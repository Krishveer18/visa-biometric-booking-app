from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from countries import COUNTRIES

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visa_camp_booking.db'
db = SQLAlchemy(app)
class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

class VisaCamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    visa_country = db.Column(db.String(50), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    visa_camp_id = db.Column(db.Integer, db.ForeignKey('visa_camp.id'), nullable=False)
    visa_camp = db.relationship('VisaCamp', backref=db.backref('bookings', lazy=True))

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        month = request.form.get('month')
        visa_country = request.form.get('visa_country')

        query = VisaCamp.query

        if city:
            query = query.filter(VisaCamp.city.like(f'%{city}%'))
        if month:
            query = query.filter(VisaCamp.date.like(f'%{month}%'))
        if visa_country:
            query = query.filter(VisaCamp.visa_country == visa_country)

        camps = query.all()
    else:
        camps = VisaCamp.query.all()

    return render_template('index.html', camps=camps, countries=COUNTRIES)

@app.route('/agent', methods=['GET', 'POST'])
def agent_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        agent = Agent.query.filter_by(username=username).first()
        if agent and check_password_hash(agent.password_hash, password):
            return redirect(url_for('manage_camps'))
        else:
            flash('Invalid username or password')
    return render_template('agent_login.html')


@app.route('/add_camp', methods=['GET', 'POST'])
def manage_camps():
    if request.method == 'POST':
        date = request.form['date']
        city = request.form['city']
        visa_country = request.form['visa_country']
        new_camp = VisaCamp(date=date, city=city, visa_country=visa_country)
        db.session.add(new_camp)
        db.session.commit()
        flash('Visa camp added successfully!')
    camps = VisaCamp.query.all()
    return render_template('add_camp.html', camps=camps, countries=COUNTRIES)

@app.route('/book/<int:camp_id>', methods=['GET', 'POST'])
def book_camp(camp_id):
    camp = VisaCamp.query.get_or_404(camp_id)
    success = False
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        booking = Booking(name=name, email=email, phone=phone, visa_camp_id=camp.id)
        db.session.add(booking)
        db.session.commit()
        success = True
    return render_template('book_camp.html', camp=camp, success=success)


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)








