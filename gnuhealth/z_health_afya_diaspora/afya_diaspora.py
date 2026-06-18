# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelSQL, ModelView, fields


class DiasporaSpecialist(ModelSQL, ModelView):
    "Diaspora Specialist Stub"
    __name__ = 'gnuhealth.afya.diaspora_specialist'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
