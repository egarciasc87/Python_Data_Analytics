import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def weight_slab(weight):
    i = round(weight % 1, 1)

    if i == 0.0:
        return weight
    elif i > 0.5:
        return int(weight) + 1.0
    else:
        return int(weight) + 0.5


#1- Get row data
courier_invoice = pd.read_csv("4_Invoice.csv")
courier_rates = pd.read_csv("4_Courier_Company_Rates.csv")
order_report = pd.read_csv("4_Order_Report.csv")
pincodes = pd.read_csv("4_pincodes.csv")
sku_master = pd.read_csv("4_SKU_Master.csv")

# print(invoice.head())
# print(courier_rates.head())
# print(order_report.head())
# print(pincodes.head())
# print(sku_master.head())


#2. Validate and clean null data
print(courier_invoice.isnull().sum())
print(courier_rates.isnull().sum())
print(order_report.isnull().sum())
print(pincodes.isnull().sum())
print(sku_master.isnull().sum())

order_report = order_report.drop(columns=["Unnamed: 3", "Unnamed: 4"])
pincodes = pincodes.drop(columns=["Unnamed: 3", "Unnamed: 4"])
sku_master = sku_master.drop(columns=["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"])

#print(order_report.isnull().sum())
#print(pincodes.isnull().sum())
#print(sku_master.isnull().sum())


#3. Merge order_report and sku_master
#print(order_report)
#print(sku_master)

merged_data = pd.merge(order_report, sku_master, on="SKU")
merged_data = merged_data.rename(columns={"ExternOrderNo": "Order ID"})
#merged_data.columns = ["Order ID", "SKU", "Order Qty", "Weight (g)"]
#print(merged_data)


#4. Merge courier_invoice with pincode
#print(courier_invoice)
#print(pincodes)
abc_courier = pincodes.drop_duplicates(subset=["Customer Pincode"])
courier_abc = courier_invoice[["Order ID", "Customer Pincode", "Type of Shipment"]]

pincodes = pd.merge(courier_abc, abc_courier, on="Customer Pincode")
#print(pincodes)
#print(pincodes.columns)

#pincodes = courier_abc.merge(abc_courier, on="Customer Pincode")
#print(pincodes)
#print(pincodes.columns)

merged = merged_data.merge(pincodes, on="Order ID")
merged["Weight (kg)"] = merged["Weight (g)"] / 1000
print(merged)


#5. Calculate the weight slabs
merged["Weight Slab (kg)"] = merged["Weight (kg)"].apply(weight_slab)
courier_invoice["Weight Slab Charged by Courier Company"] = (courier_invoice["Charged Weight"]).apply(weight_slab)
courier_invoice = courier_invoice.rename(columns={"Zone": "Delivery Zone Charged by Courier Company"})
merged = merged.rename(columns={"Zone": "Delivery Zone As Per ABC"})
merged = merged.rename(columns={"Weight Slab (kg)": "Weight Slab As Per ABC"})
#print(merged)
#print("courier_invoice: ", courier_invoice)


#6. Calculate expected charges
total_expected_charge = []

for _, row in merged.iterrows():
    fwd_category = 'fwd_' + row['Delivery Zone As Per ABC']
    fwd_fixed = courier_rates.at[0, fwd_category + '_fixed']
    fwd_additional = courier_rates.at[0, fwd_category + '_additional']
    rto_category = 'rto_' + row['Delivery Zone As Per ABC']
    rto_fixed = courier_rates.at[0, rto_category + '_fixed']
    rto_additional = courier_rates.at[0, rto_category + '_additional']

    weight_slab = row['Weight Slab As Per ABC']

    if row['Type of Shipment'] == 'Forward charges':
        additional_weight = max(0, (weight_slab - 0.5) / 0.5)
        total_expected_charge.append(fwd_fixed + additional_weight * fwd_additional)
    elif row['Type of Shipment'] == 'Forward and RTO charges':
        additional_weight = max(0, (weight_slab - 0.5) / 0.5)
        total_expected_charge.append(fwd_fixed + additional_weight * (fwd_additional + rto_additional))
    else:
        total_expected_charge.append(0)

merged['Expected Charge as per ABC'] = total_expected_charge
merged_output = merged.merge(courier_invoice, on="Order ID")
#print(merged_output)
#print(merged_output.columns)


#7. Calculate differences in charges and expected charges
df_diff = merged_output
df_diff["Difference (Rs.)"] = df_diff["Billing Amount (Rs.)"] - df_diff["Expected Charge as per ABC"]
df_new = df_diff[["Order ID", "Difference (Rs.)", "Expected Charge as per ABC"]]
print(df_new)

# Calculate the total orders in each category
total_correctly_charged = len(df_new[df_new['Difference (Rs.)'] == 0])
total_overcharged = len(df_new[df_new['Difference (Rs.)'] > 0])
total_undercharged = len(df_new[df_new['Difference (Rs.)'] < 0])

# Calculate the total amount in each category
amount_overcharged = abs(df_new[df_new['Difference (Rs.)'] > 0]['Difference (Rs.)'].sum())
amount_undercharged = df_new[df_new['Difference (Rs.)'] < 0]['Difference (Rs.)'].sum()
amount_correctly_charged = df_new[df_new['Difference (Rs.)'] == 0]['Expected Charge as per ABC'].sum()

# Create a new DataFrame for the summary
summary_data = {'Description': ['Total Orders where ABC has been correctly charged',
                                'Total Orders where ABC has been overcharged',
                                'Total Orders where ABC has been undercharged'],
                'Count': [total_correctly_charged, total_overcharged, total_undercharged],
                'Amount (Rs.)': [amount_correctly_charged, amount_overcharged, amount_undercharged]}

df_summary = pd.DataFrame(summary_data)
print(df_summary)

fig = go.Figure(data=go.Pie(labels=df_summary["Description"],
                            values=df_summary["Count"],
                            textinfo="label+percent",
                            hole=0.4))
fig.update_layout(title="Proportion")
fig.show()

