import pandas as pd

#knock 11
uriage_data = pd.read_csv('uriage.csv')
kokyaku_data = pd.read_excel('kokyaku_daicho.xlsx')

# print(uriage_data.head())
# print("*************************")
# print(kokyaku_data.head())
# print("*************************")

#knock 12
# print(uriage_data["item_name"].head())
# print(uriage_data["item_price"].head())

#knock 13
uriage_data["purchase_date"] = pd.to_datetime(uriage_data["purchase_date"])
uriage_data["purchase_month"] = uriage_data["purchase_date"].dt.strftime("%Y%m")
res = uriage_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# print(res)

res2 = uriage_data.pivot_table(index="purchase_month", columns="item_name",
                               values="item_price", aggfunc="sum", fill_value="0")
# print(res2)

#knock 14
# print(len(pd.unique(uriage_data.item_name)))

uriage_data["item_name"] = uriage_data["item_name"].str.upper()
uriage_data["item_name"] = uriage_data["item_name"].str.replace(" ", "")
uriage_data["item_name"] = uriage_data["item_name"].str.replace("　", "")
uriage_data.sort_values(by=["item_name"], ascending=True).head(20)

# print(pd.unique(uriage_data["item_name"]))
# print(len(pd.unique(uriage_data["item_name"])))

#knock 15
# print(uriage_data.isnull().any(axis=0)　)

#欠損値のある箇所を特定
flg_is_null = uriage_data["item_price"].isnull()

#欠損している商品名の一覧を作成する処理
#Listは変数の値をリスト形式に変換
#loc関数は条件を付与し，それに合致するデータを抽出することができる
#flg_is_nullで欠損値の位置，item_nameで商品名を取得している
#NULLのある商品名を取得している．uniqueで商品名の重複を防ぐ
for trg in list(uriage_data.loc[flg_is_null, "item_name"].unique()):
    #~flg_is_nullは否定演算子である
    #商品名から金額がNULLではない行から商品の金額を取得している
    price = uriage_data.loc[(~flg_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
    #取得した金額でNULLを補完している
    uriage_data["item_price"].loc[(flg_is_null) & (uriage_data["item_name"] == trg)] = price

# print(uriage_data.head(10))
# print(uriage_data.isnull().any(axis=0))

#1行目ですべての商品に対してループ処理を実施している
for trg in list(uriage_data["item_name"].sort_values().unique()):
    pass
    #最大値と最小値を出力
    # print(trg + "の最大値:" + str(uriage_data.loc[uriage_data["item_name"] == trg]["item_price"].max()) +
    #       "の最小額:" + str(uriage_data.loc[uriage_data["item_name"] == trg]["item_price"].min(skipna=False)))


#knock 16
# print(kokyaku_data["顧客名"].head())
# print(uriage_data["customer_name"].head())

kokyaku_data["顧客名"] = kokyaku_data["顧客名"].str.replace(" ", "")
kokyaku_data["顧客名"] = kokyaku_data["顧客名"].str.replace("　", "")
# print(kokyaku_data["顧客名"].head(10))

#knock 17
#数値を格納している
flg_is_serial = kokyaku_data["登録日"].astype("str").str.isdigit()
# print(flg_is_serial.sum())

fromSerial = (pd.to_timedelta(kokyaku_data.loc[flg_is_serial, "登録日"].astype("float"), unit="D")
              + pd.to_datetime("1900/01/01"))
# print(fromSerial)

fromString = pd.to_datetime(kokyaku_data.loc[~flg_is_serial, "登録日"])
# print(fromString)
kokyaku_data["登録日"] = pd.concat([fromSerial, fromString])
# print(kokyaku_data.head())

kokyaku_data["登録年月"] = kokyaku_data["登録日"].dt.strftime("%Y%m")
rslt = kokyaku_data.groupby("登録年月").count()["顧客名"]
# print(rslt)
# print(len(kokyaku_data))

flg_is_serial = kokyaku_data["登録日"].astype("str").str.isdigit()
# print(flg_is_serial.sum())


#knock 18
join_data = pd.merge(uriage_data, kokyaku_data, left_on="customer_name", right_on="顧客名", how="left")
join_data = join_data.drop("customer_name", axis=1)
# print(join_data)

#knock 19
dump_data = join_data[["purchase_date", "purchase_month", "item_name", "item_price",
                       "顧客名", "かな", "地域", "メールアドレス", "登録日"]]
# print(dump_data)

dump_data.to_csv("dump_data_practice.csv", index=False)

#knock 20
import_data = pd.read_csv("dump_data_practice.csv")
# print(import_data.head())

byItem = import_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
# print(byItem)
byPrice = import_data.pivot_table(index="purchase_month", columns="item_name",
                                  values="item_price", aggfunc="sum", fill_value=0)
# print(byPrice)
byCustomer = import_data.pivot_table(index="purchase_month", columns="顧客名", aggfunc="size", fill_value=0)
# print(byCustomer)
byRegion = import_data.pivot_table(index="purchase_month", columns="地域", aggfunc="size", fill_value=0)
# print(byRegion)

away_data = pd.merge(uriage_data, kokyaku_data, left_on="customer_name", right_on="顧客名", how="right")
#購入していないユーザをチェック
print(away_data[away_data["purchase_date"].isnull()][["顧客名", "メールアドレス", "登録日"]])