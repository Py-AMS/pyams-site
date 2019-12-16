==================
PyAMS_site package
==================

.. contents::


What is PyAMS?
==============

PyAMS (Pyramid Application Management Suite) is a small suite of packages written for applications
and content management with the Pyramid framework.

**PyAMS** is actually mainly used to manage web sites through content management applications (CMS,
see PyAMS_content package), but many features are generic and can be used inside any kind of web
application.

All PyAMS documentation is available on `ReadTheDocs <https://pyams.readthedocs.io>`_


What is PyAMS_site?
===================

PyAMS_site is an extension package for Pyramid and PyAMS frameworks. It provides a small set of
features related to **sites**, which are the base components of any web site or application.

One of the main features of PyAMS_site packages is the management of site's **generations**, which
is largely based on *zope.generations* package (but with much less features); a *generation* is
defined when a new version of any package is requiring database updates to convert
contents by adding or updating properties, or renaming classes. But unlike other frameworks,
PyAMS made the choice to **not** automatically do this conversion, which is done using the
"pyams_upgrade" console script; the **zodbupdate** console script can also be used in a
first step when some classes need to be renamed before doing an upgrade.

PyAMS_site also provides a Pyramid's **root factory**, which is used by Pyramid on application
startup to initialize a new site.
