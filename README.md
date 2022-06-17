# Inscorep Data Engineering Case Study

## Data

In the data folder there are four files which was sent from an Insurance Underwriting Management Agency (UMA). The files were:

- A broker file
- A line of business file
- A policy file
- A policy Item file

The policy file contains a policy per client. Each policy can have multiple policy items underwritten to them such as a property, motor and personal. All the policy items are in the policy item file. The broker file contains a list of all the brokers. The line of business file contains a list of all the line of business of insurance being underwritten such as property, motor, personal, medical, etc.

### Questions

1. Fill null values with appropriate substitutes. Example policy_insured_value_excl_vat filled with 0.
2. What is the total policy insured including vat?
3. What is the total policy insured including vat per broker?
4. Fix the policy_effective_date to have a constant format (Use dateutil package)
5. Which policies have the most policy items (Join & Filter)
6. Which broker made the most profit? (Join & GroupBy)
7. Which Line of Business is the most profitable? (Join & GroupBy)
8. Which broker made the most money per line of business? (Join & Pivot)
9. Which effective date had the largest effective policy insured including vat?

Please create an answer.py file to answer the above questions.
