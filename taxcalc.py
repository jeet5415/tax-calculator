def calculate_tax(x): 
    tax = (
        (max(0, min(x, 800000) - 400000) * 0.05) +
        (max(0, min(x, 1200000) - 800000) * 0.10) +
        (max(0, min(x, 1600000) - 1200000) * 0.15) +
        (max(0, min(x, 2000000) - 1600000) * 0.20) +
        (max(0, min(x, 2400000) - 2000000) * 0.25) +
        (max(0, x - 2400000) * 0.30)
    )
 
    return tax 
import os
import re

FORCE_STRING_FIELDS = {
    "pan", "co_owner_pan", "tenant_pan",
    "aadhaar_number",
    "mobile_no", "secondary_mobile_no",
    "pin_code", "pin_code_2",
    "din_number",
    "receipt_no",
    "bank_ifsc", "bank_account_number",
    "bsr_code", "challan_serial_no",
    "tan", "tcs_tan",
}


def read_user_data():
    filepath = os.path.join("inputs", "user_data.txt")
 
    try:
        file = open(filepath, "r")
    except FileNotFoundError:
        print(f"ERROR: '{filepath}' not found.")
        print("Make sure your data file is saved as 'user_data.txt' inside the 'inputs' folder.")
        raise SystemExit(1)
    user_data = {}
    for line in file:
        line = line.strip()
 
        if line == "" or line.startswith("#"):
            continue
 
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            continue
        base_key = re.sub(r"_\d+$", "", key)  # e.g. "bank_account_number_2" -> "bank_account_number"
        if base_key in FORCE_STRING_FIELDS:
            pass  # keep as string, preserves leading zeros and formatting
        elif value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass  # keep as string (e.g. names, dates, other free text)
        user_data[key] = value
    file.close()
    return user_data
# PART A - GENERAL NFORMATION
# ==============================
 
def get_general_info(user_data):
    g = user_data.get
    full_name = " ".join(p for p in [g("first_name", ""), g("middle_name", ""), g("last_name", "")] if p)
    opting_new_regime = g("opting_new_regime", "Yes")
    tax_regime = "New Regime" if str(opting_new_regime).strip().lower() == "yes" else "Old Regime"
 
    info = {
        "assessment_year": g("assessment_year", "2026-27"),
        "pan": g("pan", ""), "full_name": full_name, "date_of_birth": g("date_of_birth", ""),
        "aadhaar_number": "[Aadhaar Redacted]",
        "mobile_no": g("mobile_no", ""), "secondary_mobile_no": g("secondary_mobile_no", ""),
        "email": g("email", ""), "secondary_email": g("secondary_email", ""),
        "filed_under_section": g("filed_under_section", "139(1)-On or before due date"),
        "notice_type": g("notice_type", ""),                          # A16
        "receipt_no": g("receipt_no", ""), "original_return_date": g("original_return_date", ""),  # A18
        "din_number": g("din_number", ""), "din_date": g("din_date", ""),  # A19
        "nature_of_employment": g("nature_of_employment", "Not Applicable"),
        "opting_new_regime": opting_new_regime, "tax_regime": tax_regime,
        "seventh_proviso_flag": g("seventh_proviso_flag", "No"),      # A21
        "foreign_travel_flag": g("foreign_travel_flag", "No"), "foreign_travel_exp": g("foreign_travel_exp", 0),
        "electricity_flag": g("electricity_flag", "No"), "electricity_exp": g("electricity_exp", 0),
        "other_seventh_proviso_flag": g("other_seventh_proviso_flag", "No"),
        "other_seventh_proviso_condition": g("other_seventh_proviso_condition", "No"),
        "rep_assessee_flag": g("rep_assessee_flag", "No"),            # A22
        "rep_name": g("rep_name", ""), "rep_email": g("rep_email", ""), "rep_contact": g("rep_contact", ""),
    }
    # Primary (A8a-A14a) and Secondary (A8b-A14b) address blocks
    for suffix in ("", "_2"):
        for field, default in [("flat_door_block", ""), ("premises_name", ""), ("road_street", ""),
                                ("area_locality", ""), ("town_city_district", ""), ("state", ""),
                                ("country", "India"), ("pin_code", "")]:
            info[field + suffix] = g(field + suffix, default)
    return info
# PART B - INCOME
# ==============================
 
def compute_income(user_data):
    """Computes salary, house property, other-sources income and taxable income (Part B)."""
    g = user_data.get
 
    # B1: Salary - itemized 17(1)+17(2)+17(3) if given, else flat gross_salary
    s17 = (g("salary_17_1", 0), g("perquisites_17_2", 0), g("profit_lieu_salary_17_3", 0))
    gross_salary = sum(s17) or g("gross_salary", 0)
 
    # B1-ii: Allowances exempt u/s 10 (e.g. HRA/LTA exemption) - subtracted before u/s 16 deductions
    exempt_allowance_10 = g("exempt_allowance_10", 0)
    salary_after_exemption = gross_salary - exempt_allowance_10
 
    # Deductions u/s 16 - itemized if given, else flat exempt_allowance
    d16 = (g("standard_deduction_16ia", 0), g("entertainment_allowance_16ii", 0), g("professional_tax_16iii", 0))
    exempt_allowance = sum(d16) or g("exempt_allowance", 0)
    net_salary = salary_after_exemption - exempt_allowance
 
    # House Property: type/co-owner/tenant PAN are informational; annual value calc as before
    house_property_type = g("house_property_type", "Self-occupied")
    co_owner_pan = g("co_owner_pan", "")
    tenant_pan = g("tenant_pan", "")
    annual_value = g("house_rent", 0) - g("unrealized_rent", 0) - g("municipal_tax", 0)
    house_property_income = annual_value * 0.70 - g("home_loan_interest", 0) + g("arrears_rent", 0) * 0.7
 
    # House Property 2
    house_property_income_2 = (
        user_data.get("house_rent_2", 0)
        - user_data.get("municipal_tax_2", 0)
        - user_data.get("home_loan_interest_2", 0)
    )
    house_property_income += house_property_income_2
 
    savings_interest = g("savings_interest", 0)
    other_income_nature = g("other_income_nature", "")            # B3: nature of other-source income
    dividend_income = g("dividend_income", 0)
    dividend_quarterly = g("dividend_quarterly", "")               # B3: quarterly breakup for 234C relief
    family_pension_deduction_57iia = g("family_pension_deduction_57iia", 0)
    # Part C: itemized deduction heads - sums into total_deductions if any are given
    c_labels = ["80C", "80CCC", "80CCD1", "80CCD1B", "80CCD2", "80CCH", "80D", "80DD", "80DDB",
                "80E", "80EE", "80EEA", "80EEB", "80G", "80GG", "80GGA", "80GGC", "80TTA", "80TTB", "80U", "other"]
    deductions_c = {c: g(f"deduction_{c.lower()}", 0) for c in c_labels}
    total_deductions = sum(deductions_c.values()) or g("total_deductions", 0)
 
    # C3: Exempt income - for reporting purposes only (e.g. agricultural income up to Rs 5,000); not taxed
    exempt_income_amount = g("exempt_income_amount", 0)
    exempt_income_nature = g("exempt_income_nature", "")
 
    ltcg_sale_consideration = g("ltcg_sale_consideration", 0)
    ltcg_cost_of_acquisition = g("ltcg_cost_of_acquisition", 0)
    ltcg_112a = max(0, ltcg_sale_consideration - ltcg_cost_of_acquisition)
 
    gross_income = (
        net_salary + house_property_income + savings_interest
        + dividend_income - family_pension_deduction_57iia + ltcg_112a
    )
 
    taxable_income = max(0, gross_income - total_deductions)
    taxable_income = round(taxable_income / 10) * 10
 
    return {
        "salary_17_1": s17[0], "perquisites_17_2": s17[1], "profit_lieu_salary_17_3": s17[2],
        "gross_salary": gross_salary,
        "exempt_allowance_10": exempt_allowance_10,
        "standard_deduction_16ia": d16[0], "entertainment_allowance_16ii": d16[1], "professional_tax_16iii": d16[2],
        "net_salary": net_salary,
        "house_property_address": g("house_property_address", ""),
        "house_property_type": house_property_type,
        "house_property_co_owned": g("house_property_co_owned", "No"),
        "house_property_share_pct": g("house_property_share_pct", 100),
        "co_owner_pan": co_owner_pan,
        "house_property_tenant_name": g("house_property_tenant_name", ""),
        "tenant_pan": tenant_pan,
        "house_property_income": house_property_income,
        "savings_interest": savings_interest,
        "other_income_nature": other_income_nature,
        "dividend_income": dividend_income,
        "dividend_quarterly": dividend_quarterly,
        "family_pension_deduction_57iia": family_pension_deduction_57iia,
        "ltcg_sale_consideration": ltcg_sale_consideration,
        "ltcg_cost_of_acquisition": ltcg_cost_of_acquisition,
        "ltcg_112a": ltcg_112a,
        "deductions_c": deductions_c,
        "exempt_income_amount": exempt_income_amount,
        "exempt_income_nature": exempt_income_nature,
        "total_deductions": total_deductions,
        "gross_income": gross_income,
        "taxable_income": taxable_income,
    }
 
# ==============================
# PART D - COMPUTATION OF TAX PAYABLE
# ==============================
 
def compute_surcharge(taxable_income, tax_after_rebate):
    """Marginal-relief-aware surcharge calculation for high incomes."""
    brackets = [(20000000, 0.25, 0.15), (10000000, 0.15, 0.10), (5000000, 0.10, 0.0)]
    for threshold, rate, prev_rate in brackets:
        if taxable_income > threshold:
            surcharge = tax_after_rebate * rate
            tax_at_threshold = calculate_tax(threshold)
            max_tax = tax_at_threshold + tax_at_threshold * prev_rate + (taxable_income - threshold)
            return max(0, min(surcharge, max_tax - tax_after_rebate))
    return 0
 
 
def compute_tax(user_data, taxable_income):
    """Runs the full D1-D17 tax computation for a given taxable income (Part D)."""
    g = user_data.get
 
    d1_tax_before_rebate = calculate_tax(taxable_income)
    d2_rebate_87a = d1_tax_before_rebate if taxable_income <= 1200000 else 0
    d3_tax_after_rebate = d1_tax_before_rebate - d2_rebate_87a
    surcharge = compute_surcharge(taxable_income, d3_tax_after_rebate)
    d4_cess = (d3_tax_after_rebate + surcharge) * 0.04
    d5_total_tax_and_cess = d3_tax_after_rebate + surcharge + d4_cess
 
    d6_relief_89 = g("relief_89", 0)
    d7_interest_234a = g("interest_234a", 0)
    d8_interest_234b = g("interest_234b", 0)
    d9_interest_234c = g("interest_234c", 0)
    d10_fee_234f = g("fee_234f", 0)
    d10a_fee_revised_return = g("fee_234i_revised_return", 0)  # D10(a), section 234-I
 
    d11_total_tax_fee_interest = (
        d5_total_tax_and_cess + d7_interest_234a + d8_interest_234b + d9_interest_234c
        + d10_fee_234f + d10a_fee_revised_return - d6_relief_89
    )
 
    # D12: Total Taxes Paid = D13 Advance Tax + D14 Self-Assessment + D15 TDS + D16 TCS
    tds_paid, advance_tax, self_assessment_tax, tcs_collected = (
        g("tds_paid", 0), g("advance_tax", 0), g("self_assessment_tax", 0), g("tcs_collected", 0)
    )
    d12_total_taxes_paid = tds_paid + advance_tax + self_assessment_tax + tcs_collected
 
    diff = d11_total_tax_fee_interest - d12_total_taxes_paid
    d13_amount_payable, d14_refund = (diff, 0) if diff > 0 else (0, -diff)
 
    return {
        "d1_tax_before_rebate": d1_tax_before_rebate, "d2_rebate_87a": d2_rebate_87a,
        "d3_tax_after_rebate": d3_tax_after_rebate, "surcharge": surcharge, "d4_cess": d4_cess,
        "d5_total_tax_and_cess": d5_total_tax_and_cess, "d6_relief_89": d6_relief_89,
        "d7_interest_234a": d7_interest_234a, "d8_interest_234b": d8_interest_234b,
        "d9_interest_234c": d9_interest_234c, "d10_fee_234f": d10_fee_234f,
        "d10a_fee_revised_return": d10a_fee_revised_return,
        "d11_total_tax_fee_interest": d11_total_tax_fee_interest,
        "d12_total_taxes_paid": d12_total_taxes_paid, "tcs_collected": tcs_collected,
        "d13_amount_payable": d13_amount_payable, "d14_refund": d14_refund,
    }
# ==============================
# PART E / SCHEDULE-IT / SCHEDULE-TDS - MULTI-ROW COLLECTOR
# ==============================
 
def collect_rows(user_data, fields, prefix=""):
    """Collects numbered rows (field_1, field_2, ...) into a list of dicts; stops at first missing row."""
    rows = []
    i = 1
    while any(f"{prefix}{f}_{i}" in user_data for f in fields):
        rows.append({f: user_data.get(f"{prefix}{f}_{i}", d) for f, d in fields.items()})
        i += 1
    return rows
 
def get_bank_details(user_data):
    fields = {"bank_ifsc": "", "bank_name": "", "bank_account_number": "",
              "account_type": "Savings", "select_for_refund": "No"}
    rows = collect_rows(user_data, fields)
    if not rows and user_data.get("bank_ifsc"):  # backward-compat: single unnumbered account
        rows = [{f: user_data.get(f, d) for f, d in fields.items()}]
        rows[0]["select_for_refund"] = user_data.get("select_for_refund", "Yes")
    return rows
 
def get_schedule_it(user_data):
    fields = {"bsr_code": "", "date_of_deposit": "", "challan_serial_no": "", "tax_paid_challan": 0}
    rows = collect_rows(user_data, fields)
    if not rows and user_data.get("bsr_code"):  # backward-compat: single unnumbered row
        rows = [{f: user_data.get(f, d) for f, d in fields.items()}]
    return rows
 
def get_schedule_tds(user_data):
    fields = {"tan": "", "deductor_name": "", "tds_section": "", "gross_payment": 0,
              "tds_year": "", "tax_deducted": 0, "tds_claimed": 0}
    return collect_rows(user_data, fields)
 
def get_schedule_tcs(user_data):
    fields = {"tcs_tan": "", "collector_name": "", "amount_paid": 0, "tax_collected": 0, "tcs_claimed": 0}
    return collect_rows(user_data, fields)
 
# ==============================
# OUTPUT
# ==============================
 
def print_report(general_info, income, tax, bank, schedule_it, schedule_tds, schedule_tcs):
 
    print(f"\nITR-1 SAHAJ | {general_info['assessment_year']} | {general_info['tax_regime']}")
    print("\n---------- PART A: GENERAL INFORMATION ----------")
    print(f"Name               : {general_info['full_name']}")
    print(f"PAN                : {general_info['pan']}")
    print(f"Aadhaar            : {general_info['aadhaar_number']}")
    print(f"DOB                : {general_info['date_of_birth']}")
    print(f"Mobile No.         : {general_info['mobile_no']}")
    print(f"Secondary Mobile   : {general_info['secondary_mobile_no']}")
    print(f"E-mail             : {general_info['email']}")
    print(f"Secondary E-mail   : {general_info['secondary_email']}")
    for label, suffix in (("Address            ", ""), ("Address (Secondary)", "_2")):
        fields = ["flat_door_block", "premises_name", "road_street", "area_locality",
                  "town_city_district", "state", "country", "pin_code"]
        vals = [general_info[f + suffix] for f in fields]
        if suffix == "" or any(vals[:6] + vals[7:]):  # ignore country default when checking "any filled"
            print(f"{label}: " + ", ".join(str(v) for v in vals[:6]) + f", {vals[6]} - {vals[7]}")
    print(f"Filed u/s          : {general_info['filed_under_section']}")
    # A16: only printed if filed in response to a notice
    if general_info['notice_type']:
        print(f"Filed in Response u/s: {general_info['notice_type']}")
    # A18: only printed if revised/defective return details were supplied
    if general_info['receipt_no'] or general_info['original_return_date']:
        print(f"Original Return    : Receipt No. {general_info['receipt_no']} dated {general_info['original_return_date']}")
    # A19: only printed if DIN details were supplied
    if general_info['din_number'] or general_info['din_date']:
        print(f"DIN / Notice Date  : {general_info['din_number']} dated {general_info['din_date']}")
    print(f"Nature of Employ.  : {general_info['nature_of_employment']}")
    print(f"Opting New Regime  : {general_info['opting_new_regime']} (u/s 115BAC)")
    # A21: only printed when the person is filing though not otherwise required to
    if str(general_info['seventh_proviso_flag']).strip().lower() == "yes":
        print(f"7th Proviso 139(1) : Foreign Travel(Y/N) {general_info['foreign_travel_flag']} "
              f"Rs {general_info['foreign_travel_exp']:,.2f} | "
              f"Electricity(Y/N) {general_info['electricity_flag']} "
              f"Rs {general_info['electricity_exp']:,.2f} | "
              f"Other Condition(Y/N) {general_info['other_seventh_proviso_flag']}: "
              f"{general_info['other_seventh_proviso_condition']}")
    # A22: only printed if filing as a representative assessee
    if str(general_info['rep_assessee_flag']).strip().lower() == "yes":
        print(f"Representative     : {general_info['rep_name']} | {general_info['rep_email']} | {general_info['rep_contact']}")
 
    print("\n---------- PART B: INCOME DETAILS ----------")
    # Salary breakup (17(1)/(2)/(3)) only printed if itemized
    if income['salary_17_1'] or income['perquisites_17_2'] or income['profit_lieu_salary_17_3']:
        print(f"  Salary u/s 17(1)   : ₹ {income['salary_17_1']:,.2f}")
        print(f"  Perquisites 17(2)  : ₹ {income['perquisites_17_2']:,.2f}")
        print(f"  Profit in Lieu 17(3): ₹ {income['profit_lieu_salary_17_3']:,.2f}")
    print(f"Gross Salary       : ₹ {income['gross_salary']:,.2f}")
    if income['exempt_allowance_10']:
        print(f"  Exempt u/s 10      : ₹ {income['exempt_allowance_10']:,.2f}")
    # Deductions u/s 16 breakup only printed if itemized
    if income['standard_deduction_16ia'] or income['entertainment_allowance_16ii'] or income['professional_tax_16iii']:
        print(f"  Std Deduction 16(ia): ₹ {income['standard_deduction_16ia']:,.2f}")
        print(f"  Entertainment 16(ii): ₹ {income['entertainment_allowance_16ii']:,.2f}")
        print(f"  Professional Tax 16(iii): ₹ {income['professional_tax_16iii']:,.2f}")
    print(f"Net Salary         : ₹ {income['net_salary']:,.2f}")
    # House property detail only printed if supplied
    if income['house_property_address']:
        print(f"  HP Address         : {income['house_property_address']} ({income['house_property_type']})")
    if str(income['house_property_co_owned']).strip().lower() == "yes":
        print(f"  Co-Owned           : Yes, Share {income['house_property_share_pct']}%"
              + (f", Co-owner PAN {income['co_owner_pan']}" if income['co_owner_pan'] else ""))
    if income['house_property_tenant_name']:
        print(f"  Tenant             : {income['house_property_tenant_name']}"
              + (f" (PAN {income['tenant_pan']})" if income['tenant_pan'] else ""))
    print(f"House Property Inc : ₹ {income['house_property_income']:,.2f}")
    print(f"Savings Interest   : ₹ {income['savings_interest']:,.2f}")
    if income['other_income_nature']:
        print(f"  Nature of Income   : {income['other_income_nature']}")
    print(f"Dividend Income    : ₹ {income['dividend_income']:,.2f}")
    if income['dividend_quarterly']:
        print(f"  Quarterly Breakup  : {income['dividend_quarterly']}")
    # LTCG u/s 112A only printed if supplied; not chargeable to tax up to Rs 1.25 lakh
    if income['ltcg_112a']:
        print(f"LTCG u/s 112A      : ₹ {income['ltcg_112a']:,.2f} "
              f"(Sale ₹{income['ltcg_sale_consideration']:,.2f} - Cost ₹{income['ltcg_cost_of_acquisition']:,.2f})"
              + (" [Not taxable, within Rs 1.25L]" if income['ltcg_112a'] <= 125000 else ""))
    if income['family_pension_deduction_57iia']:
        print(f"Family Pension Ded.(57iia): ₹ {income['family_pension_deduction_57iia']:,.2f}")
    # Part C: itemized deductions only printed for heads that were actually used
    if any(income['deductions_c'].values()):
        print("  Deductions (Part C):")
        for label, amt in income['deductions_c'].items():
            if amt:
                print(f"    {label:8s}: ₹ {amt:,.2f}")
    print(f"Total Deductions   : ₹ {income['total_deductions']:,.2f}")
    # C3: Exempt income - reporting only, printed if supplied
    if income['exempt_income_amount']:
        print(f"Exempt Income (C3) : ₹ {income['exempt_income_amount']:,.2f} ({income['exempt_income_nature']}) [Not taxed]")
    print(f"Gross Income       : ₹ {income['gross_income']:,.2f}")
    print(f"Taxable Income     : ₹ {income['taxable_income']:,.2f}")
    
    print("\n---------- PART D: COMPUTATION OF TAX PAYABLE ----------")
    print(f"D1  Tax before Rebate        : ₹ {tax['d1_tax_before_rebate']:,.2f}")
    print(f"D2  Rebate u/s 87A           : ₹ {tax['d2_rebate_87a']:,.2f}")
    print(f"D3  Tax after Rebate         : ₹ {tax['d3_tax_after_rebate']:,.2f}")
    print(f"    Surcharge (if any)       : ₹ {tax['surcharge']:,.2f}")
    print(f"D4  Health & Edu Cess @4%    : ₹ {tax['d4_cess']:,.2f}")
    print(f"D5  Total Tax and Cess       : ₹ {tax['d5_total_tax_and_cess']:,.2f}")
    print(f"D6  Relief u/s 89            : ₹ {tax['d6_relief_89']:,.2f}")
    print(f"D7  Interest u/s 234A        : ₹ {tax['d7_interest_234a']:,.2f}")
    print(f"D8  Interest u/s 234B        : ₹ {tax['d8_interest_234b']:,.2f}")
    print(f"D9  Interest u/s 234C        : ₹ {tax['d9_interest_234c']:,.2f}")
    print(f"D10 Fee u/s 234F             : ₹ {tax['d10_fee_234f']:,.2f}")
    if tax['d10a_fee_revised_return']:
        print(f"D10(a) Fee Revised Return    : ₹ {tax['d10a_fee_revised_return']:,.2f}")
    print(f"D11 Total Tax, Fee & Interest: ₹ {tax['d11_total_tax_fee_interest']:,.2f}")
    print(f"D12 Total Taxes Paid         : ₹ {tax['d12_total_taxes_paid']:,.2f}")
    if tax['tcs_collected']:
        print(f"  D16 TCS Collected          : ₹ {tax['tcs_collected']:,.2f}")
    print(f"D13 Amount Payable           : ₹ {tax['d13_amount_payable']:,.2f}")
    print(f"D14 Refund                   : ₹ {tax['d14_refund']:,.2f}")
    
    print("\n---------- PART E: BANK ACCOUNT DETAILS ----------")
    for i, acc in enumerate(bank, 1):
        print(f"  A/c {i}: IFSC {acc['bank_ifsc']} | {acc['bank_name']} | {acc['bank_account_number']} "
              f"| {acc['account_type']} | Refund: {acc['select_for_refund']}")
    print("\n---------- SCHEDULE-IT: ADVANCE / SELF-ASSESSMENT TAX ----------")
    for i, row in enumerate(schedule_it, 1):
        print(f"  R{i}: BSR {row['bsr_code']} | {row['date_of_deposit']} | Challan {row['challan_serial_no']} "
              f"| ₹ {row['tax_paid_challan']:,.2f}")
    if schedule_tds:
        print("\n---------- SCHEDULE-TDS: TAX DEDUCTED AT SOURCE ----------")
        for i, row in enumerate(schedule_tds, 1):
            print(f"  T{i}: TAN {row['tan']} | {row['deductor_name']} | Sec {row['tds_section']} "
                  f"| Gross ₹ {row['gross_payment']:,.2f} | TDS ₹ {row['tax_deducted']:,.2f} "
                  f"| Claimed ₹ {row['tds_claimed']:,.2f}")
        print(f"  D15 Total TDS Claimed: ₹ {sum(r['tds_claimed'] for r in schedule_tds):,.2f}")
    if schedule_tcs:
        print("\n---------- SCHEDULE-TCS: TAX COLLECTED AT SOURCE ----------")
        for i, row in enumerate(schedule_tcs, 1):
            print(f"  C{i}: TAN {row['tcs_tan']} | {row['collector_name']} | Paid ₹ {row['amount_paid']:,.2f} "
                  f"| Collected ₹ {row['tax_collected']:,.2f} | Claimed ₹ {row['tcs_claimed']:,.2f}")
        print(f"  D16 Total TCS Collected: ₹ {sum(r['tcs_claimed'] for r in schedule_tcs):,.2f}")
    print("\n---------- FINAL RESULT ----------")
    
    if tax['d13_amount_payable'] > 0:
        print(f"Tax Payable        : ₹ {tax['d13_amount_payable']:,.2f}")
    else:
        print(f"Refund Amount      : ₹ {tax['d14_refund']:,.2f}")
    print("==========================================\n")
def process_itr(user_data):
    general_info = get_general_info(user_data)
    income = compute_income(user_data)
    tax = compute_tax(user_data, income["taxable_income"])
    bank = get_bank_details(user_data)
    schedule_it = get_schedule_it(user_data)
    schedule_tds = get_schedule_tds(user_data)
    schedule_tcs = get_schedule_tcs(user_data)
    print_report(general_info, income, tax, bank, schedule_it, schedule_tds, schedule_tcs)
if __name__ == "__main__":
    user_data = read_user_data()
    process_itr(user_data)
