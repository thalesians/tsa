import thalesians.tsa.checks as checks
import thalesians.tsa.conversions as conv
import thalesians.tsa.pandasutils as pdutils
from thalesians.tsa.conditions import precondition

def convert_ascii_rptd_vol_tx(s):
    try: return float(s)
    except:
        if s == '': return float('nan')
        elif s == '1MM+': return 1000000
        elif s == '5MM+': return 5000000
        else: raise ValueError('Unexpected value: \"%s\"' % str(s))
        
trace_df_column_conversions = {
        'ATS_indicator'    : None,
        'ascii_rptd_vol_tx': convert_ascii_rptd_vol_tx,
        'asof_cd'          : None,
        'bond_sym_id'      : None,
        'bsym'             : None,
        'chng_cd'          : conv.str_to_int,
        'cmsn_trd'         : None,
        'company_symbol'   : None,
        'contra_party_type': None,
        'cusip_id'         : None,
        'days_to_sttl_ct'  : None,
        'diss_rptg_side_cd': None,
        'frmt_cd'          : None,
        'function'         : None,
        'high_yld_pt'      : conv.str_to_float,
        'high_yld_sign_cd' : None,
        'low_yld_pt'       : conv.str_to_float,
        'low_yld_sign_cd'  : None,
        'lsal_yld_pt'      : conv.str_to_float,
        'lsal_yld_sign_cd' : None,
        'msg_seq_nb'       : conv.str_to_int,
        'orig_dis_dt'      : conv.str_to_date,
        'orig_msg_seq_nb'  : conv.str_to_int,
        'remuneration'     : None,
        'rptd_high_pr'     : conv.str_to_float,
        'rptd_last_pr'     : conv.str_to_float,
        'rptd_low_pr'      : conv.str_to_float,
        'rptd_pr'          : conv.str_to_float,
        'rptg_party_type'  : None,
        'sale_cndtn2_cd'   : None,
        'sale_cndtn_cd'    : None,
        'side'             : None,
        'spcl_trd_fl'      : None,
        'sttl_dt'          : conv.str_to_date,
        'sub_prd_type'     : None,
        'trans_dt'         : conv.str_to_date,
        'trc_st'           : None,
        'trd_exctn_dt'     : conv.str_to_date,
        'trd_exctn_tm'     : conv.str_to_time,
        'wis_fl'           : None,
        'yld_pt'           : conv.str_to_float,
        'yld_sign_cd'      : None
    }
    
enhanced_trace_df_column_conversions = {
        # TODO To be continued
        'LCKD_IN_IND'      : None,
    }

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
