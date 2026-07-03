def calculate_tax(x):
    if x <= 1200000:
        return 0   # rebate 87A

    tax = 0

    tax = tax + min(400000, max(0, x - 400000)) * 0.05
    tax = tax + min(400000, max(0, x - 800000)) * 0.10
    tax = tax + min(400000, max(0, x - 1200000)) * 0.15
    tax = tax + min(400000, max(0, x - 1600000)) * 0.20
    tax = tax + min(400000, max(0, x - 2000000)) * 0.25
    tax = tax + max(0, x - 2400000) * 0.30

    return tax


def main():
    gross_salary = 1210000
    standard_deduction = 75000
    tds_paid = 40000

    total_deductions = standard_deduction
    taxable_income = max(0, gross_salary - total_deductions)

    tax = calculate_tax(taxable_income)
    cess = tax * 0.04
    total_tax = tax + cess
    balance = total_tax - tds_paid

    print("Gross Salary: ₹", gross_salary)
    print("Total Deductions: ₹", total_deductions)
    print("Taxable Income: ₹", taxable_income)
    print("Tax: ₹", tax)
    print("Cess: ₹", cess)
    print("Total Tax: ₹", total_tax)

    if balance > 0:
        print("Tax need to be paid: ₹", balance)
    else:
        print("Refund: ₹", abs(balance))


main()
