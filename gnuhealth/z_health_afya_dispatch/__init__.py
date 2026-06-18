# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.pool import Pool
from . import afya_dispatch


def register():
    Pool.register(
        afya_dispatch.DispatchStub,
        module='z_health_afya_dispatch', type_='model')
