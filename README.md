# SepeScan tool
A scanning tool written in Python used to automate the information-gathering process when performing audits.

## Modes
### Scanning mode
This mode uses **`nmap`**, **`nikto`** and **`whatweb`** to scan the target host. 

Reports are saved to a specified path or `.` by default.

### Fuzzing mode
Coming soon...

## Usage
```yaml
usage: SepeScan [-h] {scan,fuzz} ...

Scanning tool

positional arguments:
  {scan,fuzz}  Choose a mode
    scan       Scan Mode
    fuzz       Fuzzing Mode
```

## Requirements
1) **nmap**
    ```bash
    sudo apt-get install nmap
    ```

2) **nikto**
    ```bash
    sudo apt-get install nikto
    ```

3) **whatweb**
    ```bash
    sudo apt-get install whatweb
    ```

4) **Pyton dependencies**
    ```bash
    pip install -r requirements.txt
    ```