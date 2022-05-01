from enum import unique
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Book(models.Model):
    
    title = models.CharField(max_length=50,unique=True)
    author = models.CharField(max_length=40)
    domain = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.title} by {self.author}'


class BookCodes(models.Model):
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    isbn = models.CharField(unique=True,max_length=13)
    STATUS = [
        ('Available','Available'),
        ('Not Available','Not Available')
    ]
    status = models.CharField(max_length=20,null=True,choices=STATUS,default='Available')

    def __str__(self):
        return f'{self.book.title} | isbn={self.isbn}'


class Student(models.Model):
    deptchoice= [
        ('Computer', 'Computer'),
        ('Mechanical', 'Mechanical'),
        ('ENTC', 'ENTC'),
        ('Civil', 'Civil'),
        ('IT', 'IT'),
        ]
    
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)    
    prn_no = models.CharField(max_length=10,unique=True)
    name = models.CharField(max_length=40)
    branch = models.CharField(max_length=30,choices=deptchoice)
    contact_no = models.CharField(max_length=10)
    total_books_due=models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.prn_no)


#relation containing info about Borrowed books
#it has  foriegn key book and student for refrencing book nad student


def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssueBook(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    book = models.ForeignKey('BookCodes', on_delete=models.CASCADE)
    issue_date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(default=get_expiry)

    def __str__(self):
        return self.student.name+" -> "+self.book.book.title+", "+str(self.book.isbn)


class RequestBook(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    timestamp=models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.timestamp=timezone.now()
        return super(RequestBook, self).save(*args, **kwargs)

    def __str__(self):
        return f'request by {self.student} to {self.book} on {self.timestamp}'

class HistoryBook(models.Model):
    RATING_CHOICES = (
    (1, 'Worse'),
    (2, 'Ok'),
    (3, 'Good'),
    (4, 'Great'),
    (5, 'Excellent')
    )
    book_copy=models.ForeignKey('BookCodes',on_delete=models.CASCADE)
    student=models.ForeignKey('Student',on_delete=models.CASCADE)
    rating=models.IntegerField(choices=RATING_CHOICES, default=3)

    def __str__(self) -> str:
        return f'rating {self.rating} by {self.student} to {self.book_copy.book.title[:20]}'

class RatingNotifier(models.Model):
    RATING_CHOICES = (
        (1, 'Worse'),
        (2, 'Ok'),
        (3, 'Good'),
        (4, 'Great'),
        (5, 'Excellent')
        )
    has_rated=models.BooleanField(default=False)
    book_to_rate=models.OneToOneField('IssueBook',on_delete=models.CASCADE)
    rating=models.IntegerField(choices=RATING_CHOICES, default=3)

    def __str__(self):
        return f'{self.rating},{self.book_to_rate},{self.has_rated}'
    