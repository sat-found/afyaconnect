# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.pool import Pool
from . import afya_analytics


def register():
    Pool.register(
        afya_analytics.AnalyticsOutbox,
        module='z_health_afya_analytics', type_='model')
