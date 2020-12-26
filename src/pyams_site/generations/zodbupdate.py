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

"""PyAMS_site.generations.zodbupdate module

This module provides ZODB classes update rules for previous PyAMS releases.
"""

__docformat__ = 'restructuredtext'


RENAMED_CLASSES = {
    'pyams_utils.interfaces.site IConfigurationManager':
        'pyams_site.interfaces IConfigurationManager',
    'pyams_utils.interfaces.site ISiteRoot':
        'pyams_site.interfaces ISiteRoot',
    'pyams_utils.site BaseSiteRoot':
        'pyams_site.site BaseSiteRoot'
}
