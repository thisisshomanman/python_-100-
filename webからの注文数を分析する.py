import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_inline

# knock 1
customer_master = pd.read_csv('customer_master.csv')
item_master = pd.read_csv('item_master.csv')
transaction_1 = pd.read_csv('transaction_1.csv')
transaction_2 = pd.read_csv('transaction_2.csv')
transaction_detail_1 = pd.read_csv('transaction_detail_1.csv')
transaction_detail_2 = pd.read_csv('transaction_detail_2.csv')

#knock 2
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)
# print(transaction_1.head())
# print("*******************")
# print(transaction_2.head())
# print("*******************")
# print(transaction.head())
# print(transaction_detail.head())

#knock 3
join_data = pd.merge(transaction_detail, transaction[["transaction_id", "payment_date", "customer_id"]],
                     on="transaction_id", how="left")
# print(join_data.head())

#knock 4
join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
# print(join_data.head())
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
# print(join_data.head())

#knock 5
join_data["price"] = join_data["quantity"] * join_data["item_price"]
# print(join_data[["quantity", "item_price", "price"]].head())

#knock 6
join_sum_price = join_data["price"].sum()
# print(join_sum_price)
transaction_sum_price = transaction["price"].sum()
# print(transaction_sum_price)

price_confirm = join_data["price"].sum() == transaction["price"].sum()
# print(price_confirm)

#knock 7
statistic = join_data.isnull().sum()
# print(statistic)
# print(join_data.describe())

min_date = join_data["payment_date"].min()
max_date = join_data["payment_date"].max()
# print(f"{min_date}から{max_date}")

#knock 8
# print(join_data.dtypes)

join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")
# print(join_data[["payment_date", "payment_month"]].head())
# print(join_data.dtypes)

pay_month = join_data.groupby("payment_month").sum()["price"]
# print(pay_month)

#knock 9
item_by_month = join_data.groupby(["payment_month", "item_name"]).sum()[["price", "quantity"]]
# print(item_by_month)

# table = pd.pivot_table(join_data, index='item_name', columns='payment_month', values=['price', 'quantity'], aggfunc='sum')
# print(table)

#knock 10
graph_data = pd.pivot_table(join_data, index='payment_month', columns='item_name', values=['price'], aggfunc='sum')
print(graph_data.head())

print(graph_data.columns)

# %matplotlib_inline
plt.plot(list(graph_data.index), graph_data["price", "PC-A"], label='PC-A')
plt.plot(list(graph_data.index), graph_data["price", "PC-B"], label='PC-B')
plt.plot(list(graph_data.index), graph_data["price", "PC-C"], label='PC-C')
plt.plot(list(graph_data.index), graph_data["price", "PC-D"], label='PC-D')
plt.plot(list(graph_data.index), graph_data["price", "PC-E"], label='PC-E')
plt.legend()
plt.show()