from __future__ import unicode_literals

from django.db import models

# Create your models here.
class subject(models.Model):
    name = models.CharField(max_length = 50)
    code = models.CharField(max_length = 10)
    credits = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "subject"
    
class day(models.Model):
    name = models.CharField(max_length=10)
    number_of_subjects = models.IntegerField()
    subject_list = models.ManyToManyField(subject)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'day'
