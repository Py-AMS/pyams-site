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

"""PyAMS_site.interfaces module

"""

from zope.annotation import IAttributeAnnotatable
from zope.interface import Attribute, Interface, implementer
from zope.interface.interfaces import IObjectEvent, ObjectEvent


PYAMS_APPLICATION_SETTINGS_KEY = 'pyams.application_name'
'''ZODB application name settings key'''

PYAMS_APPLICATION_DEFAULT_NAME = 'application'
'''ZODB default application name'''

PYAMS_APPLICATION_FACTORY_KEY = 'pyams.application_factory'
'''Settings key to define site root factory'''


class ISiteRoot(IAttributeAnnotatable):
    """Marker interface for site root"""


class ISiteRootFactory(Interface):
    """Site root utility factory interface"""


class INewLocalSiteCreatedEvent(IObjectEvent):
    """Event interface when a new site root has been created"""


@implementer(INewLocalSiteCreatedEvent)
class NewLocalSiteCreatedEvent(ObjectEvent):
    """New local site creation event"""


class ISiteEtcTraverser(Interface):
    """Site ++etc++ traverser extension interface"""


class IConfigurationManager(Interface):
    """Configuration manager marker interface"""


class ISiteUpgradeEvent(IObjectEvent):
    """Event interface when a site upgrade is requested"""


@implementer(ISiteUpgradeEvent)
class SiteUpgradeEvent(ObjectEvent):
    """Site upgrade request event"""


SITE_GENERATIONS_KEY = 'pyams.generations'


class ISiteGenerations(Interface):
    """Site generations interface"""

    order = Attribute("Order in which generations should be upgraded")
    generation = Attribute("Current schema generation")

    def evolve(self, site, current=None):
        """Evolve database from current generation to last one"""
