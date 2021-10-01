# PySISKAPERBAPO
Python client to scrap Jatimprov's Siskaperbapo

## Installation
### Using `pip+git`:
```
pip install git+https://github.com/anangsahroni/pysiskaperbapo.git
```
### Using `pip` editable:
Using `pip`:
1. Activate your virtual environment
2. Clone or download the repository:
```
git clone https://github.com/anangsahroni/pysiskaperbapo.git
```
3. Go to project folder where `setup.py` is located (using `cd` or change directory)
4. Run `pip install -e`

## Usage
1. Import the package:
```python
from ejperbo import EJPERBO
```
2. Define input: `region`, `min_date`, `max_date`:
```python
region="bangkalankab"
min_date="2021-09-15"
max_date="2021-09-17"
```
3. Create instance:
```python
scrap=EJPERBO(min_date,max_date,region)
```
Input parameters and available market will be printed:
```
SISKAPERBO East Java Python Client (unofficial)
==================================================
Selected region:  Bangkalan
Time range: 2021-09-15 - 2021-09-17
Available market:  ['Pasar Senenan', 'Pasar Ki Lemah Duwur', 'Pasar Baru Bancaran']
```
4. Query all available market using `market="all"`:
```python
scrap.query(market="all)
```

or specific market using `market=[market name]`:
```python
scrap.query(market="Pasar Senenan")
```

the download will begin and progress bar will appear.

5. To preview the result:
```python
scrap.data
```
6. Save the data to `csv` using `Pandas`:
```python
scrap.data.to_csv("[filename].csv", index=False)
```
