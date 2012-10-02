from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import utils

class Versioned(object):

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



class Language(models.Model):
    language = models.CharField(max_length=30, primary_key=True)
    def __unicode__(self):
        return self.language

# Class for the exercise
class Page(models.Model, Versioned):
    def __unicode__(self):
        return str(self.pk)


# Page in a specific language.
class PageLocal(models.Model, Versioned):
    language = models.ForeignKey(Language)
    page = models.ForeignKey(Page)
    def __unicode__(self):
        return u"%s (%s)" % (self.page, self.language)

# A revision of the page content
# For now, ignore the language stuff.
class Revision(models.Model):
    page = models.ForeignKey(Page, related_name='revisions')
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), null=True, blank=True)
    description = models.CharField(_("Description"), max_length=400, blank=True)

    def __unicode__(self):
        return u"%s (%s, %s): %s" % (self.page, self.author, self.created, self.description)

    class Meta:
        abstract = True
        ordering = ('-created',)

class PageRevision(Revision):
    content1 = models.TextField()
    content2 = models.TextField()
    def __init__(self, *args, **kwargs):
        if 'base_revision' in kwargs and kwargs['base_revision'] is not None:
            base_revision = kwargs.pop('base_revision')
            content1 = base_revision.content1
            content2 = base_revision.content2
            super(PageRevision, self).__init__(*args,
                                               content1=content1,
                                               content2=content2,
                                               **kwargs)
        else:
            super(PageRevision, self).__init__(*args,
                                               **kwargs)
            
    
## class Content(models.Model):
##     text = models.TextField(_("Content"), blank=True)
##     def __unicode__(self):
##         return self.text

##     def rebase(self, base, last):
##         # TODO: Do some diff and patch stuff
##         #pass
##         base_text = base.text
##         last_text = last.text
##         new_text = self.text
##         (new_text, results) = utils.rebase(base_text, last_text, new_text)
##         self.text = new_text
##         return results
    
## # A revision of the page content
## # For now, ignore the language stuff.
## class PageRevision(Revision):
##     page = models.ForeignKey(Page, related_name='revisions')
##     #content = models.TextField(_("Content"), blank=True)
##     content = models.ForeignKey(Content, blank=False, null=False)
##     ## def __init__(self, content_class=Content):
##     ##     self.content = models.TextField(_("Content"), blank=True)
##     ##     ## self.content = models.ForeignKey(content_class,
##     ##     ##                                  blank=False,
##     ##     ##                                  null=False)
##     ##     super(PageRevision, self).save(*args, **kwargs)
##     def __unicode__(self):
##         return u"%s (%s, %s): %s" % (self.page, self.author, self.created, self.description)
    
