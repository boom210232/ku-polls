import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    """Class purpose is make sure that question will appear correctly."""

    def test_was_published_recently_with_future_question(self):
        """Test that the future question is not published before publication time."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Test that function will not publish old question."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test that the question is published recently correctly."""
        time = timezone.now() - \
               datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_can_vote_before_date(self):
        """Test can_vote function that it can vote before time or not."""
        test_time = timezone.now() + \
                    datetime.timedelta(hours=23, minutes=59, seconds=59)
        publish_question = Question(pub_date=test_time)
        self.assertFalse(publish_question.can_vote())

    def test_published_after_publish_date(self):
        """
        Test is published function.

        Make sure that it show after the time that announced or not.

        Assertion:
            assertTrue when the poll is published after the publication date.
        """
        test_time = timezone.now() - \
                    datetime.timedelta(hours=23, minutes=59, seconds=59)
        publish_question = Question(pub_date=test_time)
        self.assertTrue(publish_question.is_published())
