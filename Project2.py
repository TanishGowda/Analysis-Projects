import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up working directory
import os

os.chdir(r"C:\Users\tanis\OneDrive\Desktop\Ecommerce Project")
print(os.getcwd())

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# =============================================================================
# Loading the datasets
# =============================================================================

order_data = pd.read_excel('C:/Users/tanis/OneDrive/Desktop/Ecommerce Project/orders.xlsx')
payments_data = pd.read_excel('C:/Users/tanis/OneDrive/Desktop/Ecommerce Project/order_payment.xlsx')
customers_data = pd.read_excel('C:/Users/tanis/OneDrive/Desktop/Ecommerce Project/customers.xlsx')

# =============================================================================
# Describing the data
# =============================================================================

order_data.info()
order_data.describe()

payments_data.info()
payments_data.describe()

customers_data.info()
customers_data.describe()

# =============================================================================
# Dealing with missing values (Cleaning the data)
# =============================================================================

order_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

order_data2 = order_data.fillna('N/A')
order_data2.isnull().sum()

payments_data2 = payments_data.dropna(subset=['payment_value'])
payments_data2.isnull().sum()

# =============================================================================
# Dealing with the duplicates
# =============================================================================

# Checking the duplicates

order_data2.duplicated().sum()
payments_data2.duplicated().sum()
customers_data.duplicated().sum()

# Removing the duplicate rows

order_data2 = order_data2.drop_duplicates()
payments_data2 = payments_data2.drop_duplicates()

order_data2.duplicated().sum()
payments_data2.duplicated().sum()

# =============================================================================
# Filtering the data
# =============================================================================

#dataframe of all the orders in invoice

invoiced_order_data = order_data[order_data['order_status'] == 'invoiced']

#resetting the index

invoiced_order_data = invoiced_order_data.reset_index(drop=True)

#dataframe of all the payments made using a credit card and value>1000

top_credit_payments = payments_data2[(payments_data2['payment_type'] == 'credit_card') & (payments_data2['payment_value'] > 1000)] 

#dataframe of all the customers of the state SP

SP_customer_data = customers_data[customers_data['customer_state'] == 'SP']
SP_customer_data.count()

country_wise_dis = SP_customer_data.groupby('customer_city')['customer_id'].count()
print(country_wise_dis)

# =============================================================================
# Joining the the three files
# =============================================================================

# joining orders and customers data
merged_data = pd.merge(order_data2, customers_data, on='customer_id')
# joining the payments data to the above joined dataframe
joined_data = pd.merge(merged_data, payments_data2, on='order_id')

# =============================================================================
# Visualizing the data
# =============================================================================

# creating new required columnn info

joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['date_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')

my_payment_val = joined_data.groupby('month_year')['payment_value'].sum()
my_payment_val = my_payment_val.reset_index()
my_payment_val['month_year'] = my_payment_val['month_year'].astype(str)

# plotting the line chart
plt.plot(my_payment_val['month_year'], my_payment_val['payment_value'], color='red', marker='o')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month-Year')
plt.ylabel('Payment-Value')
plt.xticks(rotation=90, fontsize=8)
plt.yticks(fontsize=8)
plt.title('Payment Value by Month-Year (Line Chart)')
plt.show()

# plotting the bar chart
plt.bar(my_payment_val['month_year'], my_payment_val['payment_value'], color='red')
plt.xticks(rotation=90)
plt.xlabel('Month-Year')
plt.ylabel('Payment-Value')
plt.title('Payment Value by Month-Year (Bar Chart)')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.show()

# Scatter plots for visualization

# Using Matplotlib
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value' : 'sum', 'payment_installments' : 'sum'})
plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'], color='purple')
plt.xlabel('Payment-Value')
plt.ylabel('Payment-Installments')
plt.title('Payment Value Vs Payment Installments')
plt.show()

# Using seaborn
sns.set_theme(style='darkgrid')

sns.scatterplot(data=scatter_df, x='payment_value', y='payment_installments')
plt.xlabel('Payment-Value')
plt.ylabel('Payment-Installments')
plt.title('Payment Value Vs Payment Installments')
plt.show()

# Creating a Bar Chart

bar_data = joined_data.groupby(['payment_type','month_year'])['payment_value'].sum()
bar_data = bar_data.reset_index()

pivot_data = bar_data.pivot(index='month_year', columns='payment_type', values='payment_value')
pivot_data.plot(kind='bar', stacked='True')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month-Year')
plt.ylabel('Payment-Value')
plt.title('Stacked Bar Chart')
plt.show()

# Creating a Box plot

payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

plt.boxplot([payment_values[payment_types=='credit_card'],
             payment_values[payment_types == 'boleto'],
             payment_values[payment_types == 'voucher'],
             payment_values[payment_types == 'debit_card']],
            labels = ['Credit Card','Boleto','Voucher','Debit Card'])

plt.xlabel('Payment Type')
plt.ylabel('Payment Value')
plt.title('Box Plot showing Payment Value ranges by Payment Type')
plt.show()













