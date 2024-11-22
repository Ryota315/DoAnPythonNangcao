import tkinter as tk
from tkinter import ttk, messagebox
import MySQLdb  # Sử dụng mysqlclient

# Kết nối cơ sở dữ liệu
def connect_db():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="123456",  # Đổi mật khẩu nếu cần
        db="product_manager",
        charset="utf8mb4"
    )

# Thêm sản phẩm vào cơ sở dữ liệu
def add_product(name, price, quantity, description):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO products (name, price, quantity, description) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, price, quantity, description))
    conn.commit()
    conn.close()

# Lấy danh sách sản phẩm
def fetch_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Xóa sản phẩm khỏi cơ sở dữ liệu
def delete_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "DELETE FROM products WHERE id = %s"
    cursor.execute(query, (product_id,))
    conn.commit()
    conn.close()

# Cập nhật sản phẩm
def update_product(product_id, name, price, quantity, description):
    conn = connect_db()
    cursor = conn.cursor()
    query = """UPDATE products SET name = %s, price = %s, quantity = %s, description = %s WHERE id = %s"""
    cursor.execute(query, (name, price, quantity, description, product_id))
    conn.commit()
    conn.close()

# Hiển thị danh sách sản phẩm trên Treeview
def load_products():
    # Làm sạch Treeview trước khi hiển thị
    for item in tree.get_children():
        tree.delete(item)
    
    # Lấy tất cả sản phẩm và thêm vào Treeview
    for row in fetch_products():
        tree.insert("", "end", values=row)

# Thêm sản phẩm UI
def add_product_ui():
    name = entry_name.get()
    price = entry_price.get()
    quantity = entry_quantity.get()
    description = entry_description.get()

    if not (name and price and quantity):
        messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
        return

    try:
        add_product(name, float(price), int(quantity), description)
        load_products()
        messagebox.showinfo("Thành công", "Đã thêm sản phẩm!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {e}")

# Xóa sản phẩm UI
def delete_product_ui():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Lỗi", "Vui lòng chọn sản phẩm để xóa!")
        return

    product_id = tree.item(selected_item, "values")[0]
    try:
        delete_product(product_id)
        load_products()
        messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa sản phẩm: {e}")

# Chỉnh sửa sản phẩm UI
def update_product_ui():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Lỗi", "Vui lòng chọn sản phẩm để chỉnh sửa!")
        return

    product = tree.item(selected_item, "values")
    product_id = product[0]

    update_window = tk.Toplevel(root)
    update_window.title("Chỉnh sửa sản phẩm")

    tk.Label(update_window, text="Tên sản phẩm").grid(row=0, column=0, padx=10, pady=10)
    entry_name_update = tk.Entry(update_window)
    entry_name_update.grid(row=0, column=1, padx=10, pady=10)
    entry_name_update.insert(0, product[1])

    tk.Label(update_window, text="Giá").grid(row=1, column=0, padx=10, pady=10)
    entry_price_update = tk.Entry(update_window)
    entry_price_update.grid(row=1, column=1, padx=10, pady=10)
    entry_price_update.insert(0, product[2])

    tk.Label(update_window, text="Số lượng").grid(row=2, column=0, padx=10, pady=10)
    entry_quantity_update = tk.Entry(update_window)
    entry_quantity_update.grid(row=2, column=1, padx=10, pady=10)
    entry_quantity_update.insert(0, product[3])

    tk.Label(update_window, text="Mô tả").grid(row=3, column=0, padx=10, pady=10)
    entry_description_update = tk.Entry(update_window)
    entry_description_update.grid(row=3, column=1, padx=10, pady=10)
    entry_description_update.insert(0, product[4])

    def save_update():
        name = entry_name_update.get()
        price = entry_price_update.get()
        quantity = entry_quantity_update.get()
        description = entry_description_update.get()
        try:
            update_product(product_id, name, float(price), int(quantity), description)
            load_products()
            update_window.destroy()
            messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sản phẩm: {e}")

    tk.Button(update_window, text="Lưu", command=save_update).grid(row=4, columnspan=2, pady=10)

# Tìm kiếm sản phẩm trong cơ sở dữ liệu theo tên
def search_products(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM products WHERE name LIKE %s"
    cursor.execute(query, (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Tìm kiếm sản phẩm UI
def search_product_ui():
    keyword = entry_search.get()
    if not keyword:
        messagebox.showwarning("Lỗi", "Vui lòng nhập từ khóa tìm kiếm!")
        return

    try:
        results = search_products(keyword)
        # Làm sạch Treeview trước khi hiển thị kết quả tìm kiếm
        for item in tree.get_children():
            tree.delete(item)
        for row in results:
            tree.insert("", "end", values=row)

        if not results:
            messagebox.showinfo("Kết quả", "Không tìm thấy sản phẩm nào.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm kiếm sản phẩm: {e}")

# Hiển thị tất cả sản phẩm
def show_all_products():
    load_products()

# Giao diện chính
root = tk.Tk()
root.title("Quản lý sản phẩm")
root.geometry("800x600")
root.configure(bg="#f2f2f2")

# Áp dụng style cho các widget
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10, relief="flat", background="#4CAF50", foreground="white")
style.configure("TButton:hover", background="#45a049")
style.configure("TLabel", font=("Arial", 12), background="#f2f2f2")
style.configure("TEntry", font=("Arial", 12), padding=5)

# Form nhập sản phẩm
frame_input = tk.Frame(root, bg="#f2f2f2")
frame_input.pack(pady=20)

tk.Label(frame_input, text="Tên sản phẩm").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(frame_input, font=("Arial", 12))
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Giá").grid(row=1, column=0, padx=10, pady=10)
entry_price = tk.Entry(frame_input, font=("Arial", 12))
entry_price.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Số lượng").grid(row=2, column=0, padx=10, pady=10)
entry_quantity = tk.Entry(frame_input, font=("Arial", 12))
entry_quantity.grid(row=2, column=1, padx=10, pady=10)

tk.Label(frame_input, text="Mô tả").grid(row=3, column=0, padx=10, pady=10)
entry_description = tk.Entry(frame_input, font=("Arial", 12))
entry_description.grid(row=3, column=1, padx=10, pady=10)

tk.Button(frame_input, text="Thêm sản phẩm", command=add_product_ui).grid(row=4, columnspan=2, pady=10)

# Khung tìm kiếm
frame_search = tk.Frame(root, bg="#f2f2f2")
frame_search.pack(pady=20)

tk.Label(frame_search, text="Tìm kiếm sản phẩm").grid(row=0, column=0, padx=10, pady=10)
entry_search = tk.Entry(frame_search, font=("Arial", 12))
entry_search.grid(row=0, column=1, padx=10, pady=10)

tk.Button(frame_search, text="Tìm kiếm", command=search_product_ui).grid(row=0, column=2, padx=10, pady=10)

# Treeview hiển thị sản phẩm
frame_table = tk.Frame(root, bg="#f2f2f2")
frame_table.pack(pady=20)

tree = ttk.Treeview(frame_table, columns=("ID", "Tên", "Giá", "Số lượng", "Mô tả"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Tên", text="Tên")
tree.heading("Giá", text="Giá")
tree.heading("Số lượng", text="Số lượng")
tree.heading("Mô tả", text="Mô tả")
tree.pack()

# Nút xóa và chỉnh sửa
frame_controls = tk.Frame(root, bg="#f2f2f2")
frame_controls.pack(pady=10)

tk.Button(frame_controls, text="Xóa sản phẩm", command=delete_product_ui).pack(side="left", padx=10, pady=10)
tk.Button(frame_controls, text="Chỉnh sửa sản phẩm", command=update_product_ui).pack(side="left", padx=10, pady=10)

# Nút hiển thị tất cả sản phẩm
tk.Button(frame_controls, text="Hiển thị tất cả sản phẩm", command=show_all_products).pack(side="left", padx=10, pady=10)

# Tải sản phẩm khi khởi động
load_products()

root.mainloop()
