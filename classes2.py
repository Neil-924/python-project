import tkinter as tk
import json
import os
from datetime import date
import copy
from datetime import datetime
#______________________________________________________________________________________________

BG         = "#0B0F1A"
BG2        = "#12182A"
BG3        = "#1A2240"
ACCENT     = "#3A7BFF"
ACCENT_H   = "#2F63D6"
CYAN       = "#38BDF8"
CYAN_H     = "#1EA7E1"
TEXT       = "#E6ECFF"
TEXT_DIM   = "#9AA6D1"
TEXT_MUTE  = "#5B628A"
SUCCESS    = "#4ADE80"
SUCCESS_H  = "#36C96B"
ERROR      = "#FF6B7A"
BORDER     = "#2A3355"
CARD_BG    = "#141B33"
CARD_BORDER= "#2F3B70"

DATA_FILE = "budget_system_data.json"
#______________________________________________________________________________________________

#______________FILE HANDLING____________________________________
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent = 2)

def input_fields(parent, text_label, card_bg=CARD_BG, **entry_kwargs):
    frame = tk.Frame(parent, bg=card_bg)
    frame.pack(padx=28, pady=(16, 0), anchor="w")
    tk.Label(frame, text=text_label, font=('Helvetica', 8, 'bold'),
             bg=card_bg, fg=TEXT_MUTE).pack(anchor="w")
    entry = tk.Entry(frame, width=36,
                     bg=BG2, fg=TEXT, insertbackground=ACCENT,
                     relief="flat", bd=0, font=('Helvetica', 11),
                     **entry_kwargs)
    entry.pack(ipady=8, ipadx=6)
    tk.Frame(frame, bg=BORDER, height=1).pack(fill="x", pady=(0, 4))
    return entry

def expense_entry(parent, text_label):
    frame = tk.Frame(parent, bg=BG3)
    frame.pack(padx=28, pady=(0, 16), fill="x")
    tk.Label(frame, text=text_label, font=('Helvetica', 8, 'bold'),
             bg=BG3, fg=TEXT_MUTE).pack(anchor="w")
    entry = tk.Entry(frame,
                     bg=BG, fg=TEXT, insertbackground=ACCENT,
                     relief="flat", bd=0, font=('Helvetica', 11))
    entry.pack(ipady=8, ipadx=12, fill="x")
    return entry
#_____________________________________________________________

DAYS_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
#_____________________________________________________________

#self = who am I
#app = controller
#parent = who i inherit
class Page(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        #refencer
        self.app = app

    def on_show(self):
        pass

    def load(self): 
        pass

#----------inside LetsGoBudget-----------
class LandingPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        
        w = tk.Frame(self, bg=BG)
        w.place(relx=0.5, rely=0.44, anchor="center")

        tk.Label(w, text="Let's Go Budget!", font=('Helvetica', 22, 'bold'),
                 bg=BG, fg=TEXT).pack(pady=(0, 4))
        #might change this
        tk.Label(w, text="Budgeted Money For a Wiser Week.", font=('Helvetica', 11),
                 bg=BG, fg=TEXT_MUTE).pack(pady=(0, 28))
        
        tk.Button(w, text="Register",
                  bg=ACCENT, fg=TEXT, activebackground=ACCENT_H, activeforeground=TEXT,
                  font=('Helvetica', 11, 'bold'), relief="flat", bd=0,
                  cursor="hand2", width=20, pady=8,
                  command=lambda: app.show_page("register")).pack(pady=(0, 8))

        tk.Button(w, text="Login",
                  bg=CARD_BG, fg=TEXT_DIM, activebackground=BG3, activeforeground=TEXT,
                  font=('Helvetica', 11), relief="flat", bd=0,
                  cursor="hand2", width=20, pady=8,
                  command=lambda: app.show_page("login")).pack()

class RegisterPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        w = tk.Frame(self, bg=BG)
        w.place(relx=0.5, rely=0.44, anchor="center")

        tk.Label(w, text="Create Account", font=('Helvetica', 20, 'bold'),
                 bg=BG, fg=TEXT).pack(pady=(0, 16))
        frame = tk.Frame(w, bg=CARD_BG, highlightbackground=CARD_BORDER,
                         highlightthickness=1)
        frame.pack(pady=4, padx=4)

        self.username = input_fields(frame, "USERNAME")
        self.password = input_fields(frame, "PASSWORD", show="*")
        self.password2 = input_fields(frame, "CONFIRM PASSWORD", show="*")

        self.msg = tk.StringVar()
        tk.Label(frame, textvariable=self.msg, fg=ERROR,
                 bg=CARD_BG, font=('Helvetica', 10)).pack(pady=(0, 4))

        tk.Button(w, text="Register",
                  bg=ACCENT, fg=TEXT, activebackground=ACCENT_H, activeforeground=TEXT,
                  font=('Helvetica', 11, 'bold'), relief="flat", bd=0,
                  cursor="hand2", width=20, pady=8,
                  command=lambda: self._register()).pack(pady=(8, 4))

        tk.Button(w, text="Already have an account? Login",
                  bg=BG, fg=TEXT_MUTE, activebackground=BG, activeforeground=CYAN,
                  font=('Helvetica', 10), relief="flat", bd=0,
                  cursor="hand2",
                  command=lambda: app.show_page("login")).pack()

    def _register(self):
        u, p, p2 = self.username.get(), self.password.get(), self.password2.get()
        if not u or not p:
            self.msg.set("Please enter username or password."); return
        if p != p2:
            self.msg.set("Password does not match.")
            self.delete_input()
            return
        if len(p) <= 3:
            self.msg.set("Password too short should be more than 3 characters.")
            self.delete_input()
            return
        if u in self.app.data:
            self.msg.set("Username already exists.") 
            self.delete_input()
            return

        self.app.data[u] = {
                            "password": p,
                            "weekly_budget": 0,
                            "current": {
                                "days_included": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                "expenses": {
                                    "daily": {},
                                    "one_time": {}
                                }
                            }
                        }
        save_data(self.app.data)
        self.app.current_user = u
        self.app.show_page("main")
    
    def delete_input(self):
        self.password.delete(0, tk.END)
        self.password2.delete(0, tk.END)

class LoginPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        w = tk.Frame(self, bg=BG)
        w.place(relx=0.5, rely=0.44, anchor="center")

        tk.Label(w, text="Welcome back", font=('Helvetica', 22, 'bold'),
                 bg=BG, fg=TEXT).pack(pady=(0, 16))

        frame = tk.Frame(w, bg=CARD_BG, highlightbackground=CARD_BORDER,
                         highlightthickness=1)
        frame.pack(pady=4, padx=4)

        self.username = input_fields(frame, "USERNAME")
        self.password = input_fields(frame, "PASSWORD", show="*")

        self.msg = tk.StringVar()
        tk.Label(frame, textvariable=self.msg, fg=ERROR,
                 bg=CARD_BG, font=('Helvetica', 10)).pack(pady=(0, 4))

        tk.Button(w, text="Sign In",
                  bg=ACCENT, fg=TEXT, activebackground=ACCENT_H, activeforeground=TEXT,
                  font=('Helvetica', 11, 'bold'), relief="flat", bd=0,
                  cursor="hand2", width=20, pady=8,
                  command=lambda: self._login()).pack(pady=(8, 4))

        tk.Button(w, text="No account yet? Register",
                  bg=BG, fg=TEXT_MUTE, activebackground=BG, activeforeground=CYAN,
                  font=('Helvetica', 10), relief="flat", bd=0,
                  cursor="hand2",
                  command=lambda: self.app.show_page("register")).pack()
    
    def _login(self):
        u, p = self.username.get(), self.password.get()
        if not u or not p:
            self.msg.set("no entry"); return
        if u not in self.app.data:
            self.msg.set("incorrect username")
            self.password.delete(0, tk.END)
            return
        if p != self.app.data[u]["password"]:
            self.msg.set("incorrect password") 
            self.password.delete(0, tk.END)
            return

        self.app.current_user = u
        self.app.show_page("main")   

class MainPage(Page):
    def __init__(self, parent, app):
        self.PAGES = [
            ("Dashboard", DashBoard),
            ("Days", DaysTab),
            ("Expenses Tab", ExpensesTab),
            ("Summary", SummaryTab),
            ("Saved Plans", SavedPlansTab)
        ]

        super().__init__(parent, app)
        self._side_panel()
        self.show_tab(0)

    #side part/nav in main after logging in
    def _side_panel(self):
        sidebar = tk.Frame(self, width=200, bg=BG2)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="LET'S GO BUDGET", font=('Helvetica', 9, 'bold'),
                bg=BG2, fg=TEXT_MUTE).pack(anchor="w", padx=16, pady=(20, 4))
        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(0, 8))

        self.nav_buttons = []
        nav_frame = tk.Frame(sidebar, bg=BG2)
        nav_frame.pack(fill="x")

        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        self.tabs = []
        #frame for content each page
        for _, PageClass in self.PAGES:
            #self.content will be their parent
            frame = PageClass(self.content, self.app)
            frame.place(relwidth=1, relheight=1)
            self.tabs.append(frame)

        self.budget_overlay = Budget(self.content, self.app)
        self.budget_overlay.place(relwidth=1, relheight=1)

        #for navigation buttons
        for i, (label, _) in enumerate(self.PAGES):
            btn = tk.Button(
                nav_frame, 
                text=f"  {label}", 
                relief="flat", 
                anchor="w",
                cursor="hand2", 
                pady=11, 
                padx=16, 
                bd=0, 
                font=('Helvetica', 11),
                bg=BG2, 
                fg=TEXT_DIM, 
                activebackground=BG3, 
                activeforeground=TEXT,
                command=lambda idx=i: self.show_tab(idx)
            )
            btn.pack(fill="x")
            self.nav_buttons.append(btn)

    def on_show(self):
        if not self.app.current_user:
            return
        budget = self.app.data[self.app.current_user]["weekly_budget"]
        if budget == 0:
            self.budget_overlay.tkraise()
        else:
            self.budget_overlay.lower()

    def show_tab(self, idx):
        self.tabs[idx].tkraise()
        self.tabs[idx].load()
        self.on_show()
        for i, btn in enumerate(self.nav_buttons):
            if i == idx:
                btn.config(bg=BG3, fg=TEXT)
            else:
                btn.config(bg=BG2, fg=TEXT_DIM)

#---------inside MainPage------------------
class DashBoard(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0,
                                yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG)
        self.win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
            lambda e: self.canvas.itemconfig(self.win_id, width=e.width))

    def load(self):
        for w in self.inner.winfo_children():
            w.destroy()

        data = self.app.data[self.app.current_user]

        today = date.today().strftime("%A, %B %d %Y")

        # ── Header ──────────────────────────────────────────────
        header = tk.Frame(self.inner, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 4))
        tk.Label(header, text=f"Hey, {self.app.current_user}!",
                 font=('Helvetica', 18, 'bold'), bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(header, text=today,
                 font=('Helvetica', 10), bg=BG, fg=TEXT_MUTE).pack(anchor="w", pady=(2, 0))
        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(12, 0))

        # ── Weekly Budget ────────────────────────────────────────
        budget_card = tk.Frame(self.inner, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
        budget_card.pack(fill="x", padx=24, pady=(16, 0))
        tk.Label(budget_card, text="WEEKLY BUDGET",
                 font=('Helvetica', 8, 'bold'), bg=CARD_BG, fg=TEXT_MUTE).pack(anchor="w", padx=16, pady=(12, 0))
        tk.Label(budget_card, text=f"₱{data['weekly_budget']:,.2f}",
                 font=('Helvetica', 22, 'bold'), bg=CARD_BG, fg=SUCCESS).pack(anchor="w", padx=16, pady=(2, 0))
        tk.Button(budget_card, text="Reset Weekly Budget",
                  bg=BG, fg=ERROR, activebackground=BG2, activeforeground=ERROR,
                  font=('Helvetica', 9, 'bold'), relief="flat", bd=0,
                  cursor="hand2", pady=6,
                  command=self._reset_budget).pack(anchor="w", padx=16, pady=(8, 12))

        # ── Days Included ────────────────────────────────────────
        tk.Label(self.inner, text="DAYS INCLUDED",
                 font=('Helvetica', 8, 'bold'), bg=BG, fg=TEXT_MUTE).pack(anchor="w", padx=24, pady=(20, 6))
        days_frame = tk.Frame(self.inner, bg=BG)
        days_frame.pack(fill="x", padx=24)

        days_included = data["current"]["days_included"]
        for day in DAYS_ORDER:
            is_on = day in days_included
            pill = tk.Label(days_frame,
                            text=day[:3],
                            font=('Helvetica', 9, 'bold'),
                            bg=ACCENT if is_on else BG3,
                            fg=TEXT if is_on else TEXT_MUTE,
                            relief="flat", padx=10, pady=5)
            pill.pack(side="left", padx=(0, 6))

        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(16, 0))

        # ── Daily Expenses ───────────────────────────────────────
        tk.Label(self.inner, text="DAILY EXPENSES",
                 font=('Helvetica', 8, 'bold'), bg=BG, fg=TEXT_MUTE).pack(anchor="w", padx=24, pady=(16, 6))

        daily = data["current"]["expenses"]["daily"]
        if daily:
            for name, e in daily.items():
                row = tk.Frame(self.inner, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
                row.pack(fill="x", padx=24, pady=(0, 6))

                tk.Label(row, text=name,
                         font=('Helvetica', 10, 'bold'), bg=CARD_BG, fg=TEXT).pack(anchor="w", padx=14, pady=(10, 0))

                info = tk.Frame(row, bg=CARD_BG)
                info.pack(fill="x", padx=14, pady=(4, 10))

                tk.Label(info, text=f"{e['Percentage']}% of budget",
                         font=('Helvetica', 9), bg=CARD_BG, fg=TEXT_MUTE).pack(side="left")
                tk.Label(info, text=f"₱{e['Daily Budget']:.2f}/day",
                         font=('Helvetica', 9), bg=CARD_BG, fg=ACCENT).pack(side="left", padx=(12, 0))
                tk.Label(info, text=f"₱{e['Total Budget']:.2f}/week",
                         font=('Helvetica', 9), bg=CARD_BG, fg=CYAN).pack(side="left", padx=(12, 0))
        else:
            tk.Label(self.inner, text="No daily expenses added yet.",
                     font=('Helvetica', 10), bg=BG, fg=TEXT_MUTE).pack(anchor="w", padx=24)

        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(10, 0))

        # ── One-Time Expenses ────────────────────────────────────
        tk.Label(self.inner, text="ONE-TIME EXPENSES",
                 font=('Helvetica', 8, 'bold'), bg=BG, fg=TEXT_MUTE).pack(anchor="w", padx=24, pady=(16, 6))

        one_time = data["current"]["expenses"]["one_time"]
        if one_time:
            for name, e in one_time.items():
                row = tk.Frame(self.inner, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=1)
                row.pack(fill="x", padx=24, pady=(0, 6))

                tk.Label(row, text=name,
                         font=('Helvetica', 10, 'bold'), bg=CARD_BG, fg=TEXT).pack(anchor="w", padx=14, pady=(10, 0))

                info = tk.Frame(row, bg=CARD_BG)
                info.pack(fill="x", padx=14, pady=(4, 10))

                tk.Label(info, text=f"₱{e['Amount']:.2f}",
                         font=('Helvetica', 9), bg=CARD_BG, fg=CYAN).pack(side="left")
                tk.Label(info, text=f"due {e['Day']}",
                         font=('Helvetica', 9), bg=CARD_BG, fg=TEXT_MUTE).pack(side="left", padx=(10, 0))
        else:
            tk.Label(self.inner, text="No one-time expenses added yet.",
                     font=('Helvetica', 10), bg=BG, fg=TEXT_MUTE).pack(anchor="w", padx=24)

        tk.Frame(self.inner, bg=BG, height=20).pack()  # bottom padding

    def _reset_budget(self):
        self.app.data[self.app.current_user]["weekly_budget"] = 0
        save_data(self.app.data)

        main = self.app.pages.get("main")
        if main:
            main.on_show()  # this raises the budget overlay since budget is now 0

class DaysTab(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        w = tk.Frame(self, bg=BG3)
        w.pack(fill="both", expand=True)
        
        days_frame = tk.Frame(w, bg=BG3)
        days_frame.pack(fill="x")

        self.day_vars = {}
        for day in DAYS_ORDER:
            var = tk.BooleanVar()
            self.day_vars[day] = var
            tk.Checkbutton(days_frame, text=day, variable=var, bg=CARD_BG, fg=TEXT,
                            selectcolor=CARD_BG, cursor="hand2", bd=0,
                            font=('Helvetica', 11, 'bold'), relief="flat", anchor="w", height=2,
                            command=lambda d=day, v=var: self._toggle_day(d, v)
                            ).pack(pady=(20, 0), padx=10, fill="x")

        bottom = tk.Frame(w, bg=BG)
        bottom.pack(fill="both", expand=True, pady=(15, 0))
        bottom.pack_propagate(False)

        save_btn = tk.Button(bottom, bg=ACCENT, text="Remove all days", 
                             relief="flat", font=('Helvetica', 12, 'bold'), 
                             bd=0, fg=TEXT, cursor="hand2",
                             command=self._remove_days)
        save_btn.pack(padx=10, pady=8, anchor="center", expand=True)

    def load(self):
        self.data_days = self.app.data[self.app.current_user]["current"]["days_included"]
        for day, var in self.day_vars.items():
            var.set(day in self.data_days)

    def _toggle_day(self, day, var):
        if var.get():
            if day not in self.data_days:
                self.data_days.append(day)
        else:
            if day in self.data_days:
                self.data_days.remove(day)

        self.data_days.sort(key=lambda d: DAYS_ORDER.index(d))

        #---------added------------------
        expenses = self.app.data[self.app.current_user]["current"]["expenses"]
        days = self.data_days
        one_time_total = sum(e["Amount"] for e in expenses["one_time"].values())
        remaining = self.app.data[self.app.current_user]["weekly_budget"] - one_time_total

        for expense_data in expenses["daily"].values():
            p = expense_data["Percentage"]
            new_total = remaining * (p / 100)
            expense_data["Total Budget"] = round(new_total, 2)
            expense_data["Daily Budget"] = round(new_total / len(days), 2) if days else 0

        save_data(self.app.data)

    def _remove_days(self):
        self.data_days.clear()

        # Uncheck all checkboxes
        for var in self.day_vars.values():
            var.set(False)

        # Recalculate budgets with no days
        expenses = self.app.data[self.app.current_user]["current"]["expenses"]
        one_time_total = sum(e["Amount"] for e in expenses["one_time"].values())
        remaining = self.app.data[self.app.current_user]["weekly_budget"] - one_time_total

        for expense_data in expenses["daily"].values():
            p = expense_data["Percentage"]
            new_total = remaining * (p / 100)
            expense_data["Total Budget"] = round(new_total, 2)
            expense_data["Daily Budget"] = 0  # no days, so 0

        save_data(self.app.data)

class ExpensesTab(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.data = self.app.data[self.app.current_user]
        self.percent_total = 0
        self.one_time_total = 0
        self.daily_total = 0
        self.remaining = 0
    
        self.w = tk.Frame(self, bg=BG)
        self.w.pack(fill="both", expand=True)

        self.all_expenses = tk.Frame(self.w, bg=BG2, width=200)
        self.all_expenses.pack(fill="y", side="right")
        self.all_expenses.pack_propagate(False)

        top_bar = tk.Frame(self.w, bg=BG, height=50)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        btn_group = tk.Frame(top_bar, bg=BG)
        btn_group.place(relx=0.5, rely=0.5, anchor="center",
                        relwidth=0.98, relheight=0.85)

        daily_btn = tk.Button(btn_group, text="Daily Expenses",
                              fg=TEXT_DIM, bg=BG3, relief="flat", bd=0,
                              command=lambda: self._daily_frame.tkraise())
        daily_btn.pack(side="left", fill="both", expand=True,
                       padx=4, pady=(4, 0))

        one_time_btn = tk.Button(btn_group, text="One Time Expenses",
                                 fg=TEXT_DIM, bg=BG3, relief="flat", bd=0,
                                 command=lambda: self._one_time_frame.tkraise())
        one_time_btn.pack(side="left", fill="both", expand=True,
                          padx=4, pady=(4, 0))

        self.panel = tk.Frame(self.w, bg=BG2)
        self.panel.pack(fill="both", expand=True)

        self._daily_frame = self._build_daily()
        self._one_time_frame = self._build_one_time()

        self._recalculate()

        # Show daily by default
        self._daily_frame.tkraise()
    
    #builds the frame for adding daily expenses
    def _build_daily(self):
        frame = tk.Frame(self.panel, bg=BG3)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Add daily expense", font=('Helvetica', 16, 'bold'),
                bg=BG3, fg=TEXT).pack(anchor="w", padx=28, pady=(24, 20))

        self.avail_percent_label = tk.Label(frame, text=f"PERCENTAGE OF BUDGET AVAILABLE: {100 - self.percent_total}%",
                                     font=('Helvetica', 10, 'bold'), bg=BG3, fg=TEXT)
        self.avail_percent_label.pack(anchor="w", padx=28, pady=(0, 10))

        self.daily_name = expense_entry(frame, "EXPENSE NAME")
        self.percentage = expense_entry(frame, "PERCENTAGE")

        self.daily_msg = tk.StringVar()
        tk.Label(frame, textvariable=self.daily_msg, fg=ERROR,
                 bg=BG3, font=('Helvetica', 10)).pack(anchor="w", padx=28, pady=(0, 4))

        btn = tk.Button(frame, text="Add expense",
                        bg=ACCENT, fg=TEXT, activebackground=ACCENT_H, activeforeground=TEXT,
                        font=('Helvetica', 11, 'bold'), relief="flat", bd=0,
                        cursor="hand2", pady=8, padx=20,
                        command=self._add_daily)
        btn.pack(anchor="w", padx=28, pady=(16, 0))

        return frame

    #builds the frame for adding one time expenses
    def _build_one_time(self):
        frame = tk.Frame(self.panel, bg=BG3)
        frame.place(relwidth=1, relheight=1)

        tk.Label(frame, text="Add one time expense", font=('Helvetica', 16, 'bold'),
                bg=BG3, fg=TEXT).pack(anchor="w", padx=28, pady=(24, 20))

        self.avail_amount_label = tk.Label(frame, text=f"AVAILABLE AMOUNT: {self.remaining} Php",
                                    font=('Helvetica', 10, 'bold'), bg=BG3, fg=TEXT)
        self.avail_amount_label.pack(anchor="w", padx=28, pady=(0,10))

        self.one_time_name = expense_entry(frame, "EXPENSE NAME")
        self.one_time_amount = expense_entry(frame, "AMOUNT")
        self.specified_day = expense_entry(frame, "DAY TO PAY")

        self.one_msg = tk.StringVar()
        tk.Label(frame, textvariable=self.one_msg, fg=ERROR,
                 bg=BG3, font=('Helvetica', 10)).pack(anchor="w", padx=28, pady=(0, 4))

        btn = tk.Button(frame, text="Add expense",
                        bg=ACCENT, fg=TEXT, activebackground=ACCENT_H, activeforeground=TEXT,
                        font=('Helvetica', 11, 'bold'), relief="flat", bd=0,
                        cursor="hand2", pady=8, padx=20,
                        command=self._add_one_time)
        btn.pack(anchor="w", padx=28, pady=(16, 0))

        return frame
    
    #like the summary of expenses shown at the right side
    def _refresh_sidebar(self):
        #destroys everything inside all_expenses to make a new one
        #all_expenses = summary of expenses
        for widget in self.all_expenses.winfo_children():
            widget.destroy()

        tk.Button(self.all_expenses, text="Remove All",
                bg=ERROR, fg=TEXT, activebackground=ERROR, activeforeground=TEXT,
                font=('Helvetica', 9, 'bold'), relief="flat", bd=0,
                cursor="hand2", pady=6,
                command=self._remove_all).pack(fill="x", padx=8, pady=(12, 8))

        tk.Label(self.all_expenses, text="DAILY", font=('Helvetica', 8, 'bold'),
                bg=BG2, fg=TEXT_MUTE).pack(anchor="w", padx=12, pady=(4, 4))

        #prints all daily with percent
        for name, data in self.data["current"]["expenses"]["daily"].items():
            row = tk.Frame(self.all_expenses, bg=BG3)
            row.pack(fill="x", padx=8, pady=2)
            
            info = tk.Frame(row, bg=BG3)
            info.pack(side="left", fill="both", expand=True)
            tk.Label(info, text=name, bg=BG3, fg=TEXT,
                    font=('Helvetica', 9, 'bold')).pack(anchor="w", padx=8, pady=(4, 0))
            tk.Label(info, text=f"{data['Percentage']}%", bg=BG3, fg=TEXT_MUTE,
                    font=('Helvetica', 8)).pack(anchor="w", padx=8, pady=(0, 4))

            tk.Button(row, text="✕", bg=BG3, fg=ERROR, activebackground=BG3, activeforeground=ERROR,
                    relief="flat", bd=0, cursor="hand2", font=('Helvetica', 10, 'bold'),
                    command=lambda n=name: self._remove_expense("daily", n)).pack(side="right", padx=6)

        tk.Frame(self.all_expenses, bg=BORDER, height=1).pack(fill="x", padx=8, pady=8)

        tk.Label(self.all_expenses, text="ONE TIME", font=('Helvetica', 8, 'bold'),
                bg=BG2, fg=TEXT_MUTE).pack(anchor="w", padx=12, pady=(0, 4))

        #prints all one time with amount and which day
        for name, data in self.data["current"]["expenses"]["one_time"].items():
            row = tk.Frame(self.all_expenses, bg=BG3)
            row.pack(fill="x", padx=8, pady=2)

            info = tk.Frame(row, bg=BG3)
            info.pack(side="left", fill="both", expand=True)
            tk.Label(info, text=name, bg=BG3, fg=TEXT,
                    font=('Helvetica', 9, 'bold')).pack(anchor="w", padx=8, pady=(4, 0))
            tk.Label(info, text=f"₱{data['Amount']:.2f} - {data['Day']}", bg=BG3, fg=TEXT_MUTE,
                    font=('Helvetica', 8)).pack(anchor="w", padx=8, pady=(0, 4))

            tk.Button(row, text="✕", bg=BG3, fg=ERROR, activebackground=BG3, activeforeground=ERROR,
                    relief="flat", bd=0, cursor="hand2", font=('Helvetica', 10, 'bold'),
                  command=lambda n=name: self._remove_expense("one_time", n)).pack(side="right", padx=6)

    #adds daily to data
    def _add_daily(self):
        n = self.daily_name.get()
        
        if not n:
            self.daily_msg.set("Please enter an expense name")
            return
        if n in self.data["current"]["expenses"]["daily"]:
            self.daily_msg.set("Expense already exists")
            return
        
        #repeats until a float is entered
        try:
            p = float(self.percentage.get())
        except ValueError:
            self.daily_msg.set("Percentage must be a number")
            return

        if p <= 0:
            self.daily_msg.set("Percentage must be greater than 0")
            return
        if p > self.percent_remaining:
            self.daily_msg.set(f"Only {100 - self.percent_total}% available")
            return

        self.daily_msg.set("")

        self.data["current"]["expenses"]["daily"][n] = {
            "Percentage": round(p, 2),
            "Total Budget": 0,
            "Daily Budget": 0
        }

        self._remove_input("daily")
        self._recalculate()

    #adds one time to data
    def _add_one_time(self):
        n = self.one_time_name.get()
        if not n:
            self.one_msg.set("Please enter an expense name")
            return
        if n in self.data["current"]["expenses"]["one_time"]:
            self.one_msg.set("Expense already exists")
            return
        
        try:
            amount = float(self.one_time_amount.get())
        except ValueError:
            self.one_msg.set("Amount must be a number")
            return

        if amount <= 0:
            self.one_msg.set("Amount must be greater than 0")
            return
        if amount > self.remaining:
            self.one_msg.set(f"Only {self.budget_remaining:.2f} Php available")
            return

        s_day = self.specified_day.get()
        if not s_day:
            self.one_msg.set("Please enter a day to pay")
            return
        s_day = s_day.capitalize()
        if s_day not in DAYS_ORDER:
            self.one_msg.set("Not a valid day to pay")
            return
        
        self.one_msg.set("")

        #without round data saves data with long version
        percentage_equivalence = (amount / self.data["weekly_budget"]) * 100
        self.data["current"]["expenses"]["one_time"][n] = {
                                                    "Amount": round(amount, 2),
                                                    "Day": s_day,
                                                    "Percentage Equivalence": round(percentage_equivalence, 2)
                                                      }

        self._remove_input("one")
        self._recalculate()

    #for removing 1 of expenses
    def _remove_expense(self, type, name):
        if type == "daily":
            del self.data["current"]["expenses"]["daily"][name]
        elif type == "one_time":
            del self.data["current"]["expenses"]["one_time"][name]
        self._recalculate()
        self._refresh_sidebar()

    #removes everything
    def _remove_all(self):
        self.data["current"]["expenses"]["daily"].clear()
        self.data["current"]["expenses"]["one_time"].clear()
        self._recalculate()
        self._refresh_sidebar()

    #recalculate everything
    def _recalculate(self):
        #WEEKLY_BUDGET -> ONE TIME -> THEN PERCENTAGE OF WHAT REMAINS FOR DAILY
        days = self.data["current"]["days_included"]

        daily_expenses   = self.data["current"]["expenses"]["daily"]
        one_time_expenses = self.data["current"]["expenses"]["one_time"]

        #sum of percent
        self.daily_percent_total = sum(e["Percentage"] for e in daily_expenses.values())
        #sum of amounts
        self.one_time_total      = sum(e["Amount"] for e in one_time_expenses.values())

        self.percent_total    = self.daily_percent_total
        self.remaining        = self.data["weekly_budget"] - self.one_time_total #<-- subtracts one time first to initial weekly budget
        self.percent_remaining = 100 - self.percent_total #<-- percentage of remaining budget that can be allocated
        self.budget_remaining  = self.remaining * (self.percent_remaining / 100) #<-- calculates what remains in the budget

        for expense_data in daily_expenses.values():
            p = expense_data["Percentage"]
            new_total = self.remaining * (p / 100)
            expense_data["Total Budget"] = round(new_total, 2)
            expense_data["Daily Budget"] = round(new_total / len(days), 2) if days else 0

        self.avail_percent_label.config(
            text=f"PERCENTAGE OF BUDGET AVAILABLE: {self.percent_remaining:.2f}%)"
        )
        self.avail_amount_label.config(
            text=f"AVAILABLE AMOUNT: ₱{self.budget_remaining:.2f}"
        )

        save_data(self.app.data)
        self._refresh_sidebar()

    #removes input 
    def _remove_input(self, type):
        if type == "daily":
            self.daily_name.delete(0, tk.END)
            self.percentage.delete(0, tk.END)
            return
        if type == "one":
            self.one_time_name.delete(0, tk.END)
            self.one_time_amount.delete(0, tk.END)
            self.specified_day.delete(0, tk.END)
            return

    def load(self):
        self.data = self.app.data[self.app.current_user]
        self._recalculate()
        self._refresh_sidebar()
    
class SummaryTab(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        w = tk.Frame(self, bg=BG)
        w.pack(fill="both", expand=True)

        #makes whole content area a canvas
        self.canvas = tk.Canvas(w, bg=BG2, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.upper = tk.Frame(self.canvas, bg=BG3)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.upper, anchor="nw")

        self.upper.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, height=e.height))

        #for scroll bar 
        scrollbar = tk.Scrollbar(w, orient="horizontal", command=self.canvas.xview)
        scrollbar.pack(fill="x")
        self.canvas.configure(xscrollcommand=scrollbar.set)

        bottom = tk.Frame(w, bg=BG, height=100)
        bottom.pack(fill="x", side="bottom")
        bottom.pack_propagate(False)

        save_btn = tk.Button(bottom, bg=ACCENT, text="SAVE BUDGET PLAN", 
                             relief="flat", font=('Helvetica', 12, 'bold'), 
                             bd=0, fg=TEXT, cursor="hand2",
                             command=self._save_plan)
        save_btn.pack(padx=10, pady=8, anchor="center", expand=True)

        self.cards = []  # track cards here

    #loads everything
    def load(self):
        for card in self.cards:
            card.destroy()
        self.cards = []

        data = self.app.data[self.app.current_user]
        daily = data["current"]["expenses"]["daily"]
        one_time = data["current"]["expenses"]["one_time"]
        days = data["current"]["days_included"]

        for day in DAYS_ORDER:
            card = self._day_card(day, daily, one_time, days)
            self.cards.append(card)

    #responsible for making the summary day cards
    def _day_card(self, day, daily, one_time, days):
        card = tk.Frame(self.upper, bg=CARD_BG, highlightbackground=CARD_BORDER,
                        highlightthickness=1, width=210)
        card.pack(side="left", fill="y", padx=10, pady=10)
        card.pack_propagate(False)

        tk.Label(card, text=day, font=('Helvetica', 10, 'bold'),
                 bg=BG, fg=TEXT, anchor="center", highlightthickness=2, highlightbackground=CARD_BORDER ).pack(fill="x", pady=12, padx=8, ipadx=5, ipady=8)

        tk.Label(card, text="DAILY", font=('Helvetica', 10, 'bold'),
                 bg=CARD_BG, fg=TEXT_DIM).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=8)

        #day already traverse in def load
        if day in days:
            for name, e in daily.items():
                tk.Label(card, text=name, font=('Helvetica', 9, 'bold'),
                        bg=CARD_BG, fg=TEXT).pack(anchor="w", padx=10, pady=(6, 0))
                tk.Label(card, text=f"₱{e['Daily Budget']:.2f}/day",
                        font=('Helvetica', 8), bg=CARD_BG, fg=ACCENT).pack(anchor="w", padx=10)

        tk.Label(card, text="ONE TIME", font=('Helvetica', 10, 'bold'),
                 bg=CARD_BG, fg=TEXT_DIM).pack(anchor="w", padx=10, pady=(15, 0))
        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=8)

        for name, e in one_time.items():
            if e["Day"] == day:
                tk.Label(card, text=name, font=('Helvetica', 9, 'bold'),
                         bg=CARD_BG, fg=TEXT).pack(anchor="w", padx=10, pady=(6, 0))
                tk.Label(card, text=f"₱{e['Amount']:.2f}",
                         font=('Helvetica', 8), bg=CARD_BG, fg=CYAN).pack(anchor="w", padx=10)

        return card

    #when saving a budget plan
    def _save_plan(self):
        data = self.app.data[self.app.current_user]
        today = str(date.today())  # e.g. "2026-04-18"

        if "saved_plans" not in self.app.data[self.app.current_user]:
            self.app.data[self.app.current_user]["saved_plans"] = {}

        key = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        #%Y=Year -%m=month in number -%d=day %H=Hour :%M=Minutes :%S=Seconds

        self.app.data[self.app.current_user]["saved_plans"][key] = {
            "weekly_budget": data["weekly_budget"],
            #copies the whole expense data without the need of another variable
            "expenses": copy.deepcopy(data["current"]["expenses"])
        }

        save_data(self.app.data)

class SavedPlansTab(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0,
                                yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.canvas.yview)

        self.inner = tk.Frame(self.canvas, bg=BG)
        self.win_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
            lambda e: self.canvas.itemconfig(self.win_id, width=e.width))

    #loads the datas
    def load(self):
        #again destroys everything inside inner to redo it
        for w in self.inner.winfo_children():
            w.destroy()

        user_data = self.app.data[self.app.current_user]
        saved = user_data.get("saved_plans", {}) #<-- gets the savedplans dictionary

        #frames per saved file
        header = tk.Frame(self.inner, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 4))

        tk.Label(header, text="Saved Plans",
                 font=('Helvetica', 18, 'bold'), bg=BG, fg=TEXT).pack(anchor="w")
        tk.Label(header, text=f"{len(saved)} plan{'s' if len(saved) != 1 else ''} saved",
                 font=('Helvetica', 10), bg=BG, fg=TEXT_MUTE).pack(anchor="w", pady=(2, 0))

        tk.Frame(self.inner, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(12, 0))

        if not saved: #<-- meaning empty
            tk.Label(self.inner,
                     text="No saved plans yet. Go to Summary and hit 'Save Budget Plan'.",
                     font=('Helvetica', 10), bg=BG, fg=TEXT_MUTE,
                     wraplength=500, justify="left").pack(anchor="w", padx=24, pady=20)
            return

        #traverse in reverse
        for plan_date in sorted(saved.keys(), reverse=True):
            self._build_plan_card(plan_date, saved[plan_date])

        tk.Frame(self.inner, bg=BG, height=24).pack()

    def _build_plan_card(self, plan_date, plan):
        daily    = plan["expenses"].get("daily", {})
        one_time = plan["expenses"].get("one_time", {})
        budget   = plan.get("weekly_budget", 0)

        wrapper = tk.Frame(self.inner, bg=BG)
        wrapper.pack(fill="x", padx=24, pady=(0, 12))

        header_bar = tk.Frame(wrapper, bg=CARD_BG,
                              highlightbackground=CARD_BORDER, highlightthickness=1)
        header_bar.pack(fill="x")

        #it is automatically opened
        toggle_var = tk.BooleanVar(value=True)

        left = tk.Frame(header_bar, bg=CARD_BG)
        left.pack(side="left", fill="both", expand=True, padx=14, pady=12)

        try:
            if " " in plan_date: #<-- checks if theres space in data          
                nice_date = datetime.strptime(plan_date, "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y  %I:%M %p") #B for month, I for 12 hour
            else:
                nice_date = datetime.strptime(plan_date, "%Y-%m-%d").strftime("%B %d, %Y")
        except Exception:
            #just shows the original if fail
            nice_date = plan_date

        arrow_lbl = tk.Label(left, text="▾", font=('Helvetica', 12),
                             bg=CARD_BG, fg=TEXT_MUTE)
        arrow_lbl.pack(side="left", padx=(0, 8))

        tk.Label(left, text=nice_date,
                 font=('Helvetica', 12, 'bold'), bg=CARD_BG, fg=TEXT).pack(side="left")

        tk.Label(header_bar, text=f"₱{budget:,.2f}",
                 font=('Helvetica', 11, 'bold'), bg=CARD_BG, fg=SUCCESS).pack(side="left", padx=(0, 16))

        tk.Button(header_bar, text="Delete",
                  bg=CARD_BG, fg=ERROR, activebackground=BG2, activeforeground=ERROR,
                  font=('Helvetica', 9, 'bold'), relief="flat", bd=0,
                  cursor="hand2", padx=12, pady=10,
                  command=lambda d=plan_date, w=wrapper: self._delete_plan(d, w)
                  ).pack(side="right", padx=8)

        body = tk.Frame(wrapper, bg=BG2,
                        highlightbackground=CARD_BORDER, highlightthickness=1)
        body.pack(fill="x")

        tk.Label(body, text="DAILY EXPENSES",
                 font=('Helvetica', 8, 'bold'), bg=BG2, fg=TEXT_MUTE
                 ).pack(anchor="w", padx=16, pady=(14, 4))

        if daily:
            for name, e in daily.items():
                row = tk.Frame(body, bg=BG3, highlightbackground=BORDER, highlightthickness=1)
                row.pack(fill="x", padx=16, pady=(0, 4))

                tk.Label(row, text=name,
                         font=('Helvetica', 10, 'bold'), bg=BG3, fg=TEXT
                         ).pack(anchor="w", padx=12, pady=(8, 0))

                info = tk.Frame(row, bg=BG3)
                info.pack(fill="x", padx=12, pady=(2, 8))

                tk.Label(info, text=f"{e['Percentage']}% of budget",
                         font=('Helvetica', 9), bg=BG3, fg=TEXT_MUTE).pack(side="left")
                tk.Label(info, text=f"₱{e['Daily Budget']:.2f}/day",
                         font=('Helvetica', 9), bg=BG3, fg=ACCENT).pack(side="left", padx=(12, 0))
                tk.Label(info, text=f"₱{e['Total Budget']:.2f}/week",
                         font=('Helvetica', 9), bg=BG3, fg=CYAN).pack(side="left", padx=(12, 0))
        else:
            tk.Label(body, text="No daily expenses.",
                     font=('Helvetica', 9), bg=BG2, fg=TEXT_MUTE).pack(anchor="w", padx=16, pady=(0, 6))

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(6, 0))

        tk.Label(body, text="ONE-TIME EXPENSES",
                 font=('Helvetica', 8, 'bold'), bg=BG2, fg=TEXT_MUTE
                 ).pack(anchor="w", padx=16, pady=(12, 4))

        if one_time:
            for name, e in one_time.items():
                row = tk.Frame(body, bg=BG3, highlightbackground=BORDER, highlightthickness=1)
                row.pack(fill="x", padx=16, pady=(0, 4))

                tk.Label(row, text=name,
                         font=('Helvetica', 10, 'bold'), bg=BG3, fg=TEXT
                         ).pack(anchor="w", padx=12, pady=(8, 0))

                info = tk.Frame(row, bg=BG3)
                info.pack(fill="x", padx=12, pady=(2, 8))

                tk.Label(info, text=f"₱{e['Amount']:.2f}",
                         font=('Helvetica', 9), bg=BG3, fg=CYAN).pack(side="left")
                tk.Label(info, text=f"due {e['Day']}",
                         font=('Helvetica', 9), bg=BG3, fg=TEXT_MUTE).pack(side="left", padx=(10, 0))
        else:
            tk.Label(body, text="No one-time expenses.",
                     font=('Helvetica', 9), bg=BG2, fg=TEXT_MUTE).pack(anchor="w", padx=16, pady=(0, 6))

        tk.Frame(body, bg=BG2, height=10).pack()

        def toggle(event=None):
            if toggle_var.get():
                body.pack_forget()
                arrow_lbl.config(text="▸")
            else:
                body.pack(fill="x")
                arrow_lbl.config(text="▾")
            toggle_var.set(not toggle_var.get())

        header_bar.bind("<Button-1>", toggle)
        left.bind("<Button-1>", toggle)
        arrow_lbl.bind("<Button-1>", toggle)

    def _delete_plan(self, plan_date, wrapper):
        user_data = self.app.data[self.app.current_user]
        if "saved_plans" in user_data and plan_date in user_data["saved_plans"]:
            del user_data["saved_plans"][plan_date]
            save_data(self.app.data)
        wrapper.destroy()
        self.load()
#ok na budget
class Budget(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)

        w = tk.Frame(self, bg=BG)
        w.place(rely=0.5, relx=0.5, anchor="center")

        tk.Label(w, text="Please enter your Weekly Budget", font=('Helvetica', 18, 'bold'),
                 bg=BG, fg=TEXT_DIM).pack(pady=10)

        self.budget_entry = tk.Entry(w, bg=CARD_BG, fg=TEXT, width=30, font=('Helvetica', 16, 'bold'), justify="center", relief="flat")
        self.budget_entry.pack(pady=10)

        self.msg = tk.StringVar()
        error = tk.Label(w, textvariable=self.msg, bg=BG, fg=ERROR)
        error.pack(pady=10)

        btn = tk.Button(w, text="ENTER", bg=ACCENT, fg=TEXT, 
                        activebackground=ACCENT_H, activeforeground=TEXT,
                        font=('Helvetica', 11, 'bold'), relief="flat", bd=0,
                        cursor="hand2", width=15, pady=8,
                        command=self._fill_budget)
        btn.pack(pady=10)

    def _fill_budget(self):
        b = self.budget_entry.get()
        if not b:
            self.msg.set("Please enter your weekly budget")
            return
        if not b.isdigit() or float(b) <= 0:
            self.msg.set("Please number or proper budget amount")
            return
        
        self.msg.set("")
        self.budget_entry.delete(0, tk.END)

        self.app.data[self.app.current_user]["weekly_budget"] = round(float(b), 2)
        save_data(self.app.data)
        self.lower()

        main = self.app.pages.get("main")
        if main:
            expenses_tab = main.tabs[2]  
            expenses_tab.data = self.app.data[self.app.current_user]
            expenses_tab._recalculate()
            main.tabs[0].load()

#------------main class------------
class LetsGoBudget(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Let's Go Budget!")
        self.geometry("900x580")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.data = load_data()
        self.current_user = None

        c = tk.Frame(self, bg=BG)
        c.pack(fill="both", expand=True)

        self.pages = {
            "landing": LandingPage(c, self),
            "register": RegisterPage(c, self),
            "login": LoginPage(c, self)
        }

        for p in self.pages.values():
            p.place(relwidth=1, relheight=1)

        self.show_page("landing")

    def show_page(self, name):
        if name == "main" and "main" not in self.pages:
            self.pages["main"] = MainPage(self.pages["landing"].master, self)
            self.pages["main"].place(relwidth=1, relheight=1)

        current = self.pages[name]
        current.tkraise()
        current.on_show()

if __name__ == "__main__":
    LetsGoBudget().mainloop()
    #test test test testing git