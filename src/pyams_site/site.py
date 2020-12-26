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

"""PyAMS_site.site module

This module provides all site-related features, like Pyramid's site factory and BaseSiteRoot
which is the base implementation of any website or application.
"""

from pyramid.exceptions import NotFound
from pyramid.path import DottedNameResolver
from pyramid.security import ALL_PERMISSIONS, Allow, Everyone
from pyramid_zodbconn import get_connection
from zope.component import queryAdapter
from zope.component.interfaces import IPossibleSite
from zope.interface import implementer
from zope.site import LocalSiteManager
from zope.site.folder import Folder
from zope.traversing.interfaces import ITraversable

from pyams_site.interfaces import IConfigurationManager, ISiteEtcTraverser, ISiteRoot, \
    ISiteRootFactory, NewLocalSiteCreatedEvent, PYAMS_APPLICATION_DEFAULT_NAME, \
    PYAMS_APPLICATION_FACTORY_KEY, PYAMS_APPLICATION_SETTINGS_KEY
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.registry import get_current_registry, set_local_registry


__docformat__ = 'restructuredtext'


@implementer(ISiteRoot, IConfigurationManager)
class BaseSiteRoot(Folder):
    """Default site root

    A site root can be used as base application root in your ZODB.
    It's also site root responsibility to manage your local site manager.

    BaseSiteRoot defines a basic ACL which gives all permissions to system administrator,
    and 'public' permission to everyone. But this ACL is generally overriden in subclasses
    which also inherit from :py:class:`ProtectedObjectMixin
    <pyams_security.security.ProtectedObjectMixin>`.
    """

    __acl__ = [(Allow, 'system:admin', ALL_PERMISSIONS),
               (Allow, Everyone, {'public'})]

    config_klass = None


@adapter_config(name='etc', required=ISiteRoot, provides=ITraversable)
class SiteRootEtcTraverser(ContextAdapter):
    """Site root ++etc++ namespace traverser

    Gives access to local site manager from */++etc++site* URL
    """

    def traverse(self, name, furtherpath=None):  # pylint: disable=unused-argument
        """Traverse to site manager;
        see :py:class:`ITraversable <zope.traversing.interfaces.ITraversable>`"""
        extension = queryAdapter(self.context, ISiteEtcTraverser, name=name)
        if extension is not None:
            return extension
        raise NotFound


@adapter_config(name='site', required=ISiteRoot, provides=ISiteEtcTraverser)
def site_root_site_traverser(context):
    """Site root ++etc++site traverser extension"""
    return context.getSiteManager()


def site_factory(request):
    """Application site factory

    On application startup, this factory checks configuration to get application name and
    load it from the ZODB; if the application can't be found, configuration is scanned to
    get application factory, create a new one and create a local site manager.
    """
    conn = get_connection(request)
    root = conn.root()
    application_key = request.registry.settings.get(PYAMS_APPLICATION_SETTINGS_KEY,
                                                    PYAMS_APPLICATION_DEFAULT_NAME)
    application = root.get(application_key)
    if application is None:
        factory = request.registry.settings.get(PYAMS_APPLICATION_FACTORY_KEY)
        if factory:
            resolver = DottedNameResolver()
            factory = resolver.maybe_resolve(factory)
        else:
            factory = request.registry.queryUtility(ISiteRootFactory, default=BaseSiteRoot)
        application = root[application_key] = factory()
        if IPossibleSite.providedBy(application):
            lsm = LocalSiteManager(application, default_folder=False)
            application.setSiteManager(lsm)
        try:
            # if some components require a valid and complete registry
            # with all registered utilities, they can subscribe to
            # INewLocalSiteCreatedEvent event interface
            set_local_registry(application.getSiteManager())
            get_current_registry().notify(NewLocalSiteCreatedEvent(application))
        finally:
            set_local_registry(None)
        import transaction  # pylint: disable=import-outside-toplevel
        transaction.commit()
    return application
