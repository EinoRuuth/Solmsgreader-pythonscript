# Python Script for a Solmsg output file Search and Visualization

## Overview
This Python script allows users to parse solmsg based on various criteria such as process time, GOID, node ID, and failed processes. Additionally, it provides functionality to specify file paths and generate visual graphs based on GOID or node ID.

## Installation
Before using this script, ensure you have the required dependencies installed. You can install them using pip:

```console
pip install --upgrade plotly
pip install --upgrade pandas
pip install --upgrade numpy
```
## Command Line Arguments
The script supports the following command-line arguments:

### 1. Search by Process Time
- **Option:** `--time SECONDS` / `-t SECONDS`
- **Description:** Searches groups by the duration of the process.
- **Example:**
  ```console
  python script.py --time 10
  ```

### 2. Search by GOID
- **Option:** `--goid GOID` / `-g GOID`
- **Description:** Searches groups based on GOID. You can be specific or broad in your search.
- **Example:**
  ```console
  python script.py --goid 1,1242,1,303
  ```
  - GOID `1` will return all groups with a GOID starting with `1`.

### 3. Search by Node ID
- **Option:** `--node ID` / `Id: ID` / `-n ID`
- **Description:** Searches groups based on node ID.
- **Example:**
  ```console
  python script.py --node 3
  ```
  or
  ```console
  python script.py Id: 3
  ```
### 4. Search for Failed Processes
- **Option:** `--failed` / `-f`
- **Description:** Searches for all failed processes.
- **Example:**
  ```console
  python script.py --failed
  ```

### 5. Specify File Path
- **Option:** `--path PATH` / `-p PATH`
- **Description:** Specifies the file path for searching. By default, it searches for folders named `tscn*`.
- **Example:**
  ```console
  python script.py --path C:\Users\user\Documents\solmsg
  ```

### 6. Specify File(s)
- **Option:** `--file FILE_PATH` / `-f FILE_PATH`
- **Description:** Specifies the file(s) to process.
- **Example:**
  ```console
  python script.py --file C:\Users\user\Documents\solmsg\tsnc\tsnc_master\solmsg.out
  ```

### 7. Generate Graph Visualization
- **Option:** `--graph`
- **Description:** Generates a visual graph based on a specified GOID or node.
- **Example:**
  ```console
  python script.py --graph -g 1,123,2,204
  ```

## Usage Examples
- Search for groups that took 20 seconds:
  ```console
  python script.py --time 20
  ```
- Search for groups with GOID starting with `5`:
  ```console
  python script.py --goid 5
  ```
- Search for failed processes:
  ```console
  python script.py --failed
  ```
- Generate a graph for GOID `1,23,4,567`:
  ```console
  python script.py --graph -g 1,23,4,567
  ```

## Notes
- Ensure the specified file path or files exist before running the script.
- Graph visualization requires Plotly to be installed.

