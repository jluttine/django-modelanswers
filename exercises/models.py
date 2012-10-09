from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from wiki.models import Revision, Versioned

class Exercise(Versioned):
    def __unicode__(self):
        return unicode(self.pk)

# A revision of the exercise content
class ExerciseRevision(Revision):
    page = models.ForeignKey(Exercise, 
                             related_name='revisions')
    question = models.TextField()
    solution = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        if 'base_revision' in kwargs and kwargs['base_revision'] is not None:
            base_revision = kwargs.pop('base_revision')
            question = base_revision.question
            solution = base_revision.solution
            super(ExerciseRevision, self).__init__(*args,
                                                   question=question,
                                                   solution=solution,
                                                   **kwargs)
        else:
            super(ExerciseRevision, self).__init__(*args,
                                                   **kwargs)

    def __unicode__(self):
        return u"%s: %s" % (self.page, self.created)
