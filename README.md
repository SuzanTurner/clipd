# clipd — Command Line Interface for Pandas

A lightweight terminal-native CLI tool for exploring, cleaning, and transforming CSV data using the power of Pandas — right from your command line.  
- Built using Typer, Rich and Panda. 
- Designed for speed, control and effortless ETL


> ⚠️ **Note:**  
> This is reference documentation.  
> **`clipd` is under active development** and version 0.0.1 will soon be released to PyPI.
> Until then, feel free to explore the sample functionality shown below.


## Current Available Functions

Here's what `clipd` can do *right now*:

### Initialise Clipd
- `clipd init`
   Initialises `clipd` in the current directory.
  
### File Management
- `clipd connect <file.csv>`  
  Connects a dataframe file for processing. All operations will apply to this active file. (Make sure the file exists in the directory `clipd` is initialised in)

- `clipd disconnect`  
  Safely disconnects the currently active file.

### Data Description
- `clipd describe`  
  Provides a detailed overview of the connected file. Supports flags like `--head`, `--tail`, `--all`, `--null`, `--unique` etc. 

### Log Management
- `clipd log`  
  View structured logs of all operations performed during the session. Supports flags like '--lines 8` to veiw exact number of log lines. 

- `clipd log clear`  
  Cleanly wipes the operation history. 

### Error Handling
- Clean, readable terminal error messages with helpful guidance.
- No cryptic stack traces

### Exporting
- Export your transformed dataset to various formats:
  ``` clipd export``` : defaults to CSV.
  Also supports:
  - `.xlsx`  
  - `.json`



## Once installed, here’s how `clipd` commands feel in your terminal workflow:

```
clipd init
clipd connect <file>
clipd describe
clipd describe --head
clipd describe --null
clipd describe --unique --dtypes
clipd export --filename yadh --xlsx
clipd disconnect
clipd log
clipd log clear
```

# Future Prospects
> As the soul and sole developer, I add new functionalities and fix bugs in the code every day.
- Expand to all major Pandas commands
- Git style verson-control for dataframes
- Pipeline support
- Export the clipd actions as a .py/.ipynb file.
- Perform basic ML algorithms. 

---

# Author
Made with love and `--force` by Yadhnika Wakde
> I hope clipd grows into a useful tool and makes etl easier and faster. 



