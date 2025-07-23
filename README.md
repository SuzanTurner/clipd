# clipd — Command Line Interface for Pandas

A slick, terminal-native CLI tool for exploring, cleaning, and transforming CSV data using the power of Pandas — right from your command line.  
Think Git meets Pandas.

---

## Features

- Explore and clean CSV files in seconds
- Null handling, data type conversion, and transformations
- Rich terminal UI powered by [Rich](https://github.com/Textualize/rich), and Typer.
- `pip` installable and easy to integrate into your workflows
- Export to Excel with styled formatting
- Batch mode for automated ETL pipelines
- Designed for speed, clarity, and terminal joy

---

> ⚠️ **Note:**  
> This is reference documentation.  
> **`clipd` is under active development** and version 0.0.1 will soon be released to PyPI.
> Until then, feel free to explore the sample functionality shown below.

---

# Once installed, here’s how `clipd` commands feel in your terminal workflow:

```
clipd init
```
Initialises clipd in current directory

```
clipd connect <file>
```
Connects to dataframe. Make sure the file exists in the directory where clipd is initialised.

```
clipd describe
```
Describes the file connected. 
Supports flags like `--head`, `--tail`, `--all`, `--null`, `--unique` etc. 
Has Rich formating.

```
clipd disconnect
```
Disonnects from the connected file. 

```
clipd export
```
Exports the altered dataframe file in csv format by default. 
Supprts `--json`, `--xlsx` formats for exporting as well, and also `--filename` and `--dir`. 

---

# Author
> Made with love and --force by Yadhnika Wakde

“Because sometimes, Jupyter is just too much.”

