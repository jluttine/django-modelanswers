from django import forms
from django.utils.translation import ugettext as _
from diff_match_patch import diff_match_patch
from . import models
from wiki import utils

class ExerciseCreateForm(forms.ModelForm):

    class Meta:
        model = models.ExerciseRevision
        exclude = ('author', 'created', 'page')

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super(ExerciseCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.page.save()
        self.instance.page = self.page
        super(ExerciseCreateForm, self).save(*args, **kwargs)

        

class ExerciseEditForm(forms.ModelForm):
    base_revision = forms.ModelChoiceField(
        queryset=models.ExerciseRevision.objects.none(),
        widget=forms.HiddenInput(),
        required=False
        )

    class Meta:
        model = models.ExerciseRevision
        exclude = ('author', 'created', 'page')
        #fields = ('content', 'description')

    def __init__(self, *args, **kwargs):
        self.page = kwargs.pop('page')
        super(ExerciseEditForm, self).__init__(*args, **kwargs)
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
