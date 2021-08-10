#----------------------------------Setup-----------------------------------------#
# Import the necessary modules
import numpy as np
import pandas as pd
import datetime as dt
from dateutil import parser

# Import the data files and assign them to DataFrames
broker_df=pd.read_csv("Data/broker.csv")
lob_df=pd.read_csv("Data/line_of_business.csv")
policy_item_df=pd.read_csv("Data/policy_item.csv")
policy_df=pd.read_csv("Data/policy.csv")

# Define a function to parse the various date formats (For use in answer 4)
def clean_date(date):
  """Function to clean and standardize the input date. Output is in the format YYYY-MM-DD."""
  try:
    d=parser.parse(date, fuzzy=True, yearfirst=True)
    return d.date()

  except (OverflowError, ParserError ) as e:
    print("Error: {} dealing with date {}".format(e, date))

#-------------------------------- Answers -------------------------------------#
#------------------------Clean the Data (Answer 1)-----------------------------#
policy_item_df.fillna(0, inplace=True)
# For null dates ascribe a completely outlying date. Better imputation possible, but would depend on use. 
policy_df['policy_effective_date'].fillna('1900-01-31', inplace=True)


#---------------Total policy insured including VAT (Answer 2)------------------#
policy_item_df['total_policy_insured_incl_vat']=policy_item_df['policy_insured_value_excl_vat']+policy_item_df['policy_insured_value_vat']
print("\n\n\nAnswer 2: Total insured policy incl. vat column added:")
print(policy_item_df)

#-------------------Standardize Date formats (Answer 4)------------------------#
# parser.parse needs to recieve string so cast the column as such. 
# Unsure of how to deal with completely ambiguous dates, ie: 20-04-21, assumed year is first. 
policy_df['policy_effective_date']=policy_df['policy_effective_date'].astype(str).apply(clean_date)
print("\n\n\nAnswer 4: Dates standardized")
print(policy_df)

#---------Total Policy Insured Per Broker (Incl. VAT) (Answer 3)---------------#
pol_comb_df=policy_item_df.set_index('policy_id').join(policy_df.set_index('policy_id'), on='policy_id')
total_by_broker_df=pol_comb_df[['total_policy_insured_incl_vat','policy_broker_id']].groupby(['policy_broker_id']).sum()
highest_broker=total_by_broker_df[total_by_broker_df['total_policy_insured_incl_vat']==total_by_broker_df['total_policy_insured_incl_vat'].max()]
print("\n\n\nAnswer 3: Total policy by broker")
print(total_by_broker_df)


#-------------Policies with the most policy items (Answer 5)-------------------#
# Create new Dataframe, grouping by policy ID and aggregating with count
pol_count_df=pol_comb_df.groupby(['policy_id']).agg(num_policies=('policy_item_id', 'count')).sort_values(by='num_policies', ascending=False)
hi_pol_count_df=pol_count_df[pol_count_df['num_policies']==pol_count_df['num_policies'].max()]
print("\n\n\nAnswer 5: Policies with most items:")
print(hi_pol_count_df)


#--------------------Most profitable broker (Answer 6)-------------------------#
# Assumption made here that the most profitable broker is the broker with the highest broker fee total. 
temp_df=pol_comb_df.merge(broker_df, left_on='policy_broker_id', right_on='broker_id')
broker_profits_df=temp_df[['broker_name','broker_fee_excl_vat']].groupby('broker_name').sum()
broker_prof_max=broker_profits_df[broker_profits_df['broker_fee_excl_vat']==broker_profits_df['broker_fee_excl_vat'].max()]
print("\n\n\nAnswer 6: Most profitable broker:")
print(broker_prof_max)


#-----------------Most profitable Line of Business (Answer 7)------------------#
profit_lob_df=pol_comb_df[['broker_fee_excl_vat', 'line_of_business_id']].groupby('line_of_business_id').sum()
temp2=profit_lob_df.merge(lob_df, on='line_of_business_id')
most_prof_lob_df=temp2[temp2['broker_fee_excl_vat']==temp2['broker_fee_excl_vat'].max()]
print("\n\n\nAnswer 7: Most profitable line of business:")
print(most_prof_lob_df)


#-------------Highest broker profit per line of business (Answer 8)------------#
t=pol_comb_df[['policy_broker_id', 'line_of_business_id', 'broker_fee_excl_vat']].groupby(by=['policy_broker_id', 'line_of_business_id']).sum()
t.reset_index(inplace=True)
tp=t.pivot(index='policy_broker_id', columns='line_of_business_id', values='broker_fee_excl_vat')
print("\n\n\nAnswer 8: Most profitable broker per line of business:")
print(tp)


#----Effective date with the largest policy insured including VAT (Answer 9)----#
# By Broker and Date
broker_by_date_df=pol_comb_df.set_index(['policy_effective_date', 'policy_broker_id'])[['total_policy_insured_incl_vat']].groupby(['policy_effective_date','policy_broker_id']).sum()
broker_by_date_df.loc[broker_by_date_df.idxmax()]
# By Date only
date_total_df=pol_comb_df.reset_index()[['policy_effective_date', 'total_policy_insured_incl_vat']].groupby(['policy_effective_date']).sum()
date_total_hi=date_total_df.loc[date_total_df.idxmax()]
print("\n\n\nAnswer 9: Effective date with the largest effective policy incl. VAT")
print(date_total_hi)
