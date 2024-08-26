import mysql.connector
from tkinter import *
from tkinter import messagebox, simpledialog
from datetime import datetime

# 数据库连接配置
db_config = {
    'user': 'root',
    'password': 'g1234',
    'host': 'localhost',
    'database': 'km'
}

# 创建数据库连接和游标
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 关闭数据库连接
def closeSqlConnection():
    cursor.close()
    conn.close()

# ===================================功能实现===================================

def view_customers():
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        customer_str = "客户信息：\n"
        for customer in customers:
            customer_str += f"ID: {customer[0]}, 姓名: {customer[1]}, 电话: {customer[2]}, 地址: {customer[3]}\n"
        messagebox.showinfo("客户信息", customer_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

def view_businesses():
    try:
        cursor.execute("SELECT * FROM businesses")
        businesses = cursor.fetchall()
        business_str = "商家信息：\n"
        for business in businesses:
            business_str += f"ID: {business[0]}, 名称: {business[1]}, 电话: {business[2]}, 地址: {business[3]}\n"
        messagebox.showinfo("商家信息", business_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

def view_orders(customer_id=None):
    try:
        if customer_id:
            cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
        else:
            cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        order_str = "订单信息：\n"
        for order in orders:
            order_str += f"订单ID: {order[0]}, 客户ID: {order[1]}, 商品ID: {order[2]}, 数量: {order[3]}, 总价: {order[4]}, 状态: {order[5]}, 订单时间: {order[6]}\n"
        messagebox.showinfo("订单信息", order_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

def view_goods():
    try:
        cursor.execute("SELECT * FROM goods")
        goods = cursor.fetchall()
        goods_str = "商品信息：\n"
        for good in goods:
            goods_str += f"商品ID: {good[0]}, 名称: {good[1]}, 商家ID: {good[2]}, 价格: {good[3]}, 限购数量: {good[4]}\n"
        messagebox.showinfo("商品信息", goods_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

def calculate_revenue(merchant_id, start_date, end_date):
    cursor.execute("SELECT SUM(number * price) FROM orders INNER JOIN goods ON orders.goods_id = goods.id WHERE goods.business_id = %s AND orders.state = 2 AND orders.order_time BETWEEN %s AND %s", (merchant_id, start_date, end_date))
    revenue = cursor.fetchone()
    if revenue[0] is not None:
        return revenue[0]
    else:
        return 0

def view_revenue():
    merchant_id = simpledialog.askinteger("输入", "请输入商家ID：")
    if merchant_id is not None:
        start_date = simpledialog.askstring("输入", "请输入开始日期（格式：YYYY-MM-DD）")
        end_date = simpledialog.askstring("输入", "请输入结束日期（格式：YYYY-MM-DD）")
        if start_date and end_date:
            revenue = calculate_revenue(merchant_id, start_date, end_date)
            messagebox.showinfo("营业额", f"商家ID：{merchant_id} 在 {start_date} 至 {end_date} 期间的营业额为：{revenue}")
        else:
            messagebox.showwarning("警告", "日期格式不正确或未输入日期")
    else:
        messagebox.showerror("错误", "商家ID不能为空")

def register_customer():
    name = simpledialog.askstring("输入", "请输入客户姓名：")
    phone = simpledialog.askstring("输入", "请输入客户电话：")
    address = simpledialog.askstring("输入", "请输入客户地址：")
    if name and phone and address:
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)", (name, phone, address))
        conn.commit()
        messagebox.showinfo("成功", "客户注册成功！")

def modify_customer_info():
    customer_id = simpledialog.askinteger("输入", "请输入客户的编号：")
    if customer_id is not None:
        new_name = simpledialog.askstring("输入", "请输入新的客户姓名：")
        new_phone = simpledialog.askstring("输入", "请输入新的客户电话：")
        new_address = simpledialog.askstring("输入", "请输入新的客户地址：")
        if new_name and new_phone and new_address:
            cursor.execute("UPDATE customers SET name = %s, phone = %s, address = %s WHERE id = %s", (new_name, new_phone, new_address, customer_id))
            conn.commit()
            messagebox.showinfo("成功", "客户信息修改成功！")

def register_business():
    name = simpledialog.askstring("输入", "请输入商家名称：")
    phone = simpledialog.askstring("输入", "请输入商家电话：")
    address = simpledialog.askstring("输入", "请输入商家地址：")
    if name and phone and address:
        cursor.execute("INSERT INTO businesses (name, phone, address) VALUES (%s, %s, %s)", (name, phone, address))
        conn.commit()
        messagebox.showinfo("成功", "商家注册成功！")

def modify_business_info():
    business_id = simpledialog.askinteger("输入", "请输入商家的编号：")
    if business_id is not None:
        new_name = simpledialog.askstring("输入", "请输入新的商家名称：")
        new_phone = simpledialog.askstring("输入", "请输入新的商家电话：")
        new_address = simpledialog.askstring("输入", "请输入新的商家地址：")
        if new_name and new_phone and new_address:
            cursor.execute("UPDATE businesses SET name = %s, phone = %s, address = %s WHERE id = %s", (new_name, new_phone, new_address, business_id))
            conn.commit()
            messagebox.showinfo("成功", "商家信息修改成功！")

def add_good():
    business_id = simpledialog.askinteger("输入", "请输入商家编号：")
    name = simpledialog.askstring("输入", "请输入商品名称：")
    price = simpledialog.askfloat("输入", "请输入商品价格：")
    limit_num = simpledialog.askinteger("输入", "请输入限购数量（如果无限购则留空）：")
    if business_id is not None and name and price is not None:
        cursor.execute("INSERT INTO goods (business_id, name, price, limit_num) VALUES (%s, %s, %s, %s)",
                      (business_id, name, price, limit_num if limit_num else None))
        conn.commit()
        messagebox.showinfo("成功", "商品录入成功！")

def modify_good_info():
    good_id = simpledialog.askinteger("输入", "请输入商品编号：")
    if good_id is not None:
        business_id = simpledialog.askinteger("输入", "请输入新的商家编号：")
        name = simpledialog.askstring("输入", "请输入新的商品名称：")
        price = simpledialog.askfloat("输入", "请输入新的商品价格：")
        limit_num = simpledialog.askinteger("输入", "请输入新的限购数量（如果无限购则留空）：")
        if business_id is not None and name and price is not None:
            cursor.execute("UPDATE goods SET business_id = %s, name = %s, price = %s, limit_num = %s WHERE id = %s",
                          (business_id, name, price, limit_num if limit_num else None, good_id))
            conn.commit()
            messagebox.showinfo("成功", "商品信息修改成功！")

def create_order():
    customer_name = simpledialog.askstring("输入", "请输入客户姓名：")
    if customer_name is None or customer_name.strip() == "":
        messagebox.showerror("错误", "请输入有效的客户姓名！")
        return

    cursor.execute("SELECT id FROM customers WHERE name = %s", (customer_name,))
    customer_id = cursor.fetchone()
    if customer_id is None:
        messagebox.showerror("错误", "找不到该客户！")
        return
    customer_id = customer_id[0]

    good_id = simpledialog.askinteger("输入", "请输入商品编号：")
    if good_id is None or good_id <= 0:
        messagebox.showerror("错误", "请输入有效的商品编号！")
        return

    number = simpledialog.askinteger("输入", "请输入购买数量：")
    if number is None or number <= 0:
        messagebox.showerror("错误", "请输入有效的购买数量！")
        return

    cursor.execute("SELECT price, limit_num FROM goods WHERE id = %s", (good_id,))
    good_info = cursor.fetchone()
    if good_info is None:
        messagebox.showerror("错误", "商品编号无效！")
        return
    price, limit_num = good_info

    if limit_num is not None and number > limit_num:
        messagebox.showerror("错误", f"超过限购数量：{limit_num}！")
        return

    total_price = number * price
    order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("INSERT INTO orders (customer_id, goods_id, number, total_price, state, order_time) VALUES (%s, %s, %s, %s, %s, %s)",
                  (customer_id, good_id, number, total_price, 1, order_time))
    conn.commit()
    messagebox.showinfo("成功", "订单创建成功！")

def confirm_order():
    order_id = simpledialog.askinteger("输入", "请输入订单编号：")
    if order_id is not None:
        cursor.execute("UPDATE orders SET state = %s WHERE id = %s", (2, order_id))
        conn.commit()
        messagebox.showinfo("成功", "订单已确认！")

def delete_order():
    order_id = simpledialog.askinteger("输入", "请输入要删除的订单编号：")
    if order_id is not None:
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()
        messagebox.showinfo("成功", "订单删除成功！")

# ===================================窗口设置===================================

root = Tk()
root.title("水果商城管理系统")
root.geometry("400x400")

btns = [
    ("查看客户信息", view_customers),
    ("查看商家信息", view_businesses),
    ("查看订单信息", view_orders),
    ("查看商品信息", view_goods),
    ("查询商家营业额", view_revenue),
    ("客户注册", register_customer),
    ("修改客户信息", modify_customer_info),
    ("商家注册", register_business),
    ("修改商家信息", modify_business_info),
    ("商品录入", add_good),
    ("修改商品信息", modify_good_info),
    ("生成订单", create_order),
    ("确认订单", confirm_order),
    ("删除订单", delete_order)
]

for (text, command) in btns:
    Button(root, text=text, command=command).pack(pady=5)

root.mainloop()
closeSqlConnection()
