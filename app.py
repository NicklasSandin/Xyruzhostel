from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookings.db'
app.config['SECRET_KEY'] = 'your-secret-key-goes-here'
db = SQLAlchemy(app)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    checkin = db.Column(db.DateTime, nullable=False)
    checkout = db.Column(db.DateTime, nullable=False)
    room_type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Booking {self.id}>'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        room_type = request.form['room_type']
        if not name:
            flash('Please enter your name.')
        elif not email:
            flash('Please enter your email address.')
        elif not checkin:
            flash('Please enter your check-in date.')
        elif not checkout:
            flash('Please enter your check-out date.')
        elif not room_type:
            flash('Please select a room type.')
        else:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
            if checkout_date <= checkin_date:
                flash('Check-out date must be after check-in date.')
            else:
                booking = Booking(name=name, email=email, checkin=checkin_date, checkout=checkout_date, room_type=room_type)
                db.session.add(booking)
                db.session.commit()
                flash('Your booking has been confirmed.')
                return redirect(url_for('confirmation', booking_id=booking.id))
    return render_template('book.html')

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('confirmation.html', booking=booking)

if __name__ == '__main__':
    app.run(debug=True)
