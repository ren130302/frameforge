""" 
Requried 2 libraries
/pandas
/numpy

ver 2.2
""" 

class Processing:
    def __init__(self, settings:dict):
        self.settings = settings
        self._func_prop = {"drop":self.__drop,"apply":self.__apply,"combinations":self.__combinations,"replace": self.__replace, "fill": self.__fill}
    
    def __drop(self, _name, _prop):
        # print(f"_drop {_name}")
        
        for item in _prop["drop"]:
            self.dataframe.drop(self.dataframe.loc[self.dataframe[_name]==item].index, inplace=True)

    def __apply(self, _name, _prop):
        # print(f"_apply {_name}")
        func = _prop["apply"]["func"]
        args = _prop["apply"]["args"]
        self.dataframe.loc[:, _name] = self.dataframe.loc[:, _name].apply(func=func, args=args)

    def __combinations(self, _name, _prop):
        # print(f"_combinations {_name}")
        from itertools import combinations
        # データ保持する用
        comb = dict()
        # データの番号
        idx = 0
        
        # 指定された項目を重複なしで全通りの組み合わせを出力する処理
        for i in range(1,len(_prop["combinations"])):
            for label in combinations(_prop["combinations"], i):
                # print(label, idx)
                comb.setdefault(label, idx)
                idx += 1
        _prop.setdefault("replace", comb)

    def __comb_get_idx(self, datas:set or tuple or list or str, dict:dict):
        # print(datas, dict)
        try :
            # 初期化処理をするための条件分岐
            if type(datas) is str:
                dataset = set()
                dataset.add(datas)
                datas = dataset
            elif type(datas) is tuple or list:
                datas = set(datas)
            
            # 比較して欲しいデータと登録されている比較用データ（辞書）を比較し、登録されている番号を返す処理
            for key, value in dict.items():
                # print(key, value)
                len_key = len(key)
                len_data = len(datas)
                
                if len_key == len_data:
                    # 比較して欲しいデータと辞書を積集合
                    intersection = datas.intersection(key)
                    len_int = len(intersection)
                    
                    if len_int == len_data:
                        # 配列の長さに差がなければ一致しているとみなし、登録されている番号を返す
                        return value
        except :
            # 処理出来なかった場合、-1を返す
            return -1

    def __replace(self, _name, _prop):
        # print(f"_replace {_name}")
        try:
            # splitが代入可能な場合、エラーが起こらない
            _prop_split = _prop["split"]
            for target in set(self.dataframe.loc[:, _name]):
                value = self.__comb_get_idx(target.split(_prop_split), _prop["replace"])
                
                if value != -1:
                    # print(target, value)
                    self.dataframe.loc[:, _name] = self.dataframe.loc[:, _name].replace(target,value)
            return
        except:
            pass
        
        try:
            _prop_replace = _prop["replace"]
            # print(_prop_replace)
            for key, value in _prop_replace.items():
                self.dataframe.loc[:, _name] = self.dataframe.loc[:, _name].replace(key,value)
        except:
            # replaceがNoneである場合、自動的に文字列を数値に変換する処理
            # 列ごとに含まれるデータ取得、重複を排除、添え字追加、辞書型に変換
            _prop_replace = dict(enumerate(set(self.dataframe.loc[:, _name])))
            # 繰り返し文：データと数値
            for value, key in _prop_replace.items():
                if type(key) is not str:
                    # 文字列じゃない場合、既に置換済みとみなし繰り返しから脱出
                    break
                # 文字列である場合、列が置換済みではないと見なし置換処理
                self.dataframe.loc[:, _name] = self.dataframe.loc[:, _name].replace(key, value)
                    
            # 置換データを保存する
            _prop.setdefault("replace", _prop_replace)

    def __fill(self, _name, _prop):
        # print(f"_fill {_name}")
        from numpy import unsignedinteger,signedinteger,floating,complexfloating
        # 欠損値を埋めるための値を取得
        _prop_fill = _prop["fill"]
        
        if _prop_fill is None:
            # 指定されていない場合は、型に沿って0で埋める
            data_type = self.dataframe.loc[:, _name].dtype.type
            if data_type is unsignedinteger or signedinteger:
                _value = 0
            elif data_type is floating or complexfloating:
                _value = 0.0
        else:
            # 指定されてる値を代入
            _value = _prop_fill
        
        # 欠損値を埋める
        self.dataframe.loc[:, _name] = self.dataframe.loc[:, _name].fillna(_value)

    def execute(self):
        from pandas import read_csv
        # データ読み込み
        self.dataframe = read_csv(self.settings["paths"]["input"])

        for _name, _prop in self.settings["columns"].items():
            if _prop is None:
                # もしも列名に対して値がNoneの場合、列を削除処理
                self.dataframe = self.dataframe.drop(_name, axis=1)
                # print(f"_droped column {_name}")
                pass
            else:
                # print(f"{_name}")
                for _fname, _func in self._func_prop.items():
                    try:
                        # もし値を持っていたらエラーが起こらずにs取得できる
                        self.settings["columns"][_name][_fname]
                    except:
                        pass
                    else:
                        # 代入が成功した場合の関数を実行
                        _func(_name, _prop)
            
        # データ書き込み
        self.dataframe.to_csv(self.settings["paths"]["output"], index=False)
        
class Generating:
    def __init__(self, settings):
        self.settings = settings
        
    def execute(self):
        from pandas import DataFrame, read_csv
        from random import randint
        
        dataframe = read_csv(self.settings["paths"]["input"])
        testdataframe = DataFrame()
        val_dict = dict()
        init_dict = dict()
        columns = dataframe.head(0)

        for column in columns:
            init_dict.setdefault(column, None)
            data = dataframe.loc[:, column]
            __min = min(data)
            __max = max(data)
            val_dict.setdefault(column, (__min, __max))
        
        for i in range(self.settings["test_size"]):
            _temp = dict()
            for column in columns:
                __min = val_dict[column][0]
                __max = val_dict[column][1]
                __rand= randint(__min, __max)
                _temp.setdefault(column, __rand)
            testdataframe = testdataframe.append(_temp, ignore_index=True)

        testdataframe.to_csv(self.settings["paths"]["output"], index=False)