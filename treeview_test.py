# Source - https://stackoverflow.com/q/20330139
# Posted by throwaway17434, modified by community. See post 'Timeline' for change history
# Retrieved 2026-05-25, License - CC BY-SA 3.0

#! coding=utf-8
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
# The "show="tree headings"" allows for the expansion indicator to be shown in the treeview.
tree = ttk.Treeview(root, columns=('column1', 'column2'),show='tree headings')
tree['columns'] = ('Account Type', 'Balance')
tree.column("#0",  width=20,stretch=False, minwidth=20)   
tree.column('Account Type', width=140, minwidth=20)
tree.heading("#1", text="Account Type")
tree.column('Balance', width=140, minwidth=20)
tree.heading("#2", text="Balance")
tree.pack(fill=tk.BOTH,expand=True)

row=("k","k")

tree.insert("", index="end",iid="Main", values=row)
tree.insert("Main", index="end", values=row)
tree.insert("Main", index="end", values=row)

root.mainloop()

