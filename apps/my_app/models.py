# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors['name'] = "Name must be more than 2 characters long"

        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be more than 2 characters long"
        
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors['email'] = "Email address is not in a valid format"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        
        if postData['password'] != postData['c_password']:
            errors['c_password'] = "Passwords must match"
        
        if postData['birthday'] < 0:
            errors['birthday'] = "Birthday is required"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return '%s %s' % (self.name, self.email)


class Poke(models.Model):
    poked = models.ForeignKey(User, related_name="pokereceiver")
    poker = models.ForeignKey(User, related_name="pokegiver")
    num_pokes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add="True")
    updated_at = models.DateTimeField(auto_now="True")