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
        pickling["picture"]=form.picture.data
        pickling["name"] = form.name.data
        pickling["location"] = form.location.data
        pickling["organization"] = form.organization.data
        pickling["about"] = form.about.data
        pickling["project"] = form.project.data
        pickling["project_description"] = form.project_description.data

        pickle.dump(pickling, open('pickledUser.p', 'wb'))
        
        #form.picture.save(filename)
        return redirect(url_for('profile'))
        
    #Get cpickle stuff here
    return render_template('edit_profile.html', form=form)

@app.route('/view/<ip>')
def view(ip):
    cached = app.cache.get(ip+"page")
    if cached:
        return cached
    else:
        output = urllib2.urlopen(ip+":1337/profile").read().replace("^url_placeholder^", ip)
        app.cache.set(ip+"page", output)
        return output

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
def profile():
    pickled = pickle.load(open('pickledUser.p', 'rb'))
    print(pickled)
    return render_template('profile.html',
                           picture=pickled["picture"],
                           name=pickled["name"],
                           location=pickled["location"],
                           org=pickled["organization"],
                           about=pickled["about"],
                           project=pickled["project"],
                           proj_desc=pickled["project_description"])
