#!/usr/bin/env bash

set -e

APP="exec poetry run python -m todoapp"


function migrate () {
  poetry run alembic upgrade head
}

migrate
${APP} $*
