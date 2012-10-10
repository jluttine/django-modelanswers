from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from wiki.models import Page, PageRevision
from wiki.forms import PageEditForm, PageCreateForm
from django.contrib import messages

#from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.http import HttpResponseRedirect
#from django.shortcuts import render_to_response

class default:
    class classes:
        Versioned = Page
        Revision = PageRevision
        EditForm = PageEditForm
        CreateForm = PageCreateForm
    class templates:
        show = 'wiki/show_page.html'
        add = 'wiki/add_page.html'
        edit = 'wiki/edit_page.html'
        list = 'wiki/list_pages.html'
        history = 'wiki/show_history.html'
        delete = 'wiki/delete_page.html'
    class urls:
        show = 'show_page'
        list = 'list_pages'


# Some conventions:
# http://ericholscher.com/projects/django-conventions/app/

# MathJax URL and settings
MATHJAX_URL = getattr(settings,
                      'MATHJAX_URL',
                      'http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML')


def show_page(request,
              primary_key,
              revision_pk=None,
              classes=default.classes,
              templates=default.templates,
              urls=default.urls):
    try:
        page = classes.Versioned.objects.get(pk=primary_key)
    except classes.Versioned.DoesNotExist:
        raise Http404 # page not found

    if revision_pk:
        try:
            revision = page.revisions.get(pk=revision_pk)
        except classes.Revision.DoesNotExist:
            return HttpResponseNotFound()
        if revision != page.last_revision():
            messages.info(request,
                          """The version you are viewing is not the
                          latest one, but represents an older
                          revision, which may have been significantly
                          modified. If it is not what you intended to
                          view, <a href=\"%(url)s\">proceed to the
                          latest version</a>.""" % {
                              'url': reverse(urls.show, 
                                             kwargs={'primary_key': primary_key})
                              })


    else:
        revision = page.last_revision()
    return render(request,
                  templates.show,
                  {
                      'page': page,
                      'revision': revision,
                      'MATHJAX_URL': MATHJAX_URL,
                  })

@login_required()
def edit_page(request,
              primary_key,
              classes=default.classes,
              templates=default.templates,
              urls=default.urls):

    # Find the exercise
    try:
        page = classes.Versioned.objects.get(pk=primary_key)
    except classes.Versioned.DoesNotExist:
        raise Http404 # page does not exist

    ## # Would like to have like this:
    ## last_revision = page.last_revision()
    ## revision = revision_class(author=request.user,
    ##                           last_revision=last_revision)
    ## form = form_class(data=request.POST or None,
    ##                   instance=revision)

    # Initialize edit
    last_revision = page.last_revision()
    revision = classes.Revision(page=page,
                                author=request.user,
                                base_revision=last_revision)
    form = classes.EditForm(data=request.POST or None,
                            instance=revision,
                            page=page)
    
    if request.method == 'POST':
        # Handle posted edit

        # Don't save, just return to the page
        if request.POST.get('action') == 'cancel':
            return HttpResponseRedirect(reverse(urls.show, 
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
                return HttpResponseRedirect(reverse(urls.show, 
                                                    args=(page.pk,)))
        
    return render(request,
                  templates.edit,
                  {
                      'page': page,
                      'form': form,
                  })


@login_required
def delete_page(request,
                primary_key,
                classes=default.classes,
                templates=default.templates,
                urls=default.urls):

    try:
        page = classes.Versioned.objects.get(pk=exercise_id)
    except classes.Versioned.DoesNotExist:
        raise Http404
    return render(request,
                  templates.delete,
                  {
                      'page': page,
                      'MATHJAX_URL': MATHJAX_URL,
                  })


@login_required
def add_page(request,
             classes=default.classes,
             templates=default.templates,
             urls=default.urls):

    # Create a new page.
    page = classes.Versioned()
    # Create a new revision for the page.
    revision = classes.Revision(page=page,
                                author=request.user)
    # Create the form to edit the contents.
    form = classes.CreateForm(data=request.POST or None,
                              instance=revision,
                              page=page)

    if request.method == 'POST':
        # Handle posted edit

        # Don't save, just return to the page
        if request.POST.get('action') == 'cancel':
            return HttpResponseRedirect(reverse(urls.list))
            
        if form.is_valid():
            # Save and show the page
            form.save()
            primary_key = page.pk
            return HttpResponseRedirect(reverse(urls.show, 
                                                args=(primary_key,)))
        
    return render(request,
                  templates.add,
                  {
                      'form': form,
                  })

def show_history(request,
                 primary_key,
                 classes=default.classes,
                 templates=default.templates,
                 urls=default.urls):
    
    try:
        page = classes.Versioned.objects.get(pk=primary_key)
    except classes.Versioned.DoesNotExist:
        raise Http404 # page not found

    return render(request,
                  templates.history,
                  {
                      'page': page,
                      'revisions': page.history,
                  })


def list_pages(request,
               classes=default.classes,
               templates=default.templates,
               urls=default.urls):

    page_list = classes.Versioned.objects.all()
    
    return render(request,
                  templates.list,
                  {
                      'page_list': page_list,
                  })
