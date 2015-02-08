# -*- coding: utf-8 -*-
#!/sevabot

"""
Simple conference call hosting
"""
from __future__ import unicode_literals

import logging
import os
import Skype4Py
import datetime

from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode

logger = logging.getLogger('sevabot')

# Set to debug only during dev
logger.setLevel(logging.INFO)

logger.debug('Call module level load import')


class DutyHandler(StatefulSkypeHandler):
    """
    Skype message handler class for the conference call hosting.
    """

    def __init__(self):
        """
        Use `init` method to initialize a handler.
        """

        logger.debug('Call handler constructed')

    def init(self, sevabot):
        """
        Set-up our state. This is called every time module is (re)loaded.

        :param skype: Handle to Skype4Py instance
        """

        logger.debug('Call handler init')

        self.skype = sevabot.getSkype()


    def handle_message(self, msg, status):
        """
        Override this method to customize a handler.
        """
        logger.info('On Duty')
        body = ensure_unicode(msg.Body).lower()

        logger.info('Call handler got: {}'.format(body))

        if not body.startswith(u'киса,') or u'кто дежурный?' not in body:
            return False

        week_num = datetime.date.today().isocalendar()[1]
        f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'duty'), 'r')
        d = f.readlines()
        f.close()
        m = d[week_num % len(d)]
        msg.Chat.SendMessage(u'Дежурит сегодня '+m)
        return True

    def shutdown(self):
        """
        Called when the module is reloaded.
        """
        logger.debug('Call handler shutdown')

# Export the instance to Sevabot
sevabot_handler = DutyHandler()

__all__ = ['sevabot_handler']
