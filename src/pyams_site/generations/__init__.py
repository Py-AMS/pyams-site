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

"""PyAMS_site.generations module

This module provides a site generations utility to check for server timezone utility, and
zodbupdate classes renaming rules.
"""

from persistent.mapping import PersistentMapping
from zope.lifecycleevent import ObjectCreatedEvent

from pyams_site.interfaces import ISiteGenerations, SITE_GENERATIONS_KEY
from pyams_site.site import site_factory
from pyams_utils.adapter import get_annotation_adapter
from pyams_utils.factory import get_object_factory
from pyams_utils.registry import get_current_registry, get_utilities_for, query_utility, \
    set_local_registry


__docformat__ = 'restructuredtext'


def upgrade_site(request):
    """Upgrade site when needed

    This function is executed by *pyams_upgrade* console script.
    Site generations are registered named utilities providing
    :py:class:`ISiteGenerations <pyams_utils.interfaces.site.ISiteGenerations>` interface.

    Current site generations are stored into annotations for each generation adapter.
    """
    application = site_factory(request)
    if application is not None:
        try:
            set_local_registry(application.getSiteManager())
            generations = get_annotation_adapter(application, SITE_GENERATIONS_KEY,
                                                 PersistentMapping, notify=False, locate=False)
            for name, utility in sorted(get_utilities_for(ISiteGenerations),
                                        key=lambda x: x[1].order):
                if not name:
                    name = '.'.join((utility.__module__, utility.__class__.__name__))
                current = generations.get(name)
                if not current:
                    print("Upgrading {0} to generation {1}...".format(name, utility.generation))
                elif current < utility.generation:
                    print("Upgrading {0} from generation {1} to {2}...".format(name, current,
                                                                               utility.generation))
                utility.evolve(application, current)
                generations[name] = utility.generation
        finally:
            set_local_registry(None)
        import transaction  # pylint: disable=import-outside-toplevel
        transaction.commit()
    return application


def check_required_utilities(site, utilities):
    """Utility function to check for required utilities

    :param ISite site: the site manager into which configuration may be checked
    :param tuple utilities: each element of the tuple is another tuple made of the utility
        interface, the utility registration name, the utility factory and the object name when
        creating the utility, as in:

    .. code-block:: python

        REQUIRED_UTILITIES = ((ISecurityManager, '', SecurityManager, 'Security manager'),
                              (IPrincipalAnnotationUtility, '', PrincipalAnnotationUtility,
                               'User profiles'))
    """
    registry = get_current_registry()
    for interface, name, factory, default_id in utilities:
        utility = query_utility(interface, name=name)
        if utility is None:
            lsm = site.getSiteManager()
            if default_id in lsm:
                continue
            if factory is None:
                factory = get_object_factory(interface)
            utility = factory()
            registry.notify(ObjectCreatedEvent(utility))
            lsm[default_id] = utility
            lsm.registerUtility(utility, interface, name=name)
