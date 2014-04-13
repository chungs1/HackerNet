from  app import app
from flask import render_template, flash, redirect, url_for, request, g
from forms import ProfileForm
import forms
import cPickle as pickle
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
@app.route('/index')
def index():
    return 'Placeholder'

@app.route('/edit_profile/', methods=('GET', 'POST'))
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        pickling = {}
        #Get form data here!
        pickled["filename"] = form.picture.file.filename
        pickling["name"] = form.name.default
        pickling["location"] = form.location.default
        pickling["organization"] = form.organization.default
        pickling["about"] = form.about.default
        pickling["project"] = form.project.default
        pickling["project_description"] = form.project_description.default

        pickle.dump(pickling, open('pickledUser.p', 'wb'))
        
        form.picture.file.save(filename)
        return redirect(url_for('upload_file', form=form))
        
    #Get cpickle stuff here
    return render_template('edit_profile.html', form=form)

@app.route('/profile/')
def upload_file():
    pickled = pickle.load(open('pickledUser.p', 'rb'))
    return render_template('profile.html', pickled=pickled)
