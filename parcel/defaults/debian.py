# -*- coding: utf-8 -*-
prerm_template = """#!/bin/sh

set -e

APP_NAME={app_name}

case "$1" in
    upgrade)
        {lines}
    ;;

    failed-upgrade|abort-install|abort-upgrade|disappear|purge|remove)
    ;;

    *)
        echo "prerm called with unknown argument \`$1'" >&2
        exit 1
    ;;
esac
"""

postrm_template = """#!/bin/sh

set -e

APP_NAME={app_name}

case "$1" in
    remove)
        {lines}
	;;

    purge)
	;;

    upgrade)
	;;

    failed-upgrade|disappear|abort-install|abort-upgrade)
	;;
    *)
	echo "$0 called with unknown argument \`$1'" 1>&2
	exit 1
	;;
esac

exit 0
"""


preinst_template = """#!/bin/sh

set -e

APP_NAME={app_name}

case "$1" in
    install)
	;;

    install|upgrade)
        {lines}
        ;;
    abort-upgrade)
	;;


    *)
	echo "$0 called with unknown argument \`$1'" 1>&2
	exit 1
	;;
esac


exit 0
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
