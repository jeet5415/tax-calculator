monthly_salary = float(input("Enter monthly salary : "))

annual_income = monthly_salary * 12

tax = 0

if annual_income <= 400000:
    tax = 0

elif annual_income <= 800000:
    tax = (annual_income - 400000) * 0.05

elif annual_income <= 1200000:
    tax = 20000 + (annual_income - 800000) * 0.10

elif annual_income <= 1600000:
    tax = 60000 + (annual_income - 1200000) * 0.15

elif annual_income <= 2000000:
    tax = 120000 + (annual_income - 1600000) * 0.20

elif annual_income <= 2400000:
    tax = 200000 + (annual_income - 2000000) * 0.25

else:
    tax = 300000 + (annual_income - 2400000) * 0.30

monthly_tax = tax / 12
monthly_take_home = monthly_salary - monthly_tax


print("Annual Income:", annual_income)
print("Annual Tax: ", tax)
print("Monthly Tax: ", monthly_tax)
print("Monthly Take Home: ",monthly_take_home)
