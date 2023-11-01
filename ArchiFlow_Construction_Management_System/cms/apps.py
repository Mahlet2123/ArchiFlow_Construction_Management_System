from django.apps import AppConfig
from allauth.socialaccount.signals import social_account_added


class CmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cms'

    def ready(self):
        from cms.signals import create_user_profile_for_google_signin

        social_account_added.connect(create_user_profile_for_google_signin)