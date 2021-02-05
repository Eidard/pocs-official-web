from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=18)
    generation = models.IntegerField()
    student_id = models.CharField(max_length=12, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    birth = models.DateField(null=True)
    phone = models.CharField(max_length=13, null=True)

    class Meta:
        db_table = 'accounts'
        ordering = ['name', 'generation', 'student_id']
 