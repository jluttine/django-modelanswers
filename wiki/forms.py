from django import forms
from django.utils.translation import ugettext as _
from diff_match_patch import diff_match_patch
from . import models

class PageCreateForm(forms.ModelForm):

    class Meta:
        model = models.PageRevision
        exclude = ('author', 'created', 'page')

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super(PageCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.page.save()
        self.instance.page = self.page
        super(PageCreateForm, self).save(*args, **kwargs)


## class PageCreateForm(forms.ModelForm):

##     class Meta:
##         model = models.PageRevision
##         fields = ('content', 'description')

##     def __init__(self, *args, **kwargs):
##         self.page = kwargs.pop('page')
##         super(PageCreateForm, self).__init__(*args, **kwargs)

##     def save(self, *args, **kwargs):
##         self.page.save()
##         self.instance.page = self.page
##         super(PageCreateForm, self).save(*args, **kwargs)

        

class PageEditForm(forms.ModelForm):
    base_revision = forms.ModelChoiceField(
        queryset=models.PageRevision.objects.none(),
        widget=forms.HiddenInput(),
        required=False
        )

    class Meta:
        model = models.PageRevision
        exclude = ('author', 'created', 'page')
        #fields = ('content', 'description')

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super(PageEditForm, self).__init__(*args, **kwargs)
        if self.page.pk:
            self.fields['base_revision'].queryset = self.page.revisions.all()
            self.fields['base_revision'].initial = self.page.last_revision()

    ## def _rebase(self, base, latest, our):
    ##     dmp = diff_match_patch()
    ##     diff = dmp.patch_make(base, our)
    ##     return dmp.patch_apply(diff, latest)

    def clean(self):
        base_revision = self.cleaned_data.get('base_revision')
        last_revision = self.page.last_revision()
        if base_revision != last_revision:
            #content = self.cleaned_data['content']
            rebase_success = False

            self.cleaned_data = self.model.rebase(self.cleaned_data,
                                                  base_revision,
                                                  last_revision)
            if not self.cleaned_data:
                raise forms.ValidationError(
                    _("Somebody else has modified this page in the meantime. It is not "\
                      "possible to merge all the changes automatically. Stash your version "\
                      "somewhere else and reapply with the latest revision."))
            
        return self.cleaned_data
            ## if base_revision:
            ##     content, results = utils.rebase(base_revision.content, last_revision.content, content)
            ##     rebase_success = False not in results
            ## if not rebase_success:
            ##     raise forms.ValidationError(
            ##         _("Somebody else has modified this page in the meantime. It is not "\
            ##           "possible to merge all the changes automatically. Stash your version "\
            ##           "somewhere else and reapply with the latest revision."))
            ## self.cleaned_data['content'] = content
        ## return self.cleaned_data

    ## def save(self, *args, **kwargs):
        ## if not self.page.pk:
        ##     self.page.save()
        ##     self.instance.page = self.page
        ## super(PageEditForm, self).save(*args, **kwargs)


## from django.forms import ModelForm
## from wiki.models import Page, PageRevision

## class PageForm(ModelForm):
##     class Meta:
##         model = Page

## class PageRevisionForm(ModelForm):
##     class Meta:
##         model = PageRevision
