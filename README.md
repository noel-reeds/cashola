# But where does your cash go?  
## Cashola, lets you find out!  
  
A simple budgeting tool to keep track users expenditure.  
Cashola aims to log users' expenditures from various payments platforms.  
  
For a start, we're making it possible to trace expenditures logged on Mpesa  
- Lipa na Mpesa options of:  
- Till Number & Paybill  

Next, we'll look into the various mobile wallets and maybe trace crypto.  
  
## Basic SET UP for development purposes only.  

Create a virtual environment.  
```
$ python -m venv .venv  
```

```
$ pip3 install -r requirements.txt  
```

## Run  
Set the ```FLASK_APP``` environment variable.  
```
$ export FLASK_APP=app.py  

$ flask run --debug  
```  
## Use a production WSGI server instead  
```
waitress-serve --port=8080 --call app:setup
```

## Visualize with swagger UI  
On your browser, go to [api docs](https://cashola.onrender.com/apidocs/) to view api documentation.  

reach out to me on [Twitter](https://x.com/noelreeds)  
xx  
