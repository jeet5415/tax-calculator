basic_salary = float(input("Enter monthly basic salary: ₹"))
hra = float(input("Enter monthly HRA: ₹"))
special_allowance = float(input("Enter monthly special allowance: ₹"))
bonus = float(input("Enter yearly bonus: ₹"))
pf = float(input("Enter yearly PF contribution: ₹"))
deduction_80c = float(input("Enter total 80C investments: ₹"))
tds = float(input("Enter yearly tax already deducted (TDS): ₹"))

if deduction_80c > 150000:
    deduction_80c = 150000

annual_basic = basic_salary * 12
annual_hra = hra * 12
annual_special = special_allowance * 12

gross_income = annual_basic + annual_hra + annual_special + bonus

standard_deduction = 75000
total_deductions = (
    standard_deduction
    + pf
    + deduction_80c
)

taxable_income = gross_income - total_deductions

if taxable_income < 0:
    taxable_income = 0


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

remaining_tax = tax - tds

print("Gross Income: ₹", gross_income)
print("Taxable Income: ₹", taxable_income)
print("Final Tax: ₹", tax)
print("TDS Paid: ₹", tds)
print(" Tax Payable: ₹", remaining_tax)
