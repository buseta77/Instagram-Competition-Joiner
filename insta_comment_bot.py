from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
import tkinter as tk
from tkinter import ttk
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import sqlite3
import pandas as pd
from tkinter import filedialog as fd


def close_all():
    window.quit()
    window.destroy()
    browser.quit()


def launch_disconnect():
    browser.get('https://www.instagram.com/')
    time.sleep(4)
    browser.find_element(By.CSS_SELECTOR, "//img[@data-testid='user-avatar']").click()
    time.sleep(3)
    browser.find_element(By.CSS_SELECTOR, "//div[@class='_01UL2']/div[2]").click()
    connect_info.config(text="You're now disconnected.")
    connect_button.config(state=enabled)
    add_comment_button.place_forget()
    disconnect_button.place_forget()


def launch_comment(post_url, value_a, value_b):
    global enabled
    global end
    event_log.delete(0, end)
    event_log.insert(0, 'Process started...')
    browser.get(post_url)
    time.sleep(5)
    try:
        browser.find_element(By.XPATH, "//textarea[@data-testid='post-comment-text-area']")
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(5)
        try:
            browser.find_element(By.XPATH, "//textarea[@data-testid='post-comment-text-area']")
        except selenium.common.exceptions.NoSuchElementException:
            event_log.insert(1, 'Error: Make sure to send proper Instagram post URL. Process stopped.')
            custom_tag_button.config(state=enabled)
            run_button.config(state=enabled)
            users_button.config(state=enabled)
            return
    p = 1
    conn = sqlite3.connect('insta_users.db')
    cursor = conn.cursor()
    for a in range(len(value_a)):
        event_log.insert(end, f"Info: Next {value_a[a]} comments will tag {value_b[a]} users each.")
        for s in range(value_a[a]):
            tag_list = ['']
            sql = f"SELECT USERNAME FROM USERS ORDER BY RANDOM() LIMIT {value_b[a]}"
            cursor.execute(sql)
            for user in cursor.fetchall():
                tag_list.append(user[0])
            comment_text = ' @'.join(tag_list).strip()
            tagged = ', '.join(tag_list).strip()
            browser.find_element(By.XPATH, "//textarea[@data-testid='post-comment-text-area']").send_keys(comment_text, Keys.ENTER)
            event_log.insert(end, f"Comment#{p} is made. Tagged users: '{tagged}'.")
            p += 1
            event_log.insert(end, "Waiting 1 minute for the next comment.")
            time.sleep(60)
    conn.close()
    event_log.insert(end, f"All comments are made. Process has finished.")
    custom_tag_button.config(state=enabled)
    run_button.config(state=enabled)
    users_button.config(state=enabled)
    add_comment_button.config(state=enabled)
    disconnect_button.config(state=enabled)
    return


def comment_insta(post_url, value_a, value_b):
    if post_url == '':
        run_info.config(text='Enter Post URL!')
    else:
        if value_a == [] or sum(value_a) == 0:
            run_info.config(text='Set Tags for Comments!')
        else:
            custom_tag_button.config(state=tk.DISABLED)
            run_button.config(state=tk.DISABLED)
            users_button.config(state=tk.DISABLED)
            add_comment_button.config(state=tk.DISABLED)
            disconnect_button.config(state=tk.DISABLED)
            uu = threading.Thread(target=lambda: launch_comment(post_url, value_a, value_b))
            uu.start()


def launch_login(a, b):
    connect_info.config(text='Connecting...')
    login_url = 'https://www.instagram.com/accounts/login/'
    browser.get(login_url)
    time.sleep(3)
    try:
        browser.find_element(By.NAME, 'username').send_keys(a, Keys.TAB, b, Keys.ENTER)
        time.sleep(3)
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(5)
        browser.find_element(By.NAME, 'username').send_keys(a, Keys.TAB, b, Keys.ENTER)
    try:
        browser.find_element(By.XPATH, "//p[@data-testid='login-error-message']")
        connect_info.config(text='Either your username or password is wrong!')
    except selenium.common.exceptions.NoSuchElementException:
        connect_info.config(text="You're connected! Now, you can comment on the posts. To disconnect from your Instagram account, click 'Disconnect' button.")
        add_comment_button.place(relx=0.08, rely=0.60, anchor=tk.W, relwidth=0.14, relheight=0.16)
        disconnect_button.place(relx=0.08, rely=0.74, anchor=tk.W, relwidth=0.14, relheight=0.10)
        connect_button.config(state=tk.DISABLED)
    return


def login_insta(username, password):
    def add_comment():
        def custom_tag():
            def add_line():
                global i
                x = pop_up.grid_size()[1]
                a1 = ttk.Spinbox(master=pop_up, from_=0, to=int(max_comment), width=3)
                spin_a.insert(i, a1)
                spin_a[i].grid(row=x, column=0, padx=10, pady=5)
                a2 = ttk.Label(master=pop_up, text='comment/s will tag')
                spin_text_a.insert(i, a2)
                spin_text_a[i].grid(row=x, column=1, pady=5)
                a3 = ttk.Spinbox(master=pop_up, from_=0, to=100, width=3)
                spin_b.insert(i, a3)
                spin_b[i].grid(row=x, column=2, padx=10, pady=5)
                a4 = ttk.Label(master=pop_up, text='username/s.')
                spin_text_b.insert(i, a4)
                spin_text_b[i].grid(row=x, column=3, pady=5)
                i += 1

            def submit_tag():
                global value_a, value_b
                value_a, value_b = [], []
                k = 0
                for j in range(0, i):
                    if spin_a[j].get() == '' or spin_a[j].get() == '0':
                        pass
                    else:
                        if spin_b[j].get() == '' or spin_b[j].get() == '0':
                            tag_info.config(text='You cannot tag 0 people!')
                            return
                        else:
                            value_a.insert(k, int(spin_a[j].get()))
                            value_b.insert(k, int(spin_b[j].get()))
                            k += 1
                if sum(value_a) == int(max_comment):
                    pop_up.destroy()
                    if run_info.cget("text") == 'Tag numbers are set.':
                        run_info.config(text='Tag numbers are updated.')
                    else:
                        run_info.config(text='Tag numbers are set.')
                else:
                    warning_1 = 'Total comment number must be ' + str(max_comment) + ' !!!'
                    tag_info.config(text=warning_1)

            max_comment = nr_comment_entry.get()
            if max_comment == '' or max_comment == '0':
                run_info.config(text='Enter number of comments first!')
            else:
                pop_up = tk.Toplevel()
                pop_up.title('Custom Tagging')
                spin_a.insert(0, ttk.Spinbox(master=pop_up, from_=0, to=int(max_comment), width=3))
                spin_a[0].grid(row=1, column=0, padx=10, pady=5)
                spin_text_a.insert(0, ttk.Label(master=pop_up, text='comment/s will tag'))
                spin_text_a[0].grid(row=1, column=1, pady=5)
                spin_b.insert(0, ttk.Spinbox(master=pop_up, from_=0, to=100, width=3))
                spin_b[0].grid(row=1, column=2, padx=10, pady=5)
                spin_text_b.insert(0, ttk.Label(master=pop_up, text='username/s.'))
                spin_text_b[0].grid(row=1, column=3, pady=5)
                spin_a.insert(1, ttk.Spinbox(master=pop_up, from_=0, to=int(max_comment), width=3))
                spin_a[1].grid(row=2, column=0, padx=10, pady=5)
                spin_text_a.insert(1, ttk.Label(master=pop_up, text='comment/s will tag'))
                spin_text_a[1].grid(row=2, column=1, pady=5)
                spin_b.insert(1, ttk.Spinbox(master=pop_up, from_=0, to=100, width=3))
                spin_b[1].grid(row=2, column=2, padx=10, pady=5)
                spin_text_b.insert(1, ttk.Label(master=pop_up, text='username/s.'))
                spin_text_b[1].grid(row=2, column=3, pady=5)
                spin_a.insert(2, ttk.Spinbox(master=pop_up, from_=0, to=int(max_comment), width=3))
                spin_a[2].grid(row=3, column=0, padx=10, pady=5)
                spin_text_a.insert(2, ttk.Label(master=pop_up, text='comment/s will tag'))
                spin_text_a[2].grid(row=3, column=1, pady=5)
                spin_b.insert(2, ttk.Spinbox(master=pop_up, from_=0, to=100, width=3))
                spin_b[2].grid(row=3, column=2, padx=10, pady=5)
                spin_text_b.insert(2, ttk.Label(master=pop_up, text='username/s.'))
                spin_text_b[2].grid(row=3, column=3, pady=5)
                tag_info = ttk.Label(master=pop_up, text='Note: You can scroll your mouse to change values.')
                tag_info.grid(row=0, column=0, columnspan=4, sticky=tk.E, pady=5)
                add_line_button = ttk.Button(master=pop_up, text='Add Line', command=add_line)
                add_line_button.grid(row=0, column=4, padx=20, pady=5)
                submit_tag_button = ttk.Button(master=pop_up, text='Submit', command=submit_tag)
                submit_tag_button.grid(row=1, column=4, padx=20, pady=5)

        url_post_text.place(relx=0.33, rely=0.10, anchor=tk.W)
        nr_comment_text.place(relx=0.33, rely=0.15, anchor=tk.W)
        nr_tag_text.place(relx=0.33, rely=0.20, anchor=tk.W)
        url_post_entry.place(relx=0.43, rely=0.10, anchor=tk.W, relwidth=0.20)
        nr_comment_entry.place(relx=0.43, rely=0.15, anchor=tk.W, relwidth=0.20)
        global i
        i = 3
        # spin_a and spin_b will store the values for value_a and value_b respectively.
        spin_a, spin_b, spin_text_a, spin_text_b = [], [], [], []
        # value_a will store the comment partition, i.e, comment number is 10 and value_a = [5, 3, 2]
        # value_b will store the tag counts, i.e., value_b = [3, 2, 1] means 5 comments will tag 3 people, 3 comments will tag 2 people, etc.
        global value_a, value_b
        value_a, value_b = [], []
        custom_tag_button.place(relx=0.53, rely=0.20, anchor=tk.W, relwidth=0.10)
        custom_tag_button.config(command=custom_tag)
        labelframe.place(relx=0.33, rely=0.60, anchor=tk.W, relwidth=0.30, relheight=0.50)
        run_button.config(command=lambda: comment_insta(url_post_entry.get(), value_a, value_b))
        run_button.place(relx=0.53, rely=0.90, anchor=tk.W, relwidth=0.10)
        run_info.place(relx=0.40, rely=0.28, anchor=tk.W)
        event_log.pack(expand=True, fill='both')

    def disconnect():
        global username
        global password
        username = ''
        password = ''
        username_entry.delete(0, tk.END)
        pw_entry.delete(0, tk.END)
        vv = threading.Thread(target=lambda: launch_disconnect())
        vv.start()

    if len(password) < 6:
        connect_info.config(text='Password must be at least 6 characters!')
    else:
        tt = threading.Thread(target=lambda: launch_login(username, password))
        tt.start()
        add_comment_button.config(command=add_comment)
        disconnect_button.config(command=disconnect)


def users_db():
    def user_adding():
        def add_new_user():
            try:
                global r_5
                user_input = []
                l = 0
                for k in range(0, r_5):
                    a1 = new_users[k].get()
                    if a1 != '':
                        user_input.insert(l, a1)
                        l += 1
                conn = sqlite3.connect('insta_users.db')
                cursor = conn.cursor()
                for element in user_input:
                    sql = f"INSERT INTO USERS(USERNAME) VALUES ('{element}')"
                    cursor.execute(sql)
                    conn.commit()
                conn.close()
                user_tree.place_forget()
                users_db()
                pop_up.destroy()
                r_5 = 5
            except sqlite3.IntegrityError:
                ttk.Label(master=pop_up, text='Duplicate usernames!').grid(row=0, column=0, padx=30, pady=10)

        def add_5_user():
            global r_5
            for j in range(0, 5):
                new_users.insert(r_5, ttk.Entry(master=pop_up))
                new_users[r_5].grid(row=r_5 + 1, column=0, pady=3)
                r_5 += 1

        def add_10_user():
            global r_5
            for j in range(0, 10):
                new_users.insert(r_5, ttk.Entry(master=pop_up))
                new_users[r_5].grid(row=r_5 + 1, column=0, pady=3)
                r_5 += 1
        new_users = []
        pop_up = tk.Toplevel()
        pop_up.title('Add Users')
        ttk.Label(master=pop_up, text='Add new users below:').grid(row=0, column=0, padx=30, pady=10)
        add_user_button = ttk.Button(master=pop_up, text='SUBMIT', command=add_new_user)
        add_user_button.grid(row=0, column=1, padx=10, pady=2, ipady=3)
        add_5 = ttk.Button(master=pop_up, text='Add 5 Lines', command=add_5_user)
        add_5.grid(row=1, column=1, padx=10, pady=1)
        add_10 = ttk.Button(master=pop_up, text='Add 10 Lines', command=add_10_user)
        add_10.grid(row=2, column=1, padx=10, pady=1)
        for i in range(0, 5):
            new_users.insert(i, ttk.Entry(master=pop_up))
            new_users[i].grid(row=i + 1, column=0, pady=3)

    def user_editing():
        def execute_edit():
            conn = sqlite3.connect('insta_users.db')
            for i in range(0, length):
                aa = edit_entry[i].get()
                bb = new_edits[i]
                cursor = conn.cursor()
                sql = f"UPDATE USERS SET USERNAME = '{aa}' WHERE USERNAME = '{bb}'"
                cursor.execute(sql)
                conn.commit()
            conn.close()
            user_tree.place_forget()
            users_db()
            pop_up.destroy()
        edit_list = []
        edit_entry = []
        new_edits = []
        edit_tuple = user_tree.selection()
        for data in edit_tuple:
            data_edit = user_tree.item(data)['values'][0]
            edit_list.append(data_edit)
        if edit_list == []:
            return
        else:
            length = len(edit_list)
            pop_up = tk.Toplevel()
            pop_up.title('Edit Users')
            ttk.Label(master=pop_up, text='Edit users below:').grid(row=0, column=0, padx=30, pady=10)
            add_user_button = ttk.Button(master=pop_up, text='SUBMIT', command=execute_edit)
            add_user_button.grid(row=0, column=1, padx=10, pady=2, ipady=3)
            conn = sqlite3.connect('insta_users.db')
            cursor = conn.cursor()
            for i in range(0, length):
                edit_entry.insert(i, ttk.Entry(master=pop_up))
                edit_entry[i].grid(row=i + 1, column=0, pady=3)
                sql = f"SELECT USERNAME FROM USERS WHERE USERNAME = '{edit_list[i]}'"
                cursor.execute(sql)
                name = str(cursor.fetchone()[0]).strip()
                new_edits.append(name)
                edit_entry[i].insert(tk.END, name)
            conn.close()

    def user_deleting():
        def execute_delete():
            conn = sqlite3.connect('insta_users.db')
            cursor = conn.cursor()
            for element in del_list:
                sql = f"DELETE FROM USERS WHERE USERNAME = '{element}'"
                cursor.execute(sql)
                conn.commit()
            conn.close()
            user_tree.place_forget()
            users_db()
            pop_up.destroy()

        def dont_execute():
            pop_up.destroy()
        del_list = []
        del_tuple = user_tree.selection()
        for data in del_tuple:
            data_del = user_tree.item(data)['values'][0]
            del_list.append(data_del)
        if del_list == []:
            return
        else:
            pop_up = tk.Toplevel()
            pop_up.title('Warning')
            ws = pop_up.winfo_screenwidth()
            hs = pop_up.winfo_screenheight()
            xx = (ws / 2) - (200 / 2)
            yy = (hs / 2) - (100 / 2)
            pop_up.geometry('%dx%d+%d+%d' % (200, 100, xx, yy))
            question = ttk.Label(master=pop_up, text='Are you sure?')
            question.place(relx=0.50, anchor=tk.CENTER, rely=0.20)
            yes = tk.Button(master=pop_up, text='Yes', command=execute_delete)
            yes.place(relx=0.35, anchor=tk.CENTER, rely=0.60, relwidth=0.30)
            no = tk.Button(master=pop_up, text='No', command=dont_execute)
            no.place(relx=0.65, anchor=tk.CENTER, rely=0.60, relwidth=0.30)

    def user_importing():
        try:
            filetypes = (('Excel files', '*.xlsx'), ('All files', '*.*'))
            filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
            excel = pd.read_excel(f'{filename}', header=None)
            conn = sqlite3.connect('insta_users.db')
            cursor = conn.cursor()
            for g in range(0, len(excel)):
                sql = f"INSERT INTO USERS(USERNAME) VALUES ('{excel[0][g]}')"
                cursor.execute(sql)
                conn.commit()
            conn.close()
            user_tree.place_forget()
            users_db()
        except sqlite3.IntegrityError:
            new_window = tk.Toplevel()
            new_window.title('Error')
            ws = new_window.winfo_screenwidth()
            hs = new_window.winfo_screenheight()
            xx = (ws / 2) - (200 / 2)
            yy = (hs / 2) - (100 / 2)
            new_window.geometry('%dx%d+%d+%d' % (200, 100, xx, yy))
            ttk.Label(master=new_window, text='Some usernames already exist!').pack(pady=20)
            ttk.Button(master=new_window, text='OK', command=new_window.destroy).pack()

    def view_data(df):
        conn = sqlite3.connect('insta_users.db')
        cursor = conn.cursor()
        sql = '''SELECT USERNAME FROM USERS ORDER BY USER_ID'''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            df.insert("", tk.END, values=row)
        conn.close()

    def reverse_third():
        db_title.place_forget()
        user_tree.place_forget()
        add_user.place_forget()
        edit_user.place_forget()
        del_user.place_forget()
        import_user.place_forget()
        users_button.config(text='Manage Users', command=users_db)

    db_title.place(relx=0.74, rely=0.08, anchor=tk.W)
    user_tree = ttk.Treeview(master=window, columns=['Username'], show='headings')
    user_tree.column("#1", anchor=tk.W)
    user_tree.heading("#1", text='List of Usernames')
    view_data(user_tree)
    user_tree.place(relx=0.69, rely=0.13, anchor=tk.NW, relwidth=0.22, relheight=0.79)
    add_user.place(relx=0.92, rely=0.13, anchor=tk.NW, relwidth=0.05, relheight=0.19)
    edit_user.place(relx=0.92, rely=0.33, anchor=tk.NW, relwidth=0.05, relheight=0.19)
    del_user.place(relx=0.92, rely=0.53, anchor=tk.NW, relwidth=0.05, relheight=0.19)
    import_user.place(relx=0.92, rely=0.73, anchor=tk.NW, relwidth=0.05, relheight=0.19)
    add_user.config(command=user_adding)
    edit_user.config(command=user_editing)
    del_user.config(command=user_deleting)
    import_user.config(command=user_importing)
    users_button.config(text='Close Users', command=reverse_third)




window = tk.Tk()
window.title('Instagram Comment Bot')
window.resizable(width=False, height=False)
width = 1400
height = 600
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
xx = (ws/2) - (width/2)
yy = (hs/2) - (height/2)
window.geometry('%dx%d+%d+%d' % (width, height, xx, yy))
connect_text = ttk.Label(master=window, text='Connect to Your Instagram Account').place(relx=0.03, rely=0.10, anchor=tk.W)
username_text = ttk.Label(master=window, text='Username/Email/Phone:').place(relx=0.03, rely=0.17, anchor=tk.W)
username_entry = ttk.Entry(master=window)
username_entry.place(relx=0.14, rely=0.17, anchor=tk.W, relwidth=0.13)
pw_text = ttk.Label(master=window, text='Password:').place(relx=0.03, rely=0.22, anchor=tk.W)
pw_entry = ttk.Entry(master=window)
pw_entry.place(relx=0.14, rely=0.22, anchor=tk.W, relwidth=0.13)
connect_info = tk.Label(master=window, text="", wraplength=320, justify='left')
connect_info.place(relx=0.03, rely=0.40, anchor=tk.W, relwidth=0.24)
connect_button = ttk.Button(master=window, text='Connect', command=lambda: login_insta(username_entry.get(), pw_entry.get()))
connect_button.place(relx=0.14, rely=0.28, anchor=tk.W, relwidth=0.13)
users_button = ttk.Button(master=window, text='Manage Users', command=users_db)
add_comment_button = ttk.Button(master=window, text='Create New Comments')
disconnect_button = ttk.Button(master=window, text='Disconnect')
users_button.place(relx=0.08, rely=0.85, anchor=tk.W, relwidth=0.14, relheight=0.10)
i = 3
value_a, value_b = [], []
separator = ttk.Separator(master=window, orient='vertical').place(relx=0.30, rely=0.05, relheight=0.9)
url_post_text = ttk.Label(master=window, text='URL of Instagram Post:')
url_post_entry = ttk.Entry(master=window)
nr_comment_text = ttk.Label(master=window, text='Number of Comments:')
nr_comment_entry = ttk.Entry(master=window)
nr_tag_text = ttk.Label(master=window, text='Number of Users to Tag Each Comment:')
custom_tag_button = ttk.Button(master=window, text='Click to Set')
labelframe = ttk.Labelframe(master=window, text='Comment Log')
run_button = ttk.Button(master=window, text='Run')
run_info = ttk.Label(master=window, text='')
event_log = tk.Listbox(master=labelframe)
enabled = tk.NORMAL
end = tk.END
separator_2 = ttk.Separator(master=window, orient='vertical').place(relx=.66, rely=0.05, relheight=0.9)
db_title = ttk.Label(master=window, text='USER DATABASE FOR TAGGING')
add_user = ttk.Button(master=window, text=' Add\nUsers')
edit_user = ttk.Button(master=window, text='    Edit\nSelected')
del_user = ttk.Button(master=window, text='  Delete\nSelected')
import_user = ttk.Button(master=window, text='Import\n From\n Excel')
r_5 = 5
user_input = []

options = Options()
options.add_argument("--headless")
options.add_experimental_option("detach", True)
options.add_argument('--log-level=3')
options.add_argument('--disable-extensions')
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
window.protocol("WM_DELETE_WINDOW", close_all)
window.mainloop()
