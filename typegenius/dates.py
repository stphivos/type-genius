import re
from enum import Enum
from datetime import datetime
from typegenius import localization


class DatePart(Enum):
    year = 1
    month = 2
    day = 3
    t = 4
    hour = 5
    minute = 6
    second = 7
    fraction = 8
    zone_pos = 9
    zone_text = 10
    zone_h = 11
    zone_m = 12


def create_date(parts):
    lst = [str(parts[DatePart.year])]
    frm = '%Y'
    if parts[DatePart.month] is not None:
        lst.append(str(parts[DatePart.month]).zfill(2))
        frm += ' %m'
        if parts[DatePart.day] is not None:
            lst.append(str(parts[DatePart.day]).zfill(2))
            frm += ' %d'
            if parts[DatePart.hour] is not None:
                lst.append(str(parts[DatePart.hour]).zfill(2))
                frm += ' %H'
                if parts[DatePart.minute] is not None:
                    lst.append(str(parts[DatePart.minute]).zfill(2))
                    frm += ' %M'
                    if parts[DatePart.second] is not None:
                        lst.append(str(parts[DatePart.second]).zfill(2))
                        frm += ' %S.%f'
                        if parts[DatePart.zone_pos] is not None:
                            lst.append(parts[DatePart.zone_text].replace(':', ''))
                            frm += ' %z'
    res = datetime.strptime(' '.join(lst), frm)
    return res


def get_descending_parts(val):
    res = {
        DatePart.year: None,
        DatePart.month: None,
        DatePart.day: None,
        DatePart.t: None,
        DatePart.hour: None,
        DatePart.minute: None,
        DatePart.second: None,
        DatePart.fraction: None,
        DatePart.zone_text: None,
        DatePart.zone_pos: None,
        DatePart.zone_h: None,
        DatePart.zone_m: None
    }

    dc = localization.get_decimal_separator()
    date_time_zone_parts = re.split('[ T]', val.replace('Z', '+00:00'))
    date_parts = re.split('[-]', date_time_zone_parts[0])
    time_zone_parts = time_parts = zone_parts = []

    if len(date_time_zone_parts) > 1:
        time_zone_parts = re.split('\+|-|Z', date_time_zone_parts[1])
        time_parts = re.split('[:]', time_zone_parts[0].replace(',', dc).replace('.', dc))
        index_list = list(i for i, v in enumerate(date_time_zone_parts[1]) if v in '\+|-|Z')
        zone_parts = re.split('[:]', date_time_zone_parts[1][index_list[0]:]) if len(index_list) > 0 else []

    # Date
    if len(date_parts) > 0 and len(date_parts[0]) == 4:
        res[DatePart.year] = int(date_parts[0])
    if len(date_parts) > 1:
        res[DatePart.month] = int(date_parts[1])
    if len(date_parts) > 2:
        res[DatePart.day] = int(date_parts[2])

    # Time
    if len(date_time_zone_parts) > 1:
        res[DatePart.t] = val.strip().replace(date_time_zone_parts[0], '').replace(date_time_zone_parts[1], '')
    if len(time_parts) > 0:
        res[DatePart.hour] = int(time_parts[0])
    if len(time_parts) > 1:
        res[DatePart.minute] = int(time_parts[1])
    if len(time_parts) > 2:
        res[DatePart.second] = float(time_parts[2])
    if len(time_zone_parts) > 0:
        res[DatePart.fraction] = ',' if ',' in time_zone_parts[0] else '.' if '.' in time_zone_parts[0] else None

    # Zone
    if len(zone_parts) > 0:
        res[DatePart.zone_text] = ':'.join(zone_parts)
    if len(zone_parts) > 0:
        res[DatePart.zone_pos] = False if zone_parts[0][0] == '-' else True if zone_parts[0][0] == '+' else None
    if len(zone_parts) > 0:
        res[DatePart.zone_h] = int(zone_parts[0]) if zone_parts[0].isdigit() else 0
    if len(zone_parts) > 1:
        res[DatePart.zone_m] = int(zone_parts[1]) if len(zone_parts) > 1 and zone_parts[1].isdigit() else 0

    return res