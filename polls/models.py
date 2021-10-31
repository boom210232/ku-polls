"""
The purpose of this file is.

Check , make and return question and choice correctly
"""
# Create your models here.


import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Objective of this class is make and check question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date', null=True)

    def __str__(self):
        """
        Objective of this method made for return question text.

        return: Question text.
        """
        return self.question_text

    def was_published_recently(self):
        """
        Objective of function make for check the question was still on publish.

        return: boolean from time compare.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Objective of this function make for check the question is publish.

        return: boolean from time compare.
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """
        Objective of this function make for check the question still can vote.

        return: boolean from time compare.
        """
        return self.pub_date <= timezone.now() \
               and (self.end_date is None or timezone.now() <= self.end_date)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Object of this class is return choice text."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Objective of method is made for return choice text.

        return: Choice text.
        """
        return self.choice_text

    # we want toe able to write "choice.votes" in our views
    # and templates to get the number of votes for a Choice.
    # We want the existing code to still work.

    @property
    def votes(self) -> int:
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    # I like to explicitly specify the id
    # id = models.AutoField(Primary_key = True)
    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"Vote by {self.user} for {self.choice.choices}"
