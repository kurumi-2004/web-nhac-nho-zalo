from django.apps import AppConfig
from django.conf import settings
from reminders.tasks import initialize_scheduled_tasks
import logging

class RemindersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reminders'
    
    def ready(self):
        """
        Initialize app configurations and register signals when Django starts
        """
        import reminders.signals  # Import signals module to register handlers
        # Initialize any additional app configurations
        
        # Register any additional signal handlers
        try:
            initialize_scheduled_tasks()
        except ImportError:
            pass
            
        # Set up logging
        logger = logging.getLogger(__name__)
        logger.info('Reminders app initialized successfully')
