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
    gross_salary = 1400000
    savings_interest = 8000
    dividend_income = 12000
    standard_deduction = 75000
    tds_paid = 30000


    gross_income = gross_salary + savings_interest + dividend_income
    total_deductions = standard_deduction
    taxable_income = max(0, gross_income - total_deductions)

    # Section 288A (Round off taxable income to nearest ₹10)
    taxable_income = round(taxable_income / 10) * 10

    # Tax Calculation
    tax = calculate_tax(taxable_income)
    cess = tax * 0.04
    total_tax = tax + cess

    # Final Balance
    balance = total_tax - tds_paid

    print("Gross Salary: ₹", gross_salary)
    print("Gross Income: ₹", gross_income)
    print("Total Deductions: ₹", total_deductions)
    print("Taxable Income (Rounded u/s 288A): ₹", taxable_income)
    print("Income Tax: ₹", tax)
    print("Health & Education Cess (4%): ₹", cess)
    print("Total Tax: ₹", total_tax)

    if balance > 0:
        print("Tax Payable: ₹", balance)
    else:
        print("Refund Amount: ₹", abs(balance))


main()
