
from django.dispatch import Signal

import logging
logger = logging.getLogger('ilogger')

# ---------------------------------------------------
# my custom signal
# -------------------------------------------------
capture_user_activity = Signal()
