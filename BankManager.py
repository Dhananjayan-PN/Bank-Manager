from tkinter import *
from PIL import ImageTk, Image
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import dateutil.parser as parser
import os
import random


def encrypt(a):
    encrypted_string = ""
    for i in range(len(a)):
        char = a[i]
        if char.isupper():
            encrypted_string += chr(ord(char) + 42 - 65)
        else:
            encrypted_string += chr(ord(char) + 42)
    encrypted_string = encrypted_string[::-1]
    return encrypted_string


def decrypt(encrypted_string):
    j = ""
    encrypted_string = encrypted_string[::-1]
    for i in range(len(encrypted_string)):
        achar = encrypted_string[i]
        if (ord(achar) > 41) and ord(achar) < 68:
            j += chr(ord(achar) - 42 + 65)
        else:
            j += chr(ord(achar) - 42)
    return j


def callback():
    ano = E1.get()
    if ano == 1:
        print('Welcome Admin:', ano)
    else:
        print("Welcome User:", ano)


def credential_check():
    password = P1.get()
    global username
    username = E1.get()
    # print(">", password, username, '<')
    if password == admin_pass and username == admin_uname:
        admin()
    elif username in users.keys() and password == users[username][0]:
        customer(username)
    else:
        popup = Tk()
        popup.configure(background='DarkSlateGray1')
        popup.iconbitmap(r'Data/Logo.ico')
        popup.title("ERROR!")
        popup.geometry('350x100+470+300')
        lbl = Label(popup, text='Invalid Login Credentials', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
        lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        fnt = ('Helvetica', 10, 'bold')
        button = Button(popup, text='OK', font=fnt, width=10, command=popup.destroy, bg='red', fg='white')
        button.grid(row=1, column=1, pady=10)


def admin():
    frame.destroy()
    admin_frame = Frame(top, bg='DarkSlateGray1')
    admin_frame.pack(expand='yes', fill=BOTH)
    fnt = ('Helvetica', 30, 'bold')
    txt = 'Welcome Admin! What would you like to do?'
    lbl = Label(admin_frame, text=txt, font=('Helvetica', 40, 'bold'), bg='DarkSlateGray1')
    lbl.grid(row=0, column=0, columnspan=4, padx=50, pady=70)
    btn1 = Button(admin_frame, text='Create Acc.', font=fnt, width=12, command=create_acc, bg='black', fg='white')
    btn1.grid(row=1, column=1, pady=40, padx=100)
    btn2 = Button(admin_frame, text='Delete Acc.', font=fnt, width=12, command=del_acc, bg='black', fg='white')
    btn2.grid(row=1, column=2, pady=40, padx=100)
    btn3 = Button(admin_frame, text='Activate Acc.', font=fnt, width=12, command=active_acc, bg='black', fg='white')
    btn3.grid(row=2, column=1, pady=40, padx=100)
    btn4 = Button(admin_frame, text='Suspend Acc.', font=fnt, width=12, command=susp_acc, bg='black', fg='white')
    btn4.grid(row=2, column=2, pady=40, padx=100)
    btn5 = Button(admin_frame, text='View Accs.', font=fnt, width=12, command=view_accs, bg='black', fg='white')
    btn5.grid(row=3, column=1, pady=40, padx=100)
    fnt = ('Helvetica', 17, 'bold')
    btn6 = Button(admin_frame, text='Logout', font=fnt, width=7, height=1, command=relogin, bg='red', fg='white')
    btn6.grid(row=0, column=4, pady=0, padx=0)


def customer(username):
    if users[username][-2] == 'Suspended':
        popup = Tk()
        popup.configure(background='DarkSlateGray1')
        popup.iconbitmap(r'Data/Logo.ico')
        popup.title("ERROR!")
        popup.geometry('360x130+470+300')
        txt = 'Your Account has been Suspended.\n Please contact your bank.'
        lbl = Label(popup, text=txt, font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
        lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        fnt = ('Helvetica', 10, 'bold')
        button = Button(popup, text='OK', font=fnt, width=10, command=popup.destroy, bg='red', fg='white')
        button.grid(row=1, column=1, pady=10)
    else:
        frame.destroy()
        name = users[username][-1]
        cust_frame = Frame(top, bg='DarkSlateGray1')
        cust_frame.pack(expand='yes', fill=BOTH)
        fnt = ('Helvetica', 30, 'bold')
        txt = 'Welcome, {}! What would you like to do?'.format(name)
        lbl = Label(cust_frame, text=txt, font=('Helvetica', 35, 'bold'), bg='DarkSlateGray1')
        lbl.grid(row=0, column=0, columnspan=4, padx=50, pady=60)
        btn1 = Button(cust_frame, text='View Balance', font=fnt, width=15, bg='black', fg='white')
        func1 = lambda balance=users[username][1]: check_balance(users[username][1])
        btn1.bind('<Button-1>', func=func1)
        btn1.grid(row=1, column=1, pady=30, padx=100)
        btn2 = Button(cust_frame, text='Withdraw Cash', font=fnt, width=15, bg='black', fg='white')
        func2 = lambda balance=users[username][1]: withdraw(users[username][1])
        btn2.bind('<Button-1>', func=func2)
        btn2.grid(row=1, column=2, pady=30, padx=100)
        btn3 = Button(cust_frame, text='Deposit Money', font=fnt, width=15, bg='black', fg='white')
        func3 = lambda balance=users[username][1]: deposit(users[username][1])
        btn3.bind('<Button-1>', func=func3)
        btn3.grid(row=2, column=1, pady=30, padx=100)
        text = 'Change Password'
        btn4 = Button(cust_frame, text=text, font=fnt, width=15, command=change_pass, bg='black', fg='white')
        btn4.grid(row=2, column=2, pady=30, padx=100)
        btn5 = Button(cust_frame, text='View Graph', font=fnt, width=15, command=view_graph, bg='black', fg='white')
        btn5.grid(row=3, column=1, pady=30, padx=100)
        fnt = ('Helvetica', 17, 'bold')
        btn7 = Button(cust_frame, text='Logout', font=fnt, width=7, height=1, command=relogin, bg='red', fg='white')
        btn7.grid(row=0, column=4, pady=0, padx=0)


def create_acc():
    def create_account():
        d = name1.get()
        e = password1.get()
        f = re_enter_password.get()
        try:
            city = listbox.get(listbox.curselection())
        except:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('370x150+470+300')
            txt = "Please fill out all details."
            lbl = Label(pop, text=txt, font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        if len(d) and len(e) and len(f) > 0:
            if e == f and len(e) >= 8:
                popup.destroy()
                accno = str(random.randint(10000000,99999999))
                while accno in users.keys():
                    accno = str(random.randint(10000000,99999999))
                name = d
                password = e
                date = datetime.datetime.now().isoformat()
                users[accno] = [password, 0, date, city , 'Active', name]
                with open(r"Data/Users.txt",'w',encoding='utf-8') as file:
                    file.write(encrypt('{}'.format(users)))
                with open(r"Data/{}.txt".format(accno),'w') as file:
                    file.write('0'+'*'+date+'\n')
                pop = Tk()
                pop.configure(background='DarkSlateGray1')
                pop.iconbitmap(r'Data/Logo.ico')
                pop.title("Success!")
                pop.geometry('370x150+470+300')
                txt = "Account Created! \n Acc no: {}".format(accno)
                lbl = Label(pop, text=txt, font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
                lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
                fnt = ('Helvetica', 10, 'bold')
                button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
                button2.grid(row=1, column=1, pady=10)

            if e != f:
                pop = Tk()
                pop.configure(background='DarkSlateGray1')
                pop.iconbitmap(r'Data/Logo.ico')
                pop.title("ERROR!")
                pop.geometry('370x150+470+300')
                txt = "Passwords Dont Match !!\n Please try again !"
                lbl = Label(pop, text=txt, font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
                lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
                fnt = ('Helvetica', 10, 'bold')
                button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
                button2.grid(row=1, column=1, pady=10)
                name1.delete(0, len(d))
                password1.delete(0, len(e))
                re_enter_password.delete(0, len(f))

            elif len(e) < 8:
                pop = Tk()
                pop.configure(background='DarkSlateGray1')
                pop.iconbitmap(r'Data/Logo.ico')
                pop.title("ERROR!")
                pop.geometry('350x150+470+300')
                txt = "Password Too Short!!\n Please try again!"
                lbl = Label(pop, text=txt, font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
                lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
                fnt = ('Helvetica', 10, 'bold')
                button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
                button2.grid(row=1, column=1, pady=10)
                name1.delete(0, len(d))
                password1.delete(0, len(e))
                re_enter_password.delete(0, len(f))

        elif len(e) == 0:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('370x150+470+300')
            txt = "Please enter a password \n and try again!"
            lbl = Label(pop, text=txt, font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
            name1.delete(0, len(d))
            password1.delete(0, len(e))
            re_enter_password.delete(0, len(f))
        else:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('390x100+470+300')
            txt = "Please fill out all details!"
            lbl = Label(pop, text=txt, font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)

    def check(pop):
        fnt = ('Helvetica', 12, 'bold')
        login = Button(pop, text='Create', font=fnt, command=create_account, width=10, bg='red', fg='white')
        login.grid(row=5, column=1, padx=10, pady=5)

    popup = Toplevel()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Create Account")
    popup.geometry('450x290+470+250')
    popup.resizable(True, True)
    _name = Label(popup, text='Username:', font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    _name.grid(row=0, column=0, padx=10, pady=5)
    _password = Label(popup, text='Password:', font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    _password.grid(row=1, column=0, padx=10, pady=5)
    _re_enter_password = Label(popup, text='Re-enter password:', font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    _re_enter_password.grid(row=2, column=0, padx=10, pady=5)
    _city = Label(popup, text='Select your city:', font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    _city.grid(row=3, column=0, padx=10, pady=5)
    name1 = Entry(popup, width=18, bd=4, font=('Helvetica', 15, 'bold'), bg='light cyan')
    name1.grid(row=0, column=1, padx=10, pady=5)
    password1 = Entry(popup, width=18, show='*', bd=4, font=('Helvetica', 15, 'bold'), bg='light cyan')
    password1.grid(row=1, column=1, padx=10, pady=5)
    re_enter_password = Entry(popup, width=18, show='*', bd=4, font=('Helvetica', 15, 'bold'), bg='light cyan')
    re_enter_password.grid(row=2, column=1, padx=10, pady=5)
    txt = "I agree to all terms and conditions"
    fnt = ('Helvetica', 15, 'bold')
    radio = Radiobutton(popup, text=txt, font=fnt, bg='DarkSlateGray1', variable=IntVar(), value=1)
    radio.bind('<Button-1>', func=lambda event, pop=popup: check(pop))
    radio.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    scrollbar = Scrollbar(popup)
    listbox = Listbox(popup, yscrollcommand=scrollbar.set, height=3, bd=2,
                      font=('Helvetica', 10, 'bold'), bg='light cyan')
    scrollbar.config(command=listbox.yview)
    scrollbar.grid(row=3, column=2, padx=10, pady=5)
    listbox.insert(END, 'Bangalore', 'Chennai', 'Cochin')
    listbox.grid(row=3, column=1, padx=10, pady=5)


def del_acc():
    def delete():
        acc_no = ano.get()
        popup.destroy()
        if acc_no not in users.keys():
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('250x100+470+300')
            lbl = Label(pop, text='Invalid Account!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        else:
            try:
                os.remove(r"Data/{}.txt".format(acc_no))
            except:
                pass
            del users[acc_no]
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("Success!")
            pop.geometry('460x100+470+300')
            lbl = Label(pop, text='Account Deleted Successfully!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button3 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button3.grid(row=1, column=1, pady=10)
    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Delete Account")
    popup.geometry('400x160+470+300')
    lbl = Label(popup, text="Account No:", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    lbl.grid(row=1, column=0, padx=20, pady=20)
    global ano
    ano = Entry(popup, bd=4, width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    ano.grid(row=1, column=1, pady=20)
    fnt = ('Helvetica', 12, 'bold')
    button = Button(popup, text='Delete', font=fnt, command=delete, width=15, bg='red', fg='white')
    button.grid(row=3, column=1, pady=10)


def active_acc():
    def activate():
        acc_no = ano.get()
        popup.destroy()
        if acc_no not in users.keys():
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('250x100+470+300')
            lbl = Label(pop, text='Invalid Account', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        elif users[acc_no][-2] == 'Active':
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('340x100+470+300')
            lbl = Label(pop, text='Account already Active!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        else:
            users[acc_no][-2] = "Active"
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("Success!")
            pop.geometry('450x100+470+300')
            lbl = Label(pop, text='Account Activated Successfully!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button3 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button3.grid(row=1, column=1, pady=10)

    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Activate Account")
    popup.geometry('400x160+470+300')
    lbl = Label(popup, text="Account No:", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    lbl.grid(row=1, column=0, padx=20, pady=20)
    global ano
    ano = Entry(popup, bd=4, width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    ano.grid(row=1, column=1, pady=20)
    fnt = ('Helvetica', 12, 'bold')
    button = Button(popup, text='Activate', font=fnt, command=activate, width=15, bg='red', fg='white')
    button.grid(row=3, column=1, pady=10)


def susp_acc():
    def suspend():
        acc_no = ano.get()
        popup.destroy()
        if acc_no not in users.keys():
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('250x100+470+300')
            lbl = Label(pop, text='Invalid Account', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        elif users[acc_no][-2] == 'Suspended':
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('410x100+470+300')
            lbl = Label(pop, text='Account already Suspended!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        else:
            users[acc_no][-2] = "Suspended"
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("Success!")
            pop.geometry('480x100+470+300')
            lbl = Label(pop, text='Account Suspended Successfully!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button3 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button3.grid(row=1, column=1, pady=10)
    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Suspend Account")
    popup.geometry('400x160+470+300')
    lbl = Label(popup, text="Account No:", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    lbl.grid(row=1, column=0, padx=20, pady=20)
    global ano
    ano = Entry(popup, bd=4, width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    ano.grid(row=1, column=1, pady=20)
    fnt = ('Helvetica', 12, 'bold')
    button = Button(popup, text='Suspend', font=fnt, command=suspend, width=15, bg='red', fg='white')
    button.grid(row=3, column=1, pady=10)


def view_accs():
    win = Tk()
    win.configure(background='DarkSlateGray1')
    win.iconbitmap(r'Data/Logo.ico')
    win.title("Account Graph")
    win.geometry('640x520+300+100')
    lbl1 = Label(win, text='Accounts:-', font=('Helvetica', 30, 'bold'), bg='DarkSlateGray1')
    lbl1.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
    accounts = [[users[i][-1], i, users[i][-2]] for i in users.keys()]
    if len(accounts) == 0:
        txt = "No accounts created."
        lbl = Label(win, text=txt, font=('Helvetica', 20), bg='DarkSlateGray1')
        lbl.grid(row=1, column=0, pady=10, padx=10)
    else:
        for i in range(0, len(accounts)):
            txt = "{}. {}....{} ({})".format(i+1, accounts[i][0], accounts[i][1], accounts[i][2   ])
            lbl = Label(win, text=txt, font=('Helvetica', 20), bg='DarkSlateGray1')
            lbl.grid(row=i+1, column=0, pady=10, padx=10)


def check_balance(balance):
    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Balance Amount")
    popup.geometry('450x100+470+300')
    # txt = "Account Balance: "+str(users[username][1])
    lbl = Label(popup, text="Account Balance: "+str(balance), font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
    lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
    fnt = ('Helvetica', 10, 'bold')
    button = Button(popup, text='OK', font=fnt, width=10, command=popup.destroy, bg='red', fg='white')
    button.grid(row=1, column=1, pady=10)


def withdraw(bal2):
    def withdraw_cash(balance):
        amt = amount.get()
        popup.destroy()
        if '.' in amt:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.title("ERROR!")
            pop.iconbitmap(r'Data/Logo.ico')
            pop.geometry('390x100+470+300')
            lbl = Label(pop, text='Please enter a valid amount', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        elif int(amt) <= 0 or '.' in amt:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('390x100+470+300')
            lbl = Label(pop, text='Please enter a valid amount', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        elif eval(amt) >= balance:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('300x100+470+300')
            lbl = Label(pop, text='Not Enough Balance !', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        else:
            users[username][1] -= int(amt)
            date = datetime.datetime.now()
            try:
                with open(r"Data/{}.txt".format(username),'a') as f:
                    f.write(str(users[username][1])+'*'+date.isoformat()+'\n')
            except:
                with open(r"Data/{}.txt".format(username)) as f:
                    f.write(str(users[username][1])+'*'+date.isoformat()+'\n')

            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("Success!")
            pop.geometry('410x100+470+300')
            lbl = Label(pop, text='Cash Withdrawn Successfully !', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button3 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button3.grid(row=1, column=1, pady=10)

    global popup
    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Withdraw Cash")
    popup.geometry('450x200+470+300')
    wa = Label(popup, text="Withdrawal Amount :", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    wa.grid(row=1, column=0, padx=20, pady=40)
    global amount
    amount = Entry(popup, bd=4, width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    amount.grid(row=1, column=1, pady=50)
    fnt = ('Helvetica', 12, 'bold')
    button = Button(popup, text='Withdraw', font=fnt, width=13, bg='red', fg='white')
    fnc = lambda balance=bal2: withdraw_cash(bal2)
    button.bind("<Button-1>", func=fnc)
    button.grid(row=2, column=1, pady=10)


def change_pass():
    def changepassword():
        old = cpass.get()
        new = npass.get()
        popup.destroy()
        if old != users[username][0]:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('390x100+470+300')
            lbl = Label(pop, text='Invalid Password', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        else:
            users[username][0] = new
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("Success!")
            pop.geometry('450x100+470+300')
            lbl = Label(pop, text='Password Changed Successfully', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button3 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button3.grid(row=1, column=1, pady=10)

    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Change Password")
    popup.geometry('450x210+470+300')
    cp = Label(popup, text="Current Password:", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    cp.grid(row=1, column=0, padx=20, pady=20)
    global cpass
    cpass = Entry(popup, bd=4, show="*", width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    cpass.grid(row=1, column=1, pady=20)
    np = Label(popup, text="New Password:", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    np.grid(row=2, column=0, padx=20, pady=20)
    global npass
    npass = Entry(popup, bd=4, show="*", width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    npass.grid(row=2, column=1, pady=20)
    fnt = ('Helvetica', 12, 'bold')
    button = Button(popup, text='Change Password', font=fnt, command=changepassword, width=15, bg='red', fg='white')
    button.grid(row=3, column=1, pady=10)


def view_graph():
    def delete_temp():
        gwin.destroy()
        try:
            os.remove(r"Data/temp.png")
        except:
            pass
        
    try:
        with open(r"Data/{}.txt".format(username), 'r') as f:
            data = f.readlines()
        fig = plt.figure()
        y = [int(i[:i.index('*')]) for i in data]
        x = [parser.parse(i[i.index('*')+1:-1]) for i in data]
        plt.plot_date(x, y, 'b-')
        gwin = Tk()
        gwin.configure(background='white')
        gwin.iconbitmap(r'Data/Logo.ico')
        gwin.title("Account Graph")
        gwin.geometry('640x520+300+100')
        canvas = FigureCanvasTkAgg(fig, master=gwin)
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=5)
        canvas.draw()
        fnt = ('Helvetica', 10, 'bold')
        button2 = Button(gwin, text='OK', font=fnt, width=10, command=delete_temp, bg='red', fg='white')
        button2.grid(row=1, column=2, pady=10)
        gwin.mainloop()
    except Exception:
        pop = Tk()
        pop.configure(background='DarkSlateGray1')
        pop.iconbitmap(r'Data/Logo.ico')
        pop.title("ERROR!")
        pop.geometry('200x100+470+300')
        lbl = Label(pop, text='NO Data!!', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
        lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        fnt = ('Helvetica', 10, 'bold')
        button2 = Button(pop, text='OK', font=fnt, width=10, command=delete_temp, bg='red', fg='white')
        button2.grid(row=1, column=1, pady=10)


def deposit(bal2):
    def withdraw_cash(balance):
        amt = amount.get()
        popup.destroy()
        if '.' in amt:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('390x100+470+300')
            lbl = Label(pop, text='Please enter a valid amount', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        elif int(amt) <= 0:
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("ERROR!")
            pop.geometry('390x100+470+300')
            lbl = Label(pop, text='Please enter a valid amount', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button2 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button2.grid(row=1, column=1, pady=10)
        else:
            users[username][1] += int(amt)
            date = datetime.datetime.now()
            try:
                with open(r"Data/{}.txt".format(username),'a') as f:
                    f.write(str(users[username][1])+'*'+date.isoformat()+'\n')
            except:
                with open(r"Data/{}.txt".format(username)) as f:
                    f.write(str(users[username][1])+'*'+date.isoformat()+'\n')
            pop = Tk()
            pop.configure(background='DarkSlateGray1')
            pop.iconbitmap(r'Data/Logo.ico')
            pop.title("Success!")
            pop.geometry('430x100+470+300')
            lbl = Label(pop, text='Money Deposited Successfully', font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
            lbl.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
            fnt = ('Helvetica', 10, 'bold')
            button3 = Button(pop, text='OK', font=fnt, width=10, command=pop.destroy, bg='red', fg='white')
            button3.grid(row=1, column=1, pady=10)
    global popup
    popup = Tk()
    popup.configure(background='DarkSlateGray1')
    popup.iconbitmap(r'Data/Logo.ico')
    popup.title("Deposit Money")
    popup.geometry('450x200+470+300')
    wa = Label(popup, text="Deposit Amount:", font=('Helvetica', 15, 'bold'), bg='DarkSlateGray1')
    wa.grid(row=1, column=0, padx=20, pady=40)
    global amount
    amount = Entry(popup, bd=4, width=15, font=('Helvetica', 15, 'bold'), bg='light cyan')
    amount.grid(row=1, column=1, pady=50)
    fnt = ('Helvetica', 12, 'bold')
    button = Button(popup, text='Deposit', font=fnt, width=13, bg='red', fg='white')
    fnc = lambda balance=bal2: withdraw_cash(bal2)
    button.bind("<Button-1>", func=fnc)
    button.grid(row=2, column=1, pady=10)                                         #


def relogin():
    with open(r"Data/Users.txt", 'w', encoding='utf-8') as file:
        file.write(encrypt(str(users)))
    top.destroy()
    start()


def start():
    # users dictionary format: {username:[password, money, date_of_creation, city, status, name_of_owner],...}
    with open("Data//Users.txt", encoding='utf-8') as file:
        data = file.read()
        global users
        users = eval(decrypt(data))
    with open("Data//Admin.txt", encoding='utf-8') as file:
        data = file.read()
        global admin_pass
        global admin_uname
        admin_uname, admin_pass = eval(decrypt(str(data)))

    global top
    top = Tk()
    top.iconbitmap(r'Data/Logo.ico')
    top.geometry('1366x760+0+0')
    top.title("THE JDAD BANK")
    top.attributes("-fullscreen", True)
    global frame
    frame = Frame(top, bg='DarkSlateGray1')

    frame.pack(expand='yes', fill=BOTH)
    # Login Heading
    H = Label(frame, text= " "*20+"THE JDAD BANK", font=('Helvetica', 45, 'bold'), bg='DarkSlateGray1')
    H.grid(row=1, column=1, columnspan=3, pady=120, padx=50)
    # Logo
    img = ImageTk.PhotoImage(Image.open(r'Data/Logo.png'))
    logo = Label(frame, image = img)
    logo.grid(row=1, column=1, pady=120, padx=250)
    # Acc Number Field
    AN = Label(frame, text="Account Number :", font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
    AN.grid(row=5, column=1, padx=50, pady=5)
    global E1
    E1 = Entry(frame, bd=4, width=40, font=('Helvetica', 15, 'bold'), bg='light cyan')
    E1.grid(row=5, column=2)
    # Password Field
    P = Label(frame, text="Password :", font=('Helvetica', 20, 'bold'), bg='DarkSlateGray1')
    P.grid(row=6, column=1, padx=10, pady=5)
    global P1
    P1 = Entry(frame, bd=5, show="*", width=40, font=('Helvetica', 15, 'bold'), bg='light cyan')
    P1.grid(row=6, column=2)
    font = ('Helvetica', 10, 'bold')
    submit = Button(frame, text="SUBMIT", font=font, width=10, command=credential_check, bg='red', fg='white')
    submit.grid(row=10, column=2, pady=50)
    top.mainloop()


start()
