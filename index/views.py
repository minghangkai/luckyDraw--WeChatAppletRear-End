from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Topic, Article
# Create your views here.
def index(request):
    latest_topic_list = Topic.objects.all()   # order_by('-pub_date')[:5]
    context = {'latest_topic_list': latest_topic_list}
    return render(request, 'index/index.html', context)


def detail(request, topic_id):
    return HttpResponse("You're looking at topic %s." % topic_id)


def results(request, topic_id):
    response = "You're looking at the results of topic %s."
    return HttpResponse(response % topic_id)
