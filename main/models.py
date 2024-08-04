from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class Opinions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)

    def __str__(self):
        return f'{self.user.username} - {self.faculty.user.get_full_name()} - {self.question.text}'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    review_text = models.TextField()

    def __str__(self):
        return f'{self.user.username} - {self.faculty.user.get_full_name()}'
    
