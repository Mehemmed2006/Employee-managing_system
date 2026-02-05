#12.12.2025  
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("İşçi İdarəetmə Sistemi")
        self.root.geometry("900x600")
        self.root.configure(bg='#f0f8ff')
        
        # Məlumatların saxlanması üçün fayl
        self.data_file = "employees.json"
        self.login_attempts_file = "login_attempts.json"
        self.audit_file = "audit_log.json"
        self.logged_in_file = "logged_in.json"
        
        # Məlumatları yüklə
        self.employees = self.load_data(self.data_file)
        self.login_attempts = self.load_data(self.login_attempts_file)
        self.audit_log = self.load_data(self.audit_file)
        self.logged_in_users = self.load_data(self.logged_in_file)
        
        # GUI yarat
        self.create_gui()
        
        # İlk açılışda login olanları göstər
        self.refresh_logged_in_list()
        
    def load_data(self, filename):
        """Məlumatları JSON faylından yüklə"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_data(self, data, filename):
        """Məlumatları JSON faylına saxla"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Xəta", f"Məlumat saxlanarkən xəta: {str(e)}")
            return False
    
    def create_gui(self):
        """GUI yarat"""
        # Başlıq
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="İşçi İdarəetmə Sistemi", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Notebook (Tab kontrolleri)
        style = ttk.Style()
        style.configure('TNotebook', background='#f0f8ff')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Qeydiyyat tab
        self.create_registration_tab()
        
        # Login tab
        self.create_login_tab()
        
        # Audit tab
        self.create_audit_tab()
        
        # Login olan işçilər tab
        self.create_logged_in_tab()
        
    def create_registration_tab(self):
        """Qeydiyyat tabını yarat"""
        reg_frame = tk.Frame(self.notebook, bg='#f0f8ff')
        self.notebook.add(reg_frame, text="Qeydiyyat")
        
        # Form çərçivəsi
        form_frame = tk.LabelFrame(reg_frame, text="Yeni İşçi Qeydiyyatı", 
                                  font=('Arial', 12, 'bold'), bg='#f0f8ff', fg='#2c3e50',
                                  padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Ad
        tk.Label(form_frame, text="Ad:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=10)
        self.name_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Soyad
        tk.Label(form_frame, text="Soyad:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=10)
        self.surname_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Parol
        tk.Label(form_frame, text="Parol:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=2, column=0, sticky='w', pady=10)
        self.password_entry = tk.Entry(form_frame, font=('Arial', 11), width=30, show='*')
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Parol təkrar
        tk.Label(form_frame, text="Parol Təkrar:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=3, column=0, sticky='w', pady=10)
        self.confirm_password_entry = tk.Entry(form_frame, font=('Arial', 11), width=30, show='*')
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Qeydiyyat button
        reg_button = tk.Button(form_frame, text="Qeydiyyatdan Keç", font=('Arial', 12, 'bold'),
                              bg='#27ae60', fg='white', padx=20, pady=10,
                              command=self.register_employee)
        reg_button.grid(row=4, column=0, columnspan=2, pady=20)
        
    def create_login_tab(self):
        """Login tabını yarat"""
        login_frame = tk.Frame(self.notebook, bg='#f0f8ff')
        self.notebook.add(login_frame, text="Login")
        
        # Form çərçivəsi
        form_frame = tk.LabelFrame(login_frame, text="İşçi Girişi", 
                                  font=('Arial', 12, 'bold'), bg='#f0f8ff', fg='#2c3e50',
                                  padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # İşçi ID
        tk.Label(form_frame, text="İşçi ID:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=15)
        self.login_id_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        self.login_id_entry.grid(row=0, column=1, padx=10, pady=15)
        
        # Parol
        tk.Label(form_frame, text="Parol:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=1, column=0, sticky='w', pady=15)
        self.login_password_entry = tk.Entry(form_frame, font=('Arial', 11), width=30, show='*')
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=15)
        
        # Login button
        login_button = tk.Button(form_frame, text="Giriş Et", font=('Arial', 12, 'bold'),
                               bg='#3498db', fg='white', padx=20, pady=10,
                               command=self.login_employee)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Status məlumatı
        self.login_status = tk.Label(form_frame, text="", font=('Arial', 10), 
                                   bg='#f0f8ff', fg='red')
        self.login_status.grid(row=3, column=0, columnspan=2)
        
    def create_audit_tab(self):
        """Audit tabını yarat"""
        audit_frame = tk.Frame(self.notebook, bg='#f0f8ff')
        self.notebook.add(audit_frame, text="Audit")
        
        # Form çərçivəsi
        form_frame = tk.LabelFrame(audit_frame, text="İşçi Audit Tarixçəsi", 
                                  font=('Arial', 12, 'bold'), bg='#f0f8ff', fg='#2c3e50',
                                  padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # İşçi seçimi
        tk.Label(form_frame, text="İşçi ID:", font=('Arial', 11, 'bold'), 
                bg='#f0f8ff', fg='#2c3e50').grid(row=0, column=0, sticky='w', pady=10)
        self.audit_id_entry = tk.Entry(form_frame, font=('Arial', 11), width=20)
        self.audit_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        
        # Audit button
        audit_button = tk.Button(form_frame, text="Audit Tarixçəsini Göstər", 
                               font=('Arial', 11, 'bold'), bg='#f39c12', fg='white',
                               command=self.show_audit)
        audit_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Audit nəticələri
        audit_results_frame = tk.Frame(form_frame, bg='#f0f8ff')
        audit_results_frame.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=10)
        
        # Treeview for audit results
        columns = ('Tarix', 'Hadisə', 'Detallar')
        self.audit_tree = ttk.Treeview(audit_results_frame, columns=columns, show='headings', height=15)
        
        # Sütun başlıqları
        for col in columns:
            self.audit_tree.heading(col, text=col)
            self.audit_tree.column(col, width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(audit_results_frame, orient=tk.VERTICAL, command=self.audit_tree.yview)
        self.audit_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.audit_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def create_logged_in_tab(self):
        """Login olan işçilər tabını yarat"""
        logged_frame = tk.Frame(self.notebook, bg='#f0f8ff')
        self.notebook.add(logged_frame, text="Login Olan İşçilər")
        
        # Başlıq
        title_label = tk.Label(logged_frame, text="Hal-hazırda Sistemdə Olan İşçilər", 
                              font=('Arial', 14, 'bold'), bg='#f0f8ff', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Treeview for logged in users
        columns = ('İşçi ID', 'Ad', 'Soyad', 'Login Vaxtı')
        self.logged_tree = ttk.Treeview(logged_frame, columns=columns, show='headings', height=20)
        
        # Sütun başlıqları
        for col in columns:
            self.logged_tree.heading(col, text=col)
            self.logged_tree.column(col, width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(logged_frame, orient=tk.VERTICAL, command=self.logged_tree.yview)
        self.logged_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.logged_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(logged_frame, bg='#f0f8ff')
        button_frame.pack(pady=10)
        
        # Yenilə button
        refresh_button = tk.Button(button_frame, text="Siyahını Yenilə", 
                                 font=('Arial', 11, 'bold'), bg='#9b59b6', fg='white',
                                 command=self.refresh_logged_in_list)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        # Təmizlə button
        clear_button = tk.Button(button_frame, text="Hamısını Çıxart", 
                               font=('Arial', 11, 'bold'), bg='#e74c3c', fg='white',
                               command=self.clear_logged_in_list)
        clear_button.pack(side=tk.LEFT, padx=5)
    
    def register_employee(self):
        """İşçi qeydiyyatı"""
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not name or not surname or not password:
            messagebox.showerror("Xəta", "Bütün sahələri doldurun!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Xəta", "Parollar uyğun gəlmir!")
            return
        
        if len(password) < 4:
            messagebox.showerror("Xəta", "Parol ən azı 4 simvol olmalıdır!")
            return
        
        # Yeni işçi ID yarat
        employee_id = str(len(self.employees) + 1001)
        
        # İşçi məlumatlarını saxla
        self.employees[employee_id] = {
            'name': name,
            'surname': surname,
            'password': password,
            'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Audit log
        self.add_audit_log(employee_id, "QEYDİYYAT", f"{name} {surname} qeydiyyatdan keçdi")
        
        # Məlumatları saxla
        if self.save_data(self.employees, self.data_file):
            messagebox.showinfo("Uğurlu", f"İşçi uğurla qeydiyyatdan keçdi!\nİşçi ID: {employee_id}")
            
            # Input sahələrini təmizlə
            self.name_entry.delete(0, tk.END)
            self.surname_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
    
    def login_employee(self):
        """İşçi login"""
        employee_id = self.login_id_entry.get().strip()
        password = self.login_password_entry.get()
        
        if not employee_id or not password:
            messagebox.showerror("Xəta", "İşçi ID və parol daxil edin!")
            return
        
        # Bloklama yoxla
        if employee_id in self.login_attempts and self.login_attempts[employee_id] >= 4:
            messagebox.showerror("Bloklanıb", "Bu hesab 4 uğursuz cəhddən sonra bloklanıb!")
            self.login_status.config(text="HESAB BLOKLANIB - İdarəçi ilə əlaqə saxlayın")
            return
        
        # İşçi yoxla
        if employee_id in self.employees:
            if self.employees[employee_id]['password'] == password:
                # Uğurlu login
                self.login_attempts[employee_id] = 0  # Uğursuz cəhdləri sıfırla
                self.save_data(self.login_attempts, self.login_attempts_file)
                
                # Login olanlar siyahısına əlavə et
                login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.logged_in_users[employee_id] = {
                    'name': self.employees[employee_id]['name'],
                    'surname': self.employees[employee_id]['surname'],
                    'login_time': login_time
                }
                self.save_data(self.logged_in_users, self.logged_in_file)
                
                # Audit log
                self.add_audit_log(employee_id, "LOGIN", "Uğurlu giriş")
                
                messagebox.showinfo("Uğurlu", f"Xoş gəldiniz, {self.employees[employee_id]['name']}!")
                self.login_status.config(text="UĞURLU GİRİŞ", fg='green')
                
                # Input sahələrini təmizlə
                self.login_id_entry.delete(0, tk.END)
                self.login_password_entry.delete(0, tk.END)
                
                # Login olanlar siyahısını yenilə
                self.refresh_logged_in_list()
                
                # Login olanlar tabına keç
                self.notebook.select(3)
                
            else:
                # Uğursuz login
                if employee_id not in self.login_attempts:
                    self.login_attempts[employee_id] = 0
                self.login_attempts[employee_id] += 1
                self.save_data(self.login_attempts, self.login_attempts_file)
                
                remaining_attempts = 4 - self.login_attempts[employee_id]
                
                # Audit log
                self.add_audit_log(employee_id, "LOGIN_XƏTA", "Yanlış parol")
                
                if remaining_attempts > 0:
                    messagebox.showerror("Xəta", f"Yanlış parol! {remaining_attempts} cəhd hüququnuz qalıb.")
                    self.login_status.config(text=f"YANLIŞ PAROL - {remaining_attempts} cəhd qalıb", fg='red')
                else:
                    messagebox.showerror("Bloklanıb", "4 uğursuz cəhd! Hesab bloklandı.")
                    self.login_status.config(text="HESAB BLOKLANIB", fg='red')
        else:
            messagebox.showerror("Xəta", "İşçi ID tapılmadı!")
            self.login_status.config(text="İŞÇİ ID TAPILMADI", fg='red')
    
    def show_audit(self):
        """Audit tarixçəsini göstər"""
        employee_id = self.audit_id_entry.get().strip()
        
        if not employee_id:
            messagebox.showerror("Xəta", "İşçi ID daxil edin!")
            return
        
        # Treeview-u təmizlə
        for item in self.audit_tree.get_children():
            self.audit_tree.delete(item)
        
        # Seçilmiş işçinin audit məlumatlarını göstər
        if employee_id in self.audit_log:
            for log in self.audit_log[employee_id]:
                self.audit_tree.insert('', tk.END, values=(
                    log.get('timestamp', ''),
                    log.get('event', ''),
                    log.get('details', '')
                ))
        else:
            messagebox.showinfo("Məlumat", "Bu işçi üçün audit məlumatı tapılmadı.")
    
    def refresh_logged_in_list(self):
        """Login olan işçilər siyahısını yenilə"""
        # Treeview-u təmizlə
        for item in self.logged_tree.get_children():
            self.logged_tree.delete(item)
        
        # Login olan işçiləri göstər
        if self.logged_in_users:
            for emp_id, info in self.logged_in_users.items():
                self.logged_tree.insert('', tk.END, values=(
                    emp_id,
                    info['name'],
                    info['surname'],
                    info['login_time']
                ))
        else:
            # Boş məlumat göstər
            self.logged_tree.insert('', tk.END, values=(
                "---", "---", "---", "---"
            ))
    
    def clear_logged_in_list(self):
        """Login olanlar siyahısını təmizlə"""
        result = messagebox.askyesno("Təsdiq", "Bütün login olan işçiləri çıxartmaq istədiyinizə əminsiniz?")
        if result:
            self.logged_in_users = {}
            self.save_data(self.logged_in_users, self.logged_in_file)
            self.refresh_logged_in_list()
            messagebox.showinfo("Uğurlu", "Bütün işçilər çıxarıldı!")
    
    def add_audit_log(self, employee_id, event, details):
        """Audit log əlavə et"""
        log_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'event': event,
            'details': details
        }
        
        if employee_id not in self.audit_log:
            self.audit_log[employee_id] = []
        
        self.audit_log[employee_id].append(log_entry)
        self.save_data(self.audit_log, self.audit_file)

def main():
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()