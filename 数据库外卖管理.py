import mysql.connector
from tkinter import *
from tkinter import Tk,messagebox,Menu,Button,simpledialog
from datetime import datetime
from tkinter.simpledialog import askinteger,askstring
import tkinter as tk

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
def closeSqlConnection(connection, cursor):
    cursor.close()
    connection.close()
# 创建窗口
root = Tk()
root.title("外卖管理系统")
# 设置窗口的初始大小
root.geometry("400x200")


# ****************************显示出表的信息内容*****************************
# ************************************************************************
# 1=============================查询客户信息=================================
def view_customers():
    try:
        cursor.execute("SELECT * FROM customers")
        customers = cursor.fetchall()
        customer_str = "客户信息：\n"
        for customer in customers:
            customer_str += f"ID: {customer[0]}, 姓名: {customer[1]}, 电话: {customer[3]}, 地址: {customer[4]}\n"
        messagebox.showinfo("客户信息", customer_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

# 2===========================查询商家信息=======================================
def view_businesses():
    try:
        cursor.execute("SELECT * FROM businesses")
        businesses = cursor.fetchall()
        business_str = "商家信息：\n"
        for business in businesses:
            business_str += f"ID: {business[0]}, 名称: {business[1]}, 电话: {business[3]}, 地址: {business[4]}\n"
        messagebox.showinfo("商家信息", business_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

# 3=================================查询订单信息================================
def view_orders():
    try:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        order_str = "订单信息：\n"
        for order in orders:
            order_str += f"订单ID: {order[0]}, 客户ID: {order[2]}, 商品ID: {order[3]}, 数量: {order[4]}, " \
                        f"总价: {order[5]}, 状态: {order[6]}, 订单时间: {order[1]}\n"
        messagebox.showinfo("订单信息", order_str)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

# 4==============================查询商品信息==================================
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

# 11==============================商家营业额=========================================
'''def calculate_business_revenue():
    business_id = simpledialog.askinteger("输入", "请输入商家的编号：")
    if business_id is not None:
        cursor.execute("SELECT SUM(number * price) FROM orders INNER JOIN goods ON orders.goods_id = goods.id WHERE goods.business_id = %s AND orders.state = 2", (business_id,))
        revenue = cursor.fetchone()
        if revenue[0] is not None:
            messagebox.showinfo("商家营业额", f"商家 {business_id} 的营业额为：{revenue[0]}")
        else:
            messagebox.showinfo("商家营业额", "该商家没有完成的订单。")
'''
# 11==============================商家营业额=========================================
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
        start_date = askstring("输入", "请输入开始日期（格式：YYYY-MM-DD）")
        end_date = askstring("输入", "请输入结束日期（格式：YYYY-MM-DD）")
        if start_date and end_date:
            revenue = calculate_revenue(merchant_id, start_date, end_date)
            messagebox.showinfo("营业额", f"商家ID：{merchant_id} 在 {start_date} 至 {end_date} 期间的营业额为：{revenue}")
        else:
            messagebox.showwarning("警告", "日期格式不正确或未输入日期")
    else:
        messagebox.showerror("错误", "商家ID不能为空")

#----------------------------开始进行功能写入------------------------------------------------
# 1======================================客户注册================================
def register_customer():
    name = simpledialog.askstring("输入", "请输入客户姓名：")
    phone = simpledialog.askstring("输入", "请输入客户电话：")
    address = simpledialog.askstring("输入", "请输入客户地址：")
    if name and phone and address:
        cursor.execute("INSERT INTO customers (name, phone, address) VALUES (%s, %s, %s)", (name, phone, address))
        conn.commit()
        messagebox.showinfo("成功", "客户注册成功！")

# 2==========================================客户信息修改==========================
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

# 3=======================================商家注册================================
def register_business():
    name = simpledialog.askstring("输入", "请输入商家名称：")
    phone = simpledialog.askstring("输入", "请输入商家电话：")
    address = simpledialog.askstring("输入", "请输入商家地址：")
    if name and phone and address:
        cursor.execute("INSERT INTO businesses (name, phone, address) VALUES (%s, %s, %s)", (name, phone, address))
        conn.commit()
        messagebox.showinfo("成功", "商家注册成功！")

# 4===================================商家信息修改===================================
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

# 5======================================商品录入================================
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

# 6=========================================商品信息修改========================
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

# 7=======================================客户下单================================
# 客户下单
def create_order():
    # 获取客户姓名
    customer_name = simpledialog.askstring("输入", "请输入客户姓名：")
    if customer_name is None or customer_name.strip() == "":
        messagebox.showerror("错误", "请输入有效的客户姓名！")
        return

    # 获取客户ID
    cursor.execute("SELECT id FROM customers WHERE name = %s", (customer_name,))
    customer_id = cursor.fetchone()
    if customer_id is None:
        messagebox.showerror("错误", "找不到该客户！")
        return
    customer_id = customer_id[0]

    # 获取商品编号
    good_id = simpledialog.askinteger("输入", "请输入商品编号：")
    if good_id is None or good_id <= 0:
        messagebox.showerror("错误", "请输入有效的商品编号！")
        return

    # 获取购买数量
    number = simpledialog.askinteger("输入", "请输入购买数量：")
    if number is None or number <= 0:
        messagebox.showerror("错误", "购买数量必须大于零！")
        return

    # 获取当前时间戳
    order_time = current_timestamp()

    try:
        # 插入订单信息
        cursor.execute("INSERT INTO orders (order_time, customer_id, goods_id, number, state) VALUES (%s, %s, %s, %s, %s)",
                      (order_time, customer_id, good_id, number, 0))
        conn.commit()
        messagebox.showinfo("成功", "下单成功！")
    except mysql.connector.Error as err:
        messagebox.showerror("错误", f"下单失败，数据库错误：{err}")
        conn.rollback()  # 如果发生错误，回滚事务

# =======================================获取当前时间戳============================
def current_timestamp():
    #return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now = datetime.now()  # 创建datetime类的实例
    return now.strftime('%Y-%m-%d %H:%M:%S')  # 使用strftime方法格式化日期时

# 8============================商家接单============================================
def accept_order():
    order_id = simpledialog.askinteger("输入", "请输入要接单的订单编号：")
    if order_id is not None:
        cursor.execute("UPDATE orders SET state = 1 WHERE id = %s AND state = 0", (order_id,))
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("成功", "接单成功！")
        else:
            messagebox.showwarning("警告", "该订单不存在或已接单！")

# 9====================================客户确认收货====================================
def confirm_receipt():
    order_id = simpledialog.askinteger("输入", "请输入要确认收货的订单编号：")
    if order_id is not None:
        cursor.execute("UPDATE orders SET state = 2 WHERE id = %s AND state = 1", (order_id,))
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("成功", "确认收货成功！")
        else:
            messagebox.showwarning("警告", "该订单不存在或未接单！")
# 10==============================取消订单=========================================
def cancel_order():
    order_id = simpledialog.askinteger("输入", "请输入要取消的订单编号：")
    if order_id is not None:
        cursor.execute("UPDATE orders SET state = 3 WHERE id = %s AND state = 0", (order_id,))
        if cursor.rowcount > 0:
            conn.commit()
            messagebox.showinfo("成功", "订单取消成功，状态已更新为已退款！")
        else:
            messagebox.showwarning("警告", "该订单不存在或已无法取消！")


# ==========================创建按钮并添加到窗口=======================
# 用于显示欢迎信息的标签
welcome_label = tk.Label(root, text="欢迎使用外卖系统", font=("Arial", 16))
welcome_label.pack(pady=20)  # pady用于设置组件在垂直方向的填充

# Client View
def client_view():
    client_root = Tk()
    client_root.title("客户端")
    messagebox.showinfo("提示", "你已进入客户端视图")

    # Add buttons for client functionalities

    btn_view_goods = Button(client_root, text="查看商品信息", command=view_goods)
    btn_view_goods.pack()

    btn_view_businesses = Button(client_root, text="查看商家信息", command=view_businesses)
    btn_view_businesses.pack()

    btn_view_orders = Button(client_root, text="查看已选商品订单信息", command=lambda: view_orders(customer_id))
    btn_view_orders.pack()

    btn_register_customer = Button(client_root, text="客户注册", command=register_customer)
    btn_register_customer.pack()

    btn_create_order = Button(client_root, text="客户下单", command=create_order)
    btn_create_order.pack()

    btn_cancel_order = Button(client_root, text="取消订单", command=cancel_order)
    btn_cancel_order.pack()

    btn_confirm_receipt = Button(client_root, text="确认收货", command=confirm_receipt)
    btn_confirm_receipt.pack()

    client_root.mainloop()

# Business View
def business_view():
    business_root = Tk()
    business_root.title("商家端")
    messagebox.showinfo("提示", "你已进入商家端视图")

    # Add buttons for business functionalities
    btn_register_business = Button(business_root, text="商家注册", command=register_business)
    btn_register_business.pack()

    btn_add_good = Button(business_root, text="商品录入", command=add_good)
    btn_add_good.pack()

    btn_modify_good_info = Button(business_root, text="商品信息修改", command=modify_good_info)
    btn_modify_good_info.pack()

    btn_view_orders = Button(business_root, text="查看订单信息", command=view_orders)
    btn_view_orders.pack()

    btn_view_businesses = Button(business_root, text="查看商家信息", command=view_businesses)
    btn_view_businesses.pack()

    btn_accept_order = Button(business_root, text="商家接单", command=accept_order)
    btn_accept_order.pack()

    #btn_calculate_revenue = Button(business_root, text="商家营业额", command=calculate_business_revenue)
    #btn_calculate_revenue.pack()
    btn_view_revenue = Button(business_root, text="查看营业额", command=view_revenue)
    btn_view_revenue.pack()

    business_root.mainloop()

'''# Add buttons to open the respective views
btn_client_view = Button(root, text="客户端", command=client_view)
btn_client_view.pack()

btn_business_view = Button(root, text="商家端", command=business_view)
btn_business_view.pack()
'''
# 创建“客户端”按钮并添加到主窗口
btn_client = tk.Button(root, text="客户端", command=client_view, font=("Arial", 12), padx=10, pady=5)
btn_client.pack(pady=10)  # pady用于设置组件在垂直方向的填充
# 创建“商家端”按钮并添加到主窗口
btn_business = tk.Button(root, text="商家端", command=business_view, font=("Arial", 12), padx=10, pady=5)
btn_business.pack(pady=10)
# 运行窗口
root.mainloop()

# 关闭数据库连接
cursor.close()
conn.close()