from django.db import models

class Menu(models.Model):
    name = models.CharField(maxlength=100)
    slug = models.SlugField()
    base_url = models.CharField(maxlength=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Admin:
        pass

    def __unicode__(self):
        return "%s" % self.name

    def save(self):
        """
        Re-order all items at from 10 upwards, at intervals of 10.
        This makes it easy to insert new items in the middle of 
        existing items without having to manually shuffle 
        them all around.
        """
        super(Menu, self).save()

        current = 10
        for item in MenuItem.objects.filter(menu=self).order_by('order'):
            item.order = current
            item.save()
            current += 10

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)
    order = models.IntegerField()
    link_url = models.CharField(maxlength=100, help_text='URL or URI to the content, eg /about/ or http://foo.com/')
    title = models.CharField(maxlength=100)
    login_required = models.BooleanField(blank=True, null=True)

    class Admin:
        pass

    def __unicode__(self):
        return "%s %s. %s" % (self.menu.slug, self.order, self.title)
