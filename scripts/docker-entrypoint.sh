#!/usr/bin/env bash

set -e

APP="exec poetry run python -m todoapp"


function migrate () {
  if [[ ! -z "${RUN_MIGRATIONS}" ]]; then
    alembic upgrade head
  fi
}

migrate
${APP} $*
