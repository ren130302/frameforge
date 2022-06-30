# frameforge

## 必要なライブラリ
- pandas
- numpy

## python動作環境確認したもの
|python|frameforge|
|---|---|
|3.8|2.3|
|3.9|2.3|

pythonのdataframeのめんどくさい作業から今すぐに開放されましょう。
<br>
### 処理される順番
1. 列の削除する
2. 特定の値の削除する
3. 値に対して関数を適用する
4. 全通りの組みあわせの値を生成する
5. 置換する
6. 欠損部分を埋める

>指定した列を削除します。<br>
>```
>"<column_name>" : None
>```

>列に含まれる特定の値を削除します。<br>
>```
>"<column_name>" : {
>  "drop" : <None | list | set | tuple> 
>}
>```
>>Noneを指定した場合の動作<br>
>>欠損値のみ行から排除します。<br>
>>```
>>"<column_name>" : {
>>  "drop" : None
>>}
>>```
>
>>list, set, tupleいずれかの型で複数を列挙した場合の動作<br>
>>列に含まれる 0,1,2,3,4,5,欠損値 いずれか一つ存在する場合、行ごとに削除されます<br>
>>```
>>"<column_name>" : {
>>  "drop" : [0,1,2,3,4,5,None] 
>>}
>>```

>列に含まれる値に対して関数を適用します。<br>
>```
>"<column_name>" : {
>  "apply" : {
>    "func":<function>, 
>    "args":<args>
>  }
>}
>```

>指定された値を重複無し組み合わせ生成し replace に置換候補として設定します。<br>
>```
>"<column_name>" : {
>  "combinations":<list | set | tuple>
>}
>```
>>列に存在する値の型が文字列かつ区切り文字が含まれていて、文字列置換を行いたい場合の指定の仕方。
>>```
>>"<column_name>" : {
>>  "combinations":<list | set | tuple>
>>  "split" : <str>,
>>}
>>```
>>具体的な例
>>```
>>csv before
>>I-was,100
>>```
>>```
>>csv after
>>2,100
>>```
>>```
>>python
>>"<column_name>" : {
>>  "combinations": ["I","was"]
>>  "split" : "-",
>>  """combinations によって自動生成された"""
>>  "replace": {("I"):0, ("was"):2, ("I","was"):3}
>>}
>>```

>列に存在する値を指定された値へと置換します。<br>
>もし combinations を指定している場合は、値が自動的に生成され replace に設定されるます。<br>
>再度、replace で指定する必要がありません。<br>
>combinations と replace を指定した場合の動作は replace で指定されたもので置換されます。<br>
>```
>"<column_name>" : {
>  "replace" : <None | dict>
>}
>```
>>Noneを指定した場合の動作<br>
>>列に存在する値を自動的に数値へ変換します。<br>
>
>>値を指定した場合の動作<br>
>>値をそのまま置換します。
>>具体的な例
>>この場合は、列に存在する値が str型の「sea」であれば int型の「0」に、<br>
もしくはstr型の「mountain」であれば int型の「1」に置換するという動作をする。<br>
>>```
>>"<column_name>" : {
>>  "replace" : {"sea":0,"mountain":1}
>>}
>>```

>欠損値の代わりに値を代入します。<br>
>```
>"<column_name>" : {
>  "fill" : <None | int | float | str>
>}
>```
>
>>Noneを指定した場合の動作<br>
>>対応する型の初期値を代入します。<br>
>
>>値を指定した場合の動作<br>
>>値をそのまま代入します。

```
settings={
  "paths":{
    "input" :"<読込ファイル名>.csv",
    "output":"<保存ファイル名>.csv",
  },
  "columns":{
    "<column_name>" : None
  }
}
Processing(settings).execute()
```
