from  app import app
from flask import render_template, flash, redirect, url_for, request, g
from forms import ProfileForm
import forms


@app.route('/')
@app.route('/index')
def index():
    return 'Placeholder'

def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        #Get form data here!
    #Get cpickle stuff here
    return render_template('edit_profile.html', form)
