# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelSQL, ModelView, fields


class AfyaConfig(ModelSQL, ModelView):
    "AfyaConnect Configuration"
    __name__ = 'gnuhealth.afya.config'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
