#updated
from tkinter import *
from tkinter import simpledialog
import tkinter as tk
from tkinter import messagebox
import mysql.connector as mysql
import re

# Function to clear entry fields
def clear_entries(*entries):
    for entry in entries:
        entry.delete(0, tk.END)

# Function to handle customer registration
def register_page():
    def regbutton():
        FirstName = FirstName_Entry.get().strip()
        LastName = LastName_Entry.get().strip()
        Email = EmailID_Entry.get().strip()
        Contact = ContactNo_Entry.get().strip()
        Address = Address_Entry.get().strip()
        Aadhar = AadharNo_Entry.get().strip()
        PIN = PIN_Entry.get().strip()
        C_PIN = C_PIN_Entry.get().strip()
        
        # Validation checks
        if not FirstName or re.search(r"[0-9!@#$%^&*(),.?\":{}|<>]", FirstName):
            messagebox.showerror("Validation Error", "First Name is required and should not contain digits or special symbols.")
            return
        if not LastName or re.search(r"[0-9!@#$%^&*(),.?\":{}|<>]", LastName):
            messagebox.showerror("Validation Error", "Last Name is required and should not contain digits or special symbols.")
            return
        if not Email or not re.match(r"[^@]+@[^@]+\.[^@]+", Email):
            messagebox.showerror("Validation Error", "Valid Email is required. eg-> someone@example.com")
            return
        if not Contact or len(Contact) < 10:
            messagebox.showerror("Validation Error", "Contact No. is required and should be at least 10 digits.")
            return
        if not Address or len(Address) < 10:
            messagebox.showerror("Validation Error", "Address is required and should be at least 10 characters.")
            return
        if not Aadhar or len(Aadhar) != 12 or not re.match(r"^[0-9]{12}$", Aadhar):
            messagebox.showerror("Validation Error", "Aadhar No. is required and should be exactly 12 digits.")
            return
        if not PIN or len(PIN) < 6 or not re.match(r"^(?=.[A-Za-z])(?=.\d)(?=.[@$!%#?&])[A-Za-z\d@$!%*#?&]{6,}$", PIN):
            messagebox.showerror("Validation Error", "PIN must be at least 6 characters long and include at least one letter, one number, and one special character.")
            return
        if PIN != C_PIN:
            messagebox.showerror("Validation Error", "PIN and Confirm PIN do not match.")
            return

        # All checks passed, proceed to database insertion
        try:
            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
            cursor = con.cursor()
            cursor.execute("INSERT INTO cust_detail (FirstName, LastName, Email, Contact, Address, Aadhar, PIN) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (FirstName, LastName, Email, Contact, Address, Aadhar, PIN))
            con.commit()
            account_no = cursor.lastrowid  # Retrieve the auto-incremented AccountNo
            con.close()
            messagebox.showinfo("Success", f"Account created successfully! AccountNo: {account_no}")
            clear_entries(FirstName_Entry, LastName_Entry, EmailID_Entry, ContactNo_Entry, Address_Entry, AadharNo_Entry, PIN_Entry, C_PIN_Entry)
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Customer registration window
    win2 = tk.Toplevel()
    win2.title("Customer Registration Form")

    # Labels and Entries for registration form
    tk.Label(win2, text="Customer Registration Form", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(win2, text="First Name").grid(row=1, column=0, pady=5, sticky=tk.E)
    FirstName_Entry = tk.Entry(win2)
    FirstName_Entry.grid(row=1, column=1, pady=5)

    tk.Label(win2, text="Last Name").grid(row=2, column=0, pady=5, sticky=tk.E)
    LastName_Entry = tk.Entry(win2)
    LastName_Entry.grid(row=2, column=1, pady=5)

    tk.Label(win2, text="Email ID").grid(row=3, column=0, pady=5, sticky=tk.E)
    EmailID_Entry = tk.Entry(win2)
    EmailID_Entry.grid(row=3, column=1, pady=5)

    tk.Label(win2, text="Contact No").grid(row=4, column=0, pady=5, sticky=tk.E)
    ContactNo_Entry = tk.Entry(win2)
    ContactNo_Entry.grid(row=4, column=1, pady=5)

    tk.Label(win2, text="Address").grid(row=5, column=0, pady=5, sticky=tk.E)
    Address_Entry = tk.Entry(win2)
    Address_Entry.grid(row=5, column=1, pady=5)

    tk.Label(win2, text="Aadhar No.").grid(row=6, column=0, pady=5, sticky=tk.E)
    AadharNo_Entry = tk.Entry(win2)
    AadharNo_Entry.grid(row=6, column=1, pady=5)

    tk.Label(win2, text="PIN").grid(row=7, column=0, pady=5, sticky=tk.E)
    PIN_Entry = tk.Entry(win2, show="*")
    PIN_Entry.grid(row=7, column=1, pady=5)

    tk.Label(win2, text="Confirm PIN").grid(row=8, column=0, pady=5, sticky=tk.E)
    C_PIN_Entry = tk.Entry(win2, show="*")
    C_PIN_Entry.grid(row=8, column=1, pady=5)

    # Register button
    tk.Button(win2, text="Register", command=regbutton).grid(row=9, column=1, pady=10)

    win2.mainloop()

# Function to handle customer login
def login_page():
    def loginbtn():
        acc = acc_no_entry.get()
        pin = pin_entry.get()
        
        try:
            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
            cursor = con.cursor()
            
            # Check if customer exists
            cursor.execute("SELECT * FROM cust_detail WHERE AccountNo = %s AND PIN = %s", (acc, pin))
            cust = cursor.fetchone()
            
            if cust:
                messagebox.showinfo("Success", "Login successful!")
                open_customer_dashboard(cust)
                win3.destroy()  # Close login window after successful login
            else:
                messagebox.showerror("Error", "Invalid username or password!")
                
            con.close()
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Customer login window
    win3 = tk.Toplevel()
    win3.title("Login Page")

    # Labels and Entries for login form
    tk.Label(win3, text="Login Page", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(win3, text="Account No").grid(row=1, column=0, pady=5, sticky=tk.E)
    acc_no_entry = tk.Entry(win3)
    acc_no_entry.grid(row=1, column=1, pady=5)

    tk.Label(win3, text="PIN").grid(row=2, column=0, pady=5, sticky=tk.E)
    pin_entry = tk.Entry(win3, show="*")
    pin_entry.grid(row=2, column=1, pady=5)

    # Login button
    tk.Button(win3, text="Login", command=loginbtn).grid(row=3, column=1, pady=10)

    win3.mainloop()

# Function to open customer dashboard
def open_customer_dashboard(customer_data):
    def apply_loan():
        def submit_loan_application():
            loan_amount = loan_amount_entry.get().strip()
            
            if not loan_amount or not loan_amount.isdigit():
                messagebox.showerror("Validation Error", "Loan amount must be a valid number.")
                return
            
            try:
                con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
                cursor = con.cursor()
                cursor.execute("INSERT INTO loans (CustomerID, LoanAmount) VALUES (%s, %s)",
                               (customer_data[0], float(loan_amount)))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Loan application submitted successfully!")
                loan_window.destroy()
            except mysql.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

        loan_window = tk.Toplevel()
        loan_window.title("Apply for Loan")

        tk.Label(loan_window, text="Apply for Loan", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(loan_window, text="Loan Amount").grid(row=1, column=0, pady=5, sticky=tk.E)
        loan_amount_entry = tk.Entry(loan_window)
        loan_amount_entry.grid(row=1, column=1, pady=5)

        tk.Button(loan_window, text="Submit", command=submit_loan_application).grid(row=2, column=1, pady=10)

        loan_window.mainloop()
        
    def update_address():
        new_address = simpledialog.askstring("Update Address", "Enter new address:")
        if new_address:
            try:
                con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
                cursor = con.cursor()
                cursor.execute("UPDATE cust_detail SET Address = %s WHERE AccountNo = %s", (new_address, customer_data[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Address updated successfully!")
            except mysql.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

    def update_pin():

        new_pin = simpledialog.askstring("Update PIN", "Enter new PIN:")
        if new_pin:
            try:
                con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
                cursor = con.cursor()
                cursor.execute("UPDATE cust_detail SET PIN = %s WHERE AccountNo = %s", (new_pin, customer_data[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "PIN updated successfully!")
            except mysql.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")

    # Customer dashboard window
    dashboard = tk.Toplevel()
    dashboard.title("Customer Dashboard")

    tk.Label(dashboard, text=f"Welcome, {customer_data[1]} {customer_data[2]}", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(dashboard, text=f"Email:, {customer_data[3]}", font=('Arial', 12)).grid(row=3, column=2, columnspan=2, pady=10)
    tk.Label(dashboard, text=f"Contact, {customer_data[4]}", font=('Arial', 12)).grid(row=4, column=2, columnspan=2, pady=10)
    tk.Label(dashboard, text=f"Address:, {customer_data[5]}", font=('Arial', 12)).grid(row=5, column=2, columnspan=2, pady=10)
    tk.Label(dashboard, text=f"Addhar no., {customer_data[6]}", font=('Arial', 12)).grid(row=6, column=2, columnspan=2, pady=10)
   
    tk.Button(dashboard, text="Apply for Loan", command=apply_loan).grid(row=1, column=0, pady=10)
    tk.Button(dashboard, text="Update Address", command=update_address).grid(row=1, column=1, pady=10)
    tk.Button(dashboard, text="Update PIN", command=update_pin).grid(row=2, column=0, pady=10)

    dashboard.mainloop()

# Function to handle manager login
def manager_login():
    def manager_login_btn():
        manager_id = manager_id_entry.get()
        manager_password = manager_password_entry.get()
        
        # Example validation (replace with actual database check)
        try:
            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
            cursor = con.cursor()
            
            cursor.execute("SELECT * FROM managers WHERE username = %s AND PIN = %s", (manager_id, manager_password))
            manager = cursor.fetchone()
            
            if manager:
                messagebox.showinfo("Success", "Manager login successful!")
                open_manager_dashboard(manager)
                win5.destroy()  # Close login window after successful login
            else:
                messagebox.showerror("Error", "Invalid manager credentials.")
                
            con.close()
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Manager login window
    win5 = tk.Toplevel()
    win5.title("Manager Login")
    
    tk.Label(win5, text="Manager Login", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
    
    tk.Label(win5, text="Manager username").grid(row=1, column=0, pady=5, sticky=tk.E)
    manager_id_entry = tk.Entry(win5)
    manager_id_entry.grid(row=1, column=1, pady=5)
    
    tk.Label(win5, text="Password").grid(row=2, column=0, pady=5, sticky=tk.E)
    manager_password_entry = tk.Entry(win5, show="*")
    manager_password_entry.grid(row=2, column=1, pady=5)
    
    tk.Button(win5, text="Login", command=manager_login_btn).grid(row=3, column=1, pady=10)
    
    win5.mainloop()

# Function to handle cashier login
def cashier_login():
    def cashier_login_btn():
        cashier_id = cashier_id_entry.get()
        cashier_password = cashier_password_entry.get()
        
        # Example validation (replace with actual database check)
        try:
            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
            cursor = con.cursor()
            
            cursor.execute("SELECT * FROM cashiers WHERE username = %s AND PIN = %s", (cashier_id, cashier_password))
            cashier = cursor.fetchone()
            
            if cashier:
                messagebox.showinfo("Success", "Cashier login successful!")
                open_cashier_dashboard(cashier)
                win6.destroy()  # Close login window after successful login
            else:
                messagebox.showerror("Error", "Invalid cashier credentials.")
                
            con.close()
        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Cashier login window
    win6 = tk.Toplevel()
    win6.title("Cashier Login")
    
    tk.Label(win6, text="Cashier Login", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
    
    tk.Label(win6, text="Cashier ID").grid(row=1, column=0, pady=5, sticky=tk.E)
    cashier_id_entry = tk.Entry(win6)
    cashier_id_entry.grid(row=1, column=1, pady=5)
    
    tk.Label(win6, text="Password").grid(row=2, column=0, pady=5, sticky=tk.E)
    cashier_password_entry = tk.Entry(win6, show="*")
    cashier_password_entry.grid(row=2, column=1, pady=5)
    
    tk.Button(win6, text="Login", command=cashier_login_btn).grid(row=3, column=1, pady=10)
    
    win6.mainloop()

# Function to open manager dashboard
def open_manager_dashboard(manager_data):
    def view_loan_requests():
        try:
            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM loans WHERE Status = 'Pending'")
            loan_requests = cursor.fetchall()
            con.close()

            if loan_requests:
                # Display loan requests
                loan_win = tk.Toplevel()
                loan_win.title("Loan Requests")

                tk.Label(loan_win, text="Loan Requests", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
                tk.Label(loan_win, text="Customer ID\tLoan Amount").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)

                for idx, request in enumerate(loan_requests, start=2):
                    tk.Label(loan_win, text=f"{request[1]}\t\t{request[2]}").grid(row=idx, column=0, pady=5, padx=10, sticky=tk.W)

                def handle_request():
                    selected_item = loan_listbox.curselection()
                    if not selected_item:
                        messagebox.showerror("Error", "Please select a loan request.")
                        return
                    selected_idx = selected_item[0]
                    selected_request = loan_requests[selected_idx]

                    decision = messagebox.askquestion("Confirm", "Do you want to approve this loan request?")
                    if decision == 'yes':
                        try:
                            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
                            cursor = con.cursor()
                            cursor.execute("UPDATE loans SET Status = 'Approved' WHERE LoanID = %s", (selected_request[0],))
                            con.commit()
                            con.close()
                            messagebox.showinfo("Success", "Loan request approved. Sent to Cashier.")
                            loan_win.destroy()
                        except mysql.Error as err:
                            messagebox.showerror("Database Error", f"Error: {err}")

                loan_listbox = tk.Listbox(loan_win)
                loan_listbox.grid(row=1, column=1, rowspan=len(loan_requests)+1, padx=10, pady=5)
                for request in loan_requests:
                    loan_listbox.insert(tk.END, f"{request[1]} - {request[2]}")

                tk.Button(loan_win, text="Approve", command=handle_request).grid(row=len(loan_requests)+2, column=0, columnspan=2, pady=10)

                loan_win.mainloop()

            else:
                messagebox.showinfo("Loan Requests", "No pending loan requests.")

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Manager dashboard window
    dashboard = tk.Toplevel()
    dashboard.title("Manager Dashboard")

    tk.Label(dashboard, text=f"Welcome, {manager_data[1]} {manager_data[2]}", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Button(dashboard, text="View Loan Requests", command=view_loan_requests).grid(row=1, column=0, pady=10)

    dashboard.mainloop()

# Function to open cashier dashboard
def open_cashier_dashboard(cashier_data):
    def view_approved_loans():
        try:
            con = mysql.connect(host="localhost", user="root", password="Gulshan@1234", database="bms1")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM loans WHERE Status = 'Approved'")
            approved_loans = cursor.fetchall()
            con.close()

            if approved_loans:
                # Display approved loans
                loan_win = tk.Toplevel()
                loan_win.title("Approved Loans")

                tk.Label(loan_win, text="Approved Loans", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)
                tk.Label(loan_win, text="Customer ID\tLoan Amount").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)

                for idx, loan in enumerate(approved_loans, start=2):
                    tk.Label(loan_win, text=f"{loan[1]}\t\t{loan[2]}").grid(row=idx, column=0, pady=5, padx=10, sticky=tk.W)

                loan_win.mainloop()

            else:
                messagebox.showinfo("Approved Loans", "No approved loans.")

        except mysql.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Cashier dashboard window
    dashboard = tk.Toplevel()
    dashboard.title("Cashier Dashboard")

    tk.Label(dashboard, text=f"Welcome, {cashier_data[1]} {cashier_data[2]}", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Button(dashboard, text="View Approved Loans", command=view_approved_loans).grid(row=1, column=0, pady=10)

    dashboard.mainloop()

# Main window
win = tk.Tk()
win.title("Bank Management System")

# Labels and Buttons for main window
tk.Label(win, text="Welcome to Bank Management System", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=10)

tk.Button(win, text="Customer Registration", command=register_page).grid(row=1, column=0, pady=10)
tk.Button(win, text="Customer Login", command=login_page).grid(row=1, column=1, pady=10)
tk.Button(win, text="Manager Login", command=manager_login).grid(row=2, column=0, pady=10)
tk.Button(win, text="Cashier Login", command=cashier_login).grid(row=2, column=1, pady=10)

win.mainloop()