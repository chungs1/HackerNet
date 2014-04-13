from  app import app
import urllib2
from flask import render_template, flash, redirect, url_for, request, g
from forms import ProfileForm
import forms

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
@app.route('/index')
def index():
    return 'Placeholder'

@app.route('/edit_profile/', methods=('GET', 'POST'))
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        #Get form data here!
        filename = secure_filename(form.picture.file.filename)
        form.picture.file.save(PATH+filename)
        
        return redirect(url_for('profile', form=form))
        
    #Get cpickle stuff here
    return render_template('edit_profile.html', form=form)

@app.route('/profile/<form>')
def upload_file(form):
   pass 

@app.route('/view/<ip>')
def view(ip):
    return urllib2.urlopen(ip+":1337/view_profile").read()

@app.route('/view_profile')
def view_profile():
    #unpickle here and put into the render template
    profile = None
    render_template("profile.html", profile);

