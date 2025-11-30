# likes app models.py -- generic model
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LikedItem(models.Model):
    # User who liked the object
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Type of object liked (Product, Article, Review, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID of the liked object
    object_id = models.PositiveIntegerField()
    # Generic reference to the liked object
    content_object = GenericForeignKey()
