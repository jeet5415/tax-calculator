def calculate_tax(x):
    if x <= 1200000:
        return 0

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

        if line == "":
            continue

        key, value = line.split("=", 1)

        if value.isdigit():
            value = int(value)

        user_data[key] = value

    file.close()

    return user_data


def process_itr(user_data):

    # ==============================
    # PART A - GENERAL INFORMATION
    # ==============================

    assessment_year = user_data.get("assessment_year", "2026-27")
    pan = user_data.get("pan", "ABCDE1234F")
    first_name = user_data.get("first_name", "Jeet")
    last_name = user_data.get("last_name", "Maheshwari")
    date_of_birth = user_data.get("date_of_birth", "10/05/2004")
    aadhaar_number = "[Aadhaar Redacted]"
    tax_regime = user_data.get("tax_regime", "New Regime")

    # ==============================
    # PART B - INCOME
    # ==============================

    gross_salary = user_data.get("gross_salary", 0)
    exempt_allowance = 20000
    net_salary = gross_salary - exempt_allowance

    house_rent = user_data.get("house_rent", 120000)
    municipal_tax = user_data.get("municipal_tax", 5000)
    home_loan_interest = user_data.get("home_loan_interest", 150000)

    house_property_income = (
        house_rent
        - municipal_tax
        - home_loan_interest
    )

    savings_interest = user_data.get("savings_interest", 8000)
    dividend_income = user_data.get("dividend_income", 12000)

    total_deductions = user_data.get("total_deductions", 75000)

    gross_income = (
        net_salary
        + house_property_income
        + savings_interest
        + dividend_income
    )

    taxable_income = max(0, gross_income - total_deductions)
    taxable_income = round(taxable_income / 10) * 10

    income_tax = calculate_tax(taxable_income)

    # ==============================
    # SURCHARGE
    # ==============================

    surcharge = 0

    if taxable_income > 20000000:

        surcharge = income_tax * 0.25

        tax_at_threshold = calculate_tax(20000000)
        surcharge_at_threshold = tax_at_threshold * 0.15

        max_tax = (
            tax_at_threshold
            + surcharge_at_threshold
            + (taxable_income - 20000000)
        )

        if income_tax + surcharge > max_tax:
            surcharge = max_tax - income_tax

    elif taxable_income > 10000000:

        surcharge = income_tax * 0.15

        tax_at_threshold = calculate_tax(10000000)
        surcharge_at_threshold = tax_at_threshold * 0.10

        max_tax = (
            tax_at_threshold
            + surcharge_at_threshold
            + (taxable_income - 10000000)
        )

        if income_tax + surcharge > max_tax:
            surcharge = max_tax - income_tax

    elif taxable_income > 5000000:

        surcharge = income_tax * 0.10

        tax_at_threshold = calculate_tax(5000000)

        max_tax = (
            tax_at_threshold
            + (taxable_income - 5000000)
        )

        if income_tax + surcharge > max_tax:
            surcharge = max_tax - income_tax

    surcharge = max(0, surcharge)

    # ==============================
    # FINAL TAX
    # ==============================

    cess = (income_tax + surcharge) * 0.04

    total_tax = income_tax + surcharge + cess

    tds_paid = user_data.get("tds_paid", 0)
    advance_tax = user_data.get("advance_tax", 0)

    total_tax_paid = tds_paid + advance_tax

    balance = total_tax - total_tax_paid

    # ==============================
    # OUTPUT
    # ==============================

    print(f"\nITR-1 SAHAJ | {assessment_year} | {tax_regime}")
    print(f"Name : {first_name} {last_name}")
    print(f"PAN : {pan}")
    print(f"Aadhaar : {aadhaar_number}")
    print(f"DOB : {date_of_birth}")

    print("\n---------- Income & Tax Details ----------")
    print(f"Gross Salary       : ₹ {gross_salary:,.2f}")
    print(f"Taxable Income     : ₹ {taxable_income:,.2f}")
    print(f"Income Tax         : ₹ {income_tax:,.2f}")
    print(f"Surcharge          : ₹ {surcharge:,.2f}")
    print(f"Health/Edu Cess    : ₹ {cess:,.2f}")
    print(f"Total Tax Computed : ₹ {total_tax:,.2f}")
    print(f"Total Taxes Paid   : ₹ {total_tax_paid:,.2f}")

    print("\n---------- Final Result ----------")

    if balance > 0:
        print(f"Tax Payable        : ₹ {balance:,.2f}")
    else:
        print(f"Refund Amount      : ₹ {abs(balance):,.2f}")

    print("==========================================")


if __name__ == "__main__":

    user_data = read_user_data()

    process_itr(user_data)
