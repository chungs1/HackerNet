from flask.ext.wtf import Form
from wtforms import TextField, validators, FileField, TextAreaField, SubmitField
#from wtforms import Required

class ProfileForm:
    name = TextField('Name', [validators.Length(min=4, max=60)])
    picture = FileField('picture')
    location = TextField('Location', [validators.Length(min=0, max=60)])
    organization = TextField('organization', [validators.Length(max=100)])
    about = TextAreaField('about')
    project = TextField('project')
    project_description = TextAreaField('project_description')
    submit = SubmitField("Send")

    

