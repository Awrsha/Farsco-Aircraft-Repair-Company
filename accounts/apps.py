# accounts/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = _('مدیریت کاربران')
    
    def ready(self):
        # Import signal handlers
        import accounts.signals