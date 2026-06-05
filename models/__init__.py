from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine
import tabula
from typing import List
import os
from fnmatch import fnmatchcase

Base = declarative_base()

from .user import User
from .expense import Expense
from app import app

engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))

Base.metadata.create_all(engine)
session_f = sessionmaker(bind=engine)
session = scoped_session(session_f)
Base.query = session.query_property()

# load expenditure details from messages or from Mpesa statements
# check with SMS Retriever API or Listen for Incoming messages
# else:
# load from statements

def find_statement(statement_pattern: str, pathdir: str) -> List:
    """
    Scans pathdir for an Mpesa statement.

    Params:
    :statement: Mpesa statement name.
    :pathdir: directory to scan for the Mpesa statement.

    Return:
    Returns location of Mpesa statement.
    """
    statements = []
    for dp, dn, fn in os.walk(pathdir):
        for f in fn:
            if fnmatchcase(f, statement_pattern):
                statements.append(os.path.join(dp, f))
    return statements

# prerequisites for statements' lookup
pattern=os.getenv('STATEMENT_NAME')
pathdir=os.getenv('STATEMENT_DIR')
pass_in=os.getenv('STATEMENT_PASSWD')
