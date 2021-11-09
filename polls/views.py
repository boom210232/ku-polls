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

from django.contrib.auth.mixins import LoginRequiredMixin

import logging

from django.dispatch import receiver

from datetime import datetime

from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

log = logging.getLogger(__name__)


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


class DetailView(generic.DetailView, LoginRequiredMixin):
    """Do the class make view in detail page."""

    model = Question
    template_name = 'polls/detail.html'
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

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
                log.warning(f"The question has not been published yet!")
                messages.error(request, error_message)
                return redirect('polls:index')
            elif not question.can_vote():
                error_message += "The vote for this question has \
                already ended!"
                log.warning(f"The vote for this question has already ended!")
                messages.error(request, error_message)
                return redirect('polls:index')
        except ObjectDoesNotExist:
            error_message = "The question does not exist!"
            log.warning(f"The question does not exist!")
            messages.error(request, error_message)
            return redirect('polls:index')

        question = get_object_or_404(Question, pk=kwargs['pk'])
        current_choice = get_vote_for_user(question, request.user)
        if not current_choice:
            return render(request, 'polls/detail.html', {'question': question, "current_choice": current_choice})
        return render(request, 'polls/detail.html', {'question': question, 'current_choice': current_choice.choice})


class ResultsView(generic.DetailView):
    """Do this class use to show the result of votes."""

    model = Question
    template_name = 'polls/results.html'


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
        log.info(f"{user} voted in {question}.")
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        messages.success(request, 'Polls already receive, Thank you')

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


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """ This function set callback when user logged in. """
    ip = get_client_ip(request)
    date = datetime.now()
    log.info(f'User {user} with {ip} login at {date}')


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """ This function set callback when user logged out. """
    ip = get_client_ip(request)
    date = datetime.now()
    log.info(f'User {user} with {ip} logout at {date}')


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    """ This function set callback when user make failed login. """
    ip = get_client_ip(request)
    date = datetime.now()
    log.warning(f"User {credentials['username']} with {ip} have error occurred at {date}")
