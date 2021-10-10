"""
The purpose of this file is.

Add a test case for make sure that code will run normally.
"""
# Create your tests here.

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


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

    def test_can_vote_after_date(self):
        """Test can_vote function that it can vote after time or not."""
        test_time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        publish_question = Question(pub_date=test_time)
        self.assertTrue(publish_question.can_vote())

    def test_can_vote_after_end_polls(self):
        """Polls can't vote after deadline."""
        test_time = timezone.now()
        publish_question = Question(pub_date=test_time,
                                    end_date=test_time - datetime.timedelta(seconds=2))
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

    def test_published_before_publish_date(self):
        """
        Test is published function.

        Make sure that it show after the time that announced or not.

        Assertion:
            assertFalse ,the poll is published after the publication date.
        """
        test_time = timezone.now() + \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        publish_question = Question(pub_date=test_time)
        self.assertFalse(publish_question.is_published())





def create_question(question_text, days):
    """
    Create a question with the given `question_text`.

    Published the given number of `days` offset to now
     (negative for questions published in the past, positive for questions
     that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    """
    Objective for this class.

    Make the correct respond in different situation.
    """

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past.

        Questions are displayed on the index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future.

        Question aren't displayed on the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist.

        Only past questions are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Objective for test question is question can vote in properly time."""

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future.

        The result will redirect back to index with error word.

        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('polls:index'), status_code=302,
                             target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)

    def test_past_question(self):
        """
        This function detail view of a question with a pub_date in the past.

        Make it displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
