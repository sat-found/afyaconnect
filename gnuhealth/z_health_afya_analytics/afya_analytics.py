# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelSQL, ModelView, fields


class AnalyticsOutbox(ModelSQL, ModelView):
    "Analytics Outbox Stub"
    __name__ = 'gnuhealth.afya.analytics_outbox'
    _rec_name = 'event_id'

    event_id = fields.Char('Event ID', required=True)
