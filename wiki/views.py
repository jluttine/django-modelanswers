from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from wiki.models import Exercise
from wiki.forms import ExerciseForm

#from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response



# Some conventions:
# http://ericholscher.com/projects/django-conventions/app/

# MathJax URL and settings
MATHJAX_URL = getattr(settings,
                      'MATHJAX_URL',
                      'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML')


def show_exercise(request,
                  exercise_id,
                  template_name='wiki/show_exercise.html'):
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404
    return render(request,
                  template_name,
                  {
                      'exercise': exercise,
                      'MATHJAX_URL': MATHJAX_URL,
                  })

@login_required
def edit_exercise(request,
                  exercise_id,
                  form_class=ExerciseForm,
                  template_name='wiki/edit_exercise.html'):
    # Find the exercise
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        # Handle posted edit
        form = form_class(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('wiki.views.show_exercise', 
                                                args=(exercise.pk,)))
    else:
        # Initialize edit
        form = form_class(instance=exercise)
    return render(request,
                  template_name,
                  {
                      'form': form,
                  })


@login_required
def delete_exercise(request,
                  exercise_id,
                  template_name='wiki/show_exercise.html'):

    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404
    return render(request,
                  template_name,
                  {
                      'exercise': exercise,
                      'MATHJAX_URL': MATHJAX_URL,
                  })


@login_required
def add_exercise(request,
                 form_class=ExerciseForm,
                 template_name='wiki/edit_exercise.html'):

    if request.method == 'POST':
        # Handle posted edit
        form = form_class(request.POST)
        if form.is_valid():
            exercise_id = form.cleaned_data['id']
            print('id', exercise_id)
            form.save()
            return HttpResponseRedirect(reverse('wiki.views.show_exercise', 
                                                args=(exercise_id,)))
    else:
        # Initialize edit
        form = form_class()
        
    return render(request,
                  template_name,
                  {
                      'form': form,
                  })

def list_exercises(request,
                   template_name='wiki/list_exercises.html'):

    exercise_list = Exercise.objects.all()
    
    return render(request,
                  template_name,
                  {
                      'exercise_list': exercise_list,
                  })
