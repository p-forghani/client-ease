from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class CreateClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField(
        'Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    address = StringField('Address', validators=[Optional()])
    submit = SubmitField('Add Client')


# FUTURE: instead of a separete form and template, use same form and template
# for creating and updating a client with dynamic values.
class UpdateClientForm(CreateClientForm):
    submit = SubmitField('Update Client')
