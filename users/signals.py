from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
            name=instance.first_name,
        )
        
        subject = 'welcome to webdev'
        message='glad u came'
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
    

post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
