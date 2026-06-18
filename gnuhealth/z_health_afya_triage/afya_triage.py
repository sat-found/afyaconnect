# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelSQL, ModelView, fields


class TriageSession(ModelSQL, ModelView):
    "AfyaConnect Triage Session"
    __name__ = 'gnuhealth.afya.triage_session'
    _rec_name = 'session_id'

    session_id = fields.Char('Session ID', required=True)


class EmergencyKeyword(ModelSQL, ModelView):
    "Emergency Keyword"
    __name__ = 'gnuhealth.afya.emergency_keyword'
    _rec_name = 'term'

    term = fields.Char('Term', required=True)
    language = fields.Selection([
        ('en', 'English'),
        ('ha', 'Hausa'),
        ('ff', 'Fulfulde'),
    ], 'Language', required=True)
    active = fields.Boolean('Active')
