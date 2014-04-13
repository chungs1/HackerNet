from flask.ext.wtf import Form
from app import app
from wtforms import TextField, validators, FileField, TextAreaField, SubmitField
#from wtforms import Required

class ProfileForm(Form):
    name = TextField('Name', [validators.Required(),validators.Length(min=4, max=60)])
    picture = FileField('picture',[validators.Required()])
    location = TextField('Location', [validators.Required(),validators.Length(min=0, max=60)])
    organization = TextField('organization', [validators.Required(),validators.Length(max=100)])
    about = TextAreaField('about', [validators.Required()])
    project = TextField('project', [validators.Required()])
    project_description = TextAreaField('project_description',[validators.Required()])
    submit = SubmitField("Send")

    def validate_picture(form, field):
        print field.data
        return '.' in field.data and \
        field.data.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    

