#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_site.generations.timezone module

This module provides timezone utility checker.
"""

from pyams_site.generations import check_required_utilities
from pyams_site.interfaces import ISiteGenerations
from pyams_utils.interfaces.timezone import IServerTimezone
from pyams_utils.registry import utility_config
from pyams_utils.timezone.utility import ServerTimezoneUtility


__docformat__ = 'restructuredtext'

REQUIRED_UTILITIES = ((IServerTimezone, '', ServerTimezoneUtility, 'Server timezone'),)


@utility_config(name='PyAMS timezone', provides=ISiteGenerations)
class TimezoneGenerationsChecker:
    """Site timezone generations checker"""

    order = 10
    generation = 1

    @staticmethod
    def evolve(site, current=None):  # pylint: disable=unused-argument
        """Check for required utilities"""
        check_required_utilities(site, REQUIRED_UTILITIES)
