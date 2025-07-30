# findtype
Type番号を指定して作例を検索するスクリプトです。
Examplesフォルダに含まれるDckファイルから、指定されたType番号を含む作例を検索します。
<br>
スクリプトを実行すると、指定したType番号のコンポーネントを含む.dckファイルがリスト表示されます。

デフォルトで以下のフォルダを対象に検索を行います。

* C:\TRNSYS18\Tess Models\Examples
* C:\TRNSYS18\Examples
* C:\TRNSYS18\TRNLib

### 注意
.tpfファイルを直接開く事はできないため、対応する.dckからTypeを検索します。<br>
前提としてExamplesフォルダの.tpfがすべて.dckに書き出されている必要があります。<br>
予め"-i"で.tpfから.dckを書き出す処理を行って下さい。

```python
python findtype.py -i
```

-p オプションでデフォルト以外の任意のフォルダを指定することも可能です。
```python
python findtype.py -i -p C:\TRNSYS18\MyProjects\BuildingModel
```

### 使用例
例）ExamplesフォルダでType56を検索する
```python
python findtype.py 56
```

-p オプションで検索対象のフォルダを指定することもできます。
以下の例では"C:\TRNSYS18\MyProjects\BuildingModel"以下のフォルダを対象にしてType56を検索します。
```python
python findtype.py 56 -p C:\TRNSYS18\MyProjects\BuildingModel
```

例）type687を検索
```
> python findtype.py 682

The Dck files containing the component are:
1 - C:\TRNSYS18\Tess Models\Examples\Cogeneration (CHP) Library\Combined Cycle with Hot Water_v2a.tpf
2 - C:\TRNSYS18\Tess Models\Examples\Cogeneration (CHP) Library\Template_ConvertingLoadsToTemperatures_v2a.tpf
3 - C:\TRNSYS18\Tess Models\Examples\Loads and Structures Library\Synthetic Building.tpf

Enter the number of the file you want to open (q to quit): 1
Opening C:\TRNSYS18\Tess Models\Examples\Cogeneration (CHP) Library\Combined Cycle with Hot Water_v2a.tpf...
```

リストアップされた作例の番号を指定すると、Simulation Studioが起動して.tpfが開かれます。
### 注意
このスクリプトでは.tpfと.dckが同じ名前であることを前提としています。通常、.dckファイルの名前は.tpfと同じ名前になりますが、もし、異なる.dckファイルを指定していた場合は、対応関係が取れなくなります。番号をしていしても.tpfは開かれません。

### バッチファイル
起動用にfindtype.batを用意しています。このリポジトリンのフォルダを環境変数Pathへ登録して次のような形式で実行することができます。
<br>
例）Type56を含む.dckを検索する
```
findtyp 56
```
例）Examplesフォルダを初期化（すべての.tpfから.dckを書き出す）
```
findtyp -i
```
例）フォルダを指定して、Type56を含む.dckを検索する
```
findtyp 56 -p C:\TRNSYS18\MyProjects\SmallHouse
```

## コマンドラインオプション
|オプション|内容|
|-|-|
|type no|検索するtypeの番号を指定する e.g. 56|
|-p | 標準以外のパスを指定する e.g. TRNSYS18\MyProjects\Project1
|-i | 初期化処理（すべての.tpfをdckファイルへエクスポートする）

例）検索するフォルダを指定して、Type682を検索
```
python findtype.py 682 -p C:\TRNSYS18\MyProjects\Project1
```
# 実行イメージの作成
pyinstaller を使って実行イメージを作成する。
```python
pip install pyinstaller
pyinstaller findtype.py --onefile
```
distフォルダにfindtype.exeが作成される。

