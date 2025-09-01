from flask_wtf import FlaskForm
from wtforms import (DateField, SelectField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField(
        'Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField(
        'End Date', format='%Y-%m-%d', validators=[DataRequired()])
    client = SelectField('Client', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')


# TODO
class DeleteProjectForm(FlaskForm):
    pass
