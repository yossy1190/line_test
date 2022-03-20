import pandas as pd


### デスクトップアプリ作成課題

def kimetsu_search(word):
    # 検索対象取得
    # https://note.nkmk.me/python-pandas-read-csv-tsv/　read_csv説明
    df=pd.read_csv("source.csv")
    # detaframeのnameカラムをリスト化。souurceというリストにvalueを入れていく
    source=list(df["name"])

    # 検索
    if word in source:
        print("『{}』はリストにあります".format(word))
        

    else:
        print("『{}』はリストにありません。リストに追加します".format(word))
        
        # 追加
        # add_flg=input("追加登録しますか？(0:しない 1:する)　＞＞　")
        # if add_flg=="1":
        
    

    