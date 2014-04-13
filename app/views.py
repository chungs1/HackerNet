from  app import app
import urllib2
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

@app.route('/view/<ip>')
def view(ip):
    #incomplete
    return urllib2.urlopen(ip+":1337/profile").read()

@app.route('/introduce')
def blank():
    return 'HackerNet'

@app.route('/introduce-reply/<pos>/<name>/')
def introduce_reply(pos, name):
    
    print request.remote_addr
    return request.remote_addr

'''
@app.route('/view_profile')
def view_profile():
    #unpickle here and put into the render template
    profile = None
    render_template("profile.html", profile);
'''

@app.route('/profile/')
def upload_file():
    pickled = pickle.load(open('pickledUser.p', 'rb'))
    return render_template('profile.html', pickled=pickled)
