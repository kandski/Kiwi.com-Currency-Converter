[Kiwi.com] Currency converter task
===
## What it is?
- Python 3.6 based CLI app with web API, based on Flask 0.12


## What it does?
- Parses input parameters and returns JSON object with values according to amount and currency

## What does it needs?
- All needed requirements are printed in ```requirements.txt```
- Web API is based on __Flask__
- Acquiring currency rates uses asynchronous requests from __aiohttp__
- Acquiring currency symbols uses 3rd party library named __forex-python__
- SQLite database is built by __sqlalchemy__

## How can i install requirements

`pip install -r requirements.txt`
- __Python 3.6 with pip-tools__ is expected to be installed

## Where do currency rates get from?
- Rates are gathered from open-source web API [fixer.io]
- Rates are published by European Central Bank daily
- Use ```update``` parameter to update currency rates once a day as described in examples

## Which currencies are supported?
- Currency rates are acquired from ECB (European Central Bank)

| Currency code | Currency symbol |
| :------------:|:-------------:|
|USD | US$ |
| JPY| ¥ |
| BGN| BGN |
|CZK |  Kč|
| DKK| Kr |
| EUR| € |
| GBP| £ |
| HUF| Ft |
| PLN|  zł|
| RON| L |
| SEK| kr |
| CHF|  Fr.|
| NOK|kr|
| HRK| kn |
| RUB|  R|
| TRY|  TRY|
| AUD| $ |
| BRL|  R$|
| CAD| $ |
| CNY| ¥ |
| HKD| HK$ |
| IDR| Rp |
| ILS|  ₪|
| INR| ₹ |
| KRW| W |
| MXN|$ |
| MYR| RM |
| NZD|  NZ$|
| PHP| ₱ |
| SGD| S$ |
| THB| ฿|
|  ZAR| R|

## How can I run it?
- On first run please update database

### CLI app example
- Parameters which are required:
    - `--input_currency XXX`
    - `--amount <float>`
- Optional parameters:
    - `--output_currency YYY`
    - `-h --help`
    - `-u --update`
- If output part is empty, please run database update or you have entered unsupported currency
- Supported currencies you can find in Currency table
- Currency codes are __case-sensitive__
#### Run in shell
```
python3 converter.py --amount 99 --input_currency USD
```
```
{
    "input": {
        "amount": 99.0,
        "currency": "USD"
    },
    "output": {
        "AUD": "125.75",
        "BGN": "159.53",
        "BRL": "317.78",
        "CAD": "123.94",
        "CHF": "96.14",
        "CNY": "639.64",
        "CZK": "2081.67",
        "DKK": "607.58",
        "GBP": "72.58",
        "HKD": "774.60",
        "HRK": "607.32",
        "HUF": "25183.62",
        "IDR": "1319769.00",
        "ILS": "336.65",
        "INR": "6296.50",
        "JPY": "11001.87",
        "KRW": "105187.50",
        "MXN": "1892.09",
        "MYR": "393.61",
        "NOK": "787.87",
        "NZD": "136.43",
        "PHP": "4987.42",
        "PLN": "340.32",
        "RON": "378.18",
        "RUB": "5604.39",
        "SEK": "802.23",
        "SGD": "131.35",
        "THB": "3165.03",
        "TRY": "371.84",
        "ZAR": "1227.40",
        "EUR": "81.57"
    }
}
```

```
python converter.py --amount 99 --input_currency USD --update
```
```
{
  "database": "was updated"
}
```
 or when database rates was updated today
```
{
  "database": "is valid"
}

```

### web API example

- If output part is empty, please run database update or you have entered unsupported currency
- Supported currencies you can find in Currency table
- Currency codes are __case-sensitive__
#### Run flask API
```FLASK_APP=run.py flask run```
#### Check 
``` localhost:5000/currency_converter?amount<float>&input_currency=XXX&output_currency=YYY```
```
GET /currency_converter?amount=99&input_currency=EUR&output_currency=JPY HTTP/1.1
```
```
{
  "input": {
    "amount": 99.0,
    "currency": "EUR"
  },
  "output": {
    "JPY": "13353.12"
  }
}
```
```
GET /update HTTP/1.1
```
```
{
  "database": "was updated"
}
```
 or when database rates was updated today
```
{
  "database": "is valid"
}

```

### Known malfunctions
- In CLI all __required__ arguments have to be entered to update database



[Kiwi.com]: http://www.kiwi.com/
[fixer.io]: http://fixer.io
