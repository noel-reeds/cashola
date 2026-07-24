# skrilla - discover your spending habits.  

## Background  
Skrilla aims to track users' spending habits to minimise impulse buying and explore users' saving opportunities.  

Skilla aims to achieve this with various mobile payments platforms.  
  
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
