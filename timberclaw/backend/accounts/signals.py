from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BuilderRole, UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_builder_profile(sender, instance, created, raw=False, **kwargs):
    if raw or not created:
        return
    UserProfile.objects.get_or_create(
        user=instance,
        defaults={"role": BuilderRole.HUMAN_DEVELOPER},
    )
