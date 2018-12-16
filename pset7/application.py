import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    # Select stocks
    portfolio=db.execute("SELECT shares, symbol FROM portfolio WHERE id=:id", id=session["user_id"])

    # Update prices and total
    total= 0
    for pstock in portfolio:
        symbol=pstock["symbol"]
        shares=pstock["shares"]
        stock=lookup(symbol)
        value= shares * stock["price"]
        total += value
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", price=usd(stock["price"]),total=usd(total),id=session["user_id"],symbol=symbol)

    # Update user's cash
    current_cash = db.execute ("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    total += current_cash[0]["cash"]

    # Display on page
    current = db.execute("SELECT * from portfolio where id=:id", id=session["user_id"])

    return render_template("index.html", stocks=current, cash=usd(current_cash[0]["cash"]), total=usd(total))



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
         # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Must provide symbol")

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("Must provide shares")

        # Ensure symbol is valid
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("Invalid symbol")

        # Ensure shares is valid

        try:
            shares = int(request.form.get("shares"))
            if shares <1:
                return apology ("Shares must be greater than or equal to 1")
        except:
            return apology("Shares must be a positive integer")

        # Ensure cash is enough for shares
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        if not cash or float(cash[0]["cash"]) < stock["price"] * shares:
            return apology("Cash not enough")

        # Check user's stock
        user_stocks = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol", id=session["user_id"], symbol=stock["symbol"])

        # If stocks exist, increment it
        if user_stocks:
           total_shares = user_stocks[0]["shares"]+shares
           db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", shares=total_shares, id=session["user_id"], symbol=stock["symbol"])
            # Else, create new stock
        else:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol,:id)", name=stock["name"],shares=shares, price=usd(stock["price"]), total=usd(shares*stock["price"]), symbol=stock["symbol"], id=session["user_id"])

        # Deduct cost from cash
        db.execute("UPDATE users SET cash = cash-:buyorder WHERE id=:id", id=session["user_id"], buyorder=stock["price"] * shares)

        # Add to histories
        db.execute("INSERT INTO histories (symbol, shares, price, id, timestamp) VALUES(:symbol, :shares, :price, :id, CURRENT_TIMESTAMP)", symbol=stock["symbol"],shares=shares, price=usd(stock["price"]), id=session["user_id"])

        # Return
        return redirect("/")


    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories=db.execute("SELECT symbol, shares, price, timestamp from histories WHERE id=:id", id=session["user_id"])

    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        result = lookup(request.form.get("symbol"))

        if not result:
            return apology("Symbol not found")

        return render_template("quoted.html", stock=result)

    else:
        return render_template("quote.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # Ensure passwords match
        elif request.form.get("password") != request.form.get("password2"):
            return apology("Passwords do not match!")

        # Insert username and password into database
        result = db.execute("INSERT INTO users(username, hash) Values(:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(request.form.get("password")))

        # Ensure username isn't a duplicate
        if not result:
            return apology("Username already taken.")

        # Store result in session
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    portfolio=db.execute("SELECT shares, symbol FROM portfolio WHERE id=:id", id=session["user_id"])

    # Update prices and total
    total= 0
    for pstock in portfolio:
        symbol=pstock["symbol"]
        shares=pstock["shares"]
        stock=lookup(symbol)
        value= shares * stock["price"]
        total += value
        db.execute("UPDATE portfolio SET price=:price, total=:total WHERE id=:id AND symbol=:symbol", price=usd(stock["price"]),total=usd(total),id=session["user_id"],symbol=symbol)

    # Update user's cash
    current_cash = db.execute ("SELECT cash FROM users WHERE id=:id", id=session["user_id"])

    total += current_cash[0]["cash"]

    # Display on page
    current = db.execute("SELECT * from portfolio where id=:id", id=session["user_id"])

    if request.method == "POST":

        # Ensure symbol is valid
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("Invalid symbol")

        # Ensure shares is valid

        try:
            shares = int(request.form.get("shares"))
            if shares <1:
                return apology ("Shares must be greater than or equal to 1")
        except:
            return apology("Shares must be a positive integer")


        # Check user's stock
        user_stocks = db.execute("SELECT shares FROM portfolio WHERE id=:id AND symbol=:symbol", id=session["user_id"], symbol=stock["symbol"])

        # If enough stock exist, decrement stock
        if not user_stocks or int(user_stocks[0]["shares"]) < shares:
            return apology("Not enough shares to sell.")

        sharehist = 0-shares

        # Add to histories
        db.execute("INSERT INTO histories (symbol, shares, price, id, timestamp) VALUES(:symbol, :shares, :price, :id, CURRENT_TIMESTAMP)", symbol=stock["symbol"], shares=sharehist, price=usd(stock["price"]), id=session["user_id"])

        # Add to cash
        db.execute("UPDATE users SET cash= cash+:sellorder WHERE id = :id", id=session["user_id"], sellorder=stock["price"]*shares)


        user_stocks = user_stocks[0]["shares"] - shares

        # If no stocks left after decrement, delete symbol
        if user_stocks == 0:
            db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol", id= session["user_id"], symbol = stock["symbol"])

        # Else, update stock
        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol", shares=user_stocks, id=session["user_id"], symbol=stock["symbol"])


        # Return
        return redirect("/")


    else:
        return render_template("sell.html", stocks=current, cash=usd(current_cash[0]["cash"]), total=usd(total))


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
