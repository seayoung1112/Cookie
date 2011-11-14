# -*- coding: utf-8 -*-
from models import *
from wtforms import Form, TextField, TextAreaField, BooleanField, DateTimeField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from shutil import move
import os
from config import SITE_PATH, MEDIA
import uuid
    
class ProductForm(Form):
    name = TextField(u'啥东东？', [validators.Length(max=50), validators.Required()])    
    description = TextAreaField(u'为什么有趣呢？')
    link = TextField(u'在哪儿买？')
    
    def __init__(self, form=None):
        if form is not None:
            self.picture_path = SITE_PATH + form['picture']
        Form.__init__(self, form)

    def create_product(self, user):
        product = Product()
        product.name = self.name.data
        product.description = self.description.data
        product.link = self.link.data
        product.share_by = user
        if os.path.isfile(self.picture_path):
            product.picture = MEDIA + 'product_img/' + uuid.uuid1().hex + '.png'
            move(self.picture_path, SITE_PATH + product.picture)  
        else:
            return None           
        product.save()
        return product