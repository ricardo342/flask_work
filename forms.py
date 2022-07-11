# -*- coding:utf-8 -*-
#!/usr/bin/python3
'''
@File: forms
@time:2022/7/11
@Author:majiaqin 170479
@Desc:
'''

from flask_wtf import FlaskForm
from wtforms import TextAreaField, TelField, IntegerField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError

class ContactForm(FlaskForm):
    name = TextAreaField("Name of Student", [validators.DataRequired("Please enter your name.")])
    Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    Address = TextAreaField("Address")

    email = TextAreaField("Email", validators.DataRequired("Please enter your email address."),
                          validators.Email("Please enter your email address."))
    Age = IntegerField("age")
    language = SelectField('Language', choices=[('cpp', 'C&plus;&plus;'),
                                                ('py', 'Python')])
    submit = SubmitField("Send")