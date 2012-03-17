from django.shortcuts import render_to_response, render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from wiki.models import Exercise
from wiki.forms import ExerciseForm

def show_exercise(request, exercise_id):
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404
    return render_to_response('wiki/show_exercise.html',
                              {'exercise': exercise})

def edit_exercise(request, exercise_id):
    # Find the exercise
    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        # Handle posted edit
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('wiki.views.show_exercise', 
                                                args=(exercise.pk,)))
    else:
        # Initialize edit
        form = ExerciseForm(instance=exercise)
    return render(request,
                  'wiki/edit_exercise.html',
                  {'form': form})


