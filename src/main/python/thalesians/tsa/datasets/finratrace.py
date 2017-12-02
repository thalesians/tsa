import thalesians.tsa.checks as checks
import thalesians.tsa.conversions as conv
import thalesians.tsa.pandasutils as pdutils
from thalesians.tsa.conditions import precondition

@precondition(lambda path, cusip=None, first_report_date=None, last_report_date=None: \
              checks.is_date(first_report_date, allow_none=True))
def load_df_from_file(path, cusip=None, first_report_date=None, last_report_date=None):
    predicates = []
    if cusip is not None:
        if checks.is_iterable_not_string(cusip): predicates.append(pdutils.isin('cusip_id', cusip))
        else: predicates.append(pdutils.eq('cusip_id', cusip))
    if first_report_date is not None:
        predicates.append(pdutils.ge('trans_dt', first_report_date, conv.str_to_date))
    if last_report_date is not None:
        predicates.append(pdutils.le('trans_dt', last_report_date, conv.str_to_date))
    return pdutils.load_df_from_zipped_csv(path, predicates=predicates)
