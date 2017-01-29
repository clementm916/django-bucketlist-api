from django.db import models
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class AbstractBaseModel(models.Model):
    """ Abstract model for creting Item and Bucketlist models"""
    name = models.CharField(blank=False, max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Bucketlist(AbstractBaseModel):
    """Defines the structure of Bucketlist objects"""
    created_by = models.ForeignKey(
        User, related_name='bucketlists', on_delete=models.CASCADE)

    class Meta:
        ordering = ('date_created',)
        unique_together = ('name', 'created_by')


class Item(AbstractBaseModel):
    """Defines the structure of Bucketlist-Item objects"""
    done = models.BooleanField(default=True)
    description = models.TextField(blank=True, default="")
    bucketlist_id = models.ForeignKey(
        Bucketlist, related_name='items', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('name', 'bucketlist_id')

#generate a token for users
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        instance.set_password(instance.password)
        instance.save()
        Token.objects.create(user=instance)
