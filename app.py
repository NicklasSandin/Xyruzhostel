from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class BookingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    checkin_date = DateField('Check-in Date', validators=[DataRequired()])
    checkout_date = DateField('Check-out Date', validators=[DataRequired()])
    submit = SubmitField('Book Now')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():
    form = BookingForm()
    if form.validate_on_submit():
        flash('Your booking request has been submitted!', 'success')
        return redirect(url_for('index'))
    return render_template('book.html', form=form)

if __name__ == '__main__':
    app.run()
