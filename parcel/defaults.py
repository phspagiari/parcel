# -*- coding: utf-8 -*-

prerm_template = """#!/bin/sh

set -e

APP_NAME={app_name}

case "$1" in
    upgrade|failed-upgrade|abort-install|abort-upgrade|disappear|purge|remove)
        {lines}
    ;;

    *)
        echo "prerm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
"""


postinst_template = """#!/bin/sh

set -e

APP_NAME={app_name}

case "$1" in
    configure)
        {lines}
    ;;

    abort-upgrade|abort-remove|abort-deconfigure)
    ;;

    *)
        echo "postinst called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
"""
