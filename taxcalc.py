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
def read_user_data():
    file = open("user_data.txt", "r")
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
        if value.isdigit():
            value = int(value)
        user_data[key] = value
    file.close()
    return user_data
# PART A - GENERAL NFORMATION
# ==============================
 
def get_general_info(user_data):
   
    first_name = user_data.get("first_name", "Jeet")
    middle_name = user_data.get("middle_name", "")
    last_name = user_data.get("last_name", "Maheshwari")
    full_name = " ".join(part for part in [first_name, middle_name, last_name] if part)
 
    opting_new_regime = user_data.get("opting_new_regime", "Yes")
    tax_regime = "New Regime" if str(opting_new_regime).strip().lower() == "yes" else "Old Regime"
 
    return {
        "assessment_year": user_data.get("assessment_year", "2026-27"),
        "pan": user_data.get("pan", "ABCDE1234F"),
        "full_name": full_name,
        "date_of_birth": user_data.get("date_of_birth", "10/05/2004"),
        "aadhaar_number": "[Aadhaar Redacted]",
        "mobile_no": user_data.get("mobile_no", ""),
        "email": user_data.get("email", ""),
        "flat_door_block": user_data.get("flat_door_block", ""),
        "premises_name": user_data.get("premises_name", ""),
        "road_street": user_data.get("road_street", ""),
        "area_locality": user_data.get("area_locality", ""),
        "town_city_district": user_data.get("town_city_district", ""),
        "state": user_data.get("state", ""),
        "country": user_data.get("country", "India"),
        "pin_code": user_data.get("pin_code", ""),
        "filed_under_section": user_data.get("filed_under_section", "139(1)-On or before due date"),
        "nature_of_employment": user_data.get("nature_of_employment", "Not Applicable"),
        "opting_new_regime": opting_new_regime,
        "tax_regime": tax_regime,
    }
# PART B - INCOME
# ==============================
 
def compute_income(user_data):
    """Computes salary, house property, other-sources income and taxable income (Part B)."""
 
    gross_salary = user_data.get("gross_salary", 0)
    exempt_allowance = user_data.get("exempt_allowance", 0)
    net_salary = gross_salary - exempt_allowance
 
    # House Property
    house_rent = user_data.get("house_rent", 0)
    municipal_tax = user_data.get("municipal_tax", 0)
    home_loan_interest = user_data.get("home_loan_interest", 0)
 
    house_property_income = (
        house_rent
        - municipal_tax
        - home_loan_interest
    )
 
    # Other Sources
    savings_interest = user_data.get("savings_interest", 0)
    dividend_income = user_data.get("dividend_income", 0)
 
    # Deductions
    total_deductions = user_data.get("total_deductions", 0)
 
    gross_income = (
        net_salary
        + house_property_income
        + savings_interest
        + dividend_income
    )
 
    taxable_income = gross_income - total_deductions
    taxable_income = max(0, taxable_income)
    taxable_income = round(taxable_income / 10) * 10
 
    return {
        "gross_salary": gross_salary,
        "net_salary": net_salary,
        "house_property_income": house_property_income,
        "savings_interest": savings_interest,
        "dividend_income": dividend_income,
        "total_deductions": total_deductions,
        "gross_income": gross_income,
        "taxable_income": taxable_income,
    }
 
# ==============================
# PART D - COMPUTATION OF TAX PAYABLE
# ==============================
 
def compute_surcharge(taxable_income, tax_after_rebate):
    """Marginal-relief-aware surcharge calculation for high incomes."""
 
    surcharge = 0
 
    if taxable_income > 20000000:
        surcharge = tax_after_rebate * 0.25
        tax_at_threshold = calculate_tax(20000000)
        surcharge_at_threshold = tax_at_threshold * 0.15
        max_tax = (
            tax_at_threshold
            + surcharge_at_threshold
            + (taxable_income - 20000000)
        )
        if tax_after_rebate + surcharge > max_tax:
            surcharge = max_tax - tax_after_rebate
 
    elif taxable_income > 10000000:
        surcharge = tax_after_rebate * 0.15
        tax_at_threshold = calculate_tax(10000000)
        surcharge_at_threshold = tax_at_threshold * 0.10
        max_tax = (
            tax_at_threshold
            + surcharge_at_threshold
            + (taxable_income - 10000000)
        )
        if tax_after_rebate + surcharge > max_tax:
            surcharge = max_tax - tax_after_rebate
 
    elif taxable_income > 5000000:
        surcharge = tax_after_rebate * 0.10
        tax_at_threshold = calculate_tax(5000000)
        max_tax = (
            tax_at_threshold
            + (taxable_income - 5000000)
        )
        if tax_after_rebate + surcharge > max_tax:
            surcharge = max_tax - tax_after_rebate
 
    return max(0, surcharge)
 
 
def compute_tax(user_data, taxable_income):
    """Runs the full D1-D14 tax computation for a given taxable income (Part D)."""
 
    # D1: Tax payable on total income (before rebate)
    d1_tax_before_rebate = calculate_tax(taxable_income)
 
    # D2: Rebate u/s 87A (full rebate if taxable income <= 12,00,000)
    d2_rebate_87a = d1_tax_before_rebate if taxable_income <= 1200000 else 0
 
    # D3: Tax after Rebate
    d3_tax_after_rebate = d1_tax_before_rebate - d2_rebate_87a
 
    # Surcharge (ITR-1 itself is capped at Rs 50 lakh total income,
    # kept here for completeness)
    surcharge = compute_surcharge(taxable_income, d3_tax_after_rebate)
 
    # D4: Health and Education Cess @ 4% on (D3 + Surcharge)
    d4_cess = (d3_tax_after_rebate + surcharge) * 0.04
 
    # D5: Total Tax and Cess
    d5_total_tax_and_cess = d3_tax_after_rebate + surcharge + d4_cess
 
    # D6: Relief u/s 89
    d6_relief_89 = user_data.get("relief_89", 0)
 
    # D7, D8, D9: Interest u/s 234A, 234B, 234C
    d7_interest_234a = user_data.get("interest_234a", 0)
    d8_interest_234b = user_data.get("interest_234b", 0)
    d9_interest_234c = user_data.get("interest_234c", 0)
 
    # D10: Fee u/s 234F (late filing fee)
    d10_fee_234f = user_data.get("fee_234f", 0)
 
    # D11: Total Tax, Fee and Interest (D5 + D7 + D8 + D9 + D10 - D6)
    d11_total_tax_fee_interest = (
        d5_total_tax_and_cess
        + d7_interest_234a
        + d8_interest_234b
        + d9_interest_234c
        + d10_fee_234f
        - d6_relief_89
    )
    # D12: Total Taxes Paid
    tds_paid = user_data.get("tds_paid", 0)
    advance_tax = user_data.get("advance_tax", 0)
    self_assessment_tax = user_data.get("self_assessment_tax", 0)
    d12_total_taxes_paid = tds_paid + advance_tax + self_assessment_tax
 
    # D13 / D14: Amount Payable / Refund
    d13_amount_payable = 0
    d14_refund = 0
    if d11_total_tax_fee_interest > d12_total_taxes_paid:
        d13_amount_payable = d11_total_tax_fee_interest - d12_total_taxes_paid
    else:
        d14_refund = d12_total_taxes_paid - d11_total_tax_fee_interest
 
    return {
        "d1_tax_before_rebate": d1_tax_before_rebate,
        "d2_rebate_87a": d2_rebate_87a,
        "d3_tax_after_rebate": d3_tax_after_rebate,
        "surcharge": surcharge,
        "d4_cess": d4_cess,
        "d5_total_tax_and_cess": d5_total_tax_and_cess,
        "d6_relief_89": d6_relief_89,
        "d7_interest_234a": d7_interest_234a,
        "d8_interest_234b": d8_interest_234b,
        "d9_interest_234c": d9_interest_234c,
        "d10_fee_234f": d10_fee_234f,
        "d11_total_tax_fee_interest": d11_total_tax_fee_interest,
        "d12_total_taxes_paid": d12_total_taxes_paid,
        "d13_amount_payable": d13_amount_payable,
        "d14_refund": d14_refund,
    }
# ==============================
# PART E - BANK ACCOUNT DETAILS
# ==============================
 
def get_bank_details(user_data):
    return {
        "bank_ifsc": user_data.get("bank_ifsc", ""),
        "bank_name": user_data.get("bank_name", ""),
        "bank_account_number": user_data.get("bank_account_number", ""),
        "select_for_refund": user_data.get("select_for_refund", "Yes"),
    }
# ==============================
# SCHEDULE-IT - ADVANCE TAX / SELF-ASSESSMENT TAX
# ==============================
 
def get_schedule_it(user_data):
    return {
        "bsr_code": user_data.get("bsr_code", ""),
        "date_of_deposit": user_data.get("date_of_deposit", ""),
        "challan_serial_no": user_data.get("challan_serial_no", ""),
        "tax_paid_challan": user_data.get("tax_paid_challan", 0),
    }
# ==============================
# OUTPUT
# ==============================
 
def print_report(general_info, income, tax, bank, schedule_it):
 
    print(f"\nITR-1 SAHAJ | {general_info['assessment_year']} | {general_info['tax_regime']}")
    print("\n---------- PART A: GENERAL INFORMATION ----------")
    print(f"Name               : {general_info['full_name']}")
    print(f"PAN                : {general_info['pan']}")
    print(f"Aadhaar            : {general_info['aadhaar_number']}")
    print(f"DOB                : {general_info['date_of_birth']}")
    print(f"Mobile No.         : {general_info['mobile_no']}")
    print(f"E-mail             : {general_info['email']}")
    print(f"Address            : {general_info['flat_door_block']}, {general_info['premises_name']}, "
          f"{general_info['road_street']}, {general_info['area_locality']}, "
          f"{general_info['town_city_district']}, {general_info['state']}, "
          f"{general_info['country']} - {general_info['pin_code']}")
    print(f"Filed u/s          : {general_info['filed_under_section']}")
    print(f"Nature of Employ.  : {general_info['nature_of_employment']}")
    print(f"Opting New Regime  : {general_info['opting_new_regime']} (u/s 115BAC)")
 
    print("\n---------- PART B: INCOME DETAILS ----------")
    print(f"Gross Salary       : ₹ {income['gross_salary']:,.2f}")
    print(f"Net Salary         : ₹ {income['net_salary']:,.2f}")
    print(f"House Property Inc : ₹ {income['house_property_income']:,.2f}")
    print(f"Savings Interest   : ₹ {income['savings_interest']:,.2f}")
    print(f"Dividend Income    : ₹ {income['dividend_income']:,.2f}")
    print(f"Total Deductions   : ₹ {income['total_deductions']:,.2f}")
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
    print(f"D11 Total Tax, Fee & Interest: ₹ {tax['d11_total_tax_fee_interest']:,.2f}")
    print(f"D12 Total Taxes Paid         : ₹ {tax['d12_total_taxes_paid']:,.2f}")
    print(f"D13 Amount Payable           : ₹ {tax['d13_amount_payable']:,.2f}")
    print(f"D14 Refund                   : ₹ {tax['d14_refund']:,.2f}")
    
    print("\n---------- PART E: BANK ACCOUNT DETAILS ----------")
    print(f"IFSC Code          : {bank['bank_ifsc']}")
    print(f"Bank Name          : {bank['bank_name']}")
    print(f"Account Number     : {bank['bank_account_number']}")
    print(f"Selected for Refund: {bank['select_for_refund']}")
    print("\n---------- SCHEDULE-IT: ADVANCE / SELF-ASSESSMENT TAX ----------")
    print(f"BSR Code           : {schedule_it['bsr_code']}")
    print(f"Date of Deposit    : {schedule_it['date_of_deposit']}")
    print(f"Challan Serial No. : {schedule_it['challan_serial_no']}")
    print(f"Tax Paid (Challan) : ₹ {schedule_it['tax_paid_challan']:,.2f}")
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
    print_report(general_info, income, tax, bank, schedule_it)
if __name__ == "__main__":
    user_data = read_user_data()
     process_itr(user_data)
