# Cash0la - But where does your cash go?  
  
A simple budgeting tool to keep track users expenditure.  
TracePesa aims to log users' expenditures from various payments platforms.  
  
For a start, we're making it possible to trace expenditures logged on Mpesa  
- Lipa na Mpesa options of:  
- Till Number & Paybill  

Next, we'll look into the various mobile wallets and maybe trace crypto.  
  
## SETUP  

Create a virtual environment.  
```
$ python -m venv .venv  
```

```
$ pip3 install -r requirements.txt  
```

## RUN  

```
$ export FLASK_APP=app.py  
$ flask run --debug  
```

## ROUTES  

All routes require authentication as such, request for an authentication  
token first before accessing further URIs  
- `GET /api/v1/access/token`: returns an access token with max_age, expire_in after sometime.  
  
- `POST /api/v1/signup`: creates a new user with specified params(email, password, username, name).  
- `POST /api/v1/expense/add`: adds a user expenditure.  
- `DELETE /api/v1/expense/remove/int:expense_id>`: deletes an expenditure.
- `GET /api/v1/expenses/<int:user_id>`: retrieves all expenses for a user.
- `PUT /api/v1/expense/update/<int:expense_id>`: updates an expenditure.
- `PUT /api/v1/reset_password:<int>`: resets user password(params: {email, newpassword})
- `GET /api/v1/users`: retrieves all users in the database
