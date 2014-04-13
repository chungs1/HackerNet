from app import app, basedir, cache, socketio
from flask.ext.socketio import emit
import json
import urllib
import urllib2
from flask import render_template, flash, redirect, url_for, request, g
from forms import ProfileForm
import forms
import cPickle as pickle
import os


@app.route('/')
@app.route('/index')
def index():
    if request.remote_addr != "127.0.0.1":
        return "UNAUTHORIZED ACCESS ATTEMPT REJECTED"
    if cache.get('rerun_setup'):
        return "Please restart the application"
    if not cache.get('ip_dict_valid'):
        flash("You need to set up your profile!")
        return render_template("indexFirst.html")
        return redirect(url_for('edit_profile'))

    ip_dict = cache.get('ip_dict')
    return render_template('index.html', ipDict=ip_dict)

@app.route('/edit_profile/', methods=['GET', 'POST'])
def edit_profile():
    if request.remote_addr != "127.0.0.1":
        return "UNAUTHORIZED ACCESS ATTEMPT REJECTED"
    form = ProfileForm()
    if form.validate_on_submit():
        if cache.get('ip_dict_valid'):
            cache.set('rerun_setup', True)
            cache.set('ip_dict_valid', True)

        file = request.files['picture']
        file.save(os.path.join(basedir,"app/static/profile.jpg"))

        pickling = {}
        #Get form data here!
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

'''
@app.route('/recieve_message', methods=['POST'])
def receive_message
'''

@app.route('/view/<ip>')
def view(ip):
    cached = cache.get(ip+"page")
    if cached:
        return cached
    else:
        output = urllib2.urlopen("http://"+ip+":1337/profile").read().replace("^url_placeholder^", ip)
        cache.set(ip+"page", output)
        return output

@app.route('/introduce')
def blank():
    return 'HackerNet'

@app.route('/introduce-reply/<loc>/<name>/')
def introduce_reply(loc, name):
    ip_dict = cache.get('ip_dict')
    ip_dict[request.remote_addr] = {'name':name, 'location':loc}
    cache.set('ip_dict', ip_dict)

    try:
        pickled = pickle.load(open('pickledUser.p', 'rb'))
    except Exception:
        pickled = {'name': "error", 'location': "error"}
    infodict = {'name':pickled['name'], 'location':pickled['location']}
    return json.dumps(infodict)

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
                           picture="/static/profile.jpg",
                           name=pickled["name"],
                           location=pickled["location"],
                           org=pickled["organization"],
                           about=pickled["about"],
                           project=pickled["project"],
                           proj_desc=pickled["project_description"])

@app.route('/catch_message', methods=['GET', 'POST'])
def catch_msg():
    print request.form
    
    socketio.emit('my response', {'data':request.form['data']}, broadcast = True)
    
    return 'Hi'


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    ip_dict = cache.get('ip_dict')
    for key, value in ip_dict.iteritems():
        print 'sending'
        req = urllib2.Request("http://"+key+":1337/catch_message")
        req.add_data(urllib.urlencode({'data':message['data']}))
        output = urllib2.urlopen(req)

    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
