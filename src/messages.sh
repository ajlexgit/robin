#!/bin/sh

pushd $1 > /dev/null
case "$2" in
    -c | --compile)
        django-admin compilemessages
        ;;
    -m | --make)
        django-admin makemessages --no-obsolete ${@:3}
        ;;
    *)
        django-admin makemessages --no-obsolete ${@:2}
        ;;
esac
popd > /dev/null