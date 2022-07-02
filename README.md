# frameforge

dataframe のコーディング量を減らすためのクラスを提供します。
python の dataframe のめんどくさい作業から今すぐに開放されましょう。

## 必要なライブラリ

- pandas
- numpy

## python 動作環境確認したもの

| python | frameforge |
| ------ | ---------- |
| 3.8    | 2.3        |
| 3.9    | 2.3        |

## 処理される順番

1. 列の削除する
2. 特定の値の削除する
3. 値に対して関数を適用する
4. 全通りの組みあわせの値を生成する
5. 置換する
6. 欠損部分を埋める

# 設定の仕方

- [dropna](#dropna)
- [drop](#drop)
- [apply](#apply)
- [combinations](#combinations)
- [replace](#replace)
- [fill](#fill)
- [template](#template)

## dropna

指定した列を削除します。

```
"column_name" : None
```

#### 記述例

列「No」を排除する場合

```
"No" : None
```

## drop

列に含まれる特定の値を削除します。

```
"column_name" : {
    "drop" : <None | list | set | tuple>
}
```

### None を指定した場合の動作

列に含まれる欠損値が存在する場合、行ごと削除されます。

#### 記述例

列「Type」に存在する欠損値を排除する場合

```
"Type" : {
    "drop" : None
}
```

### list, set, tuple いずれかの型で複数を列挙した場合の動作

指定した値のいずれか一つに合致した場合、行ごと削除されます。

#### 記述例

列「Type」に存在する値「0,1,2,欠損値」いずれか一つ合致させ、行ごとに削除する。

```
"Type" : {
    "drop" : [0,1,2,None]
}
```

## apply

列に含まれる値に対して指定された関数を適用します。

```
"column_name" : {
    "apply" : {
        "func":function,
        "args":args
    }
}
```

## combinations

指定された値を重複無し組み合わせ生成し、replace に置換候補として設定します。

```
"column_name" : {
    "combinations":<list | set | tuple>
}
```

#### 記述例

```
"column_name" : {
    "combinations": ["I","was"]
    "split" : "-",
    """combinationsによって自動生成されたコード"""
    "replace": {("I"):0, ("was"):2, ("I", "was"):3}
}
```

## replace

列に存在する値を指定された値へと置換します。

combinations を指定している場合は、値が自動的に生成され replace に設定されます。<br>
つまり、replace に指定をしなくても良いということです。<br>
combinations と replace の両方を指定した場合は、<br>
replace で指定されたものが有効となり置換の処理がされてしまいます。<br>
つまり、combinations で指定したことが無意味となります。<br>
combinationsで生成された値を設定したい場合は、手動で設定するしかありません。<br>

```
"column_name" : {
    "replace" : <None | dict>
}
```

### None を指定した場合の動作

列に存在する値を自動的に数値へ変換します。

```
"column_name" : {
    "replace" : None
}
```

### 値を指定した場合の動作

指定された値に置換します。

#### 記述例

この場合は、列に存在する値が str 型の「sea」であれば int 型の「0」に、<br>
もしくは str 型の「mountain」であれば int 型の「1」に置換する処理を行う。

```
"column_name" : {
    "replace" : {"sea":0, "mountain":1}
}
```

## fill

```
"column_name" : {
    "fill" : <None | int | float | str>
}
```

### None を指定した場合の動作

対応する型の初期値を代入します。

### 値を指定した場合の動作

指定された値を代入します

## template

```
settings = {
    "paths" : {
        "input" : csv,
        "output": csv,
    },
    "columns":{
        "column_name" : None
    }
}
Processing(settings).execute()
```
