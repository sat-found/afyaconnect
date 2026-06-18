# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime

from trytond.model import ModelView, fields
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateTransition, StateView, Button


class ReviewTriageStart(ModelView):
    'Review Triage Start'
    __name__ = 'gnuhealth.afya.review_triage.start'

    reviewer_decision = fields.Selection([
        ('confirmed', 'Confirmed'),
        ('overridden', 'Overridden'),
        ('rejected', 'Rejected'),
    ], 'Reviewer Decision', required=True)
    reviewer_notes = fields.Text('Reviewer Notes')


class ReviewTriage(Wizard):
    'Review Triage'
    __name__ = 'gnuhealth.afya.review_triage'

    start = StateView(
        'gnuhealth.afya.review_triage.start',
        'z_health_afya_triage.review_triage_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Submit Review', 'review', 'tryton-ok', default=True),
        ])
    review = StateTransition()

    def transition_review(self):
        pool = Pool()
        TriageSession = pool.get('gnuhealth.afya.triage_session')
        sessions = TriageSession.browse(Transaction().context.get('active_ids'))
        with Transaction().set_context(_afya_review_wizard=True):
            TriageSession.write(sessions, {
                'reviewer_decision': self.start.reviewer_decision,
                'reviewer_notes': self.start.reviewer_notes,
                'review_timestamp': datetime.now(),
            })
            TriageSession.reviewed(sessions)
        return 'end'
