# findtype
A script to search for examples by specifying a Type number.
Searches for examples containing the specified Type number from Dck files included in the Examples folder.
<br>
When the script is executed, .dck files containing components of the specified Type number are listed.

By default, the following folders are searched:

* C:\TRNSYS18\Tess Models\Examples
* C:\TRNSYS18\Examples
* C:\TRNSYS18\TRNLib

### Note
Since .tpf files cannot be opened directly, Types are searched from corresponding .dck files.<br>
As a prerequisite, all .tpf files in the Examples folder must be exported to .dck files.<br>
Please run the "-i" option beforehand to export .tpf files to .dck files.

```python
python findtype.py -i
```
This initialization process takes a very long time. It's recommended to run this before taking a break, so you can enjoy a coffee while waiting.

You can also specify any folder other than the default folders using the -p option.
```python
python findtype.py -i -p C:\TRNSYS18\MyProjects\BuildingModel
```

### Usage Examples
Search for Type56 in Examples folder
```python
python findtype.py 56
```

You can also specify the target folder for search using the -p option.
The following example searches for Type56 in folders under "C:\TRNSYS18\MyProjects\BuildingModel".
```python
python findtype.py 56 -p C:\TRNSYS18\MyProjects\BuildingModel
```

Search for type682
```
> python findtype.py 682

The Dck files containing the component are:
1 - C:\TRNSYS18\Tess Models\Examples\Cogeneration (CHP) Library\Combined Cycle with Hot Water_v2a.tpf
2 - C:\TRNSYS18\Tess Models\Examples\Cogeneration (CHP) Library\Template_ConvertingLoadsToTemperatures_v2a.tpf
3 - C:\TRNSYS18\Tess Models\Examples\Loads and Structures Library\Synthetic Building.tpf

Enter the number of the file you want to open (q to quit): 1
Opening C:\TRNSYS18\Tess Models\Examples\Cogeneration (CHP) Library\Combined Cycle with Hot Water_v2a.tpf...
```

When you specify the number of a listed example, Simulation Studio launches and opens the .tpf file.

### Note
This script assumes that .tpf and .dck files have the same name. By default, .dck files have the same name as .tpf files, but some .tpf files have different .dck file names specified. In this case, the correspondence will be lost. Even if you specify a number, the .tpf file will not be opened.

### Batch File
A batch file findtype.bat is provided for launching the script. You can register this repository folder to the PATH environment variable and execute it in the following format:
<br>
Search for .dck files containing Type56
```
findtyp 56
```
Initialize Examples folder (export all .tpf files to .dck files)
```
findtyp -i
```
Specify a folder and search for .dck files containing Type56
```
findtyp 56 -p C:\TRNSYS18\MyProjects\SmallHouse
```

## Command Line Options
|Option|Description|
|-|-|
|type no|Specify the type number to search for e.g. 56|
|-p | Specify a non-standard path e.g. TRNSYS18\MyProjects\Project1
|-i | Initialize process (export all .tpf files to dck files)

Specify search folder and search for Type682
```
python findtype.py 682 -p C:\TRNSYS18\MyProjects\Project1
```
# Creating Executable Image
Create an executable image using pyinstaller.
```python
pip install pyinstaller
pyinstaller findtype.py --onefile
```
findtype.exe will be created in the dist folder.

