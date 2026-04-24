# PySISKAPERBAPO
Python client to scrap Jatimprov's Siskaperbapo

This project was built with responsible scraping principles in mind:

- **Rate limiting** — requests were throttled to avoid overloading the server,
  mimicking normal human browsing intervals
- **Public data only** — only publicly accessible pages were scraped,
  no authentication bypass or private endpoints
- **Non-commercial** — data was collected solely for research and 
  monitoring purposes

## Installation
### Using `pip` editable:
Using `pip`:
1. Activate your virtual environment
2. Clone or download the repository:
```
git clone https://github.com/anangsahroni/pysiskaperbapo.git
```
3. Go to project folder where `setup.py` is located (using `cd` or change directory)
4. Run `pip install -e .`
### Using `pip+git`:
PS: Not working for private repo (this is private repo), should not be used, just for testing.
```
pip install git+https://github.com/anangsahroni/pysiskaperbapo.git
```
### Manual
If not familiar with `pip` and `git`:
1. Download the repository as zip using the `clone` button above
2. Extract the zip
3. Install using the above step in **Using `pip` editable** and skip step number 2

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
scrap.query(market="all")
```

or specific market using `market=[market name]`:
```python
scrap.query(market="Pasar Senenan")
```
or specific days using `days=[days_list]`:
```python
scrap.query(days=["Friday","Saturday"])
```
or the combination:
```python
scrap.query(market="Pasar Senenan", days=["Friday","Saturday"])
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
7. To query by month use:
```python
scrap.query_by_month(request_delay=1, month_delay=60, market="all", days="all", max_try=2)
```
`request_delay`: delay every request/ every market
`month_delay`: delay every month
`max_try`: maximum number of retries if error occurs
