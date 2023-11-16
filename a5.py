import tkinter as tk
from tkinter import ttk, filedialog
import ds_messenger
import ds_storage
from Profile import Profile
from pathlib import Path

"""
Contains all functions needed to draw and maintain the GUI using tkinter.
Main module for execution.
"""


class Body(tk.Frame):
    """Contains functions that maintain the body of the application."""
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.tag_config('user', foreground='blue', justify='right', font='Perptua 15')
        if message == None:
            message = ""
        self.entry_editor.insert(tk.END, message + '\n', 'user')
        self.entry_editor.see("end")

    def insert_contact_message(self, message:str):
        self.entry_editor.tag_config('contact', foreground='black', justify='left', font='Perpetua 15')
        if message == None:
            message = ""
        self.entry_editor.insert(tk.END, message + '\n', 'contact')
        self.entry_editor.see("end")

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def set_message_board(self, text:str):
        self.entry_editor.delete(1.0, tk.END)
        self.entry_editor.insert(1.0, text)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250, bg="#a8bedb")
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        ttk.Style().configure("Treeview", background="#84a3cc", foreground="black", fieldbackground="#ccd9ea")
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.heading('#0', text='Contacts')
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=10, pady=10)

        label_frame = tk.Frame(master=self, bg="#84a3cc")
        label_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)
        self.contact_label = tk.Label(master=label_frame, text="Contact", font='Arial 18 bold', bg="#ccd9ea")
        self.contact_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

        self.user_label = tk.Label(master=label_frame, text="user", font='Arial 18 bold', fg="blue", bg="#ccd9ea")
        self.user_label.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5)

        entry_frame = tk.Frame(master=self, bg="#84a3cc")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="#a8bedb")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, width=10, bg="#a8bedb")
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="#a8bedb")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5, bg="#ccd9ea")
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=5, pady=5)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, bg="#ccd9ea")

        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=5, pady=5)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    """Contains functions for the footer of the Tk window."""
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def add_user_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def set_status(self, status):
        self.footer_label["text"] = status

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=10, command=self.send_click, highlightbackground="#84a3cc")
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)




class NewContactDialog(tk.simpledialog.Dialog):
    """Dialog box for creating a new user profile."""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address (DSP 168.235.86.101)")
        self.server_label.pack()
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class OpenDialog(tk.simpledialog.Dialog):
    """Dialog box for opening a user profile."""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.pack()


    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = "168.235.86.101" # default server
        self.recipient = None

        self.direct_messenger = ds_messenger.DirectMessenger()
        self._draw()

    def send_message(self):
        """
        Send the message that the user types into the text
        widget.
        """
        ds = ds_messenger.DirectMessenger(self.server, self.username, self.password)
        msg = self.body.get_text_entry()
        ds.send(msg, self.recipient)
        store = ds_storage.Storage()
        store.save_sent(self.username, self.password, ds.sent)
        self.body.set_text_entry("")
        self.body.insert_user_message(msg)

    def add_contact(self):
        """
        Prompts user to enter the name of a new contact.
        Adds the contact to their contact list.
        """
        new_contact = tk.simpledialog.askstring("Add Contact", "Enter the name of your new contact:")
        self.body.insert_contact(new_contact)
        dsu_name = self.username + ".dsu"
        directory = "."
        p = Path(directory) / dsu_name
        if not p.exists():
            self.footer.set_status("Error: Path does not exist.")
        else:
            p_str = str(p)
            profile = Profile(self.server, self.username, self.password)
            profile.load_profile(p_str)
            profile.friend.append(new_contact)
            profile.save_profile(p_str)

    def recipient_selected(self, recipient):
        """Update message box when recipient is clicked on treeview."""
        self.recipient = recipient
        self.body.contact_label["text"] = recipient
        ds = ds_messenger.DirectMessenger(self.server, self.username, self.password)
        dm_lst = ds.retrieve_all()
        store = ds_storage.Storage()

        store.save_received(dm_lst, self.username, self.password, self.server)
        recv_dict = store.get_contact_messages(self.recipient, self.username, self.password)

        sent_dict = store.get_user_messages(self.recipient, self.username, self.password)
        convo_dict = dict(recv_dict)
        convo_dict.update(sent_dict)
        srt = dict(sorted(convo_dict.items()))

        post = ""
        self.body.set_message_board("")
        for msg in srt.values():
            post = msg[1]
            if msg[0] == self.recipient:
                self.body.insert_contact_message(post)
            elif msg[0] == self.username:
                self.body.insert_user_message(post)

    def new_update(self, new_friends):
        """Update the messages in realtime."""
        ds = ds_messenger.DirectMessenger(self.server, self.username, self.password)
        store = ds_storage.Storage()

        recv_dict = store.get_contact_messages(self.recipient, self.username, self.password)

        sent_dict = store.get_user_messages(self.recipient, self.username, self.password)
        convo_dict = dict(recv_dict)
        convo_dict.update(sent_dict)
        srt = dict(sorted(convo_dict.items()))

        post = ""
        self.body.set_message_board("")
        for msg in srt.values():
            post = msg[1]
            if msg[0] == self.recipient:
                self.body.insert_contact_message(post)
            elif msg[0] == self.username:
                self.body.insert_user_message(post)

        open_user = self.username
        user_pwd = self.password

        dsu_name = open_user + ".dsu"
        directory = "."
        p = Path(directory) / dsu_name
        if not p.exists():
            self.footer.set_status("Error: This user does not exist. Use New to create user.")
        else:
            p_str = str(p)
            profile = Profile(self.server, open_user, self.password)
            profile.load_profile(p_str)
            if profile.password == user_pwd:
                self.username = open_user
                self.password = user_pwd
                for friend in profile.friend:
                    if friend not in self.body._contacts:
                        self.body.insert_contact(friend)
                self.body.user_label["text"] = open_user

    def configure_server(self):
        """For configuring the DS server."""
        ud = NewContactDialog(self.root, "Configure Account",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)

    def check_new(self):
        """Check if there are new contacts or new messages."""
        new_friends = []
        ds = ds_messenger.DirectMessenger(self.server, self.username, self.password)
        dm_lst = ds.retrieve_new()
        if dm_lst != []:
            store = ds_storage.Storage()
            new_friends = store.check_new_contact(dm_lst, self.username, self.password)
            if self.recipient != None:
                self.new_update(new_friends)
        self.root.after(1000, self.check_new)

    def open_user(self):
        """
        Open and load the user's profile to show their messages
        and contacts.
        """
        ud = OpenDialog(self.root, "Open User Profile",
                              self.username, self.password, self.server)
        open_user = ud.user
        user_pwd = ud.pwd

        dsu_name = open_user + ".dsu"
        directory = "."
        p = Path(directory) / dsu_name
        valid_inp = True
        if not p.exists():
            self.footer.set_status("Error: This user does not exist. Use New to create user.")
        else:
            p_str = str(p)
            profile = Profile(self.server, open_user, self.password)
            profile.load_profile(p_str)
            if profile.password == user_pwd:
                self.username = open_user
                self.password = user_pwd
                for friend in profile.friend:
                    self.body.insert_contact(friend)
                self.body.user_label["text"] = open_user
                self.footer.set_status("Opened profile successfully")
            else:
                self.footer.set_status("Open failure, password does not match")

    def open_new_user(self):
        """For opening a new user profile."""
        open_user = self.username
        user_pwd = self.password

        dsu_name = open_user + ".dsu"
        directory = "."
        p = Path(directory) / dsu_name
        valid_inp = True
        if not p.exists():
            self.footer.set_status("Error: This user does not exist. Use New to create user.")
        else:
            p_str = str(p)
            profile = Profile(self.server, open_user, self.password)
            profile.load_profile(p_str)
            if profile.password == user_pwd:
                self.username = open_user
                self.password = user_pwd
                for friend in profile.friend:
                    self.body.insert_contact(friend)
                self.body.user_label["text"] = open_user
                self.footer.set_status("Opened profile successfully")
            else:
                self.footer.set_status("Open failure, password does not match")

    def create_new_user(self):
        """Creates the new user profile."""
        ud = NewContactDialog(self.root, "Create New User",
                              self.username, self.password, self.server)
        self.username = ud.user
        self.password = ud.pwd
        self.server = ud.server
        self.direct_messenger = ds_messenger.DirectMessenger(self.server, self.username, self.password)

        if self.direct_messenger.get_token():
            dsu_name = self.username + ".dsu"
            directory = "."
            p = Path(directory) / dsu_name
            valid_inp = True
            if p.exists():
                self.footer.set_status("Error: This file already exists")
            else:
                if self.username == "":
                    valid_inp = False
                if self.password == "":
                    valid_inp = False
                if " " in self.username:
                    valid_inp = False
                if " " in self.password:
                    valid_inp = False

                if valid_inp:
                    p_str = str(p)
                    newfile = open(p, "x")
                    newfile.close()
                    profile = Profile(self.server, self.username, self.password)
                    profile.bio = ""
                    profile.save_profile(p_str)
                    self.footer.set_status("New profile created successfully")
                    self.open_new_user()
        else:
            self.footer.set_status("Token failure")

    def quit(self):
        """Quit the application window."""
        self.root.destroy()

    def _draw(self):
        """Build a menu and add it to the root frame."""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.create_new_user)
        menu_file.add_command(label='Open...', command=self.open_user)
        menu_file.add_command(label='Close', command=self.quit)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        self.check_new()


if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")

    main.attributes('-alpha', 0.9,)
    main["bg"] = "black"

    main.option_add('*tearOff', False)

    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())

    main.after(1000, app.check_new)

    main.mainloop()
