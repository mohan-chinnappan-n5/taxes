import streamlit as st

# author: Mohan Chinnappan
# ---------------------------


# Streamlit app title and layout settings
st.set_page_config(page_title="Simple Income Tax Calculator", layout="centered")
st.title("Simple Income Tax Calculator")

# Initialize session state to store input values if not already initialized
if "income" not in st.session_state:
    st.session_state["income"] = 0.0
if "filing_status" not in st.session_state:
    st.session_state["filing_status"] = "Single"
if "deductions" not in st.session_state:
    st.session_state["deductions"] = 0.0
if "credits" not in st.session_state:
    st.session_state["credits"] = 0.0

# Sidebar - User Guide and Info
st.sidebar.header("Options")
section = st.sidebar.radio("Go to", ("Calculator", "About", "Tax Guide"))

# Calculator Section
if section == "Calculator":
    st.header("Enter Your Income Tax Details")

    # Input fields for income, filing status, deductions, and credits, using session state to remember values
    st.session_state["income"] = st.number_input("Annual Income", min_value=0.0, step=1000.0, value=st.session_state["income"])
    st.session_state["filing_status"] = st.selectbox("Filing Status", ("Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"), index=["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"].index(st.session_state["filing_status"]))
    st.session_state["deductions"] = st.number_input("Deductions", min_value=0.0, step=500.0, value=st.session_state["deductions"])
    st.session_state["credits"] = st.number_input("Credits", min_value=0.0, step=100.0, value=st.session_state["credits"])

    # Calculation
    if st.button("Calculate Tax"):
        # Standard deductions based on filing status
        standard_deductions = {
            "Single": 12950,
            "Married Filing Jointly": 25900,
            "Married Filing Separately": 12950,
            "Head of Household": 19400
        }

        adjusted_gross_income = max(st.session_state["income"] - (st.session_state["deductions"] + standard_deductions[st.session_state["filing_status"]]), 0)

        # Federal tax brackets
        tax_brackets = [
            { "rate": 0.10, "income": 10275 },
            { "rate": 0.12, "income": 41775 },
            { "rate": 0.22, "income": 89075 },
            { "rate": 0.24, "income": 170050 },
            { "rate": 0.32, "income": 215950 },
            { "rate": 0.35, "income": 539900 },
            { "rate": 0.37, "income": float("inf") }
        ]

        # Tax calculation
        tax_owed = 0.0
        remaining_income = adjusted_gross_income

        for i, bracket in enumerate(tax_brackets):
            if remaining_income > 0:
                prev_income = tax_brackets[i - 1]["income"] if i > 0 else 0
                taxable_at_bracket = min(remaining_income, bracket["income"] - prev_income)
                tax_owed += taxable_at_bracket * bracket["rate"]
                remaining_income -= taxable_at_bracket

        # Adjust tax owed by credits
        final_tax_owed = max(tax_owed - st.session_state["credits"], 0)

        # Display the result
        st.subheader("Tax Calculation Result")
        st.write(f"**Adjusted Gross Income:** ${adjusted_gross_income:,.2f}")
        st.write(f"**Tax Owed Before Credits:** ${tax_owed:,.2f}")
        st.write(f"**Tax Owed After Credits:** ${final_tax_owed:,.2f}")

# About Section
elif section == "About":
    st.header("About This Calculator")
    st.write("""
    This tax calculator is designed to give you an estimate of the amount of income tax you owe based on your annual income,
    filing status, deductions, and credits. It uses basic federal tax brackets and standard deductions according to U.S. tax laws.
    """)

# Tax Guide Section (using Markdown)
 # Tax Guide Section (using Markdown)
elif section == "Tax Guide":
    st.header("Tax Guide")
    st.write("""
    ## Filing Status
    - **Single:** Individuals who are not married, divorced, or legally separated.
    - **Married Filing Jointly:** Married couples who choose to file a joint tax return.
    - **Married Filing Separately:** Married individuals who choose to file separate returns. This can be beneficial in certain cases but may result in loss of certain credits and deductions.
    - **Head of Household:** Unmarried individuals who pay more than half the cost of keeping up a home for themselves and a qualifying person.

    ## Standard Deductions
    The IRS allows taxpayers to reduce their taxable income by claiming a standard deduction. The standard deduction amount varies by filing status:
    
    - **Single:** $12,950
    - **Married Filing Jointly:** $25,900
    - **Married Filing Separately:** $12,950
    - **Head of Household:** $19,400

    You may also claim **itemized deductions** if they exceed the standard deduction. Common itemized deductions include:
    - **Mortgage Interest:** Interest paid on a home mortgage.
    - **Medical and Dental Expenses:** Expenses that exceed 7.5% of your Adjusted Gross Income (AGI).
    - **State and Local Taxes (SALT):** Includes state and local income, sales, and property taxes (limited to $10,000).
    - **Charitable Contributions:** Donations to qualified charities, limited to a certain percentage of your AGI.

    ## Tax Credits
    Tax credits directly reduce the amount of tax you owe, making them generally more valuable than deductions. Here are some commonly available tax credits:

    - **Child Tax Credit:** Up to $2,000 per qualifying child under 17. Part of this credit may be refundable as the Additional Child Tax Credit.
    - **Earned Income Tax Credit (EITC):** A refundable credit for low-to-moderate income working individuals and families, particularly those with children.
    - **American Opportunity Credit (AOC):** A credit of up to $2,500 per eligible student for qualified education expenses during the first four years of higher education.
    - **Lifetime Learning Credit (LLC):** Up to $2,000 per tax return for post-secondary education and courses to acquire or improve job skills, with no limit on the number of years you can claim it.
    - **Retirement Savings Contributions Credit:** A credit for low- and moderate-income individuals who contribute to a retirement plan like an IRA or 401(k).

    ### Important Notes
    - **Deductions vs. Credits:** Deductions reduce your taxable income, while credits directly reduce the tax you owe. Credits are typically more advantageous since they lower the tax dollar-for-dollar.
    - **Refundable Credits:** Some credits, like the Earned Income Tax Credit and Additional Child Tax Credit, are refundable, meaning they can result in a tax refund even if you owe no tax.
    - **Non-Refundable Credits:** Other credits, such as the Lifetime Learning Credit, can reduce your tax to zero but cannot result in a refund.

    For more details, visit the [IRS website](https://www.irs.gov/) or consult a tax professional.
    """)