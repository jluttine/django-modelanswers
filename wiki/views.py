from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from wiki.models import Exercise
from wiki.forms import ExerciseForm
from django.conf import settings

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
    return render_to_response(template_name,
                              {'exercise': exercise,
                               'MATHJAX_URL': MATHJAX_URL})

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
                  {'form': form})


