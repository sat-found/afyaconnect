# SPDX-FileCopyrightText: 2024 Gerald Wiese <wiese@gnuhealth.org>
# SPDX-FileCopyrightText: 2024 Leibniz University Hannover
#
# SPDX-License-Identifier: GPL-3.0-or-later

#FROM python:3.11.8-bookworm
FROM python:3.11.9

RUN apt-get update && apt-get install -y postgresql-client wget npm grunt && \
  cd /tmp/ && wget https://www.gnuhealth.org/downloads/postgres_dumps/gnuhealth-44-demo.sql.gz && \
  gunzip gnuhealth-44-demo.sql.gz

RUN apt-get install -y expect graphviz libreoffice-writer-nogui libreoffice-calc-nogui && \
  pip3 install uwsgi && \
  pip3 install gnuhealth-all-modules

COPY mosquito_registration /usr/local/lib/python3.11/site-packages/trytond/modules/mosquito_registration
COPY z_health_afya_core /usr/local/lib/python3.11/site-packages/trytond/modules/z_health_afya_core
COPY z_health_afya_access /usr/local/lib/python3.11/site-packages/trytond/modules/z_health_afya_access
COPY z_health_afya_triage /usr/local/lib/python3.11/site-packages/trytond/modules/z_health_afya_triage
COPY z_health_afya_dispatch /usr/local/lib/python3.11/site-packages/trytond/modules/z_health_afya_dispatch
COPY z_health_afya_diaspora /usr/local/lib/python3.11/site-packages/trytond/modules/z_health_afya_diaspora
COPY z_health_afya_analytics /usr/local/lib/python3.11/site-packages/trytond/modules/z_health_afya_analytics
COPY seed /opt/gnuhealth/seed

RUN mkdir -p /opt/gnuhealth/etc /opt/gnuhealth/var/log /opt/gnuhealth/var/lib && \
  cp `pip3 show uwsgi | grep "Location" | cut -b 10-`/gnuhealth-all-modules/etc/trytond.conf /opt/gnuhealth/etc/ && \
  cp `pip3 show uwsgi | grep "Location" | cut -b 10-`/gnuhealth-all-modules/etc/gnuhealth_log.conf /opt/gnuhealth/etc/

COPY ./trytond.ini /opt/gnuhealth/etc/trytond.ini
COPY ./init_and_run.sh /scripts/init_and_run.sh
COPY ./init /scripts/init
COPY ./banner.txt /tmp/banner.txt

RUN chmod +x /scripts/init_and_run.sh
RUN chmod +x /scripts/init

RUN groupadd --gid 1000 node \
    && useradd --uid 1000 --gid node --shell /bin/bash --create-home node

USER node
WORKDIR /home/node
RUN wget -qO- https://downloads.tryton.org/7.0/tryton-sao-7.0.51.tgz | tar -xzf - && mv package sao
WORKDIR /home/node/sao
RUN npm install --legacy-peer-deps
RUN grunt dev
USER root
##RUN npm i tryton-sao
COPY ./modify_trytondconf.sh /tmp/modify_trytondconf.sh
RUN chmod +x /tmp/modify_trytondconf.sh
RUN /tmp/modify_trytondconf.sh

COPY sao-branding /tmp/sao-branding
RUN chmod +x /tmp/sao-branding/apply-branding.sh && /tmp/sao-branding/apply-branding.sh /home/node/sao

ENTRYPOINT ["/scripts/init_and_run.sh"]
