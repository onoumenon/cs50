This week's pset is relatively simple, in the sense that it doesn't use any complex algorithms. 

The skeleton is already provided, and we are expected to finish the implementations for application.py, the html pages, and the sql database.
It is a little more tedious to debug due to the interplay of database, html, and the python code (MVC model).
I would write down what I name my variables and have a clearer idea of my MVC structure if I do it from scratch next time.


# Things of note:
SQL Injection: https://www.w3schools.com/sql/sql_injection.asp

# Password hash: 
from werkzeug.security import check_password_hash, generate_password_hash


# Using Jinja:
              {% for stock in stocks%}
              <option value="{{ stock.symbol }}">{{ stock.symbol }}</option>
              {% endfor %}
              
             

# Resources:
Flask: https://www.youtube.com/embed/X0dwkDh8kwA?autoplay=1&rel=0

MVC: https://www.youtube.com/embed/Fr4P6FkZUTE?autoplay=1&rel=0

SQL:https://www.youtube.com/embed/AywtnUjQ6X4?autoplay=1&rel=0
