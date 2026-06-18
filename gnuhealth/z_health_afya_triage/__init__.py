# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.pool import Pool
from . import afya_triage
from . import ir
from . import wizard


def register():
    Pool.register(
        ir.Cron,
        module='z_health_afya_triage', type_='model')
    Pool.register(
        afya_triage.TriageSession,
        afya_triage.EmergencyKeyword,
        module='z_health_afya_triage', type_='model')
    Pool.register(
        wizard.review_triage.ReviewTriageStart,
        wizard.review_triage.ReviewTriage,
        module='z_health_afya_triage', type_='wizard')
