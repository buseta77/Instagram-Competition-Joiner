from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import ttk
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import sqlite3
import pandas as pd
from tkinter import filedialog as fd
import random


# FUNCTION FOR CLOSING THE APP
def close_all():

    def execute_close():
        browser.quit()
        window.quit()
        window.destroy()

    def dont_close():
        pop_up.destroy()
    try:
        x = running_thread[0]
        pop_up = tk.Toplevel()
        pop_up.title('Warning')
        ws = pop_up.winfo_screenwidth()
        hs = pop_up.winfo_screenheight()
        xx = (ws / 2) - (400 / 2)
        yy = (hs / 2) - (100 / 2)
        pop_up.geometry('%dx%d+%d+%d' % (300, 100, xx, yy))
        question = ttk.Label(master=pop_up, text='Comment process is still running. Are you sure?')
        question.place(relx=0.50, anchor=tk.CENTER, rely=0.20)
        yes = tk.Button(master=pop_up, text='Yes', command=execute_close)
        yes.place(relx=0.35, anchor=tk.CENTER, rely=0.60, relwidth=0.30)
        no = tk.Button(master=pop_up, text='No', command=dont_close)
        no.place(relx=0.65, anchor=tk.CENTER, rely=0.60, relwidth=0.30)
    except IndexError:
        browser.quit()
        window.quit()
        window.destroy()


# THREADING FUNCTION FOR DISCONNECTING FROM INSTAGRAM - INITIATED BY disconnect()
def launch_disconnect():
    browser.get('https://www.instagram.com/')
    connect_info.config(text="Disconnecting...")
    time.sleep(1)
    try:
        ui.WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
    except:
        pass
    browser.find_element(By.XPATH, "//div[@class='J5g42']/div[6]").click()
    time.sleep(2)
    browser.find_element(By.XPATH, "//div[@class='-qQT3']/following-sibling::div").click()
    connect_info.config(text="You're now disconnected.")
    connect_button.config(state=enabled)
    add_comment_button.place_forget()
    disconnect_button.place_forget()
    url_post_text.place_forget()
    url_post_entry.place_forget()
    nr_comment_text.place_forget()
    nr_comment_entry.place_forget()
    nr_tag_text.place_forget()
    custom_tag_button.place_forget()
    time_interval_text.place_forget()
    min_time.place_forget()
    max_time.place_forget()
    labelframe.place_forget()
    run_button.place_forget()
    run_info.place_forget()
    event_log.place_forget()
    stop_button.place_forget()
    pause_button.place_forget()


# THREADING FUNCTION FOR COMMENTING IN INSTAGRAM - INITIATED BY comment_insta()
def launch_comment(post_url, value_1, value_2, event, time_min, time_max):
    global enabled
    global end
    event_log.delete(0, end)
    event_log.insert(0, 'Process started...')
    try:
        browser.get(post_url)
    except selenium.common.exceptions.InvalidArgumentException:
        event_log.insert(1, 'Error: Make sure to send proper URL. Process stopped.')
        custom_tag_button.config(state=enabled)
        run_button.config(state=enabled)
        users_button.config(state=enabled)
        pause_button.place_forget()
        resume_button.place_forget()
        stop_button.place_forget()
        disconnect_button.config(state=enabled)
        add_comment_button.config(state=enabled)
        return
    try:
        ui.WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.bIiDR"))).click()
    except:
        pass
    time.sleep(2)
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
            add_comment_button.config(state=enabled)
            disconnect_button.config(state=enabled)
            pause_button.place_forget()
            resume_button.place_forget()
            stop_button.place_forget()
            return
    p = 1
    all_user_list = []
    conn = sqlite3.connect('insta_users.db')
    cursor = conn.cursor()
    sql_2 = '''SELECT USERNAME FROM USERS'''
    cursor.execute(sql_2)
    all_users = cursor.fetchall()
    for item in all_users:
        all_user_list.append(item[0])
    conn.close()
    needed_number = 0
    for a in range(len(value_1)):
        necessary = value_1[a] * value_2[a]
        needed_number += necessary
    if needed_number > len(all_user_list):
        event_log.insert(end, 'Error: Not enough username in database. Process stopped.')
        custom_tag_button.config(state=enabled)
        run_button.config(state=enabled)
        users_button.config(state=enabled)
        add_comment_button.config(state=enabled)
        disconnect_button.config(state=enabled)
        pause_button.place_forget()
        resume_button.place_forget()
        stop_button.place_forget()
        running_thread.clear()
        return
    for a in range(len(value_1)):
        event_log.insert(end, f"Info: Next {value_1[a]} comments will tag {value_2[a]} users each.")
        time.sleep(3)
        for s in range(value_1[a]):
            tag_list = ['']
            show_tag_list = []
            current_tag = random.sample(all_user_list, value_2[a])
            for user in current_tag:
                tag_list.append(user)
                show_tag_list.append(user)
                all_user_list.remove(user)
            comment_text = ' @'.join(tag_list).strip()
            tagged = ', '.join(show_tag_list).strip()
            try:
                browser.find_element(By.XPATH, "//textarea[@data-testid='post-comment-text-area']").click()
            except selenium.common.exceptions.NoSuchElementException:
                browser.get(post_url)
                time.sleep(4)
                browser.find_element(By.XPATH, "//textarea[@data-testid='post-comment-text-area']").click()
            time.sleep(1)
            browser.find_element(By.XPATH, "//textarea[@data-testid='post-comment-text-area']").send_keys(comment_text)
            time.sleep(1)
            browser.find_element(By.XPATH, "//button[@data-testid='post-comment-input-button']").click()
            time.sleep(3)
            rand = random.randint(time_min, time_max)
            wait = int(rand / 10)
            global paused
            try:
                browser.find_element(By.XPATH, "//div[@class='JBIyP']")
                paused = True
                pause_button.config(state=disabled)
                resume_button.config(state=enabled)
                event_log.insert(end, "Comment limit error is received. We paused the process.")
                time.sleep(10)
                browser.refresh()
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(3)
                try:
                    browser.find_element(By.XPATH, "//div[@class='JBIyP']")
                    paused = True
                    pause_button.config(state=disabled)
                    resume_button.config(state=enabled)
                    event_log.insert(end, "Comment limit error is received. We paused the process.")
                    time.sleep(10)
                    browser.refresh()
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        browser.find_element(By.CSS_SELECTOR, ".aOOlW.HoLwm")
                        paused = True
                        pause_button.config(state=disabled)
                        resume_button.config(state=enabled)
                        event_log.insert(end, "Comment limit error is received. We paused the process.")
                        time.sleep(10)
                        browser.refresh()
                    except selenium.common.exceptions.NoSuchElementException:
                        event_log.insert(end, f"Comment#{p} is made. Tagged users: '{tagged}'.")
                        if sum(value_1) == p:
                            break
                        p += 1
                        event_log.insert(end, f"Waiting {rand+10} seconds for the next comment.")
            time.sleep(10)
            for t in range(10):
                time.sleep(wait)
                if stop_event.is_set():
                    event_log.insert(end, f"Process stopped. Total comments done: {p-1}")
                    stop_button.place_forget()
                    pause_button.place_forget()
                    custom_tag_button.config(state=enabled)
                    run_button.config(state=enabled)
                    users_button.config(state=enabled)
                    add_comment_button.config(state=enabled)
                    disconnect_button.config(state=enabled)
                    running_thread.clear()
                    return
                if paused is True:
                    with event:
                        event.wait()
    event_log.insert(end, "All comments are made. Process has finished.")
    custom_tag_button.config(state=enabled)
    run_button.config(state=enabled)
    users_button.config(state=enabled)
    add_comment_button.config(state=enabled)
    disconnect_button.config(state=enabled)
    pause_button.place_forget()
    resume_button.place_forget()
    stop_button.place_forget()
    running_thread.clear()
    return


# FUNCTION FOR COMMENTING IN INSTAGRAM - INITIATES launch_comment()
def comment_insta(post_url, value_1, value_2):

    def resume_process(event):
        global paused
        paused = False
        stop_button.config(state=tk.NORMAL)
        pause_button.config(state=tk.NORMAL)
        resume_button.config(state=tk.DISABLED)
        event_log.insert(end, "Process continuing...")
        with event:
            pause_event.notify()

    def pause_process():
        global paused
        paused = True
        event_log.insert(end, "Process paused.")
        stop_button.config(state=tk.DISABLED)
        pause_button.config(state=tk.DISABLED)
        resume_button.config(state=tk.NORMAL)

    def stop_process():
        stop_event.set()
        stop_button.config(text='Stopping...')
        stop_button.config(state=tk.DISABLED)
        pause_button.config(state=tk.DISABLED)
        resume_button.config(state=tk.DISABLED)

    if post_url == '':
        run_info.config(text='Enter Post URL!')
    else:
        if value_1 == [] or sum(value_1) == 0:
            run_info.config(text='Set Tags for Comments!')
        else:
            try:
                time_min = int(min_time.get()) - 10
                time_max = int(max_time.get()) - 10
            except ValueError:
                run_info.config(text='Time must be integer!')
                return
            if time_min < 0:
                run_info.config(text='Minimum waiting time is 10 seconds!')
            else:
                custom_tag_button.config(state=tk.DISABLED)
                run_button.config(state=tk.DISABLED)
                add_comment_button.config(state=tk.DISABLED)
                disconnect_button.config(state=tk.DISABLED)
                uu = threading.Thread(target=lambda: launch_comment(post_url, value_1, value_2, pause_event, time_min, time_max))
                running_thread.append(uu)
                stop_button.config(command=stop_process)
                stop_button.place(relx=0.33, rely=0.90, anchor=tk.W, relwidth=0.05)
                pause_button.config(command=pause_process)
                pause_button.place(relx=0.38, rely=0.90, anchor=tk.W, relwidth=0.05)
                resume_button.config(command=lambda: resume_process(pause_event), state=disabled)
                resume_button.place(relx=0.43, rely=0.90, anchor=tk.W, relwidth=0.05)
                uu.start()


# THREADING FUNCTION FOR CONNECTING INSTAGRAM - INITIATED BY login_insta()
def launch_login(a, b):
    connect_info.config(text='Connecting...')
    login_url = 'https://www.instagram.com/accounts/login/'
    browser.get(login_url)
    time.sleep(3)
    try:
        ui.WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.bIiDR"))).click()
    except:
        pass
    try:
        browser.find_element(By.NAME, 'username').send_keys(a)
        try:
            ui.WebDriverWait(browser, 4).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.bIiDR"))).click()
        except:
            pass
        browser.find_element(By.NAME, 'password').send_keys(b, Keys.ENTER)
        time.sleep(2)
    except selenium.common.exceptions.NoSuchElementException:
        time.sleep(5)
        browser.find_element(By.NAME, 'username').send_keys(a, Keys.TAB, b, Keys.ENTER)
        time.sleep(5)
    try:
        browser.find_element(By.XPATH, "//p[@data-testid='login-error-message']")
        connect_info.config(text='Either your username or password is wrong!')
    except selenium.common.exceptions.NoSuchElementException:
        connect_info.config(text="You're connected! Now, you can comment on the posts. To disconnect from your Instagram account, click 'Disconnect' button.")
        add_comment_button.place(relx=0.08, rely=0.60, anchor=tk.W, relwidth=0.14, relheight=0.16)
        disconnect_button.place(relx=0.08, rely=0.74, anchor=tk.W, relwidth=0.14, relheight=0.10)
        connect_button.config(state=tk.DISABLED)
    return


# FUNCTION FOR CONNECTING TO INSTAGRAM - INITIATES launch_login()
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
            # spin_a and spin_b will store the values for value_a and value_b respectively.
            spin_a, spin_b, spin_text_a, spin_text_b = [], [], [], []
            if max_comment == '' or max_comment == '0':
                run_info.config(text='Enter number of comments first!')
            else:
                pop_up = tk.Toplevel()
                pop_up.geometry("+700+300")
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
        time_interval_text.place(relx=0.33, rely=0.25, anchor=tk.W)
        url_post_entry.place(relx=0.43, rely=0.10, anchor=tk.W, relwidth=0.20)
        nr_comment_entry.place(relx=0.43, rely=0.15, anchor=tk.W, relwidth=0.20)
        global i
        i = 3
        # value_a will store the comment partition, i.e, comment number is 10 and value_a = [5, 3, 2]
        # value_b will store the tag counts, i.e., value_b = [3, 2, 1] means 5 comments will tag 3 people, 3 comments will tag 2 people, etc.
        global value_a, value_b
        value_a, value_b = [], []
        custom_tag_button.place(relx=0.53, rely=0.20, anchor=tk.W, relwidth=0.10)
        custom_tag_button.config(command=custom_tag)
        min_time.place(relx=0.56, rely=0.25, anchor=tk.W, relwidth=0.03)
        max_time.place(relx=0.60, rely=0.25, anchor=tk.W, relwidth=0.03)
        min_time.delete(0, tk.END)
        min_time.insert(0, '35')
        max_time.delete(0, tk.END)
        max_time.insert(0, '70')
        labelframe.place(relx=0.33, rely=0.60, anchor=tk.W, relwidth=0.30, relheight=0.50)
        run_button.config(command=lambda: comment_insta(url_post_entry.get(), value_a, value_b))
        run_button.place(relx=0.53, rely=0.90, anchor=tk.W, relwidth=0.10)
        run_info.place(relx=0.40, rely=0.32, anchor=tk.W)
        run_info.config(text="We recommend minimum waiting time to be at least a minute.")
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


# FUNCTION FOR USER DATABASE MANAGEMENT
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
        pop_up.geometry("+700+300")
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
        except FileNotFoundError:
            pass
        except ValueError:
            pass

    def user_del_all():
        def execute_del_all():
            conn = sqlite3.connect('insta_users.db')
            cursor = conn.cursor()
            sql = f"DELETE FROM USERS"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            user_tree.place_forget()
            users_db()
            pop_up.destroy()

        def dont_execute_all():
            pop_up.destroy()

        pop_up = tk.Toplevel()
        pop_up.title('Warning')
        ws = pop_up.winfo_screenwidth()
        hs = pop_up.winfo_screenheight()
        xx = (ws / 2) - (200 / 2)
        yy = (hs / 2) - (100 / 2)
        pop_up.geometry('%dx%d+%d+%d' % (200, 100, xx, yy))
        question = ttk.Label(master=pop_up, text='Are you sure?')
        question.place(relx=0.50, anchor=tk.CENTER, rely=0.20)
        yes = tk.Button(master=pop_up, text='Yes', command=execute_del_all)
        yes.place(relx=0.35, anchor=tk.CENTER, rely=0.60, relwidth=0.30)
        no = tk.Button(master=pop_up, text='No', command=dont_execute_all)
        no.place(relx=0.65, anchor=tk.CENTER, rely=0.60, relwidth=0.30)

    def view_data(df):
        conn = sqlite3.connect('insta_users.db')
        cursor = conn.cursor()
        sql = '''SELECT USERNAME FROM USERS ORDER BY USER_ID'''
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            df.insert("", tk.END, values=row)
        sql_2 = '''SELECT COUNT(*) FROM USERS'''
        cursor.execute(sql_2)
        global user_count
        user_count = cursor.fetchone()[0]
        conn.close()

    def reverse_button():
        db_title.place_forget()
        user_tree.place_forget()
        add_user.place_forget()
        edit_user.place_forget()
        del_user.place_forget()
        import_user.place_forget()
        del_all.place_forget()
        scroll_bar.place_forget()
        users_button.config(text='Manage Users', command=users_db)

    db_title.place(relx=0.74, rely=0.09, anchor=tk.W)
    user_tree = ttk.Treeview(master=window, columns=['Username'], show='headings')
    user_tree.column("#1", anchor=tk.W)
    view_data(user_tree)
    global user_count
    user_tree.heading("#1", text=f'List of Usernames ({user_count})')
    scroll_bar = ttk.Scrollbar(master=window, orient='vertical', command=user_tree.yview)
    scroll_bar.place(relx=0.8974, rely=0.132, anchor=tk.NW, relheight=0.796)
    user_tree.config(yscrollcommand=scroll_bar.set)
    user_tree.place(relx=0.69, rely=0.13, anchor=tk.NW, relwidth=0.22, relheight=0.80)
    add_user.place(relx=0.92, rely=0.13, anchor=tk.NW, relwidth=0.05, relheight=0.16)
    edit_user.place(relx=0.92, rely=0.29, anchor=tk.NW, relwidth=0.05, relheight=0.16)
    del_user.place(relx=0.92, rely=0.45, anchor=tk.NW, relwidth=0.05, relheight=0.16)
    del_all.place(relx=0.92, rely=0.61, anchor=tk.NW, relwidth=0.05, relheight=0.16)
    import_user.place(relx=0.92, rely=0.77, anchor=tk.NW, relwidth=0.05, relheight=0.16)
    add_user.config(command=user_adding)
    edit_user.config(command=user_editing)
    del_user.config(command=user_deleting)
    del_all.config(command=user_del_all)
    import_user.config(command=user_importing)
    users_button.config(text='Close Users', command=reverse_button)


# CORE VARIABLES AND WIDGETS FOR THE APP
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
pw_entry = ttk.Entry(master=window, show="*")
pw_entry.place(relx=0.14, rely=0.22, anchor=tk.W, relwidth=0.13)
connect_info = tk.Label(master=window, text="", wraplength=320, justify='left')
connect_info.place(relx=0.03, rely=0.40, anchor=tk.W, relwidth=0.24)
connect_button = ttk.Button(master=window, text='Connect', command=lambda: login_insta(username_entry.get(), pw_entry.get()))
connect_button.place(relx=0.14, rely=0.28, anchor=tk.W, relwidth=0.13)
users_button = ttk.Button(master=window, text='Manage Users', command=users_db)
add_comment_button = ttk.Button(master=window, text='Create New Comments')
disconnect_button = ttk.Button(master=window, text='Disconnect')
users_button.place(relx=0.08, rely=0.85, anchor=tk.W, relwidth=0.14, relheight=0.10)
value_a, value_b, i = [], [], 3
# --------------- #
separator = ttk.Separator(master=window, orient='vertical').place(relx=0.30, rely=0.05, relheight=0.9)
# --------------- #
url_post_text = ttk.Label(master=window, text='URL of Instagram Post:')
url_post_entry = ttk.Entry(master=window)
nr_comment_text = ttk.Label(master=window, text='Number of Comments:')
nr_comment_entry = ttk.Entry(master=window)
nr_tag_text = ttk.Label(master=window, text='Number of Users to Tag Each Comment:')
custom_tag_button = ttk.Button(master=window, text='Click to Set')
time_interval_text = ttk.Label(master=window, text='Seconds to Wait Between Each Comment (Min-Max):')
min_time = ttk.Entry(master=window)
max_time = ttk.Entry(master=window)
labelframe = ttk.Labelframe(master=window, text='Comment Log')
run_button = ttk.Button(master=window, text='Run')
stop_button = ttk.Button(master=window, text='Stop')
pause_button = ttk.Button(master=window, text='Pause')
resume_button = ttk.Button(master=window, text='Resume')
run_info = ttk.Label(master=window, text='')
event_log = tk.Listbox(master=labelframe)
enabled = tk.NORMAL
end = tk.END
disabled = tk.DISABLED
stop_event = threading.Event()
pause_event = threading.Condition()
paused = False
# --------------- #
separator_2 = ttk.Separator(master=window, orient='vertical').place(relx=.66, rely=0.05, relheight=0.9)
# --------------- #
db_title = ttk.Label(master=window, text='USER DATABASE FOR TAGGING')
add_user = ttk.Button(master=window, text=' Add\nUsers')
edit_user = ttk.Button(master=window, text='    Edit\nSelected')
del_user = ttk.Button(master=window, text='  Delete\nSelected')
del_all = ttk.Button(master=window, text='Delete\n   All')
import_user = ttk.Button(master=window, text='Import\n From\n Excel')
r_5 = 5
user_input = []
running_thread = []
user_count = 0
# --------------- #
options = Options()
options.add_argument("--headless")
options.add_experimental_option("detach", True)
options.add_argument('--log-level=3')
options.add_argument('--disable-extensions')
options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
window.protocol("WM_DELETE_WINDOW", close_all)
# --------------- #
window.mainloop()
