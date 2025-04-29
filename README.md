# 💊 RxRewards – Medical Store Loyalty System

RxRewards is a loyalty program web platform tailored for medical supply stores. It enables administrators to manage customer data, track purchase activity, configure loyalty discounts, and maintain product records — all from a centralized dashboard.

🔐 Note: This system is built for admin-only access.

---

# 🚀 Features

🧑‍⚕️ Customer Management  
 Add, edit, delete, and view customer details including loyalty points

💊 Product Management  
 Maintain a database of medical products with pricing and categories

🛒 Purchase Tracking  
 Record and manage detailed purchase histories for customers

💸 Discount Management  
 Create and configure discount schemes based on eligibility criteria

📊 Admin Dashboard  
 Visual overview of purchases, customers, and loyalty statistics

📄 About Page  
 Informational section about the RxRewards program

🔐 Admin Authentication  
 Secured login access for store administrators

---

# 🛠️ Prerequisites

Python 3.8+
SQLite3 (bundled with Python)
A modern web browser

---

📦 Installation

Clone the repository:

git clone https://github.com/msuryawanshi05/Loyalty-Based-Discount-System.gitt
cd rxrewards

Create a virtual environment and activate it:
python -m venv venv
venv\Scripts\activate # On Windows

Install required packages:
pip install -r requirements.txt

Initialize the database:
python database.py

Start the Flask application:
python app.py

Access the system at:
👉 http://localhost:5000

🔐 Usage
Log in with:

Username: admin
Password: password

Available operations:

View dashboard stats
Manage customers (IDs auto-generated)
Manage products (ProductName used as ID)
Record/view/edit/delete purchases
Configure and assign discounts
Read about RxRewards in the About section

💡 All prices are displayed in Indian Rupees (₹)

📁 Data is stored in rxrewards.db (SQLite)

🗃️ Database Schema

Customer (CustomerID, Name, Email, Phone, LoyaltyPoints, TotalPurchase)
Product (ProductName, Category, Price)
Purchase (PurchaseID, CustomerID, ProductName)
PurchaseDetail (PurchaseDetailID, PurchaseID, PurchaseDate, TotalAmount)
Discount (DiscountID, DiscountType, EligibilityCriteria, Percentage)

⚠️ Security Note
This is a basic prototype and not production-ready.
Before deployment:
Implement proper admin auth (e.g., Flask-Login, hashed passwords)
Use HTTPS in production
Add CSRF protection and input validation
Schedule regular database backups

📜 License
This project is open-source and available under the MIT License.

🧑‍💻 Author
Mukul Suryawanshi
