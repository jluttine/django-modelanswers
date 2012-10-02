from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from wiki.models import Page, PageLocal, PageRevision
from wiki.forms import PageEditForm, PageCreateForm
from django.contrib import messages

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


def show_page(request,
              primary_key,
              revision_pk=None,
              page_class=Page,
              revision_class=PageRevision,
              template_name='wiki/show_page.html'):
    try:
        page = page_class.objects.get(pk=primary_key)
    except page_class.DoesNotExist:
        raise Http404 # page not found

    if revision_pk:
        try:
            revision = page.revisions.get(pk=revision_pk)
        except revision_class.DoesNotExist:
            return HttpResponseNotFound()
        if revision != page.last_revision():
            messages.info(request,
                          """The version you are viewing is not the
                          latest one, but represents an older revision
                          of this page, which may have been
                          significantly modified. If it is not what
                          you intended to view, <a
                          href=\"%(url)s\">proceed to the latest
                          version</a>.""" % {
                              'url': reverse('show_page', kwargs={'primary_key': primary_key})
                              })


    else:
        revision = page.last_revision()
    return render(request,
                  template_name,
                  {
                      'page': page,
                      'revision': revision,
                      'MATHJAX_URL': MATHJAX_URL,
                  })

@login_required
def edit_page(request,
              primary_key,
              page_class=Page,
              revision_class=PageRevision,
              form_class=PageEditForm,
              template_name='wiki/edit_page.html'):
    # Find the exercise
    try:
        page = page_class.objects.get(pk=primary_key)
    except page_class.DoesNotExist:
        raise Http404 # page does not exist

    ## # Would like to have like this:
    ## last_revision = page.last_revision()
    ## revision = revision_class(author=request.user,
    ##                           last_revision=last_revision)
    ## form = form_class(data=request.POST or None,
    ##                   instance=revision)

    # Initialize edit
    last_revision = page.last_revision()
    revision = revision_class(page=page,
                              author=request.user,
                              base_revision=last_revision)
    form = form_class(data=request.POST or None,
                      instance=revision,
                      page=page)
    
    if request.method == 'POST':
        # Handle posted edit

        # Don't save, just return to the page
        if request.POST.get('action') == 'cancel':
            return HttpResponseRedirect(reverse('show_page', 
                                                args=(page.pk,)))
            

        # Check validity of the form
        if form.is_valid():

            if False:
                # If another revision has happened during this revision,
                # merge the revisions and propose to user.
                pass
            else:
                # Save the edit (could also request for a preview
                # here)
                form.save()
                return HttpResponseRedirect(reverse('show_page', 
                                                    args=(page.pk,)))
        
    return render(request,
                  template_name,
                  {
                      'page': page,
                      'form': form,
                  })


@login_required
def delete_page(request,
                primary_key,
                page_class=Page,
                template_name='wiki/show_page.html'):

    try:
        page = page_class.objects.get(pk=exercise_id)
    except page_class.DoesNotExist:
        raise Http404
    return render(request,
                  template_name,
                  {
                      'page': page,
                      'MATHJAX_URL': MATHJAX_URL,
                  })


@login_required
def add_page(request,
             page_class=Page,
             revision_class=PageRevision,
             form_class=PageCreateForm,
             template_name='wiki/add_page.html'):

    # Create a new page.
    page = page_class()
    # Create a new revision for the page.
    revision = revision_class(page=page,
                              author=request.user)
    # Create the form to edit the contents.
    form = form_class(data=request.POST or None,
                      instance=revision,
                      page=page)

    if request.method == 'POST':
        # Handle posted edit

        # Don't save, just return to the page
        if request.POST.get('action') == 'cancel':
            return HttpResponseRedirect(reverse('list_pages'))
            
        if form.is_valid():
            # Save and show the page
            form.save()
            primary_key = page.pk
            return HttpResponseRedirect(reverse('show_page', 
                                                args=(primary_key,)))
        
    return render(request,
                  template_name,
                  {
                      'form': form,
                  })

def show_history(request,
                 primary_key,
                 page_class=Page,
                 template_name='wiki/show_history.html'):
    
    try:
        page = page_class.objects.get(pk=primary_key)
    except page_class.DoesNotExist:
        raise Http404 # page not found

    return render(request,
                  template_name,
                  {
                      'page': page,
                      'revisions': page.history,
                  })


def list_pages(request,
               page_class=Page,
               template_name='wiki/list_pages.html'):

    page_list = page_class.objects.all()
    
    return render(request,
                  template_name,
                  {
                      'page_list': page_list,
                  })
