from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=32, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    name = models.CharField(max_length=18, null=False)
    email = models.EmailField(max_length=128, unique=True, null=False)
    generation = models.IntegerField(null=False)
    student_id = models.CharField(max_length=12, unique=True, null=False)
    gender = models.CharField(max_length=6, null=False)
    birth = models.DateField(auto_now_add=False, blank=True)
    phone = models.CharField(max_length=13, blank=True)
    joined_at = models.DateField(auto_now_add=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', 'generation', 'student_id']
 