from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField
from datetime import datetime
from django.utils import timezone


class Book(models.Model):
    book_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    subject = models.CharField(max_length=100)
    book_add_time = models.TimeField(default=timezone.now)
    book_add_date = models.DateTimeField(default=datetime.now)

    class Meta:
        unique_together = (('book_name', 'author_name'),)

    def __str__(self):
        return self.book_name

class Item(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(default=datetime.now, blank=False)
    returned_date = models.DateTimeField(null=True, blank=True)

    @property
    def book_name(self):
        return self.book_id.book_name

    @property
    def username(self):
        return self.user_id.username

    def __str__(self):
        return(
            self.book_id.book_name
            + "issues by"
            + self.user_id.first_name
            + "on"
            + str(self.issued_date)
        )

