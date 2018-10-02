#!/usr/bin/env bash

LOCAL_SETTINGS_DIR="./openstack_dashboard/local"

# only run when building.
if [ -e /.dockerenv ]; then
  echo "Setting up ddash for production..."

  cp $LOCAL_SETTINGS_DIR/local_settings_prod.py $LOCAL_SETTINGS_DIR/local_settings.py
  python3 manage.py compress
fi
