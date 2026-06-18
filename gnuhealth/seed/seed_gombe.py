#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Seed synthetic Gombe State data for AfyaConnect Phase 0.

Run inside the app container:
  python3 /opt/gnuhealth/seed/seed_gombe.py

Idempotent: skips records that already exist (matched by code/name).
"""

import random
from datetime import date

from trytond.config import config
from trytond.pool import Pool
from trytond.transaction import Transaction

CONFIG_FILE = '/opt/gnuhealth/etc/trytond.conf'
DATABASE = 'health'
USER_ID = 1

GOMBE_FACILITIES = [
    ('GOM-FMC-001', 'Federal Medical Centre Gombe', 10.2891, 11.1673),
    ('GOM-GSH-001', 'Gombe State Specialist Hospital', 10.2799, 11.1712),
    ('GOM-PHC-DUK-001', 'Dukku Primary Health Centre', 10.7712, 11.2381),
    ('GOM-PHC-KLT-001', 'Kaltungo Primary Health Centre', 9.8198, 11.3085),
    ('GOM-PHC-BLI-001', 'Billiri Primary Health Centre', 9.8654, 11.2214),
    ('GOM-PHC-SHG-001', 'Shongom Primary Health Centre', 9.6123, 11.1023),
    ('GOM-PHC-FUN-001', 'Funakaye Primary Health Centre', 10.4521, 11.3124),
    ('GOM-PHC-NFD-001', 'Nafada Primary Health Centre', 11.0832, 11.3287),
    ('GOM-PHC-AKO-001', 'Akko Primary Health Centre', 10.2512, 11.1823),
    ('GOM-PHC-YAL-001', 'Yamaltu/Deba Primary Health Centre', 10.1823, 11.4123),
]

EMERGENCY_KEYWORDS = [
    ('cannot breathe', 'en'), ('chest pain', 'en'), ('unconscious', 'en'),
    ('severe bleeding', 'en'), ('stroke', 'en'), ('heart attack', 'en'),
    ('seizure', 'en'), ('choking', 'en'),
    ('ba iya numfashi', 'ha'), ('ciwon kirji', 'ha'), ('faint', 'ha'),
    ('jini mai yawa', 'ha'), ('bugun jini', 'ha'), ('zazzabi mai tsanani', 'ha'),
    ('ciwon kai', 'ha'), ('gudawa', 'ha'),
    ('a numaani', 'ff'), ('mettu', 'ff'), ('ngol ngol', 'ff'),
    ('ngesa', 'ff'), ('doole', 'ff'),
    ('difficulty breathing', 'en'), ('high fever', 'en'), ('convulsion', 'en'),
    ('pregnancy bleeding', 'en'), ('severe headache', 'en'),
    ('ba a iya numfashi', 'ha'), ('zazzabi', 'ha'), ('ciwon ciki mai tsanani', 'ha'),
    ('ciki mai zafi', 'ha'), ('jini daga al\'umma', 'ha'),
    ('labour pain', 'en'), ('severe abdominal pain', 'en'), ('allergic reaction', 'en'),
    ('poisoning', 'en'), ('burn', 'en'), ('fracture', 'en'),
    ('drowning', 'en'), ('electric shock', 'en'), ('snake bite', 'en'),
    ('dog bite', 'en'), ('road accident', 'en'), ('fall from height', 'en'),
    ('gunshot', 'en'), ('stab wound', 'en'), ('anaphylaxis', 'en'),
    ('diabetic emergency', 'en'), ('overdose', 'en'), ('heat stroke', 'en'),
    ('hypothermia', 'en'), ('drowning child', 'en'), ('newborn not breathing', 'en'),
]

FIRST_NAMES_M = ['Ahmadu', 'Ibrahim', 'Musa', 'Yusuf', 'Ali', 'Hassan', 'Bala', 'Danladi']
FIRST_NAMES_F = ['Fatima', 'Aisha', 'Hauwa', 'Maryam', 'Zainab', 'Amina', 'Halima', 'Rukayya']
LAST_NAMES = ['Abubakar', 'Mohammed', 'Usman', 'Bello', 'Suleiman', 'Garba', 'Adamu', 'Yakubu']


def _expand_facilities():
    facilities = list(GOMBE_FACILITIES)
    lgas = ['Akko', 'Balanga', 'Billiri', 'Dukku', 'Funakaye', 'Gombe', 'Kaltungo',
            'Kwami', 'Nafada', 'Shongom', 'Yamaltu']
    idx = len(facilities) + 1
    while len(facilities) < 50:
        lga = lgas[idx % len(lgas)]
        code = f'GOM-PHC-{lga[:3].upper()}-{idx:03d}'
        lat = 10.0 + random.uniform(-0.5, 0.8)
        lon = 11.0 + random.uniform(-0.3, 0.5)
        name = f'{lga} Community Health Post {idx}'
        facilities.append((code, name, round(lat, 4), round(lon, 4)))
        idx += 1
    return facilities


def seed_facilities(Institution, Party):
    created = 0
    for code, name, _lat, _lon in _expand_facilities():
        existing = Institution.search([('code', '=', code)], limit=1)
        if existing:
            continue
        party = Party(
            name=name,
            is_institution=True,
            fed_country='NGA',
            fsync=False,
        )
        party.save()
        inst = Institution(
            party=party.id,
            code=code,
            institution_type='primary_care',
            public_level='public',
        )
        inst.save()
        created += 1
    return created


def seed_patients(Patient, Party):
    created = 0
    for i in range(1, 201):
        pname = f'AFYA-PAT-{i:04d}'
        existing = Party.search([('name', '=', pname)], limit=1)
        if existing:
            continue
        gender = random.choice(['m', 'f'])
        first = random.choice(FIRST_NAMES_M if gender == 'm' else FIRST_NAMES_F)
        last = random.choice(LAST_NAMES)
        display_name = f'{first} {last} ({pname})'
        dob = date(1950 + random.randint(0, 60), random.randint(1, 12), random.randint(1, 28))
        party = Party(
            name=display_name,
            is_person=True,
            is_patient=True,
            dob=dob,
            gender=gender,
            fed_country='NGA',
            fsync=False,
        )
        party.save()
        patients = Patient.search([('party', '=', party.id)], limit=1)
        if not patients:
            patient = Patient(party=party.id)
            patient.save()
        created += 1
    return created


def seed_workers(Party):
    created = 0
    for i in range(1, 21):
        wname = f'AFYA-HCW-{i:03d}'
        existing = Party.search([('name', '=', wname)], limit=1)
        if existing:
            continue
        party = Party(
            name=wname,
            is_person=True,
            is_healthprof=True,
            gender=random.choice(['m', 'f']),
            fed_country='NGA',
            fsync=False,
        )
        party.save()
        created += 1
    return created


def seed_keywords(EmergencyKeyword):
    created = 0
    for term, language in EMERGENCY_KEYWORDS:
        existing = EmergencyKeyword.search([
            ('term', '=', term),
            ('language', '=', language),
        ], limit=1)
        if existing:
            continue
        kw = EmergencyKeyword(term=term, language=language, active=True)
        kw.save()
        created += 1
    return created


def main():
    config.update_etc(CONFIG_FILE)

    pool = Pool(DATABASE)
    pool.init()

    with Transaction().start(DATABASE, USER_ID, context={}):
        Institution = pool.get('gnuhealth.institution')
        Party = pool.get('party.party')
        Patient = pool.get('gnuhealth.patient')
        EmergencyKeyword = pool.get('gnuhealth.afya.emergency_keyword')

        f = seed_facilities(Institution, Party)
        p = seed_patients(Patient, Party)
        w = seed_workers(Party)
        k = seed_keywords(EmergencyKeyword)

    print(f'Seed complete: {f} facilities, {p} patients, {w} workers, {k} keywords created.')


if __name__ == '__main__':
    main()
