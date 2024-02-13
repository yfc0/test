#!/bin/sh -evx
alembic upgrade head
exec "$@"
