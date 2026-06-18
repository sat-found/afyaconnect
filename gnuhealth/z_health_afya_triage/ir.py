# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from trytond.pool import PoolMeta


class Cron(metaclass=PoolMeta):
    __name__ = 'ir.cron'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.method.selection.extend([
            ('gnuhealth.afya.triage_session|purge_expired_symptoms_raw',
                'Purge expired AfyaConnect symptoms_raw'),
        ])
