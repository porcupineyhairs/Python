from __future__ import absolute_import, unicode_literals

import logging

from dingtalk.client import SecretClient, AppKeyClient  # NOQA
from dingtalk.client.isv import ISVClient  # NOQA
from dingtalk.core.exceptions import DingTalkClientException, DingTalkException  # NOQA

__version__ = '2.0.1'
__author__ = '007gzs'

# Set default logging modules to avoid "No modules found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
