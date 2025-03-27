from flask_wtf import FlaskForm
from wtforms import (DateField, FloatField, SelectField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length, NumberRange


class InvoiceForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    amount = FloatField(
        'Amount', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')
