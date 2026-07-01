def calculate_tax(taxable_income):
    tax = 0

    if taxable_income <= 400000:
        tax = 0

    elif taxable_income <= 800000:
        tax = (taxable_income - 400000) * 0.05

    elif taxable_income <= 1200000:
        tax = 20000 + (taxable_income - 800000) * 0.10

    elif taxable_income <= 1600000:
        tax = 60000 + (taxable_income - 1200000) * 0.15

    elif taxable_income <= 2000000:
        tax = 120000 + (taxable_income - 1600000) * 0.20

    elif taxable_income <= 2400000:
        tax = 200000 + (taxable_income - 2000000) * 0.25

    else:
        tax = 300000 + (taxable_income - 2400000) * 0.30

    return tax


def main():
    gross_salary = 1300000
    standard_deduction = 40000
    deduction_80c = 75000
    tds_paid =40000

    total_deductions = standard_deduction + deduction_80c
    taxable_income = gross_salary - total_deductions

    if taxable_income < 0:
        taxable_income = 0

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


main()
