import csv
import re
import sys

from airtable import Airtable

cases = {}

with open(sys.argv[1]) as infile:
    reader = csv.DictReader(infile)
    event_types = set()

    airtable = Airtable("appnHTbPMc3f8dELw", "Evictions")
    print(airtable.get_all())

    for rec in reader:
        dock13 = rec['DOCK13']
        event_type = rec['OUTINT']
        if rec['CASINTX'] == 'Eviction':
            print(rec)
            if dock13:
                if dock13 not in cases:
                    cases[dock13] = {}

                if rec['PDTYPE'] == 'P':
                    cases[dock13]['plaintiff'] = rec['N28']
                elif rec['PDTYPE'] == 'D':
                    cases[dock13]['defendant'] = rec['N28']
                x = re.search("Schedule Date: (\S+) Event: (.+)$", rec['DATETIP'])
                (schedule_date, event) = x.groups()

                if(event_type == 'First App'):
                    cases[dock13]['First App'] = schedule_date
                if event_type == 'Eviction':
                    cases[dock13]['Eviction'] = schedule_date
                if event_type == 'Hearing':
                    cases[dock13]['Hearing'] = schedule_date

                event_types.add(event_type)

for case_id in cases.keys():
    print(case_id)

    case = cases[case_id]
    first_app = case['First App'] if 'First App' in case else None
    eviction = case['Eviction'] if 'Eviction' in case else None
    hearing = case['Hearing'] if 'Hearing' in case else None
    plaintiff = case['plaintiff'] if 'plaintiff' in case else None
    defendant = case['defendant'] if 'defendant' in case else None
    out_rec = {
        'CaseID': case_id,
        'Plaintiff': plaintiff,
        'Defendant': defendant,
        'FirstApp': first_app,
        'Hearing': hearing,
        'Eviction': eviction
    }

    case_record = airtable.match('CaseID', case_id)
    if case_record:
        sparse_record = {k: v for k, v in out_rec.items() if v is not None}
        airtable.update(case_record['id'], sparse_record)
    else:
        airtable.insert(out_rec)
