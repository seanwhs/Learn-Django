# tags app models.py  -- generic model
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    # Name of the tag (e.g., "Electronics", "Featured", etc.)
    label = models.CharField(max_length=255)


class TagItem(models.Model):
    # Links a tag to any object in the system
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # The model type being tagged (Product, Article, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # The object's primary key
    object_id = models.PositiveBigIntegerField()
    # Generic reference to the actual tagged object
    content_object = GenericForeignKey()
