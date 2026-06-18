# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelSQL, ModelView, fields


class AccessSession(ModelSQL, ModelView):
    "AfyaConnect Access Session"
    __name__ = 'gnuhealth.afya.access_session'
    _rec_name = 'session_id'

    session_id = fields.Char('Session ID', required=True)
