def calculate_tax(x):
    if x <= 1200000:
        return 0   # Section 87A rebate

    tax = (
        (max(0, min(x, 800000) - 400000) * 0.05) +
        (max(0, min(x, 1200000) - 800000) * 0.10) +
        (max(0, min(x, 1600000) - 1200000) * 0.15) +
        (max(0, min(x, 2000000) - 1600000) * 0.20) +
        (max(0, min(x, 2400000) - 2000000) * 0.25) +
        (max(0, x - 2400000) * 0.30)
    )
    return tax


def main():

    # ==============================
    # PART A - GENERAL INFORMATION
    # ==============================
    assessment_year = "2026-27"
    pan = "ABCDE1234F"
    first_name = "Jeet"
    last_name = "maheshwari"
    date_of_birth = "10/05/2004"
    aadhaar_number = "123456789012"

    primary_mobile = "9876543210"
    secondary_mobile = "9999999999"

    primary_email = "jeet@gmail.com"
    secondary_email = "jeet123@gmail.com"


    tax_regime = "New Regime"
    

    # ==============================
    # PART B - SALARY
    # ==============================
    gross_salary = 14000000
    exempt_allowance = 20000
    net_salary = gross_salary - exempt_allowance

    # House Property
    house_rent = 120000
    municipal_tax = 5000
    home_loan_interest = 150000
    house_property_income = house_rent - municipal_tax - home_loan_interest

    # Other Sources
    savings_interest = 8000
    dividend_income = 12000

    # Deductions
    total_deductions = 75000

    gross_income = (
        net_salary
        + house_property_income
        + savings_interest
        + dividend_income
    )

    taxable_income = max(0, gross_income - total_deductions)
    taxable_income = round(taxable_income / 10) * 10

    income_tax = calculate_tax(taxable_income)
    
    # ==========================================
    # NEW CODE ADDED: SURCHARGE & MARGINAL RELIEF
    # ==========================================
    surcharge = 0
    if taxable_income > 20000000:
        surcharge = income_tax * 0.25
        tax_at_threshold = calculate_tax(20000000)
        surcharge_at_threshold = tax_at_threshold * 0.15
        max_tax = tax_at_threshold + surcharge_at_threshold + (taxable_income - 20000000)
        if (income_tax + surcharge) > max_tax:
            surcharge = max_tax - income_tax
            
    elif taxable_income > 10000000:
        surcharge = income_tax * 0.15
        tax_at_threshold = calculate_tax(10000000)
        surcharge_at_threshold = tax_at_threshold * 0.10
        max_tax = tax_at_threshold + surcharge_at_threshold + (taxable_income - 10000000)
        if (income_tax + surcharge) > max_tax:
            surcharge = max_tax - income_tax
            
    elif taxable_income > 5000000:
        surcharge = income_tax * 0.10
        tax_at_threshold = calculate_tax(5000000)
        max_tax = tax_at_threshold + (taxable_income - 5000000)
        if (income_tax + surcharge) > max_tax:
            surcharge = max_tax - income_tax
            
    surcharge = max(0, surcharge)
    # ==========================================

    cess = (income_tax + surcharge) * 0.04
    total_tax = income_tax + surcharge + cess

    tds_paid = 30000
    advance_tax = 10000
    total_tax_paid = tds_paid + advance_tax

    balance = total_tax - total_tax_paid

    print("ITR-1 SAHAJ")
    print("Assessment Year :", assessment_year)
    print("PAN :", pan)
    print("Name :", first_name, last_name)
    print("Date of Birth :", date_of_birth)
    print("Aadhaar :", aadhaar_number)
    print("Mobile :", primary_mobile)
    print("Email :", primary_email)
    print("Tax Regime :", tax_regime)
    

    print("\n---------- Income Details ----------")
    print("Gross Salary : ₹", gross_salary)
    print("Taxable Income : ₹", taxable_income)

    print("\n---------- Tax Details ----------")
    print("Income Tax : ₹", income_tax)
    print("Surcharge : ₹", surcharge) # New print statement
    print("Health & Education Cess : ₹", cess)
    print("Total Tax : ₹", total_tax)
    print("TDS Paid : ₹", tds_paid)
    print("Advance Tax Paid : ₹", advance_tax)
    print("Total Taxes Paid : ₹", total_tax_paid)

    print("\n---------- Final Result ----------")
    if balance > 0:
        print("Tax Payable : ₹", balance)
    else:
        print("Refund Amount : ₹", abs(balance))

main()
