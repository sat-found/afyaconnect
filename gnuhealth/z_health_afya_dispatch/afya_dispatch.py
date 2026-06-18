# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.model import ModelSQL, ModelView, fields


class DispatchStub(ModelSQL, ModelView):
    "AfyaConnect Dispatch Stub"
    __name__ = 'gnuhealth.afya.dispatch_stub'
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
