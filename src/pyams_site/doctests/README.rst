==================
PyAMS_site package
==================


Site factory
------------

This package is composed of a set of utility functions, usable into any Pyramid application.

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp(hook_zca=True)
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)

    >>> from pyramid.interfaces import IRootFactory
    >>> factory = config.registry.queryUtility(IRootFactory)
    >>> factory
    <function site_factory at 0x...>

PyAMS provides a default root factory, but any application can provide it's own root factory
by setting the key *pyams.application_factory* with the dotted name of the factory. The application
name, which is the key with which the site is stored into ZODB's root object (it's default value is
*application*), can be defined using the *pyams.application_name* settings key; this allows several
sites to be stored into a single ZODB.


Site generations
----------------

Site generations is a small API which is used to handle database upgrade between subsequent
releases of any package; actually, it's not required in this example to use our site factory
by hand: the generations upgrade process (called by *pyams_upgrade* command line script) will
do it for us:

Until now the new local registry is empty; generations will allow to create a few set of
required utilities:

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyams_utils.registry import handle_site_before_traverse, get_local_registry
    >>> from pyams_site.generations import upgrade_site

    >>> request = DummyRequest()
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    >>> app
    <...BaseSiteRoot object at 0x... oid 0x1 in <Connection at ...>>
    >>> list(app.getSiteManager().keys())
    ['Server timezone']

    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))
    >>> get_local_registry() is app.getSiteManager()
    True

Well, the upgrade process has initialized our local site manager (or local 'registry') with a
new server timezone utility; when other packages are included into Pyramid configuration, they
can register new generations upgrade utilities which will be able to create and initialize new
mandatory utilities, or to update database contents if required. But keep in mind that this upgrade
is not automatic on application startup, the site administrator has to execute the upgrade process
by hand!

Each "generations" utility can handle an "upgrade level"; after an upgrade, this level is stored
into application annotations and will be passed as a parameter to the *evolve* method, so that,
when several levels of upgrades are required, the utility knows which ones to apply:

    >>> from zope.annotation.interfaces import IAnnotations
    >>> from pyams_site.interfaces import SITE_GENERATIONS_KEY
    >>> IAnnotations(app).get(SITE_GENERATIONS_KEY)
    {'PyAMS timezone': 1}


PyAMS upgrade script
--------------------

Sometimes, we don't want automatic database upgrade; the "pyams_upgrade" command line script
can then be used to apply database upgrades on request; it takes the Pyramid configuration
file as argument:

    >>> from pyams_site.scripts import pyams_upgrade_cmd
    >>> pyams_upgrade_cmd()
    Traceback (most recent call last):
    ...
    SystemExit: 2


Site "++etc++" traverser
------------------------

The "++etc++" traverser can be used to provides custom traversers for contents which support
the `ISiteEtcTraverser`:

    >>> from pyams_utils.adapter import adapter_config
    >>> from pyams_utils.testing import call_decorator

    >>> from zope.traversing.interfaces import ITraversable
    >>> from pyams_site.interfaces import ISiteRoot, ISiteEtcTraverser
    >>> from pyams_site.site import SiteRootEtcTraverser, site_root_site_traverser
    >>> call_decorator(config, adapter_config, SiteRootEtcTraverser, name='etc',
    ...                required=ISiteRoot, provides=ITraversable)
    >>> call_decorator(config, adapter_config, site_root_site_traverser, name='site',
    ...                required=ISiteRoot, provides=ISiteEtcTraverser)

    >>> from zope.component import getAdapter
    >>> traverser = getAdapter(app, ITraversable, name='etc')
    >>> traverser.traverse('site')
    <LocalSiteManager ++etc++site>

    >>> traverser.traverse('unknown')
    Traceback (most recent call last):
    ...
    pyramid.httpexceptions.HTTPNotFound: The resource could not be found.


Tests cleanup:

    >>> tearDown()
