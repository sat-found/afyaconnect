#!/bin/bash

# SPDX-FileCopyrightText: 2024 Gerald Wiese <wiese@gnuhealth.org>
# SPDX-FileCopyrightText: 2024 Leibniz University Hannover
#
# SPDX-License-Identifier: GPL-3.0-or-later

grep -v '^#' /tmp/banner.txt 
echo

# check env vars
echo "Checking which env vars are present"

DB_HOSTNAME="db"
DB_PORT="5432"
DB_USERNAME="gnuhealth"
DB_PW="gnusolidario"
DB_NAME="health"
ADMIN_MAIL="example@example.com"
ADMIN_PW="gnusolidario"

if [[ -n "${GNUHEALTH_DB_HOST}" ]]; then
  echo "using provided DB hostname"
  DB_HOSTNAME=$GNUHEALTH_DB_HOST
fi

if [[ -n "${GNUHEALTH_DB_PORT}" ]]; then
  echo "using provided DB port"
  DB_PORT=$GNUHEALTH_DB_PORT
fi

if [[ -n "${GNUHEALTH_DB_USERNAME}" ]]; then
  echo "using provided DB user name"
  DB_USERNAME=$GNUHEALTH_DB_USERNAME
fi

if [[ -n "${GNUHEALTH_DB_PW}" ]]; then
  echo "using provided DB user name"
  DB_PW=$GNUHEALTH_DB_PW
fi

if [[ -n "${GNUHEALTH_DB_NAME}" ]]; then
  echo "using provided DB user name"
  DB_NAME=$GNUHEALTH_DB_NAME
fi

if [[ -n "${GNUHEALTH_ADMIN_MAIL}" ]]; then
  echo "using provided admin user mail"
  ADMIN_MAIL=$GNUHEALTH_ADMIN_MAIL
fi

if [[ -n "${GNUHEALTH_ADMIN_PW}" ]]; then
  echo "using provided admin user password"
  ADMIN_PW=$GNUHEALTH_ADMIN_PW
fi

if [[ -n "${GNUHEALTH_DEMO_DB}" ]]; then
  echo "using provided demo db boolean"
  DEMO_DB=$GNUHEALTH_DEMO_DB
fi

sed -i "s#uri = .*#uri = postgresql://${DB_USERNAME}:${DB_PW}@${DB_HOSTNAME}:${DB_PORT}/#" /opt/gnuhealth/etc/trytond.conf

echo "Creating local demo database if not exists already (and boolean is true)"
export PGPASSWORD=$DB_PW;
if $DEMO_DB && (! psql -h $DB_HOSTNAME -U $DB_USERNAME  -lqt | cut -d \| -f 1 | grep ghdemo44); then
  cd /tmp/
  createdb -h $DB_HOSTNAME -U $DB_USERNAME ghdemo44
  psql -h $DB_HOSTNAME -U $DB_USERNAME ghdemo44 < gnuhealth-44-demo.sql
  cd -
fi

echo "Initializing fresh database if not done already"
if ! psql -h $DB_HOSTNAME -U $DB_USERNAME -d $DB_NAME -c "\dt" | grep res_user; then
  /scripts/init $ADMIN_MAIL $ADMIN_PW $DB_NAME
fi

NEEDS_MODULE_UPDATE=false
if ! psql -h $DB_HOSTNAME -U $DB_USERNAME -d $DB_NAME -tAc \
    "SELECT 1 FROM ir_module WHERE name='health' AND state='activated'" | grep -q 1; then
  NEEDS_MODULE_UPDATE=true
fi
if ! psql -h $DB_HOSTNAME -U $DB_USERNAME -d $DB_NAME -tAc \
    "SELECT 1 FROM ir_module WHERE name='z_health_afya_core' AND state='activated'" | grep -q 1; then
  NEEDS_MODULE_UPDATE=true
fi

if $NEEDS_MODULE_UPDATE; then
  echo "Activating GNU Health and AfyaConnect modules on ${DB_NAME}"
  trytond-admin -c /opt/gnuhealth/etc/trytond.conf -d "${DB_NAME}" \
    --activate-dependencies -u health health_lab health_ems health_icd10 \
    health_federation health_crypto health_reporting \
    z_health_afya_core z_health_afya_access z_health_afya_triage \
    z_health_afya_dispatch z_health_afya_diaspora z_health_afya_analytics
fi

/usr/local/bin/uwsgi --ini /opt/gnuhealth/etc/trytond.ini
