from flask import Blueprint, request, g
from flask import jsonify as js, jsonify
from api.v1.users import auth

expense = Blueprint('expense', __name__)

@expense.route('/dfs_from_statements')
@auth.login_required
def loads_expenses_dfs():
    """
    Loads expenditure from dataframes.
    ---
    tags:
        - Expenses
    responses:
        200:
            description: OK!
        404:
            description: error occured.
    params:
        description: None
    """
    from models import find_statement, pattern, pathdir, Expense, session
    statements = find_statement(pattern, pathdir)
    # NotImplemented for more than one statements.
    dfs = tabula.read_pdf(statements[0],
                        password=pass_in, silent=True,
                        lattice=True, pages='all')
    for df in dfs:
        payments = df.loc[[x for x in df.index if df.loc[x, 'Details'].startswith(
                'Merchant Payment') or dfs[1].loc[x, 'Details'].startswith('Pay Bill')]]
    payments.dropna(axis=1).to_sql(name='_expenses',
                    con=session.bind, if_exists='append', index=False)
    return {'message': 'OK'}

@expense.route('/add/<int:user_id>', methods=['POST'])
@auth.login_required
def add_expense(user_id):
    """
    Adds an expenditure linked to a specific user 
    to the database.
    ---
    tags:
        - Expenses
    responses:
        200:
            description: expense add, OK!
        404:
            description: error.
    params:
        description: user_id foreign key from user table.
    """
    from models import Expense, session
    try:
        if not request.is_json:
            raise Exception
        r = request.json
        category = r.get('category')
        description = r.get('description')
        name = r.get('name')
        amount_spent = r.get('amount')
        new = Expense(user_id=g.user.id,
                        category=category,
                        description=description,
                        name=name,
                        amount=amount_spent
                    )
        session.add(new)
        session.commit()
        return {'message': 'OK'}
    except Exception as e:
        return {'message': 'error adding an expenditure'}

@expense.route('/delete/<string:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """
    Deletes an expenditure from the database if it exists,
    otherwise return an error.
    ---
    tags:
        - Expenses
    responses:
        200:
            description: expense delete, OK!
        404:
            description: error with the delete request.
    params:
        description: expenditure_id
    """
    try:
        from models import Expense, session
        expense = session.query(Expense).filter_by(id=expense_id).first()
        if not expense:
            return {'message': 'expense does not exist!'}
        session.delete(expense)
        session.commit()
        return {'message': 'OK'}
    except Exception as e:
        return {"message": "an error occured!"}

@expense.route('/expenses', methods=['GET'])
@auth.login_required
def user_expenses():
    """
    Queries the database and returns all expenses of a
    user of any.
    ---
    tags:
        - Expenses
    responses:
        200:
            description: List of expenses for a user.
        404:
            description: No expenses for this user.
    params:
        description: user_id of the user.
    """
    from models import Expense, session
    expenses = session.query(Expense).filter_by(user_id=g.user.id).all()
    if expenses:
        return {"expenses": [k.to_dict() for k in expenses]}
    return {'message': 'no expenses for this user'}


@expense.route('/update/<string:expense_id>', methods=['UPDATE'])
@auth.login_required
def update_expense(expense_id):
    """
    Updates a user expenditure if it exists, otherwise
    return an error.
    ---
    tags:
        - Expenses
    responses:
        200:
            description: user expenditure update, OK!
        404:
            description: error updating an expense.
    Params:
        description: expense_id
    """
    from models import Expense, session
    try:
        if not request.is_json:
            raise Exception
        update_info = request.get_json()
        session.query(Expense).filter_by(id=expense_id).update(update_info)
        session.commit()
        return {"message": "OK"}
    except Exception as e:
        return {'message': 'An error occured!'}

@expense.route('/expense/<string:expense_id>', methods=['GET'])
@auth.login_required
def expenditure(expense_id):
    """
    Return a specific expenditure
    ---
    tags:
        - Expenses
    responses:
        200:
            description: return a specific expenditure.
        404:
            description: expense does not exist.
    params:
        description: expense_id
    """
    from models import Expense, session
    try:
        e = session.query(Expense).filter_by(id=expense_id).first()
        print(e)
        if e is None:
            return {'error': 'expense does not exist!'}
        return {"expense": e.to_dict()}
    except Exception as err:
        return {"error": "{}".format(err)}
