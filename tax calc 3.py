def calculate_tax(x):
    if x <= 1200000:
        return 0   # 87A rebate

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
    gross_salary = 1400000

    # Exempt Allowance u/s 10
    exempt_allowance = 20000
    net_salary = gross_salary - exempt_allowance

    # House Property
    house_rent = 120000
    municipal_tax = 5000
    home_loan_interest = 150000   # if applicable

    house_property_income = (
        house_rent
        - municipal_tax
        - home_loan_interest
    )

    # Other Income
    savings_interest = 8000
    dividend_income = 12000

    # Deductions
    total_deductions = 75000

    # Taxes Already Paid
    tds_paid = 30000
    advance_tax = 10000   # if applicable

    # Gross Income
    gross_income = (
        net_salary
        + house_property_income
        + savings_interest
        + dividend_income
    )

    taxable_income = max(0, gross_income - total_deductions)

    # Section 288A (Round off taxable income to nearest ₹10)
    taxable_income = round(taxable_income / 10) * 10

    # Tax Calculation
    tax = calculate_tax(taxable_income)
    cess = tax * 0.04
    total_tax = tax + cess

    # Total Taxes Paid
    total_tax_paid = tds_paid + advance_tax

    # Final Balance
    balance = total_tax - total_tax_paid

    print("Gross Salary: ₹", gross_salary)
    print("Gross Income: ₹", gross_income)
    print("Taxable Income: ₹", taxable_income)
    print("Income Tax: ₹", tax)
    print("Total Tax: ₹", total_tax)
    print("TDS Paid: ₹", tds_paid)
    print("Advance Tax Paid: ₹", advance_tax)
    print("Total Taxes Paid: ₹", total_tax_paid)

    if balance > 0:
        print("Tax Payable: ₹", balance)
    else:
        print("Refund Amount: ₹", abs(balance))


main()
