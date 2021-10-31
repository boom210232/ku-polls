"""Make this file as a view of polls."""
# Create your views here.

from django.http import HttpResponseRedirect

# from django.template import loader

from django.shortcuts import get_object_or_404, render, redirect

# from django.http import Http404

from django.urls import reverse

from .models import Choice, Question, Vote

from django.views import generic

from django.utils import timezone

from django.contrib import messages

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

import logging


class IndexView(generic.ListView):
    """Make this class as a index view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Do the class make view in detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """Question Error Handling."""
        error_message = "The question cannot be accessed, "
        try:
            question = Question.objects.get(pk=kwargs['pk'])
            if not question.is_published():
                error_message += "The question has not been published yet!"
                messages.error(request, error_message)
                return redirect('polls:index')
            elif not question.can_vote():
                error_message += "The vote for this question has \
                already ended!"
                messages.error(request, error_message)
                return redirect('polls:index')
        except ObjectDoesNotExist:
            error_message = "The question does not exist!"
            messages.error(request, error_message)
            return redirect('polls:index')
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data
                                       (object=self.get_object()))


class ResultsView(generic.DetailView):
    """Do this class use to show the result of votes."""

    model = Question
    template_name = 'polls/results.html'


logs = logging.getLogger("polls")


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Do this function get direct for vote."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        # messages.warning(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        user = request.user
        vote = get_vote_for_user(question, user)
        if not vote:
            vote = Vote(user=request.user, choice=selected_choice)
        else:
            vote.choice = selected_choice
        vote.save()
        # selected_choice.votes += 1
        # selected_choice.save()
        logs.info(f"{user} voted in {question}.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # messages.success(request, 'Polls already receive, Thank you')
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def get_vote_for_user(question: Question, user: User):
    """Find and return an existing vote for a user on a poll question.

    Returns:
        The user's Vote or None if no vote for this poll_question
    """
    try:
        return Vote.objects.get(user=user, choice__question=question)
    except Vote.DoesNotExist:
        return None
