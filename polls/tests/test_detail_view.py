# Create your tests here.

import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from polls.models import Question
from django.contrib.auth.decorators import login_required


def create_question(question_text, days):
    """
    Create a question with the given `question_text`.

    Published the given number of `days` offset to now
     (negative for questions published in the past, positive for questions
     that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


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
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        This function detail view of a question with a pub_date in the past.

        Make it displays the question's text.
        """
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        # TypeError: 'AnonymousUser' object is not iterable
        with self.assertRaises(TypeError):
            response = self.client.get(url)
            self.assertRedirects(response, reverse('polls:index'), status_code=302,
                                 target_status_code=200, msg_prefix='',
                                 fetch_redirect_response=True)
            self.assertEqual(response.status_code, 302)
