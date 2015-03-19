from typegenius import localization, dates
from typegenius.dates import DatePart
from datetime import datetime


def is_float(val, out_res=None):
    if out_res is None:
        out_res = []

    if isinstance(val, float):
        out_res.append(val)
        return True

    dc = localization.get_decimal_separator()
    ts = localization.get_thou_separator()

    if dc in str(val) and str(val).replace(dc, '').replace(ts, '').isdigit():
        out_res.append(float(val))
        return True
    else:
        return False


def is_int(val, out_res=None):
    if out_res is None:
        out_res = []

    if isinstance(val, int):
        out_res.append(val)
        return True

    ts = localization.get_thou_separator()

    if str(val).replace(ts, '').isdigit():
        out_res.append(int(val))
        return True
    else:
        return False


def is_bool(val, out_res=None):
    if out_res is None:
        out_res = []
    if isinstance(val, bool):
        out_res.append(val)
        return True
    elif str(val).lower() in ['true', 'false']:
        out_res.append(bool(val))
        return True
    else:
        return False


def is_date_rfc_2822(val, out_res=None):
    """
    Format: Wed, 05 Oct 2011 22:26:12 -0400
    """
    pass


def is_date_rfc_2616(val, out_res=None):
    """
    Format: Thu, 06 Oct 2011 02:26:12 GMT
    """
    pass


def is_date_rfc_3339(val, out_res=None):
    """
    Format: 1997-07-16T19:20:30.45+01:00
    Allows the "T" to be replaced by a space (or other character)
    Allows -00:00
    """
    parts = dates.get_descending_parts(val)

    if len(list(p for p in parts if p != DatePart.fraction and parts[p] is None)) > 0:
        return False  # Requires a complete representation of date and time (only fractional seconds are optional)
    if parts[DatePart.fraction] is not None and parts[DatePart.fraction] != '.':
        return False  # Only allows a period character to be used as the decimal point for fractional seconds

    if out_res is None:
        out_res = []

    date = dates.create_date(parts)
    out_res.append(date)

    return True


def is_date_iso_8601(val, out_res=None):
    """
    Format: 1997-07-16T19:20:30.45+01:00
    Allows elements to the right to be omitted
    Does not allow T to be replaced only omitted
    """
    parts = dates.get_descending_parts(val)

    if parts[DatePart.year] is None or parts[DatePart.month] is None or parts[DatePart.month] is None:
        return False  # Requires at least the date
    if parts[DatePart.fraction] is not None and parts[DatePart.fraction] not in ['.', ',']:
        return False  # Allows comma or period for decimal fractions of time elements
    if not parts[DatePart.zone_pos] and parts[DatePart.zone_h] == 0:
        return False  # Does not allow -00:00

    if out_res is None:
        out_res = []

    date = dates.create_date(parts)
    out_res.append(date)

    return True


def is_date(val, out_res=None):
    if out_res is None:
        out_res = []
    if isinstance(val, datetime):
        out_res.append(val)
        return True
    elif is_date_rfc_3339(val, out_res):
        return True
    elif is_date_iso_8601(val, out_res):
        return True
    elif is_date_rfc_2822(val, out_res):
        return True
    elif is_date_rfc_2616(val, out_res):
        return True
    else:
        return False


def get(val):
    out_res = []
    if val is None:
        return None
    elif is_float(val, out_res):
        return out_res[0]
    elif is_int(val, out_res):
        return out_res[0]
    elif is_bool(val, out_res):
        return out_res[0]
    elif is_date(val, out_res):
        return out_res[0]
    else:
        return val