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

"""PyAMS_site.scripts module

This module provides a "pyams_upgrade" command line utility, which can be used to
"upgrade" a site, which means creating all it's required persistent utilities and
registering them into it's local site manager.
"""

import argparse
import sys
import textwrap

from pyramid.paster import bootstrap

from pyams_site.generations import upgrade_site


__docformat__ = 'restructuredtext'


def pyams_upgrade_cmd():
    """Check for site upgrade"""
    usage = "usage: {0} config_uri".format(sys.argv[0])
    description = """Check for database upgrade.
                  Usage: pyams_upgrade production.ini
                  """
    parser = argparse.ArgumentParser(usage=usage,
                                     description=textwrap.dedent(description))
    parser.add_argument('config_uri', help='Name of configuration file')
    args = parser.parse_args()

    config_uri = args.config_uri
    env = bootstrap(config_uri)
    closer = env['closer']
    try:
        upgrade_site(env['request'])
    finally:
        closer()
