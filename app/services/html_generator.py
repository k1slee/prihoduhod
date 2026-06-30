from flask import render_template

def generate_calendar_html(data):
    return render_template('calendar.html', **data)