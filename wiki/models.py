from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import utils

class Versioned(models.Model):

    def history(self):
        return self.revisions.order_by('-created')
        
    def last_revision(self):
        try:
            return self.revisions.order_by('-created')[0]
        except IndexError:
            return None

    def last_change(self):
        last = self.last_revision()
        if last:
            return last.created

    def last_author(self):
        last = self.last_revision()
        if last:
             return last.author

# A revision of the page content
# For now, ignore the language stuff.
class Revision(models.Model):
    created = models.DateTimeField(_("Created"), 
                                   auto_now_add=True)
    author = models.ForeignKey(User, 
                               verbose_name=_("Author"), 
                               null=True, 
                               blank=True)
    description = models.CharField(_("Description"), 
                                   max_length=400, 
                                   blank=True)

    def __unicode__(self):
        return u"%s (%s, %s): %s" % (self.page, self.author, self.created, self.description)

    class Meta:
        abstract = True
        ordering = ('-created',)



## class Language(models.Model):
##     language = models.CharField(max_length=30, primary_key=True)
##     def __unicode__(self):
##         return self.language

# Class for the exercise
class Page(Versioned):
    pass


# Page in a specific language.
## class PageLocal(models.Model, Versioned):
##     language = models.ForeignKey(Language)
##     page = models.ForeignKey(Page)
##     def __unicode__(self):
##         return u"%s (%s)" % (self.page, self.language)

class PageRevision(Revision):
    page = models.ForeignKey(Page, 
                             related_name='revisions')
    title = models.CharField(max_length=50)
    content = models.TextField()
    def __init__(self, *args, **kwargs):
        if 'base_revision' in kwargs and kwargs['base_revision'] is not None:
            base_revision = kwargs.pop('base_revision')
            title = base_revision.title
            content = base_revision.content
            super(PageRevision, self).__init__(*args,
                                               title=title,
                                               content=content,
                                               **kwargs)
        else:
            super(PageRevision, self).__init__(*args,
                                               **kwargs)
            
    def __unicode__(self):
        return unicode(self.title)
