# Cash0la - But where does your cash go?  
  
A simple budgeting tool to keep track users expenditure.  
TracePesa aims to log users' expenditures from various payments platforms.  
  
For a start, we're making it possible to trace expenditures logged on Mpesa  
- Lipa na Mpesa options of:  
- Till Number & Paybill  

Next, we'll look into the various mobile wallets and maybe trace crypto.  
  
## Setup  

Create a virtual environment.  
```
$ python -m venv .venv  
```

```
$ pip3 install -r requirements.txt  
```

## Run  

```
$ export FLASK_APP=app.py  
$ flask run --debug  
```

## Visualize with swagger UI  
On your browser, go to `http://localhost:5000/apidocs/` to view api documentation.  
  
xx  
