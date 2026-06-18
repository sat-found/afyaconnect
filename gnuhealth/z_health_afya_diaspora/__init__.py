# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.pool import Pool
from . import afya_diaspora


def register():
    Pool.register(
        afya_diaspora.DiasporaSpecialist,
        module='z_health_afya_diaspora', type_='model')
