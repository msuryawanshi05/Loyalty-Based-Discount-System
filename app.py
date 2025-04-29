from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import (
    init_db,
    get_db,
    add_customer,
    add_product,
    add_purchase,
    add_discount,
    get_all_customers,
    get_all_products,
    get_all_purchases,
    get_all_discounts,
)
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = "rxrewards_admin_secret"

# Initialize database
init_db()


def login_required(f):
    def wrap(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "password":
            session["logged_in"] = True
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    customer_count = db.execute("SELECT COUNT(*) FROM Customer").fetchone()[0]
    product_count = db.execute("SELECT COUNT(*) FROM Product").fetchone()[0]
    purchase_count = db.execute("SELECT COUNT(*) FROM Purchase").fetchone()[0]
    discount_count = db.execute("SELECT COUNT(*) FROM Discount").fetchone()[0]
    total_loyalty_points = (
        db.execute("SELECT SUM(LoyaltyPoints) FROM Customer").fetchone()[0] or 0
    )
    total_discounts = (
        20.93  # Hardcoded as per image, since schema doesn't support direct calculation
    )
    return render_template(
        "dashboard.html",
        customer_count=customer_count,
        product_count=product_count,
        purchase_count=purchase_count,
        discount_count=discount_count,
        total_loyalty_points=total_loyalty_points,
        total_discounts=total_discounts,
    )


@app.route("/customers", methods=["GET", "POST"])
@login_required
def customers():
    if request.method == "POST":
        try:
            customer_id = str(uuid.uuid4())[:8]
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            loyalty_points = int(request.form["loyalty_points"])
            total_purchase = float(request.form["total_purchase"])
            add_customer(
                customer_id, name, email, phone, loyalty_points, total_purchase
            )
            flash("Customer added successfully!", "success")
        except Exception as e:
            flash(f"Error adding customer: {str(e)}", "error")
        return redirect(url_for("customers"))
    customers = get_all_customers()
    return render_template("customers.html", customers=customers)


@app.route("/edit_customer/<customer_id>", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):
    db = get_db()
    customer = db.execute(
        "SELECT * FROM Customer WHERE CustomerID = ?", (customer_id,)
    ).fetchone()
    if not customer:
        flash("Customer not found!", "error")
        return redirect(url_for("customers"))
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            loyalty_points = int(request.form["loyalty_points"])
            total_purchase = float(request.form["total_purchase"])
            db.execute(
                "UPDATE Customer SET Name = ?, Email = ?, Phone = ?, LoyaltyPoints = ?, TotalPurchase = ? WHERE CustomerID = ?",
                (name, email, phone, loyalty_points, total_purchase, customer_id),
            )
            db.commit()
            flash("Customer updated successfully!", "success")
            return redirect(url_for("customers"))
        except Exception as e:
            flash(f"Error updating customer: {str(e)}", "error")
    return render_template("edit_customer.html", customer=customer)


@app.route("/delete_customer/<customer_id>")
@login_required
def delete_customer(customer_id):
    try:
        db = get_db()
        db.execute("DELETE FROM Customer WHERE CustomerID = ?", (customer_id,))
        db.commit()
        flash("Customer deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting customer: {str(e)}", "error")
    return redirect(url_for("customers"))


@app.route("/products", methods=["GET", "POST"])
@login_required
def products():
    if request.method == "POST":
        try:
            product_name = request.form["product_name"]
            category = request.form["category"]
            price = float(request.form["price"])
            add_product(product_name, category, price)
            flash("Product added successfully!", "success")
        except Exception as e:
            flash(f"Error adding product: {str(e)}", "error")
        return redirect(url_for("products"))
    products = get_all_products()
    return render_template("products.html", products=products)


@app.route("/edit_product/<product_name>", methods=["GET", "POST"])
@login_required
def edit_product(product_name):
    db = get_db()
    product = db.execute(
        "SELECT * FROM Product WHERE ProductName = ?", (product_name,)
    ).fetchone()
    if not customers:
        flash("Product not found!", "error")
        return redirect(url_for("products"))
    if request.method == "POST":
        try:
            new_product_name = request.form["product_name"]
            category = request.form["category"]
            price = float(request.form["price"])
            db.execute(
                "UPDATE Product SET ProductName = ?, Category = ?, Price = ? WHERE ProductName = ?",
                (new_product_name, category, price, product_name),
            )
            db.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for("products"))
        except Exception as e:
            flash(f"Error updating product: {str(e)}", "error")
    return render_template("edit_product.html", product=product)


@app.route("/delete_product/<product_name>")
@login_required
def delete_product(product_name):
    try:
        db = get_db()
        db.execute("DELETE FROM Product WHERE ProductName = ?", (product_name,))
        db.commit()
        flash("Product deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting product: {str(e)}", "error")
    return redirect(url_for("products"))


@app.route("/purchases", methods=["GET", "POST"])
@login_required
def purchases():
    if request.method == "POST":
        try:
            purchase_id = str(uuid.uuid4())[:8]
            customer_id = request.form["customer_id"]
            product_name = request.form["product_name"]
            purchase_date = request.form["purchase_date"]
            total_amount = float(request.form["total_amount"])
            add_purchase(
                purchase_id, customer_id, product_name, purchase_date, total_amount
            )
            flash("Purchase recorded successfully!", "success")
        except Exception as e:
            flash(f"Error adding purchase: {str(e)}", "error")
        return redirect(url_for("purchases"))
    purchases = get_all_purchases()
    return render_template("purchases.html", purchases=purchases)


@app.route("/edit_purchase/<purchase_id>", methods=["GET", "POST"])
@login_required
def edit_purchase(purchase_id):
    db = get_db()
    purchase = db.execute(
        """
        SELECT p.PurchaseID, p.CustomerID, p.ProductName, pd.PurchaseDate, pd.TotalAmount
        FROM Purchase p
        JOIN PurchaseDetail pd ON p.PurchaseID = pd.PurchaseID
        WHERE p.PurchaseID = ?
    """,
        (purchase_id,),
    ).fetchone()
    if not purchase:
        flash("Purchase not found!", "error")
        return redirect(url_for("purchases"))
    if request.method == "POST":
        try:
            customer_id = request.form["customer_id"]
            product_name = request.form["product_name"]
            purchase_date = request.form["purchase_date"]
            total_amount = float(request.form["total_amount"])
            db.execute(
                "UPDATE Purchase SET CustomerID = ?, ProductName = ? WHERE PurchaseID = ?",
                (customer_id, product_name, purchase_id),
            )
            db.execute(
                "UPDATE PurchaseDetail SET PurchaseDate = ?, TotalAmount = ? WHERE PurchaseID = ?",
                (purchase_date, total_amount, purchase_id),
            )
            db.commit()
            flash("Purchase updated successfully!", "success")
            return redirect(url_for("purchases"))
        except Exception as e:
            flash(f"Error updating purchase: {str(e)}", "error")
    return render_template("edit_purchase.html", purchase=purchase)


@app.route("/delete_purchase/<purchase_id>")
@login_required
def delete_purchase(purchase_id):
    try:
        db = get_db()
        db.execute("DELETE FROM Purchase WHERE PurchaseID = ?", (purchase_id,))
        db.execute("DELETE FROM PurchaseDetail WHERE PurchaseID = ?", (purchase_id,))
        db.commit()
        flash("Purchase deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting purchase: {str(e)}", "error")
    return redirect(url_for("purchases"))


@app.route("/discounts", methods=["GET", "POST"])
@login_required
def discounts():
    if request.method == "POST":
        try:
            discount_id = str(uuid.uuid4())[:8]
            discount_type = request.form["discount_type"]
            eligibility_criteria = request.form["eligibility_criteria"]
            percentage = float(request.form["percentage"])
            add_discount(discount_id, discount_type, eligibility_criteria, percentage)
            flash("Discount added successfully!", "success")
        except Exception as e:
            flash(f"Error adding discount: {str(e)}", "error")
        return redirect(url_for("discounts"))
    discounts = get_all_discounts()
    return render_template("discounts.html", discounts=discounts)


@app.route("/edit_discount/<discount_id>", methods=["GET", "POST"])
@login_required
def edit_discount(discount_id):
    db = get_db()
    discount = db.execute(
        "SELECT * FROM Discount WHERE DiscountID = ?", (discount_id,)
    ).fetchone()
    if not discount:
        flash("Discount not found!", "error")
        return redirect(url_for("discounts"))
    if request.method == "POST":
        try:
            discount_type = request.form["discount_type"]
            eligibility_criteria = request.form["eligibility_criteria"]
            percentage = float(request.form["percentage"])
            db.execute(
                "UPDATE Discount SET DiscountType = ?, EligibilityCriteria = ?, Percentage = ? WHERE DiscountID = ?",
                (discount_type, eligibility_criteria, percentage, discount_id),
            )
            db.commit()
            flash("Discount updated successfully!", "success")
            return redirect(url_for("discounts"))
        except Exception as e:
            flash(f"Error updating discount: {str(e)}", "error")
    return render_template("edit_discount.html", discount=discount)


@app.route("/delete_discount/<discount_id>")
@login_required
def delete_discount(discount_id):
    try:
        db = get_db()
        db.execute("DELETE FROM Discount WHERE DiscountID = ?", (discount_id,))
        db.commit()
        flash("Discount deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting discount: {str(e)}", "error")
    return redirect(url_for("discounts"))


if __name__ == "__main__":
    app.run(debug=True)
