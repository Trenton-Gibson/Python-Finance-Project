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
from tkinter import messagebox
from enum import StrEnum
import FinanceProjectDatabaseAccess
class BudgetAllocationTypes(StrEnum):
	PERCENTAGE="Percentage"
	FIXED="Fixed"
	REMAINDER="Remainder"

class BudgetExpenditureTypes(StrEnum):
	INCOME="Income"
	EXPENSE="Expense"

class AccountTypes(StrEnum):
	REAL="Real"
	LOGICAL="Logical"

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
		self.BudgetAmountLabel=tk.Label(self.CreateBudgetFrame, text="Budget Amount")
		self.BudgetAmountField=tk.Entry(self.CreateBudgetFrame)
		self.BudgetDescriptionLabel=tk.Label(self.CreateBudgetFrame, text="Budget Description")
		self.BudgetDescriptionField=tk.Entry(self.CreateBudgetFrame)
		self.CreateBudgetButton=tk.Button(self.CreateBudgetFrame, text="Create Budget", command=self.CreateBudget)
		## Add widgets to create budget frame
		self.CreateBudgetLabel.grid(row=1, column=0)
		self.BudgetNameLabel.grid(row=0, column=1)
		self.BudgetNameField.grid(row=1, column=1)
		self.BudgetAmountLabel.grid(row=0, column=2)
		self.BudgetAmountField.grid(row=1, column=2)
		self.BudgetDescriptionLabel.grid(row=0, column=3)
		self.BudgetDescriptionField.grid(row=1, column=3)
		self.CreateBudgetButton.grid(row=1, column=4)
		## Create Widgets for Edit Budget Frame
		self.BudgetEditingAndViewingLabel=tk.Label(self.EditBudgetFrame, text="Budget Editing and Viewing")
		self.BudgetEditingDropdownLabel=tk.Label(self.EditBudgetFrame, text="Budget to Edit or View")
		# The following 3 lines, respectively, create a variable to store the selected of the
		# Budget Editing Dropdown, create the BudgetEditingDropdown with that previously created variable,
		# and bind the action of selecting an option in the combobox to the ResetBudgetTree method.
		self.BudgetDropdownChoice = tk.StringVar()
		self.BudgetEditingDropdown=ttk.Combobox(self.EditBudgetFrame, textvariable = self.BudgetDropdownChoice)
		self.BudgetEditingDropdown.bind("<<ComboboxSelected>>", self.ResetBudgetTree)
		self.AddNewBudgetItemLabel=tk.Label(self.EditBudgetFrame, text="Add new button budget item below!")
		self.EditBudgetLogicalDropdownLabel=tk.Label(self.EditBudgetFrame,text="Logical Account")
		self.EditBudgetLogicalDropdown=ttk.Combobox(self.EditBudgetFrame)
		self.BudgetAllocationTypeDropdownLabel=tk.Label(self.EditBudgetFrame, text="Budget Allocation Type")
		self.BudgetAllocationTypeDropdown=ttk.Combobox(self.EditBudgetFrame)
		self.BudgetAllocationAmountLabel=tk.Label(self.EditBudgetFrame, text="Budget Allocation Amount")
		self.BudgetAllocationAmountField=tk.Entry(self.EditBudgetFrame)
		self.BudgetItemNoteLabel=tk.Label(self.EditBudgetFrame, text="Budget Item Note")
		self.BudgetItemNoteField=ttk.Entry(self.EditBudgetFrame)
		self.CreateBudgetItemButton=tk.Button(self.EditBudgetFrame, text="Create Budget Item", command=self.AddBudgetItem)
		self.Budget_yscroll = Scrollbar(self.EditBudgetFrame)
		self.BudgetInfoTreeview = ttk.Treeview(self.EditBudgetFrame, height=10,
												 columns=('column1', 'column2', 'column3', 'column4'),
												 show='tree headings', yscrollcommand=self.Budget_yscroll.set)
		##Define and create the columns for the Account Treeview
		self.BudgetInfoTreeview['columns'] = ('Budget Name', 'Budget Item ID','Logical Account', 'Budget Allocation Type', 'Budget Allocation Amount','Budget Item Note')
		self.BudgetInfoTreeview.column("#0",width=20)
		self.BudgetInfoTreeview.column('Budget Name', width=80)
		self.BudgetInfoTreeview.heading("#1", text="Budget Name")
		self.BudgetInfoTreeview.column('Budget Item ID', width=20)
		self.BudgetInfoTreeview.heading("#2", text="Budget Item ID")
		self.BudgetInfoTreeview.column('Logical Account', width=80)
		self.BudgetInfoTreeview.heading("#3", text="Logical Account")
		self.BudgetInfoTreeview.column('Budget Allocation Type', width=80)
		self.BudgetInfoTreeview.heading("#4", text="Budget Allocation Type")
		self.BudgetInfoTreeview.column('Budget Allocation Amount', width=80)
		self.BudgetInfoTreeview.heading("#5", text="Budget Allocation Amount")
		self.BudgetInfoTreeview.column('Budget Item Note', width=80)
		self.BudgetInfoTreeview.heading("#6", text="Budget Item Note")
		self.Budget_yscroll.config(command=self.BudgetInfoTreeview.yview)
		self.BudgetStatsLabel=tk.Label(self.EditBudgetFrame,
			text="Total Budget Allocation:      Unallocated Funds:           Percentage of Funds Unallocated:        Funds Allocated to the Remainder:")
		self.DeleteItemButtonTutorial=tk.Label(self.EditBudgetFrame,
			text="If you wish to delete a budget item, click on said budget item in the viewing table and press the Delete Budget Item button to remove the unvwanted budget item.")
		self.DeleteItemButton=tk.Button(self.EditBudgetFrame, text="Delete Budget Item", command=self.DeleteBudgetItem)
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
		self.AccountNoteEntry = tk.Entry(self.AddAccountFrame)
		self.ChooseAccountCategoryLabel = tk.Label(self.AddAccountFrame,text='Account Category')
		self.ChooseAccountCategoryDropbox = ttk.Combobox(self.AddAccountFrame,values=['Real','Logical'])
		self.CreateAccountButton=tk.Button(self.AddAccountFrame, text='Create Account', command=self.AddAccount)
		## add the create account frame widgets
		self.CreateAccountLabel.grid(row=0,column=0, columnspan=2,padx=10)
		self.NameAccountLabel.grid(row=1, column=0,padx=10)
		self.NameAccountEntry.grid(row=1, column=1,padx=10)
		self.IntialBalanceLabel.grid(row=2, column=0,padx=10)
		self.IntialBalanceEntry.grid(row=2, column=1, padx=10)
		self.AccountNoteLabel.grid(row=3, column=0, padx=10)
		self.AccountNoteEntry.grid(row=3, column=1, padx=10)
		self.ChooseAccountCategoryLabel.grid(row=4, column=0, padx=10)
		self.ChooseAccountCategoryDropbox.grid(row=4, column=1, padx=10)
		self.CreateAccountButton.grid(row=5, column=0, columnspan=2, ipadx=10)
		## Create Delete Account Frame Widgets
		self.DeleteAccountLabel=tk.Label(self.DeleteAccountFrame, text='Account Deletion')
		self.AccountToDeleteLabel=tk.Label(self.DeleteAccountFrame, text='Account to Delete')
		self.AccountToDeleteDropdown=ttk.Combobox(self.DeleteAccountFrame)
		self.DeleteAccountButton=tk.Button(self.DeleteAccountFrame, text='Delete Account', command=self.DeleteAccount)
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
		self.RenameAccountButton=tk.Button(self.RenameAccountFrame, text='Rename Account', command=self.RenameAccount)
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
		self.LogicalAccountLabel=tk.Label(self.HandleAccountFrame, text='Logical Account (If Expense)')
		self.LogicalAccountDropdown=ttk.Combobox(self.HandleAccountFrame)
		self.IncomeOrExpenseLabel=tk.Label(self.HandleAccountFrame, text='Income or Expense')
		self.IncomeOrExpenseDropdown=ttk.Combobox(self.HandleAccountFrame,values=['Income','Expense'])
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
		self.EnterTransactionButton = tk.Button(self.HandleAccountFrame, text='Enter Transaction', command=self.TransDataAndTransCommit)
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
		self.TransferDateLabel=tk.Label(self.TransferMoneyFrame,text='Transfer Date')
		self.TransferDateField=tk.Entry(self.TransferMoneyFrame)
		self.TransferDescriptionLabel=tk.Label(self.TransferMoneyFrame, text='Transfer Description')
		self.TransferDescriptionField=tk.Entry(self.TransferMoneyFrame)
		self.RecordTransferButton = tk.Button(self.TransferMoneyFrame, text='Record Transfer', command=self.TransferringMoney)
		## Pack Transfer money frame widgets
		self.MoneyTransferLabel.grid(row=0, column=0, columnspan=2)
		self.ExpendingAccountLabel.grid(row=1, column=0)
		self.ExpendingAccountDropdown.grid(row=1, column=1)
		self.RecipientAccountLabel.grid(row=2, column=0)
		self.RecipientAccountDropdown.grid(row=2, column=1)
		self.TransferAmountLabel.grid(row=3, column=0)
		self.TransferAmountField.grid(row=3, column=1)
		self.TransferDateLabel.grid(row=4, column=0)
		self.TransferDateField.grid(row=4, column=1)
		self.TransferDescriptionLabel.grid(row=5, column=0)
		self.TransferDescriptionField.grid(row=5, column=1)
		self.RecordTransferButton.grid(row=6, column=0, columnspan=2)
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
		# self.AccountsInfoTreeview.insert()
		## Populate treeview with data
		self.RepopulateAccountsTreeview()


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
		self.RepopulateTransactionsTreeview()
		# Change the style of the Treeviews
		style = ttk.Style()
		style.configure("Treeview.Heading", fieldbackground='#9613bb', )
		style.configure("Treeview", )
		style.configure("Treeview", foreground='yellow', background='#9613bb')

		self.RepopulateAccountDropboxes()

		# Start the mainloop
		tk.mainloop()
		
		
	# Additional Methods
	#Handles Typical transactions.Is called by Handle Account Frame Widgets.
	def TransDataAndTransCommit(self):
		try:
			# Get data for Transaction
			RealAccount=self.RealAccountDropdown.get()
			LogicalAccount=self.LogicalAccountDropdown.get()
			ExpenditureType=self.IncomeOrExpenseDropdown.get()
			ChosenBudget=self.BudgetDropdown.get()
			TransactionAmount=self.TransactionAmountField.get()
			Month=self.MonthofTransEntry.get()
			Day=self.DayofTransEntry.get()
			Year=self.YearofTransEntry.get()
			TransactionDate=Month+'-'+Day+'-'+Year
			TransactionDescription=self.TransactionTypeEntry.get()
			#If any of the entries are unpopulated or aren't within the proper date range, it sends an error message and the core code isn't executed
			if ExpenditureType=='' or TransactionAmount =='' or TransactionDescription == '' \
			or Month=='' or Year==''or Day=='' or int(Month) > 12 or int(Month)<1 or int(Day)<0 or int(Day)>31 or int(Year) < 2026  :
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			# The core code
			else:
				#Calls the Handle Account Function from the other module to interact with the database
				FinanceProjectDatabaseAccess.HandleAccount(RealAccount, LogicalAccount,ExpenditureType,ChosenBudget, TransactionAmount, TransactionDate,TransactionDescription)
				# Repopulate treeviews with data after the changes are made to represent them
				self.RepopulateAccountsTreeview()
				self.RepopulateTransactionsTreeview()
				self.RealAccountDropdown.delete(0,END)
				self.LogicalAccountDropdown.delete(0,END)
				self.IncomeOrExpenseDropdown.delete(0,END)
				self.BudgetDropdown.delete(0,END)
				self.TransactionAmountField.delete(0,END)
				self.MonthofTransEntry.delete(0,END)
				self.DayofTransEntry.delete(0,END)
				self.YearofTransEntry.delete(0,END)
				TransactionDescription=self.TransactionTypeEntry.delete(0,END)
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
			self.IntialBalance = float(self.IntialBalance)
			self.AccountDescription = self.AccountNoteEntry.get()
			self.AccountCategory = self.ChooseAccountCategoryDropbox.get()
			# If any of the entries are unpopulated, it sends an error message and the core code isn't executed
			if self.AccountName == '' or self.IntialBalance == '' or self.AccountCategory == '':
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			#The core code
			else:
				#Add Account Function is called from the other module to interact with the database
				FinanceProjectDatabaseAccess.AddAccount(self.IntialBalance, self.AccountName, self.AccountDescription, self.AccountCategory)
				# Repopulate treeviews with data
				self.RepopulateAccountsTreeview()
				self.RepopulateTransactionsTreeview()
				self.NameAccountEntry.delete(0,END)
				self.IntialBalanceEntry.delete(0,END)
				self.AccountNoteEntry.delete(0,END)
				self.ChooseAccountCategoryDropbox.delete(0,END)
				self.RepopulateAccountDropboxes()
		except:
			# Create an error message variable
			self.ErrorMessage ='Error! Follow the directions and please try again.'
			# Display the error message in an info dialog box.
			tk.messagebox.showinfo('Error!', self.ErrorMessage)
	
			
	#Deletes an account if called
	def DeleteAccount(self):
		try:
			self.AccountToDelete= self.AccountToDeleteDropdown.get()
			#Calls Delete account function from the other module to interact with the database
			FinanceProjectDatabaseAccess.DeleteAccount(self.AccountToDelete)
			# Repopulate treeviews with data
			self.RepopulateAccountsTreeview()
			self.RepopulateTransactionsTreeview()
			self.RepopulateAccountDropboxes()
			self.AccountToDeleteDropdown.delete(0,END)
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
			ExpendingAccount=self.ExpendingAccountDropdown.get()
			RecipientAccount=self.RecipientAccountDropdown.get()
			TransferAmount=self.TransferAmountField.get()
			TransferDescription=self.TransferDescriptionField.get()
			TransferDate=self.TransferDateField.get()
			#if any of the values are empty then an error message will pop up and the core code will not execute
			if ExpendingAccount == '' or RecipientAccount == '' or TransferAmount==TransferAmount.isalpha()\
			or TransferAmount=='' or TransferDescription=='' or TransferDate=='':
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			else:
				#Calls Account transfer function which will handle the database interactions for transferring money
				FinanceProjectDatabaseAccess.AccountTransfer(ExpendingAccount, RecipientAccount,TransferAmount,TransferDescription,TransferDate)
				# Repopulate treeviews with data
				self.RepopulateAccountsTreeview()
				self.RepopulateTransactionsTreeview()
				#clear amount transferred entry
				ExpendingAccount=self.ExpendingAccountDropdown.delete(0, END)
				RecipientAccount=self.RecipientAccountDropdown.delete(0, END)
				TransferAmount=self.TransferAmountField.delete(0, END)
				TransferDescription=self.TransferDescriptionField.delete(0, END)
				TransferDate=self.TransferDateField.delete(0, END)
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
		RealAccounts=self.AccountsInfoTreeview.insert("",-1,values=("Real Accounts","","","","",""))
		LogicalAccounts=self.AccountsInfoTreeview.insert("",-1,values=("Logical Accounts","","","","",""))
		#obtain data for accounts with transactions recorded and add the data to the treeview
		RealAccountsList, LogicalAccountsList = FinanceProjectDatabaseAccess.AccountOverviewData()
		for row in RealAccountsList:
			self.AccountsInfoTreeview.insert(RealAccounts, -1, values=row)
		for row in LogicalAccountsList:
			self.AccountsInfoTreeview.insert(LogicalAccounts, -1, values=row)
			
			
	#Repopulate the transaction treeview with data
	def RepopulateTransactionsTreeview(self):
		#get the transaction history for all the accounts
		TransactionAccountHistory = FinanceProjectDatabaseAccess.AccountTransactionHistory(self.StartAccountHistory)
		#clear the transaction treeview
		for item in self.TransHisTransactionInfo.get_children():	
			self.TransHisTransactionInfo.delete(item)
		#Insert new transaction treeview data into the transaction treeview
		for row in TransactionAccountHistory:
			TransactionType,TransactionDate,TransactionAmount,\
			RealAccountName, RealPreviousBalance, RealCurrentBalance,\
			LogicalAccountName, LogicalPreviousBalance, LogicalCurrentBalance=row
			TransactionRow=self.TransHisTransactionInfo.insert("", tk.END, values=(TransactionType,TransactionDate,TransactionAmount,"","","",""))
			self.TransHisTransactionInfo.insert(TransactionRow, tk.END, values=("","","","Real",RealAccountName,RealPreviousBalance,RealCurrentBalance))
			self.TransHisTransactionInfo.insert(TransactionRow, tk.END, values=("","","","Logical",LogicalAccountName,LogicalPreviousBalance,LogicalCurrentBalance))


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
		# try:
			#get the new name for the account and find the name of the account you wish to change
			self.NewName = self.NewAccountNameField.get()
			self.ToBeRenamedAccount = self.AccountToRenameDropdown.get()
			self.NewDescription = self.RevisedAccountDescriptionField.get()
			if self.NewName == '' or self.ToBeRenamedAccount == '':
				# Create an error message variable
				self.ErrorMessage = 'Error! Follow the directions and please try again.'
				# Display the error message in an info dialog box.
				tk.messagebox.showinfo('Error!', self.ErrorMessage)
			else:
				FinanceProjectDatabaseAccess.RenamingAccount(self.ToBeRenamedAccount,self.NewName,
				self.NewDescription)
				self.RepopulateAccountsTreeview()
				self.NewAccountNameField.delete(0, END)
				self.AccountToRenameDropdown.delete(0, END)
				self.RevisedAccountDescriptionField.delete(0, END)
				self.RepopulateAccountDropboxes()
		# except:
		# 	# Create an error message variable
		# 	self.ErrorMessage = 'Error! Follow the directions and please try again.'
		# 	# Display the error message in an info dialog box.
		# 	tk.messagebox.showinfo('Error!', self.ErrorMessage)


	def ShowBudgetingWidgets(self):
		self.TopFrame.grid_remove()
		self.TopMidFrame.grid_remove()
		self.TrueMiddleFrame.grid_remove()
		self.BudgetingFrame.grid(row=0,column=1)
		self.RepopulateBudgetDropboxes()
		RealAccountsList, LogicalAccountsList = FinanceProjectDatabaseAccess.AccountOverviewData()
		LogicalAccountNames=[]
		for row in LogicalAccountsList:
			row=str(row)
			row=row.rstrip(")")
			row=row.lstrip("(")
			row=row.split(",")
			Name=row[0]
			Name=Name.strip("'")
			LogicalAccountNames.append(Name)
		self.EditBudgetLogicalDropdown['values']=LogicalAccountNames
		TypesToAdd=[]
		for typetoadd in BudgetAllocationTypes:
			TypesToAdd.append(typetoadd.value)
		self.BudgetAllocationTypeDropdown['values']=TypesToAdd
	

	def ShowAccountManagementWidgets(self):
		self.BudgetingFrame.grid_remove()
		self.TopFrame.grid(row=0, column=1)
		self.TopMidFrame.grid(row=1, column=1)
		self.TrueMiddleFrame.grid(row=2, column=1)
		self.RepopulateAccountDropboxes()
		self.RepopulateBudgetDropboxes()


	def RepopulateAccountDropboxes(self):
		RealAccountsList, LogicalAccountsList = FinanceProjectDatabaseAccess.AccountOverviewData()
		AccountDropboxList=[self.AccountToDeleteDropdown, self.AccountToRenameDropdown, 
		self.RealAccountDropdown, self.LogicalAccountDropdown, self.ExpendingAccountDropdown,
		self.RecipientAccountDropdown, self.AccountChoiceDropdown]
		Accounts=[]
		RealAccounts=[]
		LogicalAccounts=[]
		for row in LogicalAccountsList:
			AccountName, *OtherData = row
			Accounts.append(AccountName)
			LogicalAccounts.append(AccountName)
		for dropbox in AccountDropboxList:
			if dropbox == self.LogicalAccountDropdown:
				dropbox['values']=LogicalAccounts
				continue
			elif dropbox == self.RealAccountDropdown:
				continue
			dropbox['values']=Accounts
		for row in RealAccountsList:
			AccountName, *OtherData = row
			Accounts.append(AccountName)
			RealAccounts.append(AccountName)
		for dropbox in AccountDropboxList:
			if dropbox == self.RealAccountDropdown:
				dropbox['values']=RealAccounts
				continue
			elif dropbox == self.LogicalAccountDropdown:
				continue
			dropbox['values']=Accounts


	def CreateBudget(self):
		BudgetName=self.BudgetNameField.get()
		BudgetAmount=self.BudgetAmountField.get()
		BudgetDescription=self.BudgetDescriptionField.get()
		FinanceProjectDatabaseAccess.AddBudget(BudgetName,BudgetAmount,BudgetDescription)
		self.BudgetNameField.delete(0, END)
		self.BudgetDescriptionField.delete(0, END)
		self.BudgetAmountField.delete(0, END)
		self.RepopulateBudgetDropbox()


	def RepopulateBudgetDropboxes(self):
		BudgetNames=FinanceProjectDatabaseAccess.GetBudgets()
		NamesList=[]
		for name in BudgetNames:
			NamesList.append(name[0])
		self.BudgetEditingDropdown['values'] = NamesList
		self.BudgetDropdown['values'] = NamesList


	def ResetBudgetTree(self,event):
		selected_value = self.BudgetDropdownChoice.get()
		#get the budget items from the other module
		BudgetItems = FinanceProjectDatabaseAccess.GetBudgetItems(selected_value)
		# clear the data out and replace it with the requested data
		for item in self.BudgetInfoTreeview.get_children():
			self.BudgetInfoTreeview.delete(item)
		for row in BudgetItems:
			self.BudgetInfoTreeview.insert("", tk.END, values=row)
		self.ResetBudgetStats()


	def AddBudgetItem(self):
		try:
			BudgetName=self.BudgetEditingDropdown.get()
			LogicalAccountName=self.EditBudgetLogicalDropdown.get()
			BudgetAllocationType=self.BudgetAllocationTypeDropdown.get()
			BudgetAllocationAmount=self.BudgetAllocationAmountField.get()
			BudgetItemNote=self.BudgetItemNoteField.get()
			FinanceProjectDatabaseAccess.AddBudgetItem(BudgetName, LogicalAccountName, BudgetAllocationType, BudgetAllocationAmount, BudgetItemNote)
			self.ResetBudgetTree("event")
			self.EditBudgetLogicalDropdown.delete(0, END)
			self.BudgetAllocationTypeDropdown.delete(0, END)
			self.BudgetAllocationAmountField.delete(0, END)
			self.BudgetItemNoteField.delete(0, END)
			self.ResetBudgetStats()
		except:
					#Create an error message variable
					self.ErrorMessage ='Error! Follow the directions and please try again.'
					#Display the error message in an info dialog box.
					tk.messagebox.showinfo('Error!', self.ErrorMessage)


	def ResetBudgetStats(self):
		# Get the current budget in use from the dropdown
		# for choosing a budget.
		BudgetName=self.BudgetEditingDropdown.get()
		# Get a list from the database module that contains all the
		# data for a row in the Budget table.
		BudgetStats=FinanceProjectDatabaseAccess.GetBudgetInfo(BudgetName)
		BudgetAmount=BudgetStats[0]
		BudgetAmount=float(BudgetAmount[3])
		BudgetItems=FinanceProjectDatabaseAccess.GetBudgetItems(BudgetName)
		AllocatedFunds=float()
		FundsInRemainder=float()
		RemainderItems=[]
		for row in BudgetItems:
			AllocationType=row[3]
			if AllocationType==BudgetAllocationTypes.PERCENTAGE:
				AllocatedFunds+=(float(row[4])/100*BudgetAmount)
			elif AllocationType==BudgetAllocationTypes.REMAINDER:
				RemainderItems.append(row)
			elif AllocationType==BudgetAllocationTypes.FIXED:
				AllocatedFunds+=float(row[4])
		if RemainderItems:
			FundsInRemainder+=BudgetAmount-AllocatedFunds
		if BudgetAmount > 0:
			self.BudgetStatsLabel['text']=f"Total Budget Allocation:${round(BudgetAmount,2)}      Unallocated Funds:${round(BudgetAmount-AllocatedFunds-FundsInRemainder, 2)}           Percentage of Funds Unallocated:{round(((BudgetAmount-AllocatedFunds-FundsInRemainder)/BudgetAmount)*100, 2)}%        Funds Allocated to the Remainder:${round(FundsInRemainder, 2)}/{len(RemainderItems)}"
		else:
			messagebox.showerror("Divison by Zero!", "Can't show the stats of a budget with no allocated funds!")


	def DeleteBudgetItem(self):
		FocusedRow=self.BudgetInfoTreeview.focus()
		FocusedRow=self.BudgetInfoTreeview.item(FocusedRow, 'values')
		BudgetItemID=str()
		count=0
		for item in FocusedRow:
			BudgetItemID=str(item)
			if count==1:
				break
			count+=1
		BudgetItemID=int(BudgetItemID)
		FinanceProjectDatabaseAccess.DeleteBudgetItem(BudgetItemID)
		self.ResetBudgetTree("event")
		self.ResetBudgetStats()


# Call the Finance GUI Class
if __name__ == '__main__':
	FinanceGUI()