import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import apology, login_required, lookup, usd, get_time, check_password
from flask_session import Session


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    prtflo = db.execute('''SELECT * FROM portfolios WHERE user_id = ?''', user_id)
    cash_left = db.execute('''SELECT cash FROM users WHERE id = ?''', user_id)

    if cash_left and "cash" in cash_left[0]:
        cash_left = float(cash_left[0]["cash"])
    else:
        cash_left = 0.0

    tamount = cash_left

    try:
        for stock in prtflo:
            symbol = s["symbol"]
            stock_info = lookup(symbol)

            current_price = float(stock_info["price"])
            stock_value = current_price * stock["shares"]

            stock.update({"current_price": current_price, "stock_value": stock_value})
            tamount += float(stock["stock_value"])
    except (ValueError, LookupError):
        return apology("Sorry, can't update stock prices!")

    return render_template("index.html", portfolio=prtflo, cash_left=cash_left, total_amount=tamount)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        user_id = session["user_id"]

        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = request.form.get("shares")

        if not symbol or not stock:
            return apology("Symbol invalid!")

        if not shares.isdigit():
            return apology("Enter a positive digit for number of symbol!")

        transaction_value = int(shares) * stock["price"]
        user_cash = db.execute('''SELECT cash FROM users WHERE id = ?''', user_id)
        user_cash = user_cash[0]["cash"]

        if user_cash < transaction_value + 1:
            return apology("Sorry, Not enough money!", 401)

        update_cash_user = user_cash - transaction_value
        db.execute('''UPDATE users SET cash = ? WHERE id = ?''', update_cash_user, user_id)

        balance = f"${update_cash_user:,.2f} (-${transaction_value:,.2f})"

        db.execute('''INSERT INTO portfolios (user_id, name, symbol, shares, paid_price, current_price, date, stock_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', user_id, stock["name"], symbol, shares, stock["price"], stock["price"], get_time(), stock["price"])

        db.execute('''INSERT INTO history (user_id, name, symbol, shares, action, balance, date) VALUES (?, ?, ?, ?, ?, ?, ?)''', user_id, stock["name"], symbol, shares, "BOUGHT", balance, get_time())

        flash(f"Successfully bought {shares} shares of {symbol}!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    user_id = session["user_id"]
    prtflo = db.execute('''SELECT * FROM history WHERE user_id = ?''', user_id)

    return render_template("history.html", portfolio = prtflo)

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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
        s = lookup(str(request.form.get("symbol")))

        if not stock:
            return apology("Symbol in not valid!")

        stock["price"] = usd(stock["price"])

        return render_template("quoted.html", stock=s)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        urnm = request.form.get('username')
        pss = request.form.get('password')
        cnfm = request.form.get('confirmation')

        if not urnm:
            return apology('Username is empty!')
        elif not pss:
            return apology('Password is empty!')
        elif not cnfm:
            return apology('You must confirm your password!')

        if pss != cnfm:
            return apology('Incorrect!')

        hash = generate_password_hash(pss)

        try:
            db.execute('''INSERT INTO users (username, hash) VALUES (?, ?)''', urnm, hash)
            return redirect('/')
        except:
            return apology('Username used before!')
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]
    prtflo = db.execute('''SELECT * FROM portfolios WHERE user_id = ?''', user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        shares = int(request.form.get("shares"))

        owned_stock = db.execute('''SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?''', user_id, symbol)

        if not owned_stock:
            return apology(f"You don't own any shares of {symbol}!")

        current_shares = sum([stock["shares"] for stock in owned_stock])
        if current_shares < shares:
            return apology("You don't have enough shares to sell!")

        cash = db.execute('''SELECT cash FROM users WHERE id = ?''', user_id)
        cash = cash[0]["cash"]
        current_price = stock["price"]
        cash += shares * current_price

        for i in owned_stock:
            if i["shares"] > shares:
                db.execute('''UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?''', i["shares"] - shares, user_id, symbol)
            else:
                db.execute('''DELETE FROM portfolios WHERE user_id = ? AND symbol = ?''', user_id, symbol)

        b = f"${cash:,.2f} (+${(shares * current_price):,.2f})"

        db.execute('''UPDATE users SET cash = ? WHERE id = ?''', cash, user_id)

        db.execute('''INSERT INTO history (user_id, name, symbol, shares, action, balance, date) VALUES (?, ?, ?, ?, ?, ?, ?)''', user_id, stock["name"], symbol, shares, "SOLD", b, get_time())

        flash(f"Successfully sold {shares} shares of {symbol}!")
        return redirect("/")

    return render_template("sell.html", portfolio = prtflo)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit funds to account."""

    if request.method == "POST":
        user_id = session["user_id"]

        amount = int(request.form.get("sum"))
        acc = db.execute('''SELECT * FROM users WHERE id = ?''', user_id)

        check_password(acc[0]["hash"], request.form.get("password"))

        cash = acc[0]["cash"] + amount
        db.execute('''UPDATE users SET cash = ? WHERE id = ?''', cash, user_id)

        flash(f"Successfully added ${amount} to your balance!")
        return redirect("/")

    return render_template("deposit.html")


@app.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    """Withdraw funds from account."""

    if request.method == "POST":
        user_id = session["user_id"]

        amount = int(request.form.get("sum"))
        acc = db.execute('''SELECT * FROM users WHERE id = ?''', user_id)

        check_password(acc[0]["hash"], request.form.get("password"))

        if amount > acc[0]["cash"]:
            return apology("Can't withdraw more than cash left!")

        cash = acc[0]["cash"] - amount
        db.execute('''UPDATE users SET cash = ? WHERE id = ?''', cash, user_id)

        flash(f"Successfully withdrew ${amount} from your balance!")
        return redirect("/")

    return render_template("withdraw.html")
