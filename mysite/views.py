"""This file is made for redirect to polls index."""
from django.shortcuts import redirect


def index(request):
    """Do the index function, redirect to polls index."""
    return redirect("polls:index")
