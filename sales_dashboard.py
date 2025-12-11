import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from datetime import datetime
import random, os, csv
from faker import Faker
from config import get_connection
from report_generator import create_pdf_report

# -------------------------------------------------------------------------
# SQL Runner
# -------------------------------------------------------------------------
def run_sql(sql, params=None):
    conn = get_connection()
    df = pd.read_sql(sql, conn, params=params)
    conn.close()
    return df
# ------------------------------------------------------------------------
# Automatic Sample Data Seeder 
# -------------------------------------------------------------------------
def seed_database(n_customers=500, n_orders=2000):
    """
    Inserts sample(fake) data into customers and orders table.
    Runs only once – comment it after your DB is filled.
    """
    fake = Faker()
    conn = get_connection()
    cursor = conn.cursor()

    print("\n📌 Seeding Database with Sample Data...")

    # ---------------- Insert Customers ----------------
    for i in range(1, n_customers + 1):
        name = fake.name()
        city = random.choice(["Chennai","Delhi","Mumbai","Hyderabad","Bangalore","Pune","Kolkata","Kochi"])
        try:
            cursor.execute("INSERT INTO customers (customer_id, customer_name, city) VALUES (:1, :2, :3)",
                           (i, name, city))
        except:
            pass    # skips if already exists

    conn.commit()
    print(f"✔ Inserted {n_customers} customers")

    # ---------------- Insert Orders ----------------
    order_id = 1
    for _ in range(n_orders):
        cid = random.randint(1, n_customers)
        amount = random.randint(500, 100000)
        date = fake.date_between(start_date='-150d', end_date='today')
        try:
            cursor.execute("INSERT INTO orders (order_id, customer_id, order_amount, order_date) VALUES (:1, :2, :3, :4)",
                           (order_id, cid, amount, date))
            order_id += 1
        except:
            pass

    conn.commit()
    conn.close()

    print(f"✔ Inserted {n_orders} orders\n")
    print("🔥 Sample data added successfully! You can now run dashboard analytics.\n")

#seed_database(500, 2000)     

# -------------------------------------------------------------------------
# Data Fetch Functions
# -------------------------------------------------------------------------

def top_customers(limit=10):
    query = f"""
        SELECT c.customer_id, c.name AS customer_name, c.city,
               SUM(o.total_amount) AS total_spent
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_id, c.name, c.city
        ORDER BY total_spent DESC
        FETCH FIRST {limit} ROWS ONLY
    """
    df = run_sql(query)
    print("\n🏆 TOP CUSTOMERS")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    return df


def city_revenue(min_amt=150000):
    query = """
        SELECT c.city, SUM(o.total_amount) AS total_revenue
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        GROUP BY c.city
        HAVING SUM(o.total_amount) > :amt
        ORDER BY total_revenue DESC
    """
    df = run_sql(query, {"amt": min_amt})
    print(f"\n🏙 CITY REVENUE (> {min_amt})")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    return df


def monthly_revenue():
    query = """
        SELECT TO_CHAR(order_date,'YYYY-MM') AS month,
               SUM(total_amount) AS revenue
        FROM orders
        GROUP BY TO_CHAR(order_date,'YYYY-MM')
        ORDER BY month
    """
    df = run_sql(query)
    print("\n📅 MONTHLY REVENUE")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    return df


def best_selling_products(limit=10):
    query = f"""
        SELECT p.product_id, p.name AS product_name,
               SUM(oi.qty) AS total_sold,
               SUM(oi.qty * oi.price_each) AS revenue_generated
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.name
        ORDER BY total_sold DESC
        FETCH FIRST {limit} ROWS ONLY
    """
    df = run_sql(query)
    print("\n🔥 BEST SELLING PRODUCTS")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    return df


def average_order_value():
    df = run_sql("SELECT AVG(total_amount) AS avg_aov FROM orders")
    print("\n💰 AVERAGE ORDER VALUE")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    return df


# -------------------------------------------------------------------------
# Chart Generators
# -------------------------------------------------------------------------

def chart_top_customers(df):
    plt.figure(figsize=(7,4))
    plt.bar(df["CUSTOMER_NAME"], df["TOTAL_SPENT"])
    plt.title("Top 10 Customers by Spending")
    plt.xticks(rotation=50)
    plt.tight_layout()
    plt.savefig("chart_top_customers.png")
    plt.close()


def chart_city_hist(df):
    plt.figure(figsize=(7,4))
    plt.bar(df["CITY"], df["TOTAL_REVENUE"])
    plt.title("City Revenue >150K")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("chart_city_bar.png")
    plt.close()


def pie_city(df):
    plt.figure(figsize=(6,4))
    plt.pie(df["TOTAL_REVENUE"], labels=df["CITY"], autopct="%.1f%%")
    plt.title("City Revenue Distribution")
    plt.savefig("chart_city_pie.png")
    plt.close()


def chart_monthly(df):
    df["MONTH"] = pd.to_datetime(df["MONTH"] + "-01").dt.strftime("%b %Y")
    plt.figure(figsize=(8,4))
    plt.plot(df["MONTH"], df["REVENUE"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xticks(rotation=40)
    plt.tight_layout()
    plt.savefig("chart_monthly.png")
    plt.close()


def chart_products(df):
    plt.figure(figsize=(7,4))
    plt.bar(df["PRODUCT_NAME"], df["TOTAL_SOLD"], color="orange")
    plt.title("Best Selling Products")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("chart_products.png")
    plt.close()


def pie_new_vs_returning():
    query = """
        SELECT
            SUM(CASE WHEN order_count=1 THEN 1 END) AS newcust,
            SUM(CASE WHEN order_count>1 THEN 1 END) AS returning
        FROM (SELECT customer_id,COUNT(order_id) order_count FROM orders GROUP BY customer_id)
    """
    df = run_sql(query)
    plt.figure(figsize=(5,4))
    plt.pie(df.iloc[0], labels=["New","Returning"], autopct="%.1f%%")
    plt.title("Customer Type Distribution")
    plt.savefig("chart_return.png")
    plt.close()


def chart_revenue_distribution():
    df = run_sql("""
        SELECT customer_id, SUM(total_amount) AS total_spent
        FROM orders GROUP BY customer_id ORDER BY total_spent DESC
    """)
    plt.figure(figsize=(7,4))
    plt.hist(df["TOTAL_SPENT"], bins=20)
    plt.title("Revenue Distribution Across Customers")
    plt.savefig("chart_revenue_dist.png")
    plt.close()

# -------------------------------------------------------------------------
# PDF GENERATOR
# -------------------------------------------------------------------------

def generate_pdf_report_final():
    # fetch data
    df_top = top_customers()
    df_city = city_revenue()
    df_month = monthly_revenue()
    df_prod = best_selling_products()
    df_aov = average_order_value()

    # generate charts (same filenames as before)
    chart_top_customers(df_top)
    chart_city_hist(df_city)
    pie_city(df_city)
    chart_monthly(df_month)
    chart_products(df_prod)
    pie_new_vs_returning()
    chart_revenue_distribution()

    # --- Correct summary values (use real DB counts, not lengths of limited dfs) ---
    total_customers = run_sql("SELECT COUNT(*) AS total_customers FROM customers").iloc[0, 0]
    total_orders = run_sql("SELECT COUNT(*) AS total_orders FROM orders").iloc[0, 0]
    avg_order_value = df_aov.iloc[0, 0] if not df_aov.empty else 0
    cities_over_threshold = len(df_city)
    months_in_data = len(df_month)

    # build a ReportLab Table for the summary
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors

    summary_table = Table([
        ["Metric", "Value"],
        ["Total Customers", int(total_customers)],
        ["Total Orders", int(total_orders)],
        ["Average Order Value", f"{avg_order_value:,.2f}"],
        ["Cities >150K", int(cities_over_threshold)],
        ["Months in Data", int(months_in_data)]
    ], colWidths=[200, 200])

    summary_table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(1,0), colors.HexColor("#1F4E79")),
        ('TEXTCOLOR',(0,0),(1,0), colors.white),
        ('GRID',(0,0),(-1,-1),1,colors.grey),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONT',(0,0),(-1,0),'Helvetica-Bold')
    ]))

    # prepare dfs & charts for PDF generator
    dfs = {
        "Top 10 Customers": df_top,
        "City Revenue (>150K)": df_city,
        "Monthly Revenue Trend": df_month,
        "Best Selling Products": df_prod
    }

    charts = [
        ("Top 10 Customers", "chart_top_customers.png"),
        ("City Revenue Bar", "chart_city_bar.png"),
        ("City Revenue Pie", "chart_city_pie.png"),
        ("Monthly Revenue Trend", "chart_monthly.png"),
        ("Best Selling Products", "chart_products.png"),
        ("New vs Returning Customers", "chart_return.png"),
        ("Revenue Distribution", "chart_revenue_dist.png")
    ]

    filename = f"Sales_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # call PDF builder with correct arguments
    create_pdf_report(filename, summary_table, dfs, charts)

    print(f"\n📄 Report Generated Successfully → {filename}")

# -------------------------------------------------------------------------
# MENU
# -------------------------------------------------------------------------

def menu():
    while True:
        print("\n=== SALES DASHBOARD ===")
        print("1. Top Customers (chart)")
        print("2. City Revenue (chart)")
        print("3. Monthly Revenue")
        print("4. Best Selling Products")
        print("5. Avg Order Value")
        print("6. Revenue Distribution Chart")
        print("7. Generate PDF (All Charts)")
        print("0. Exit")

        ch = input("Enter Choice: ")

        if ch=='1': chart_top_customers(top_customers())
        elif ch=='2': chart_city_hist(city_revenue())
        elif ch=='3': chart_monthly(monthly_revenue())
        elif ch=='4': chart_products(best_selling_products())
        elif ch=='5': average_order_value()
        elif ch=='6': chart_revenue_distribution()
        elif ch=='7': generate_pdf_report_final()
        elif ch=='0': break
        else: print("Invalid Choice!")

if __name__=="__main__":
    menu()
