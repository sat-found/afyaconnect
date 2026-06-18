# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.pool import Pool
from . import afya_triage


def register():
    Pool.register(
        afya_triage.TriageSession,
        afya_triage.EmergencyKeyword,
        module='z_health_afya_triage', type_='model')
