# Trenton Gibson
# Created: 05/30/26
# FinanceProjectGUI_V3.py

#Explanation of project:
#This a personal finance manager that can access my SQLite Database
#and can handle my accounts and transactions.

# import tkinter GUI materials
import tkinter as tk
from tkinter import *
from tkinter import ttk
import FinanceProjectDatabaseAccess
# Create Finance GUI class
class FinanceGUI:
	def __init__(self):
		# Create Personal Finance Manager window, maximize the window, and create universal styles
		self.PersonalFinanceManager = tk.Tk()
		self.PersonalFinanceManager.title('Personal Finance Manager')
		self.PersonalFinanceManager.state('zoomed')
		self.ProjectStyle=ttk.Style()
		self.ProjectStyle.configure('TLabel', font=('Helvetica', 11))
		self.ProjectStyle.configure('TFrame', borderwidth='10', relief='solid')
		
		# Create Frames for Personal Finance Manager window
		# Create Parent Frames
		self.SidebarFrame=ttk.Frame(self.PersonalFinanceManager)
		self.TopFrame=ttk.Frame(self.PersonalFinanceManager)
		self.TopMidFrame =ttk.Frame(self.PersonalFinanceManager)
		self.TrueMiddleFrame=ttk.Frame(self.PersonalFinanceManager)
		self.BudgetingFrame=ttk.Frame(self.PersonalFinanceManager)
		# Create Child frames
		##Child frames of top frame
		self.AddAccountFrame=ttk.Frame(self.TopFrame)
		self. DeleteAccountFrame=ttk.Frame(self.TopFrame)
		self.RenameAccountFrame =ttk.Frame(self.TopFrame)
		##Child frames of top middle frame
		self.HandleAccountFrame =ttk.Frame(self.TopMidFrame)
		self.TransferMoneyFrame=ttk.Frame(self.TopMidFrame)
		self.TransactionHistoryFrame =ttk.Frame(self.TopMidFrame)
		##Child Frames of true middle frame
		self.AccountTreeviewFrame =ttk.Frame(self.TrueMiddleFrame)
		self.TransactionTreeviewFrame =ttk.Frame(self.TrueMiddleFrame)
		##Child frames of Budgeting Frame
		self.CreateBudgetFrame=ttk.Frame(self.BudgetingFrame)
		self.EditBudgetFrame=ttk.Frame(self.BudgetingFrame)
		
		#pack parent frames
		self.SidebarFrame.grid(row=0,column=0,rowspan=4,sticky="nsew")
		
		#pack child frames
		##Frames of Top Frame
		self.AddAccountFrame.grid(row=0,column=0)
		self.DeleteAccountFrame.grid(row=0,column=1)
		self.RenameAccountFrame.grid(row=0, column=2)
		##Frames of Top Middle Frame
		self.HandleAccountFrame.grid(row=0, column=0)
		self.TransferMoneyFrame.grid(row=0, column=1)
		self.TransactionHistoryFrame.grid(row=0, column=2)
		##Frames of True Middle Frame
		self.AccountTreeviewFrame.grid(row=0, column=0)
		self.TransactionTreeviewFrame.grid(row=0, column=1)
		##Frames of Budgeting Frame
		self.CreateBudgetFrame.grid(row=0, column=0,sticky="ew")
		self.EditBudgetFrame.grid(row=1, column=0, sticky="ew")
		
		# Create Widgets for Personal Finance Manager Window
		#Create UI for Budgeting Page
		## Create Widgets for the Create Budget Frame
		self.CreateBudgetLabel=tk.Label(self.CreateBudgetFrame, text="Budget Creation")
		self.BudgetNameLabel=tk.Label(self.CreateBudgetFrame, text="Budget Name")
		self.BudgetNameField=tk.Entry(self.CreateBudgetFrame)
		self.BudgetDescriptionLabel=tk.Label(self.CreateBudgetFrame, text="Budget Description")
		self.BudgetDescriptionField=tk.Entry(self.CreateBudgetFrame)
		self.CreateBudgetButton=tk.Button(self.CreateBudgetFrame, text="Create Budget")
		## Add widgets to create budget frame
		self.CreateBudgetLabel.grid(row=1, column=0)
		self.BudgetNameLabel.grid(row=0, column=1)
		self.BudgetNameField.grid(row=1, column=1)
		self.BudgetDescriptionLabel.grid(row=0, column=2)
		self.BudgetDescriptionField.grid(row=1, column=2)
		self.CreateBudgetButton.grid(row=1, column=3)
		## Create Widgets for Edit Budget Frame
		self.BudgetEditingAndViewingLabel=tk.Label(self.EditBudgetFrame, text="Budget Editing and Viewing")
		self.BudgetEditingDropdownLabel=tk.Label(self.EditBudgetFrame, text="Budget to Edit or View")
		self.BudgetEditingDropdown=ttk.Combobox(self.EditBudgetFrame)
		self.AddNewBudgetItemLabel=tk.Label(self.EditBudgetFrame, text="Add new button budget item below!")
		self.EditBudgetLogicalDropdownLabel=tk.Label(self.EditBudgetFrame,text="Logical Account")
		self.EditBudgetLogicalDropdown=ttk.Combobox(self.EditBudgetFrame)
		self.BudgetAllocationTypeDropdownLabel=tk.Label(self.EditBudgetFrame, text="Budget Allocation Type")
		self.BudgetAllocationTypeDropdown=ttk.Combobox(self.EditBudgetFrame)
		self.BudgetAllocationAmountLabel=tk.Label(self.EditBudgetFrame, text="Budget Allocation Amount")
		self.BudgetAllocationAmountField=tk.Entry(self.EditBudgetFrame)
		self.BudgetItemNoteLabel=tk.Label(self.EditBudgetFrame, text="Budget Item Note")
		self.BudgetItemNoteField=ttk.Combobox(self.EditBudgetFrame)
		self.CreateBudgetItemButton=tk.Button(self.EditBudgetFrame, text="Create Budget Item")
		self.Budget_yscroll = Scrollbar(self.EditBudgetFrame)
		self.BudgetInfoTreeview = ttk.Treeview(self.EditBudgetFrame, height=10,
												 columns=('column1', 'column2', 'column3', 'column4'),
												 show='tree headings', yscrollcommand=self.Budget_yscroll.set)
		##Define and create the columns for the Account Treeview
		self.BudgetInfoTreeview['columns'] = ('Logical Account', 'Budget Allocation Type', 'Budget Allocation Amount','Budget Item Note')
		self.BudgetInfoTreeview.column("#0",width=20)   
		self.BudgetInfoTreeview.column('Logical Account', width=100)
		self.BudgetInfoTreeview.heading("#1", text="Logical Account")
		self.BudgetInfoTreeview.column('Budget Allocation Type', width=100)
		self.BudgetInfoTreeview.heading("#2", text="Budget Allocation Type")
		self.BudgetInfoTreeview.column('Budget Allocation Amount', width=100)
		self.BudgetInfoTreeview.heading("#3", text="Budget Allocation Amount")
		self.BudgetInfoTreeview.column('Budget Item Note', width=100)
		self.BudgetInfoTreeview.heading("#4", text="Budget Item Note")
		row=("1","k","k","k")
		for i in range(20):
			id2=self.BudgetInfoTreeview.insert("", tk.END, values=row)
			self.BudgetInfoTreeview.insert(id2, tk.END, values=row)
		self.Budget_yscroll.config(command=self.BudgetInfoTreeview.yview)
		self.BudgetStatsLabel=tk.Label(self.EditBudgetFrame,
			text="Total Budget Allocation:      Unallocated Funds:           Percentage of Funds Unallocated:        Funds Allocated to the Remainder:")
		self.SaveandExitButton=tk.Button(self.EditBudgetFrame, text="Save and Exit")
		self.DeleteItemButtonTutorial=tk.Label(self.EditBudgetFrame,
			text="If you wish to delete a budget item, click on said budget item in the viewing table and press the Delete Budget Item button to remove the unvwanted budget item.")
		self.DeleteItemButton=tk.Button(self.EditBudgetFrame, text="Delete Item Budget")
		## Add widgets to Edit Budget Frame
		self.BudgetEditingAndViewingLabel.grid(row=0,column=0,columnspan=3)
		self.BudgetEditingDropdownLabel.grid(row=0,column=3)
		self.BudgetEditingDropdown.grid(row=0,column=4)
		self.AddNewBudgetItemLabel.grid(row=1,column=0,columnspan=9)
		self.EditBudgetLogicalDropdownLabel.grid(row=2,column=0)
		self.EditBudgetLogicalDropdown.grid(row=2,column=1)
		self.BudgetAllocationTypeDropdownLabel.grid(row=2,column=2)
		self.BudgetAllocationTypeDropdown.grid(row=2,column=3)
		self.BudgetAllocationAmountLabel.grid(row=2,column=4)
		self.BudgetAllocationAmountField.grid(row=2,column=5)
		self.BudgetItemNoteLabel.grid(row=2,column=6)
		self.BudgetItemNoteField.grid(row=2,column=7)
		self.CreateBudgetItemButton.grid(row=2,column=8)
		self.BudgetInfoTreeview.grid(row=3,column=4)
		self.Budget_yscroll.grid(row=3,column=5,sticky='wns')
		self.BudgetStatsLabel.grid(row=4,column=1,columnspan=7)
		self.SaveandExitButton.grid(row=5,column=1)
		self.DeleteItemButtonTutorial.grid(row=5,column=2,columnspan=5)
		self.DeleteItemButton.grid(row=5,column=7)
										 
		#Create widgets for Sidebar Frame
		self.AccountManagementButton=tk.Button(self.SidebarFrame, text='Account\nManagement', command=self.ShowAccountManagementWidgets)
		self.BudgetingButton=tk.Button(self.SidebarFrame, text='Budgeting', command=self.ShowBudgetingWidgets)
		## Add Sidebar Frame widgets
		self.AccountManagementButton.grid(row=0, column=0)
		self.BudgetingButton.grid(row=1, column=0)
		#Create widgets for the Top Frame
		##create account frame widgets
		self.CreateAccountLabel = tk.Label(self.AddAccountFrame,text='Account Creation')
		self.NameAccountLabel = tk.Label(self.AddAccountFrame, text='Account Name')
		self.NameAccountEntry = tk.Entry(self.AddAccountFrame)
		self.IntialBalanceLabel = tk.Label(self.AddAccountFrame,text='Intial Balance')
		self.IntialBalanceEntry = tk.Entry(self.AddAccountFrame)
		self.AccountNoteLabel = tk.Label(self.AddAccountFrame,text='Account Description')
		self.AccontNoteEntry = tk.Entry(self.AddAccountFrame)
		self.ChooseAccountCategoryLabel = tk.Label(self.AddAccountFrame,text='Account Category')
		self.ChooseAccountCategoryDropbox = ttk.Combobox(self.AddAccountFrame)
		self.CreateAccountButton=tk.Button(self.AddAccountFrame, text='Create Account', command=self.GetGivingAccount)
		## add the create account frame widgets
		self.CreateAccountLabel.grid(row=0,column=0, columnspan=2,padx=10)
		self.NameAccountLabel.grid(row=1, column=0,padx=10)
		self.NameAccountEntry.grid(row=1, column=1,padx=10)
		self.IntialBalanceLabel.grid(row=2, column=0,padx=10)
		self.IntialBalanceEntry.grid(row=2, column=1, padx=10)
		self.AccountNoteLabel.grid(row=3, column=0, padx=10)
		self.AccontNoteEntry.grid(row=3, column=1, padx=10)
		self.ChooseAccountCategoryLabel.grid(row=4, column=0, padx=10)
		self.ChooseAccountCategoryDropbox.grid(row=4, column=1, padx=10)
		self.CreateAccountButton.grid(row=5, column=0, columnspan=2, ipadx=10)
		## Create Delete Account Frame Widgets
		self.DeleteAccountLabel=tk.Label(self.DeleteAccountFrame, text='Account Deletion')
		self.AccountToDeleteLabel=tk.Label(self.DeleteAccountFrame, text='Account to Delete')
		self.AccountToDeleteDropdown=ttk.Combobox(self.DeleteAccountFrame)                                                       
		self.DeleteAccountButton=tk.Button(self.DeleteAccountFrame, text='Delete Account')
		## Add Delete Account Frame Widgets
		self.DeleteAccountLabel.grid(row=0, column=0,columnspan=2)
		self.AccountToDeleteLabel.grid(row=1, column=0)
		self.AccountToDeleteDropdown.grid(row=1,column=1)
		self.DeleteAccountButton.grid(row=2,column=0, columnspan=2)
		## Create Widgets for Account Renaming Frame
		self.AccountRenamingLabel=tk.Label(self.RenameAccountFrame,text='Account Renaming')
		self.AccountToRenameLabel=tk.Label(self.RenameAccountFrame,text='Account to Rename')
		self.AccountToRenameDropdown=ttk.Combobox(self.RenameAccountFrame)
		self.NewAccountNameLabel=tk.Label(self.RenameAccountFrame,text='New Account Name')
		self.NewAccountNameField=tk.Entry(self.RenameAccountFrame)
		self.RevisedAccountDescriptionLabel=tk.Label(self.RenameAccountFrame,text='Revised Account Description (Optional)')
		self.RevisedAccountDescriptionField=tk.Entry(self.RenameAccountFrame)
		self.RenameAccountButton=tk.Button(self.RenameAccountFrame, text='Rename Account')
		## Add Widgets for Account Renaming Frame
		self.AccountRenamingLabel.grid(row=0, column=0, columnspan=2)
		self.AccountToRenameLabel.grid(row=1, column=0)
		self.AccountToRenameDropdown.grid(row=1, column=1)
		self.NewAccountNameLabel.grid(row=2, column=0)
		self.NewAccountNameField.grid(row=2, column=1)
		self.RevisedAccountDescriptionLabel.grid(row=3,column=0)
		self.RevisedAccountDescriptionField.grid(row=3,column=1)
		self.RenameAccountButton.grid(row=4, column=0, columnspan=2)
		
		#Create Top Middle Frame Widgets
		## Create handle account frame widgets
		self.TransactionLabel = tk.Label(self.HandleAccountFrame, text='Transaction Entry')
		self.RealAccountLabel = tk.Label(self.HandleAccountFrame,text='Real Account')
		self.RealAccountDropdown=ttk.Combobox(self.HandleAccountFrame)
		self.LogicalAccountLabel=tk.Label(self.HandleAccountFrame, text='Logical Account')
		self.LogicalAccountDropdown=ttk.Combobox(self.HandleAccountFrame)
		self.IncomeOrExpenseLabel=tk.Label(self.HandleAccountFrame, text='Income or Expense')
		self.IncomeOrExpenseDropdown=ttk.Combobox(self.HandleAccountFrame)
		self.BudgetLabel=tk.Label(self.HandleAccountFrame, text='Budget (If Income)')
		self.BudgetDropdown=ttk.Combobox(self.HandleAccountFrame)
		self.TransactionAmountLabel=tk.Label(self.HandleAccountFrame, text='Transaction Amount')
		self.TransactionAmountField=tk.Entry(self.HandleAccountFrame)
		self.DateofTransLabel = tk.Label(self.HandleAccountFrame, text='Transaction Date')
		self.MonthofTransEntry = tk.Entry(self.HandleAccountFrame)
		self.DateDashLabel1= tk.Label(self.HandleAccountFrame,text='-')
		self.DayofTransEntry = tk.Entry(self.HandleAccountFrame,)
		self.DateDashLabel2 = tk.Label(self.HandleAccountFrame, text='-')
		self.YearofTransEntry = tk.Entry(self.HandleAccountFrame,)
		self.TransactionTypeLabel = tk.Label(self.HandleAccountFrame, text='Transaction Description')
		self.TransactionTypeEntry = tk.Entry(self.HandleAccountFrame,)
		self.EnterTransactionButton = tk.Button(self.HandleAccountFrame, text='Enter Transaction')
		## Pack Handle Account Frame Widgets
		self.TransactionLabel.grid(row=0, column=0, columnspan=6)
		self.RealAccountLabel.grid(row=1, column=0)
		self.RealAccountDropdown.grid(row=1, column=1, columnspan=5)
		self.LogicalAccountLabel.grid(row=2, column=0)
		self.LogicalAccountDropdown.grid(row=2, column=1, columnspan=5)
		self.IncomeOrExpenseLabel.grid(row=3, column=0)
		self.IncomeOrExpenseDropdown.grid(row=3, column=1, columnspan=5)
		self.BudgetLabel.grid(row=4, column=0)
		self.BudgetDropdown.grid(row=4, column=1, columnspan=5)
		self.TransactionAmountLabel.grid(row=5, column=0)
		self.TransactionAmountField.grid(row=5, column=1, columnspan=5)
		self.DateofTransLabel.grid(row=6, column=0)
		self.MonthofTransEntry.grid(row=6, column=1)
		self.DateDashLabel1.grid(row=6, column=2)
		self.DayofTransEntry.grid(row=6, column=3)
		self.DateDashLabel2.grid(row=6, column=4)
		self.YearofTransEntry.grid(row=6, column=5)
		self.TransactionTypeLabel.grid(row=7, column=0)
		self.TransactionTypeEntry.grid(row=7, column=1, columnspan=5)
		self.EnterTransactionButton.grid(row=8, column=0, columnspan=6)
		##Create Transfer money frame widgets
		self.MoneyTransferLabel = tk.Label(self.TransferMoneyFrame, text='Money Transfer')
		self.ExpendingAccountLabel=tk.Label(self.TransferMoneyFrame, text='Expending Account')
		self.ExpendingAccountDropdown=ttk.Combobox(self.TransferMoneyFrame,)
		self.RecipientAccountLabel=tk.Label(self.TransferMoneyFrame, text='Recipient Account')
		self.RecipientAccountDropdown=ttk.Combobox(self.TransferMoneyFrame)
		self.TransferAmountLabel=tk.Label(self.TransferMoneyFrame,text='Transfer Amount')
		self.TransferAmountField=tk.Entry(self.TransferMoneyFrame)
		self.TransferDescriptionLabel=tk.Label(self.TransferMoneyFrame, text='Transfer Description')
		self.TransferDescriptionField=tk.Entry(self.TransferMoneyFrame)
		self.RecordTransferButton = tk.Button(self.TransferMoneyFrame, text='Record Transfer', command=self.GetGivingAccount)
		## Pack Transfer money frame widgets
		self.MoneyTransferLabel.grid(row=0, column=0, columnspan=2)
		self.ExpendingAccountLabel.grid(row=1, column=0)
		self.ExpendingAccountDropdown.grid(row=1, column=1)
		self.RecipientAccountLabel.grid(row=2, column=0)
		self.RecipientAccountDropdown.grid(row=2, column=1)
		self.TransferAmountLabel.grid(row=3, column=0)
		self.TransferAmountField.grid(row=3, column=1)
		self.TransferDescriptionLabel.grid(row=4, column=0)
		self.TransferDescriptionField.grid(row=4, column=1)
		self.RecordTransferButton.grid(row=5, column=0, columnspan=2)
		## Create transaction history frame widgets
		self.TransactionHistoryLabel = tk.Label(self.TransactionHistoryFrame, text='Transaction History')
		self.AccountChoiceLabel = tk.Label(self.TransactionHistoryFrame, text='Account Choice')
		self.AccountChoiceDropdown=ttk.Combobox(self.TransactionHistoryFrame)
		self.ChosenAccountsLabel=tk.Label(self.TransactionHistoryFrame, text='Chosen Accounts')
		self.ChosenAccountsField=tk.Entry(self.TransactionHistoryFrame)
		self.ShowHistoryButton=tk.Button(self.TransactionHistoryFrame, text='Show History')
		##Pack Transaction history frame widgets
		self.TransactionHistoryLabel.grid(row=0, column=0, columnspan=2)
		self.AccountChoiceLabel.grid(row=1, column=0)
		self.AccountChoiceDropdown.grid(row=1, column=1)
		self.ChosenAccountsLabel.grid(row=2, column=0)
		self.ChosenAccountsField.grid(row=2, column=1)
		self.ShowHistoryButton.grid(row=3, column=0, columnspan=2)
		
		#Create widgets for the True Middle Frame
		self.AccountsInfoLabel=tk.Label(self.AccountTreeviewFrame, text="Account Table")
		self.AccountsInfoLabel.grid(row=0,column=0, columnspan=2 )
		# Create Account Treeview
		##Create Account Treeview ScrollBar
		self.Accounts_yscroll = Scrollbar(self.AccountTreeviewFrame)
		self.Accounts_yscroll.grid(row=1, column=1, sticky="ns")
		##Create actual Account Treeview
		self.AccountsInfoTreeview = ttk.Treeview(self.AccountTreeviewFrame, height=10,
												 columns=(
												 'column1', 'column2', 'column3', 'column4', 'column5', 'column6'),
												 show='tree headings', yscrollcommand=self.Accounts_yscroll.set)
		##Define and create the columns for the Account Treeview
		self.AccountsInfoTreeview['columns'] = (
		'Account Name', 'Account Description', 'Balance','Transaction Description','Transaction Amount', 'Date of Transaction')
		self.AccountsInfoTreeview.column("#0",width=20)   
		self.AccountsInfoTreeview.column('Account Name', width=100)
		self.AccountsInfoTreeview.heading("#1", text="Account Name")
		self.AccountsInfoTreeview.column('Account Description', width=100)
		self.AccountsInfoTreeview.heading("#2", text="Account Description")
		self.AccountsInfoTreeview.column('Balance', width=100)
		self.AccountsInfoTreeview.heading("#3", text="Balance")
		self.AccountsInfoTreeview.column('Transaction Description', width=100)
		self.AccountsInfoTreeview.heading("#4", text="Transaction Description")
		self.AccountsInfoTreeview.column('Transaction Amount', width=100)
		self.AccountsInfoTreeview.heading("#5", text="Transaction Amount")
		self.AccountsInfoTreeview.column('Date of Transaction', width=100)
		self.AccountsInfoTreeview.heading("#6", text="Date of Transaction")
		## Pack and configure the scrollbar for the Accounts Treeview
		self.AccountsInfoTreeview.grid(row=1, column=0, sticky='ns')
		self.Accounts_yscroll.config(command=self.AccountsInfoTreeview.yview)
		row=("1","k","k","k","k","k")
		for i in range(20):
			id2=self.AccountsInfoTreeview.insert("", tk.END, values=row)
			self.AccountsInfoTreeview.insert(id2, tk.END, values=row)
		# self.AccountsInfoTreeview.insert()
		## Populate treeview with data
		rows = FinanceProjectDatabaseAccess.AccOverDataWithTransID()
		for row in rows:
			self.AccountsInfoTreeview.insert("", tk.END, values=row)
		rows = FinanceProjectDatabaseAccess.AccOverDataWithoutTransID()
		for row in rows:
			self.AccountsInfoTreeview.insert("", tk.END, values=row)
		
		# Create Transaction Info treeview
		#Create Transaction table widget
		self.TransactionHistoryLabel=tk.Label(self.TransactionTreeviewFrame, text="Transaction Table")
		self.TransactionHistoryLabel.grid(row=0,column=0, columnspan=2 )
		##Create Scrollbars for Transaction Treeview
		self.Transaction_yscroll = Scrollbar(self.TransactionTreeviewFrame)
		self.Transaction_yscroll.grid(row=1, column=1, sticky='ns')
		##Create the actual Transaction Treeview
		self.TransHisTransactionInfo = ttk.Treeview(self.TransactionTreeviewFrame, height=10,
													columns=(
													'column1', 'column2', 'column3', 'column4', 'column5', 'column6', 'column7'),
													show='tree headings', yscrollcommand=self.Transaction_yscroll.set)
		##Define and create the columns for the Transaction Treeview
		self.TransHisTransactionInfo['columns'] = ( 'Account Type', 'Account Name','Previous Balance', 'Current Balance',
												   'Transaction Type', 'Transaction Amount', 'Transaction Date')
		self.TransHisTransactionInfo.column('#0', width=20)
		self.TransHisTransactionInfo.column('Transaction Type', width=100)
		self.TransHisTransactionInfo.heading("#1", text="Transaction Type")
		self.TransHisTransactionInfo.column('Transaction Date', width=100)
		self.TransHisTransactionInfo.heading("#2", text="Transaction Date")
		self.TransHisTransactionInfo.column('Transaction Amount', width=100)
		self.TransHisTransactionInfo.heading("#3", text="Transaction Amount")
		self.TransHisTransactionInfo.column('Account Type', width=100)
		self.TransHisTransactionInfo.heading("#4", text="Account Type")
		self.TransHisTransactionInfo.column('Account Name', width=100)
		self.TransHisTransactionInfo.heading("#5", text="Account Name")
		self.TransHisTransactionInfo.column('Previous Balance', width=100)
		self.TransHisTransactionInfo.heading("#6", text="Previous Balance")
		self.TransHisTransactionInfo.column('Current Balance', width=100)
		self.TransHisTransactionInfo.heading("#7", text="Current Balance")
		##Pack the Transaction Treeview
		self.TransHisTransactionInfo.grid(row=1, column=0, sticky='ns')
		##Configure the Transaction Treeview Scrollbar
		self.Transaction_yscroll.config(command=self.TransHisTransactionInfo.yview)
		##Populate the Transaction Treeview with data
		self.StartAccountHistory = ''
		rows = FinanceProjectDatabaseAccess.AccountTransactionHistory(self.StartAccountHistory)
		row=("1","k","k","","","","")
		row2=("","","","k","k","k","k")
		for i in range(20):
			id2=self.TransHisTransactionInfo.insert("", tk.END, values=row)
			self.TransHisTransactionInfo.insert(id2, tk.END, values=row2)
		for row in rows:
			self.TransHisTransactionInfo.insert("", tk.END, values=row)
		
		# Change the style of the Treeviews
		style = ttk.Style()
		style.configure("Treeview.Heading", fieldbackground='#9613bb', )
		style.configure("Treeview", )
		style.configure("Treeview", foreground='yellow', background='#9613bb')

		# Start the mainloop
		tk.mainloop()
		
		
	# Additional Methods
	#Handles Typical transactions.Is called by Handle Account Frame Widgets.
	def TransDataAndTransCommit(self):
		try:
			# Get data for Transaction
			self.selected = self.AccountsInfoTreeview.focus()
			self.Account = self.AccountsInfoTreeview.item(self.selected, 'values')
			self.Month=self.MonthofTransEntry.get()
			self.Day = self.DayofTransEntry.get()
			self.Year=self.YearofTransEntry.get()
			self.TransactionDate=self.Month+'-'+self.Day+'-'+self.Year
			self.TransactionAmount = self.TransactionEntry.get()
			self.TransactionType = self.TransactionTypeEntry.get()
			#if any of the date entries can't be converted to integers then the exception handling will kick in
			self.MonthTest= int(self.Month)
			self.DayTest= int(self.Day)
			self.YearTest=int(self.Year)
			#If any of the entries are unpopulated or aren't within the proper date range, it sends an error message and the core code isn't executed
			if self.TransactionAmount =='' or self.TransactionType == '' or self.Month=='' or self.Year==''or self.Day==''\
			or self. MonthTest > 12 or self. MonthTest<1 or self.DayTest<0 or self.DayTest>31 or self.YearTest < 2023  :
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			# The core code
			else:
				#Calls the Handle Account Function from the other module to interact with the database
				FinanceProjectDatabaseAccess.HandleAccount(self.Account, self.TransactionDate, self.TransactionAmount, self.TransactionType)
				# Repopulate treeviews with data after the changes are made to represent them
				self.RepopulateAccountsTreeview()
				self.RepopulateTransactionsTreeview()
				self.TransactionEntry.delete(0, END)
				self.TransactionTypeEntry.delete(0, END)
				self.YearofTransEntry.delete(0,END)
				self.DayofTransEntry.delete(0,END)
				self.MonthofTransEntry.delete(0,END)
		except:
			#Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			#Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
			
			
	#Creates a new account
	def AddAccount(self):
		try:
			#get data from the entries to create a new account
			self.AccountName = self.NameAccountEntry.get()
			self.IntialBalance = self.IntialBalanceEntry.get()
			self.IntialBalance= float(self.IntialBalance)
			# If any of the entries are unpopulated, it sends an error message and the core code isn't executed
			if self.AccountName == '' or self.IntialBalance == '':
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			#The core code
			else:
				#Add Account Function is called from the other module to interact with the database
				FinanceProjectDatabaseAccess.AddAccount(self.IntialBalance, self.AccountName)
				# Repopulate treeviews with data
				self.RepopulateAccountsTreeview()
				self.RepopulateTransactionsTreeview()
				self.NameAccountEntry.delete(0,END)
				self.IntialBalanceEntry.delete(0,END)
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
	
			
	#Deletes an account if called
	def DeleteAccount(self):
		try:
			#get data for which account to delete
			self.selected = self.AccountsInfoTreeview.focus()
			self.AccountToDelete= self.AccountsInfoTreeview.item(self.selected, 'values')
			
			#set up accumulator to end the loop when the correct tuple data is place
			count=0
			#processe tuple data into a usable string form
			for item in self.AccountToDelete:
				count+=1
				String = str(item)
				String = String.lstrip('(')
				String = String.rstrip(')')
				String = String.rstrip(',')
				self.AccountToDelete = String
				#loop ends when the second data value gets processed
				if count==1:
					break
			#Calls Delete account function from the other module to interact with the database
			FinanceProjectDatabaseAccess.DeleteAccount(self.AccountToDelete)
			# Repopulate treeviews with data
			self.RepopulateAccountsTreeview()
			self.RepopulateTransactionsTreeview()
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
			
	
	#Gets the account transaction history of a specific account
	def AccountHistory(self):
		try:
			#get the selected account name from the accounts treeview
			self.selected = self.AccountsInfoTreeview.focus()
			self.AccountHistory = self.AccountsInfoTreeview.item(self.selected, 'values')
			#isolate the account name from the rest of the data
			# start accumulator to act as a trigger to end the loop early so the needed value can be obtained
			count = 0
			# process tuple data into string data
			for item in self.AccountHistory:
				count += 1
				String = str(item)
				self.AccountHistory = String
				# end the loop when the correct value is in play
				if count == 1:
					break
			#if there is no account clicked the table is restored
			if self.AccountHistory!='':
				# call the Account transaction History function to retrieve data from the database to view
				self.TransactionAccountHistory = FinanceProjectDatabaseAccess.AccountTransactionHistory(
					self.AccountHistory)
				# clear the data out and replace it with the requested data
				for item in self.TransHisTransactionInfo.get_children():
					self.TransHisTransactionInfo.delete(item)
				for row in self.TransactionAccountHistory:
					self.TransHisTransactionInfo.insert("", tk.END, values=row)
			else:
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
			
			
	#Handles transferring money between two accounts
	def TransferringMoney(self):
		try:
			#get accounts transferring and amount of money being transferred
			self.TransferredMoney = self.AmountTransferredEntry.get()
			self.TransMonGivingAccount = self.GivingAccount
			self.TransMonRecipientAccount = self.RecipientAccount
			#if any of the values are empty then an error message will pop up and the core code will not execute
			if self.TransferredMoney == '' or self.TransMonGivingAccount == '' \
			or self.TransMonRecipientAccount=='' or self.TransferredMoney==self.TransferredMoney.isalpha():
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			else:
				#Calls Account transfer function which will handle the database interactions for transferring money
				FinanceProjectDatabaseAccess.AccountTransfer(self.TransferredMoney, self.TransMonGivingAccount, self.TransMonRecipientAccount)
				# Repopulate treeviews with data
				self.RepopulateAccountsTreeview()
				self.RepopulateTransactionsTreeview()
				#reformat labels back to original state
				self.GiverAccountLabel.config(text='Giving Account:', foreground='black', background='white')
				self.RecipientAccountLabel.config(text='Recipient Account:', foreground='black', background='white')
				#clear amount transferred entry
				self.AmountTransferredEntry.delete(0,END)
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
	
	
	#gets the giving account for transferring money
	def GetGivingAccount(self):
		try:
			#obtains the giving account
			self.selected = self.AccountsInfoTreeview.focus()
			self.GivingAccount = self.AccountsInfoTreeview.item(self.selected, 'values')
			#start accumulator to act as a trigger to end the loop early so the needed value can be obtained
			count = 0
			#process tuple data into string data
			for item in self.GivingAccount:
				count += 1
				String = str(item)
				self.GivingAccount = String
				#end the loop when the correct value is in play
				if count == 1:
					break
			#if the Giving Account variable isn't empty, make the Giving account label change text and coloring
			if self.GivingAccount!= '':
				self.GiverAccountLabel.config(text='Giving Account:'+self.GivingAccount,font=('Times New Roman',11), foreground='yellow', background='#9613bb')
			# return the variable for transferring the money
			return self.GivingAccount
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
			
			
	# gets the recipient account for transferring money
	def GetRecipientAccount(self):
		try:
			#obtain the recipient account from the accounts treeview and put in the recipient account variable
			self.selected = self.AccountsInfoTreeview.focus()
			self.RecipientAccount = self.AccountsInfoTreeview.item(self.selected, 'values')
			# start accumulator to act as a trigger to end the loop early so the needed value can be obtained
			count = 0
			# process tuple data into string data
			for item in self.RecipientAccount:
				count += 1
				String = str(item)
				self.RecipientAccount = String
				# end the loop when the correct value is in play
				if count == 1:
					break
			#if the Recipient Account variable isn't empty, make the Recipient account label change text and coloring
			if self.RecipientAccount!= '':
				self.RecipientAccountLabel.config(text='Recipient Account:' + self.RecipientAccount,font=('Times New Roman',11), foreground='yellow', background='#9613bb')
			# return the variable for transferring the money
			return self.RecipientAccount
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
			
			
	#Repopulates the accounts treeview with data
	def RepopulateAccountsTreeview(self):
		#Clears the old treeview data
		for item in self.AccountsInfoTreeview.get_children():
			self.AccountsInfoTreeview.delete(item)
		#obtain data for accounts with transactions recorded and add the data to the treeview
		rows = FinanceProjectDatabaseAccess.AccOverDataWithTransID()
		for row in rows:
			self.AccountsInfoTreeview.insert("", tk.END, values=row)
		# obtain data for accounts without transactions recorded and add the data to the treeview
		rows = FinanceProjectDatabaseAccess.AccOverDataWithoutTransID()
		for row in rows:
			self.AccountsInfoTreeview.insert("", tk.END, values=row)
			
			
	#Repopulate the transaction treeview with data
	def RepopulateTransactionsTreeview(self):
		#get the transaction history for all the accounts
		TransactionAccountHistory = FinanceProjectDatabaseAccess.AccountTransactionHistory(self.StartAccountHistory)
		#clear the transaction treeview
		for item in self.TransHisTransactionInfo.get_children():
			self.TransHisTransactionInfo.delete(item)
		#Insert new transaction treeview data into the transaction treeview
		for row in TransactionAccountHistory:
			self.TransHisTransactionInfo.insert("", tk.END, values=row)
	
	def ResetTransHisTree(self):
		#make account history an empty string to reset the treeview
		self.AccountHistory=''
		#get the transaction info from the other module
		self.TransactionAccountHistory = FinanceProjectDatabaseAccess.AccountTransactionHistory(
			self.AccountHistory)
		# clear the data out and replace it with the requested data
		for item in self.TransHisTransactionInfo.get_children():
			self.TransHisTransactionInfo.delete(item)
		for row in self.TransactionAccountHistory:
			self.TransHisTransactionInfo.insert("", tk.END, values=row)
	
	##Renames the account of your choosing to whatever you put in the entry
	def RenameAccount(self):
		try:
			#get the new name for the account and find the name of the account you wish to change
			self.NewName = self.RenameAccountEntry.get()
			self.selected = self.AccountsInfoTreeview.focus()
			self.ToBeRenamedAccount = self.AccountsInfoTreeview.item(self.selected, 'values')
			if self.NewName == '' or self.ToBeRenamedAccount == '':
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			else:
				#this section turns the tuple from the treeview into a string
				# start accumulator to act as a trigger to end the loop early so the needed value can be obtained
				count = 0
				# process tuple data into string data
				for item in self.ToBeRenamedAccount:
					count += 1
					String = str(item)
					self.ToBeRenamedAccount = String
					# end the loop when the correct value is in play
					if count == 1:
						break
				FinanceProjectDatabaseAccess.RenamingAccount(self.ToBeRenamedAccount,self.NewName)
				self.RepopulateAccountsTreeview()
				self.RenameAccountEntry.delete(0, END)
		except:
			# Create an error message variable
			self.ErrorMessage = 'Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)

	def ShowBudgetingWidgets(self):
		self.TopFrame.grid_remove()
		self.TopMidFrame.grid_remove()
		self.TrueMiddleFrame.grid_remove()
		self.BudgetingFrame.grid(row=0,column=1)
	
	def ShowAccountManagementWidgets(self):
		self.BudgetingFrame.grid_remove()
		self.TopFrame.grid(row=0, column=1)
		self.TopMidFrame.grid(row=1, column=1)
		self.TrueMiddleFrame.grid(row=2, column=1)

# Call the Finance GUI Class
if __name__ == '__main__':
	FinanceGUI()