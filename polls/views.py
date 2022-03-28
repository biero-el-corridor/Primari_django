from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here. 
from .models import Choice ,  Question 
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questionsn (en enlevant celle qui seront publier dans le future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try: 
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist): 
        return render(request, 'polls/detail.html', {
            'question': question, 
            'error_message': "you didn't seect a choice"
            })
    else: 
        selected_choice.vote += 1
        selected_choice.save()

        return HttpResponse(reverse('polls:result', args=(question_id,)))
