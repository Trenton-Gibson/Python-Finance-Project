#Created: 04/24/23
#Trenton Gibson
#FinanceProjectDatabaseAccess.py

# import sqlite resources
import sqlite3 as lite
import os.path
from FinanceProjectGUI_V3 import BudgetAllocationTypes
from FinanceProjectGUI_V3 import BudgetExpenditureTypes
from FinanceProjectGUI_V3 import AccountTypes
#Specify the specific filepath of the database so it can be used in the python interpreter
# and establish a connection with the finances database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_PATH= os.path.join(BASE_DIR, "PythonFinances.db")
with lite.connect(DIR_PATH) as conn:

	# Gets accountIDs with Transactions and
	# returns the info on the latest transaction for that account
	def AccountOverviewData():
		#connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		# create a rows list and add rows tuple
		# rows list holds data for the lastest transaction in an account,
		# RowGroup contains the data for a specific type of account either
		# real or logical, AddRows tuple receives the data from the SQL queries acquiring 
		# data on the most recent transaction for an account.
		rows=[]
		RowGroup=[]
		AddRows=()
		# The following for loop get account overview data for the 
		# account types in the list right below.
		AccountTypes=['Real','Logical']
		for AccountType in AccountTypes:
			RowGroup=[]
			#Gets a list of all the account IDs in integer form
			AccountIDs = AccountOverviewTreeviewDataFiltering(AccountType)
			if AccountIDs=='':
				return
			#loop acquires all data for accounts with transactionIDs
			for row in AccountIDs:
				#gets a list of all the transactionIDs in integer form
				TransIDList = TransIDProcessing(AccountType, row)
				#if an account doesn't have transactions recorded for it TransIDList will equal 'e'
				# and thus won't get access to the core code
				if 'e' not in TransIDList:
					#we get the highest transactionID because it will be the most recent.
					#turn into a string so it can be processed
					#get all the info for the account and its most recent transaction
					#and put it in the rows list to populate the account treeview
					MaxTransID = max(TransIDList)
					MaxTransID=int(MaxTransID)
					AddRows= WithTransIDAccountInfo(AccountType,MaxTransID)
					for row in AddRows:
						RowGroup.insert(1,row)
			if AccountType=='Real':
				cur.execute('''SELECT Real_Account_Type,Real_Account_Note,Real_Account_Balance FROM Real_Account
				WHERE RealAccountID NOT IN (SELECT RealAccountID FROM 'Transaction')''')
			elif AccountType=='Logical':
				cur.execute('''SELECT Logical_Account_Type,Logical_Account_Note,Logical_Account_Balance FROM Logical_Account
				WHERE LogicalAccountID NOT IN (SELECT LogicalAccountID FROM 'Transaction')''')
			AddRows=cur.fetchall()
			RowGroup+=AddRows
			rows.insert(1,RowGroup)
		#close the database and return our data
		conn.close()
		return rows
	
		
	#transforms all the accountsID from tuple into usable integer form
	def AccountOverviewTreeviewDataFiltering(AccountType):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#get all the accountIds from the database
		if AccountType=='Real':
			cur.execute('''SELECT RealAccountID FROM Real_Account''')
		elif AccountType=='Logical':
			cur.execute('''SELECT LogicalAccountID FROM Logical_Account''')
		else:
			return ''
		rows = list(cur.fetchall())
		# make an empty list to put all the transformed account Ids in
		AccIDList = []
		#turns each tuple value and into an integer and puts it in the AccIDList
		for row in rows:
			AccIDString = str(row)
			AccIDString = AccIDString.lstrip('(')
			AccIDString = AccIDString.rstrip(')')
			AccIDString = AccIDString.rstrip(',')
			AccIDInt = int(AccIDString)
			AccIDList.insert(1, AccIDInt)
		#sends out the list of account IDs
		return AccIDList
	
	
	#Gets a list of transactionIDs in integer form, instead of tuple,
	# so we can determine the most recent transaction ID for an account(the highest integer)
	def TransIDProcessing(AccountType,AccountID):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#get all the transactionIDs for a specific account
		if AccountType=='Real':
			cur.execute("SELECT TransactionID FROM 'Transaction' WHERE RealAccountID=?", (AccountID,))
		elif AccountType=='Logical':
			cur.execute("SELECT TransactionID FROM 'Transaction' WHERE LogicalAccountID=?", (AccountID,))
		TransID = cur.fetchall()
		#create a list that will be filled with TransactionIDs
		#that have been transformed from tuple into integer
		TransIDList = []
		#if there isn't anything in the list it can't access the core code
		if len(TransID)>0:
			#turns each TransactionID into integer form and inserts it into list
			for row in TransID:
				TransIDString = str(row)
				TransIDString = TransIDString.lstrip('(')
				TransIDString = TransIDString.rstrip(')')
				TransIDString = TransIDString.rstrip(',')
				TransIDInt=int(TransIDString)
				TransIDList.insert(1, TransIDInt)
		#close the database
		conn.close()
		#If there's no data in the list it will equal 'e'
		if not TransIDList:
			TransIDList='e'
		#if the list has data in it return the list and closes the database
		if TransIDList:
			return TransIDList
		
			
	#gets the account info for accounts with transaction records
	def WithTransIDAccountInfo(AccountType, MaxTransID):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur=conn.cursor()
		rows=''
		#get all the data from the database for accounts with transactions
		if AccountType==AccountTypes.REAL:
			cur.execute('''SELECT Real_Account.Real_Account_Type,Real_Account.Real_Account_Note,Real_Account.Real_Account_Balance,'Transaction'.Transaction_Type
			,'Transaction'.Money_Transferred,'Transaction'.Date_Of_Transaction
			FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID
			WHERE TransactionID=?''',(MaxTransID,))
			rows = cur.fetchall()
		elif AccountType==AccountTypes.LOGICAL:
			cur.execute('''SELECT Logical_Account.Logical_Account_Type,Logical_Account.Logical_Account_Note,Logical_Account.Logical_Account_Balance,'Transaction'.Transaction_Type
			,'Transaction'.Money_Transferred,'Transaction'.Date_Of_Transaction
			FROM Logical_Account INNER JOIN 'Transaction' ON Logical_Account.LogicalAccountID= 'Transaction'.LogicalAccountID
			WHERE TransactionID=?''',(MaxTransID,))
			rows = cur.fetchall()
		#close the database and return rows
		conn.close()
		return rows	
	

	#Inserts transaction record for a specific account
	def HandleAccount(RealAccount,LogicalAccount,ExpenditureType,ChosenBudget,TransactionAmount,TransactionDate,TransactionDescription):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		# if the transaction amount isn't empty and meets the required
		# criteria for the expenditure type, convert the transaction into
		# float and round it to two decimals. If the criteria isn't met,
		# trigger an exception by dividing by zero.
		if len(TransactionAmount)>0:
			TransactionAmount=float(TransactionAmount)
			TransactionAmount = round(TransactionAmount, 2)
			TransactionAmount = abs(TransactionAmount)
			if ExpenditureType == BudgetExpenditureTypes.INCOME:
				BudgetAmount=float(GetBudgetInfo(ChosenBudget)[0][3])
				# If the expenditure type is income and there is no
				# chosen budget, then trigger an exception by dividing
				# zero.
				if ChosenBudget=='' or RealAccount=='' or BudgetAmount>TransactionAmount:
					TriggerException=1/0
				pass
			elif ExpenditureType == BudgetExpenditureTypes.EXPENSE:
				# If the expenditure type is expense and there is no
				# logical or real account, then trigger an exception by dividing
				# zero.
				if RealAccount=='' or LogicalAccount=='':
					TriggerException=1/0
				TransactionAmount*=-1
			else:
				TriggerException=1/0
		if ExpenditureType == BudgetExpenditureTypes.INCOME:
			RealAccountID,RealAccountCurrentBalance=GetAccountIDAndBalance(RealAccount,"Real")
			RealAccountNewBalance=RealAccountCurrentBalance+TransactionAmount
			RealAccountNewBalance=round(RealAccountNewBalance, 2)
			# add the new balance for the real account
			cur.execute('''UPDATE Real_Account SET Real_Account_Balance=? WHERE RealAccountID=? ''',(RealAccountNewBalance,RealAccountID))
			#commit the data
			conn.commit()
			BudgetItems=GetBudgetItems(ChosenBudget)
			RemainderItemCount=0
			for item in BudgetItems:
				BudgetAllocationType=item[3]
				if BudgetAllocationType==BudgetAllocationTypes.REMAINDER:
					RemainderItemCount+=1
			TotalAmountAllocated=0	
			for item in BudgetItems:
				LogicalAccountName=item[2]
				LogicalAccountID,LogicalAccountCurrentBalance=GetAccountIDAndBalance(LogicalAccountName,"Logical")
				BudgetAllocationType=item[3]
				BudgetAllocationAmount=float(item[4])
				if BudgetAllocationType==BudgetAllocationTypes.FIXED:
					TotalAmountAllocated+=BudgetAllocationAmount
					TotalAmountAllocated=round(TotalAmountAllocated,2)
					LogicalAccountNewBalance=LogicalAccountCurrentBalance+BudgetAllocationAmount
					LogicalAccountNewBalance=round(LogicalAccountNewBalance,2)
				elif BudgetAllocationType==BudgetAllocationTypes.PERCENTAGE:
					TotalAmountAllocated+=(float(BudgetAllocationAmount)/100*TransactionAmount)
					LogicalAccountNewBalance=LogicalAccountCurrentBalance+(float(BudgetAllocationAmount)/100*TransactionAmount)
					LogicalAccountNewBalance=round(LogicalAccountNewBalance,2)
				elif BudgetAllocationType==BudgetAllocationTypes.REMAINDER:
					LogicalAccountNewBalance=LogicalAccountCurrentBalance+(abs(TransactionAmount-TotalAmountAllocated)/RemainderItemCount)
					LogicalAccountNewBalance=round(LogicalAccountNewBalance,2)
				#Add transaction info into database
				cur.execute('''INSERT INTO 'Transaction'(RealAccountID,LogicalAccountID,Date_Of_Transaction,Money_Transferred,
				Real_Account_Previous_Balance, Real_Account_New_Balance,Logical_Account_Previous_Balance,Logical_Account_New_Balance,
				Transaction_Type) VALUES(?,?,?,?,?,?,?,?,?)''' ,(RealAccountID,LogicalAccountID,TransactionDate,BudgetAllocationAmount,
				RealAccountCurrentBalance,RealAccountNewBalance, LogicalAccountCurrentBalance,LogicalAccountNewBalance,TransactionDescription))
				#commit the data
				conn.commit()
				#add the new balances for the accounts
				cur.execute('''UPDATE Logical_Account SET Logical_Account_Balance=? WHERE LogicalAccountID=? ''',(LogicalAccountNewBalance,LogicalAccountID))
				#commit the data
				conn.commit()
		elif ExpenditureType == BudgetExpenditureTypes.EXPENSE:
			RealAccountID,RealAccountCurrentBalance=GetAccountIDAndBalance(RealAccount,"Real")
			LogicalAccountID,LogicalAccountCurrentBalance=GetAccountIDAndBalance(LogicalAccount,"Logical")
			RealAccountNewBalance=RealAccountCurrentBalance+TransactionAmount
			RealAccountNewBalance=round(RealAccountNewBalance, 2)
			LogicalAccountNewBalance=LogicalAccountCurrentBalance+TransactionAmount
			LogicalAccountNewBalance=round(LogicalAccountNewBalance,2)
			# Trigger an exception if the new balance would be negative
			if RealAccountNewBalance<0 or LogicalAccountNewBalance<0:
				TriggerException=1/0
			#Add transaction info into database
			cur.execute('''INSERT INTO 'Transaction'(RealAccountID,LogicalAccountID,Date_Of_Transaction,Money_Transferred,
			Real_Account_Previous_Balance, Real_Account_New_Balance,Logical_Account_Previous_Balance,Logical_Account_New_Balance,
			Transaction_Type) VALUES(?,?,?,?,?,?,?,?,?)''' ,(RealAccountID,LogicalAccountID,TransactionDate,TransactionAmount,
			RealAccountCurrentBalance,RealAccountNewBalance, LogicalAccountCurrentBalance,LogicalAccountNewBalance,TransactionDescription))
			#commit the data
			conn.commit()
			#add the new balances for the accounts
			cur.execute('''UPDATE Real_Account SET Real_Account_Balance=? WHERE RealAccountID=? ''',(RealAccountNewBalance,RealAccountID))
			cur.execute('''UPDATE Logical_Account SET Logical_Account_Balance=? WHERE LogicalAccountID=? ''',(LogicalAccountNewBalance,LogicalAccountID))
			#commit the data
			conn.commit()
		#close the database
		conn.close()
		
		
	#add account into database
	def AddAccount(Balance,AccountName,AccountNote,AccountType):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#insert the new account data into the appropriate table
		if AccountType=='Real':
			cur.execute('''INSERT INTO Real_Account (Real_Account_Balance,Real_Account_Type,Real_Account_Note)VALUES(?,?,?)''',(Balance,AccountName,AccountNote))
		elif AccountType=='Logical':
			cur.execute('''INSERT INTO Logical_Account (Logical_Account_Balance,Logical_Account_Type,Logical_Account_Note)VALUES(?,?,?)''',(Balance,AccountName,AccountNote))
		#commit the data, and close the database
		conn.commit()
		conn.close()


	#Deletes selected account
	def DeleteAccount(ToBeDeletedAccount):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		RealAccountsList, LogicalAccountsList = AccountOverviewData()
		for row in RealAccountsList:
			AccountName, *OtherData = row
			if AccountName==ToBeDeletedAccount:
				cur.execute('''DELETE FROM Real_Account WHERE Real_Account_Type=?''',(ToBeDeletedAccount,))
				break
		for row in LogicalAccountsList:
			AccountName, *OtherData = row
			if AccountName==ToBeDeletedAccount:
				cur.execute('''DELETE FROM Logical_Account WHERE Logical_Account_Type=?''',(ToBeDeletedAccount,))
				break
		#delete specified account from the database,commit the deletion, close the database
		conn.commit()
		conn.close()
	
	
	#retrieves account transaction history for all tables or a specific table depending
	def AccountTransactionHistory(AccountHistory):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		AccountTransactionHistory=[]
		# get the transaction history of all accounts if the argument some version of 'All'
		if AccountHistory == '':
			cur.execute('''SELECT 'Transaction'.Transaction_Type,'Transaction'.Date_Of_Transaction,'Transaction'.Money_Transferred,
			Real_Account.Real_Account_Type,'Transaction'.Real_Account_Previous_Balance,'Transaction'.Real_Account_New_Balance,
			Logical_Account.Logical_Account_Type,'Transaction'.Logical_Account_Previous_Balance,'Transaction'.Logical_Account_New_Balance
			FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID INNER JOIN Logical_Account
			ON Logical_Account.LogicalAccountID = 'Transaction'.LogicalAccountID''')
			AccountTransactionHistory=cur.fetchall()
		#get transaction history of account specified by argument
		else:
			AccountHistory=AccountHistory.split(",")
			RealAccounts=[]
			LogicalAccounts=[]
			for account in AccountHistory:
				cur.execute("SELECT Real_Account_Type FROM Real_Account WHERE Real_Account_Type=?",(account,))
				test=cur.fetchall()
				if test:
					RealAccounts.append(account)
				else:
					LogicalAccounts.append(account)
			if RealAccounts:
				for account in RealAccounts:
					cur.execute('''SELECT 'Transaction'.Transaction_Type,'Transaction'.Date_Of_Transaction,'Transaction'.Money_Transferred,
					Real_Account.Real_Account_Type,'Transaction'.Real_Account_Previous_Balance,'Transaction'.Real_Account_New_Balance,
					Logical_Account.Logical_Account_Type,'Transaction'.Logical_Account_Previous_Balance,'Transaction'.Logical_Account_New_Balance
					FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID INNER JOIN Logical_Account
					ON Logical_Account.LogicalAccountID = 'Transaction'.LogicalAccountID WHERE Real_Account_Type=?''', (account,))
					Transactions=cur.fetchall()
					for transaction in Transactions:
						AccountTransactionHistory.append(transaction)
			if LogicalAccounts:
				for account in LogicalAccounts:
					cur.execute('''SELECT 'Transaction'.Transaction_Type,'Transaction'.Date_Of_Transaction,'Transaction'.Money_Transferred,
					Real_Account.Real_Account_Type,'Transaction'.Real_Account_Previous_Balance,'Transaction'.Real_Account_New_Balance,
					Logical_Account.Logical_Account_Type,'Transaction'.Logical_Account_Previous_Balance,'Transaction'.Logical_Account_New_Balance
					FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID INNER JOIN Logical_Account
					ON Logical_Account.LogicalAccountID = 'Transaction'.LogicalAccountID WHERE Logical_Account_Type=?''', (account,))
					Transactions=cur.fetchall()
					for transaction in Transactions:
						AccountTransactionHistory.append(transaction)

		# close the database, return the account transaction history
		conn.close()
		return AccountTransactionHistory
	
	
	#Handles all the database transactions for transferring money between accounts
	def AccountTransfer(ExpendingAccount, RecipientAccount,TransferAmount,TransferDescription,TransferDate):
		if ExpendingAccount==RecipientAccount:
			TriggerException=1/0
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#transform the amount transferred parameter into float data that is rounded
		TransferAmount=float(TransferAmount)
		TransferAmount = round(TransferAmount, 2)
		#Check to make sure both accounts are logical or real and not mixed
		ExpendingAccountID=int()
		RecipientAccountID=int()
		TupleTest=''
		RealAccountIDs=[]
		cur.execute('''SELECT RealAccountID FROM Real_Account WHERE Real_Account_Type=?''',(ExpendingAccount,))
		TupleTest=cur.fetchall()
		if TupleTest:
			RealAccountIDs.append(TupleTest[0])
		cur.execute('''SELECT RealAccountID FROM Real_Account WHERE Real_Account_Type=?''',(RecipientAccount,))
		TupleTest=cur.fetchall()
		if TupleTest:
			RealAccountIDs.append(TupleTest[0])
		RealAccountCount=0
		for item in RealAccountIDs:
			RealAccountCount+=1
		LogicalAccountIDs=[]
		cur.execute('''SELECT LogicalAccountID FROM Logical_Account WHERE Logical_Account_Type=?''',(ExpendingAccount,))
		TupleTest=cur.fetchall()
		if TupleTest:
			LogicalAccountIDs.append(TupleTest[0])
		cur.execute('''SELECT LogicalAccountID FROM Logical_Account WHERE Logical_Account_Type=?''',(RecipientAccount,))
		TupleTest=cur.fetchall()
		if TupleTest:
			LogicalAccountIDs.append(TupleTest[0])
		LogicalAccountCount=0
		for item in LogicalAccountIDs:
			LogicalAccountCount+=1
		LogicalAccountID1=int()
		LogicalAccountID2=int()
		RealAccountID1=int()
		RealAccountID2=int()
		RealAccountCurrentBalance1=0
		RealAccountNewBalance1=0
		RealAccountCurrentBalance2=0
		RealAccountNewBalance2=0
		LogicalAccountCurrentBalance1=0
		LogicalAccountNewBalance1=0
		LogicalAccountCurrentBalance2=0
		LogicalAccountNewBalance2=0
		if RealAccountCount==2:
			# get all account ids and account balances for all the proceeding SQL for this function
			ExpendingAccountID,ExpendingAccountCurrentBalance=GetAccountIDAndBalance(ExpendingAccount,"Real")
			RecipientAccountID,RecipientAccountCurrentBalance=GetAccountIDAndBalance(RecipientAccount,"Real")
			cur.execute('SELECT LogicalAccountID, Logical_Account_Balance FROM Logical_Account WHERE LogicalAccountID>=0')
			LogicalAccountInfo=cur.fetchall()
			LogicalAccountID1,LogicalAccountCurrentBalance1=LogicalAccountInfo[0]
			LogicalAccountID2,LogicalAccountCurrentBalance2=LogicalAccountInfo[0]
			RealAccountID1=ExpendingAccountID
			RealAccountID2=RecipientAccountID
			# update balances for real accounts
			ExpendingAccountNewBalance=ExpendingAccountCurrentBalance-TransferAmount
			ExpendingAccountNewBalance=round(ExpendingAccountNewBalance, 2)
			RecipientAccountNewBalance=RecipientAccountCurrentBalance+TransferAmount
			RecipientAccountNewBalance=round(RecipientAccountNewBalance,2)
			# Trigger an exception if the new balances would be negative
			if ExpendingAccountNewBalance<0 or RecipientAccountNewBalance<0:
				TriggerException=1/0
			# set values for real account balances
			RealAccountCurrentBalance1=ExpendingAccountCurrentBalance
			RealAccountNewBalance1=ExpendingAccountNewBalance
			RealAccountCurrentBalance2=RecipientAccountCurrentBalance
			RealAccountNewBalance2=RecipientAccountNewBalance
			#add the new balances for the accounts
			cur.execute('''UPDATE Real_Account SET Real_Account_Balance=? WHERE RealAccountID=? ''',(ExpendingAccountNewBalance,ExpendingAccountID))
			cur.execute('''UPDATE Real_Account SET Real_Account_Balance=? WHERE RealAccountID=? ''',(RecipientAccountNewBalance,RecipientAccountID))
			#commit the data
			conn.commit()
		elif LogicalAccountCount==2:
			# get all account ids and account balances for all the proceeding SQL for this function
			ExpendingAccountID,ExpendingAccountCurrentBalance=GetAccountIDAndBalance(ExpendingAccount,"Logical")
			RecipientAccountID,RecipientAccountCurrentBalance=GetAccountIDAndBalance(RecipientAccount,"Logical")
			cur.execute('SELECT RealAccountID, Real_Account_Balance FROM Real_Account WHERE RealAccountID>=0')
			RealAccountInfo=cur.fetchall()
			LogicalAccountID1=ExpendingAccountID
			LogicalAccountID2=ExpendingAccountID
			RealAccountID1,RealAccountCurrentBalance1=RealAccountInfo[0]
			RealAccountID2,RealAccountCurrentBalance2=RealAccountInfo[0]
			# update balances for logical accounts
			ExpendingAccountNewBalance=ExpendingAccountCurrentBalance-TransferAmount
			ExpendingAccountNewBalance=round(ExpendingAccountNewBalance, 2)
			RecipientAccountNewBalance=RecipientAccountCurrentBalance+TransferAmount
			RecipientAccountNewBalance=round(RecipientAccountNewBalance,2)
			# Trigger an exception if the new balances would be negative
			if ExpendingAccountNewBalance<0 or RecipientAccountNewBalance<0:
				TriggerException=1/0
			# set values for real account balances
			LogicalAccountCurrentBalance1=ExpendingAccountCurrentBalance
			LogicalalAccountNewBalance1=ExpendingAccountNewBalance
			LogicalAccountCurrentBalance2=RecipientAccountCurrentBalance
			LogicalAccountNewBalance2=RecipientAccountNewBalance
			#add the new balances for the accounts
			cur.execute('''UPDATE Logical_Account SET Logical_Account_Balance=? WHERE LogicalAccountID=? ''',(ExpendingAccountNewBalance,ExpendingAccountID))
			cur.execute('''UPDATE Logical_Account SET Logical_Account_Balance=? WHERE LogicalAccountID=? ''',(RecipientAccountNewBalance,RecipientAccountID))
			#commit the data
			conn.commit()
		else:
			TriggerException=1/0
		#Add transaction info into database
		cur.execute('''INSERT INTO 'Transaction'(RealAccountID,LogicalAccountID,Date_Of_Transaction,Money_Transferred,
		Real_Account_Previous_Balance, Real_Account_New_Balance,Logical_Account_Previous_Balance,Logical_Account_New_Balance,
		Transaction_Type) VALUES(?,?,?,?,?,?,?,?,?)''' ,(RealAccountID1,LogicalAccountID1,TransferDate,-TransferAmount,
		RealAccountCurrentBalance1,RealAccountNewBalance1, LogicalAccountCurrentBalance1,LogicalAccountNewBalance1,TransferDescription))
		#commit the data
		conn.commit()
		#Add transaction info into database
		cur.execute('''INSERT INTO 'Transaction'(RealAccountID,LogicalAccountID,Date_Of_Transaction,Money_Transferred,
		Real_Account_Previous_Balance, Real_Account_New_Balance,Logical_Account_Previous_Balance,Logical_Account_New_Balance,
		Transaction_Type) VALUES(?,?,?,?,?,?,?,?,?)''' ,(RealAccountID2,LogicalAccountID2,TransferDate,TransferAmount,
		RealAccountCurrentBalance2,RealAccountNewBalance2, LogicalAccountCurrentBalance2,LogicalAccountNewBalance2,TransferDescription))
		#commit the data
		conn.commit()
		conn.close()
		
	#Handles the transformation of account names on the database side
	def RenamingAccount(ToBeChangedAccount,NewName,NewDescription):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		RealAccountsList, LogicalAccountsList = AccountOverviewData()
		for row in RealAccountsList:
			AccountName, *OtherData = row
			if AccountName==ToBeChangedAccount and NewDescription != '':
				cur.execute('''UPDATE Real_Account SET Real_Account_Type=?, Real_Account_Note=? WHERE Real_Account_Type=?'''
				,(NewName, NewDescription, ToBeChangedAccount))
				break
			elif AccountName==ToBeChangedAccount:
				cur.execute('''UPDATE Real_Account SET Real_Account_Type=? WHERE Real_Account_Type=?'''
				,(NewName, ToBeChangedAccount))
				break
		for row in LogicalAccountsList:
			AccountName, *OtherData = row
			if AccountName==ToBeChangedAccount and NewDescription != '':
				cur.execute('''UPDATE Logical_Account SET Logical_Account_Type=?, Logical_Account_Note=? WHERE Logical_Account_Type=?'''
				,(NewName, NewDescription, ToBeChangedAccount))
				break
			elif AccountName==ToBeChangedAccount:
				cur.execute('''UPDATE Logical_Account SET Logical_Account_Type=? WHERE Logical_Account_Type=?'''
				,(NewName, ToBeChangedAccount))
				break
		#update the account name for the selected account
		#commit the transaction and close the database
		conn.commit()
		conn.close


	def AddBudget(BudgetName, BudgetAmount, BudgetDescription):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#insert the new budget into the appropriate table
		cur.execute('''INSERT INTO Budget (Budget_Name,Budget_Amount, Budget_Note)VALUES(?,?,?)''',(BudgetName, BudgetAmount, BudgetDescription))
		#commit the data, and close the database
		conn.commit()
		conn.close()


	def GetBudgets():
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#Get the budget rows for specified budget
		cur.execute('''SELECT Budget_Name FROM Budget''')
		# Fetch the rows from the SELECT query
		rows = cur.fetchall()
		rows = TupleToString(rows)
		#close the database and return rows
		conn.close()
		return rows	
	

	def GetBudgetItems(BudgetName):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#Get the budget rows for specified budget
		cur.execute('''SELECT Budget.Budget_Name, Budget_Item.BudgetItemID, Logical_Account.Logical_Account_Type, Budget_Allocation.Budget_Allocation_Type, Budget_Allocation.Budget_Allocation_Amount,
		Budget_Item.Budget_Item_Note FROM Budget_Item INNER JOIN Logical_Account ON Budget_Item.LogicalAccountID = Logical_Account.LogicalAccountID
		INNER JOIN Budget_Allocation ON Budget_Item.BudgetAllocationID = Budget_Allocation.BudgetAllocationID
		INNER JOIN Budget ON Budget_Item.BudgetID = Budget.BudgetID  WHERE Budget.Budget_Name=? ORDER BY Budget_Allocation.Budget_Allocation_Type ASC''', (BudgetName,))
		# Fetch the rows from the SELECT query
		rows = cur.fetchall()
		rows=TupleToString(rows)
		#close the database and return rows
		conn.close()
		return rows	
	

	def AddBudgetItem(BudgetName, LogicalAccountName, BudgetAllocationType, BudgetAllocationAmount, BudgetRowNote):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		# Determine if there's remaining funds in the budget to prevent
		# the program crashing.
		BudgetStats=GetBudgetInfo(BudgetName)
		BudgetAmount=BudgetStats[0]
		BudgetAmount=float(BudgetAmount[3])
		BudgetItems=GetBudgetItems(BudgetName)
		BudgetItems.append(['','','',BudgetAllocationType,BudgetAllocationAmount])
		AllocatedFunds=float()
		FundsInRemainder=float()
		RemainderItems=[]
		if BudgetItems:
			for row in BudgetItems:
				AllocationType=row[3]
				if AllocationType==BudgetAllocationTypes.PERCENTAGE:
								AllocatedFunds+=round(((float(row[4])/100) * (BudgetAmount)),2)
				elif AllocationType==BudgetAllocationTypes.REMAINDER:
					RemainderItems.append(row)
				elif AllocationType==BudgetAllocationTypes.FIXED:
					AllocatedFunds+=round(float(row[4]), 2)
		if RemainderItems:
					FundsInRemainder+=BudgetAmount-AllocatedFunds
		AllocatedFunds=round(AllocatedFunds, 2)
		if RemainderItems and AllocatedFunds==BudgetAmount:
			TriggerException=1/0
		if AllocatedFunds>BudgetAmount:
			TriggerException=1/0

		if BudgetAllocationType == BudgetAllocationTypes.REMAINDER:
			BudgetAllocationAmount=0
		if (BudgetAllocationType == BudgetAllocationTypes.PERCENTAGE or BudgetAllocationType==BudgetAllocationTypes.FIXED) and BudgetAllocationAmount==0:
			ExceptionTrigger=1/0
		# Insert the new budget allocation entry into the Budget_Allocation table
		cur.execute('''INSERT INTO Budget_Allocation (Budget_Allocation_Type, Budget_Allocation_Amount)VALUES(?,?)'''
			,(BudgetAllocationType,BudgetAllocationAmount))
		conn.commit()
		#Get the ID for desired budget allocation based off the fact that its the most recent
		cur.execute('''SELECT MAX(BudgetAllocationID) FROM Budget_Allocation''')
		BudgetAllocationID=cur.fetchall()
		BudgetAllocationID=BudgetAllocationID[0]
		BudgetAllocationID=TupleToString(BudgetAllocationID)
		BudgetAllocationID=BudgetAllocationID[0]
		BudgetAllocationID=int(BudgetAllocationID[0])
		#Get the ID for the desired budget based off the budget name
		cur.execute('''SELECT BudgetID from Budget WHERE Budget_Name=?''', (BudgetName,))
		# this will retrieve the desired BudgetID whilst not returning any data from
		# the following query if .fetchall() is used again before closing the database
		# connection.
		BudgetID=cur.fetchall()
		BudgetID=BudgetID[0]
		BudgetID=TupleToString(BudgetID)
		BudgetID=BudgetID[0]
		BudgetID=int(BudgetID[0])
		#Get the ID for the desired budget based off the budget name
		cur.execute('''SELECT LogicalAccountID FROM Logical_Account WHERE Logical_Account_Type=?''', (LogicalAccountName,))
		LogicalAccountID=cur.fetchall()
		LogicalAccountID=LogicalAccountID[0]
		LogicalAccountID=TupleToString(LogicalAccountID)
		LogicalAccountID=LogicalAccountID[0]
		LogicalAccountID=int(LogicalAccountID[0])
		# Insert the new budget row into the Budget_Item table
		cur.execute('''INSERT INTO Budget_Item (BudgetID, LogicalAccountID, BudgetAllocationID,Budget_Item_Note)VALUES(?,?,?,?)''', 
			(BudgetID,LogicalAccountID,BudgetAllocationID,BudgetRowNote))
		conn.commit()
		#close the database and return rows
		conn.close()
	

	def TupleToString(strng):
		strng=str(strng)
		strng=strng.rstrip("]")
		strng=strng.lstrip("[")
		StrngList1=strng.split("(")
		StrngList2=[]
		for row in StrngList1:
			row=row.replace("'", "")
			row=row.replace(")", "")
			row=row.rstrip(" ")
			row=row.rstrip(",")
			row=row.split(",")
			count=0
			for item in row:
				row[count]=item.lstrip(" ")
				if row[count]=='':
					row.pop(count)

				count+=1
			StrngList2.append(row)
		StrngList2.pop(0)
		return StrngList2
	

	def GetBudgetInfo(BudgetName):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		cur.execute('''SELECT * FROM Budget WHERE Budget_Name=?''', (BudgetName,))
		# Fetch the rows from the SELECT query
		row = cur.fetchall()
		# Turn the budget info into a string and have each
		# data point be a separate string in a list
		row=TupleToString(row)
		#close the database and return rows
		conn.close()
		return row	
	

	def DeleteBudgetItem(BudgetItemID):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		cur.execute('''DELETE FROM Budget_Item WHERE BudgetItemID=?''',(BudgetItemID,))
		conn.commit()
		conn.close()


	def DeleteBudget(BudgetName):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		cur.execute('''DELETE FROM Budget WHERE Budget_Name=?''',(BudgetName,))
		conn.commit()
		conn.close()

	#get the account ID and account's current balance
	def GetAccountIDAndBalance(AccountName, AccountType):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		AccountID=""
		PreviousBalance=0.0
		# get ID and balance if account type is real
		if AccountType==AccountTypes.REAL:
			cur.execute('''SELECT RealAccountID FROM Real_Account WHERE Real_Account_Type=?''',(AccountName,))
			AccountID=cur.fetchall()
			AccountID=TupleToString(AccountID)
			AccountID=AccountID[0]
			AccountID=AccountID[0]		
			AccountID=int(AccountID)
			cur.execute('SELECT Real_Account_Balance FROM Real_Account WHERE RealAccountID = ?',(AccountID,))
			PreviousBalance =cur.fetchall()
		# get ID and balance if account type is real
		if AccountType==AccountTypes.LOGICAL:
			cur.execute('''SELECT LogicalAccountID FROM Logical_Account WHERE Logical_Account_Type=?''',(AccountName,))
			AccountID=cur.fetchall()
			AccountID=TupleToString(AccountID)
			AccountID=AccountID[0]
			AccountID=AccountID[0]
			AccountID=int(AccountID)
			cur.execute('SELECT Logical_Account_Balance FROM Logical_Account WHERE LogicalAccountID = ?',(AccountID,))
			PreviousBalance =cur.fetchall()
		#Turn previous balance from tuple to float
		PreviousBalance=TupleToString(PreviousBalance)
		PreviousBalance=PreviousBalance[0]
		PreviousBalance=PreviousBalance[0]
		PreviousBalance = float(PreviousBalance)
		PreviousBalance = round(PreviousBalance, 2)
		# close database connection
		conn.close()
		return AccountID, PreviousBalance	