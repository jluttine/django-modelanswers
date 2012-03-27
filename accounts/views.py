from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm


def register(request,
             form_class=UserCreationForm,
             template_name='registration/register.html'):
    
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('accounts.views.profile'))
            #return HttpResponseRedirect("/books/")
    else:
        form = form_class()
        
    return render(request,
                  template_name,
                  {
                      'form': form,
                  })


@login_required
def profile(request,
            template_name='registration/profile.html'):
            
    return render(request,
                  template_name)
