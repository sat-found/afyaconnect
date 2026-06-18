# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later

import re

NIGERIAN_PHONE = re.compile(
    r'\b(0[789][01]\d{8}|\+234[789][01]\d{8})\b')


def redact_phone_numbers(text):
    """Redact Nigerian phone numbers before storing symptoms_raw."""
    if not text:
        return text
    return NIGERIAN_PHONE.sub('[PHONE_REDACTED]', text)


def coarsen_region(sector_count, lga_count, state_count):
    """Return region level and code for k-anonymity cascade (SPEC-SURV-001)."""
    if sector_count >= 10:
        return 'sector', None
    if lga_count >= 10:
        return 'lga', None
    if state_count >= 10:
        return 'state', None
    return 'suppressed', 'INSUFFICIENT_VOLUME'
