#Created: 04/24/23
#Trenton Gibson
#FinanceProjectDatabaseAccess.py

# import sqlite resources
import sqlite3 as lite
import os.path
#Specify the specific filepath of the database so it can be used in the python interpreter
# and establish a connection with the finances database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_PATH= os.path.join(BASE_DIR, "PythonFinances.db")
with lite.connect(DIR_PATH) as conn:

	#Gets AccountIDs with Transactions and
	# returns the info on the latest transaction for that account
	def AccOverDataWithTransID():
		#connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#Gets a list of all the account IDs in integer form
		AccountIDs = AccountOverviewTreeviewDataFiltering()
		# create a rows list and add rows tuple
		#rows list holds data for the lastest transaction in that account
		#AddRows tuple receives the data from the queries acquiring data on the most recent transaction for an account
		rows=[]
		AddRows=()
		#loop acquires all data for accounts with transactionIDs
		for item in AccountIDs:
			#gets a list of all the transactionIDs in integer form
			TransIDList= TransIDProcessing(item)
			#if an account doesn't have transactions recorded for it TransIDList will equal 'e'
			# and thus won't get access to the core code
			if 'e' not in TransIDList:
				#we get the highest transactionID because it will be the most recent.
				#turn into a string so it can be processed
				#get all the info for the account and its most recent transaction
				#and put it in the rows list to populate the account treeview
				MaxTransID = max(TransIDList)
				MaxTransID=str(MaxTransID)
				AddRows= tuple(WithTransIDAccountInfo(MaxTransID))
				rows.insert(1,AddRows)
		#close the database and return our data
		conn.close()
		return rows
	
		
	#transforms the all the accountsID from tuple into usable integer form
	def AccountOverviewTreeviewDataFiltering():
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#get all the accountIds from the database
		cur.execute("SELECT RealAccountID FROM Real_Account")
		rows = list(cur.fetchall())
		# make an empty list to put all the transformed account Ids in
		AccIDList = []
		#turns each tuple value and into an integer and puts it in the AccIDList
		for item in rows:
			AccIDString = str(item)
			AccIDString = AccIDString.lstrip('(')
			AccIDString = AccIDString.rstrip(')')
			AccIDString = AccIDString.rstrip(',')
			AccIDInt = int(AccIDString)
			AccIDList.insert(1, AccIDInt)
		#sends out the list of account IDs
		return AccIDList
	
	
	#Gets a list of transactionIDs in integer form, instead of tuple,
	# so we can determine the most recent transaction ID for an account(the highest integer)
	def TransIDProcessing(AccountID):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#get all the transactionIDs for a specific account
		cur.execute("SELECT TransactionID FROM 'Transaction' WHERE RealAccountID=?", (AccountID,))
		TransID = cur.fetchall()
		#create a list that will be filled with TransactionIDs
		#that have been transformed from tuple into integer
		TransIDList = []
		#if there isn't anything in the list it can't access the core code
		if len(TransID)>0:
			#turns each TransactionID into integer form and inserts it into list
			for item in TransID:
				TransIDString = str(item)
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
	def WithTransIDAccountInfo(MaxTransID):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur=conn.cursor()
		#get all the data from the database for accounts with transactions
		cur.execute('''SELECT Real_Account.Real_Account_Type,Real_Account.Real_Account_Balance,'Transaction'.Transaction_Type
		,'Transaction'.Money_Transferred,'Transaction'.Date_Of_Transaction
		FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID
		WHERE TransactionID=?''',(MaxTransID,))
		rows = cur.fetchall()
		#turn the rows into a string
		for item in rows:
			String =item
			break
		rows=String
		#close the database and return rows
		conn.close()
		return rows
	
	
	#Get Accounts without Transactions
	def AccOverDataWithoutTransID():
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#get the data for accounts without transaction records
		cur.execute('''SELECT Real_Account_Type,Real_Account_Balance FROM Real_Account
		WHERE RealAccountID NOT IN (SELECT RealAccountID FROM 'Transaction') ''')
		rows=cur.fetchall()
		# close the database and return rows
		conn.close()
		return rows
	
	
	#Inserts transaction record for a specific account
	def HandleAccount(AccountInfo,TransactionDate,TransactionAmount,TransactionType):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#if the transaction amount isn't empty,
		#convert the transaction into float and round it to two decimals
		if len(TransactionAmount)>0:
			TransactionAmount=float(TransactionAmount)
			TransactionAmount = round(TransactionAmount, 2)
		#get the account number
		UntransformedAccountInfo = str(AccountInfo[0])
		AccountInfo=''
		for item in UntransformedAccountInfo:
			AccountInfo+=item
		cur.execute('''SELECT RealAccountID FROM Real_Account WHERE Real_Account_Type=?''',(AccountInfo,))
		AccountNum=cur.fetchall()
		for item in AccountNum:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			AccountNum = (String)
		#retrive the previous balance for the specific account
		cur.execute('SELECT Real_Account_Balance FROM Real_Account WHERE RealAccountID = ?',(AccountNum,))
		PreviousBalance =cur.fetchall()
		
		#turn previous balance tuple into string
		for item in PreviousBalance:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			PreviousBalance=(String)
		#turn previous balance into float and round it
		PreviousBalance = float(PreviousBalance)
		PreviousBalance = round(PreviousBalance, 2)
		# if the transaction amount isn't 0,
		#get the new balance and round it
		if TransactionAmount!=0:
			NewBalance=PreviousBalance+TransactionAmount
			NewBalance = round(NewBalance, 2)
		#select the highest transactionID
		cur.execute('SELECT max(TransactionID) FROM "Transaction"')
		TransID=cur.fetchall()
		#Convert the maximum transaction into int
		#and make the next transaction ID
		for item in TransID:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			if String == 'None':
				NewTransID=1
			else:
				NewTransID = float(String) + 1
		#Add transaction info into database
		cur.execute('''INSERT INTO 'Transaction'VALUES(?,?,?,?,?,?,?)'''
		,(NewTransID,AccountNum,TransactionDate,TransactionAmount,PreviousBalance,NewBalance,TransactionType))
		rows=cur.fetchall()
		#commit the data
		conn.commit()
		#add the new balance for the account
		cur.execute('''UPDATE Real_Account SET Balance=? WHERE RealAccountID=? ''',(NewBalance,AccountNum))
		rows = cur.fetchall()
		#commit the data and close the database
		conn.commit()
		conn.close()
		
		
	#add account into database
	def AddAccount(Balance,AccountType):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#insert the new account data, commit the data, and close the database
		cur.execute('''INSERT INTO Real_Account (Balance,Real_Account_Type)VALUES(?,?)''',(Balance,AccountType))
		conn.commit()
		conn.close()


	#Deletes selected account
	def DeleteAccount(ToBeDeletedAccount):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#delete specified account from the database,commit the deletion, close the database
		cur.execute('''DELETE FROM Real_Account WHERE Real_Account_Type=?''',(ToBeDeletedAccount,))
		conn.commit()
		conn.close()
	
	
	#retrieves account transaction history for all tables or a specific table depending
	def AccountTransactionHistory(AccountHistory):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		# get the transaction history of all accounts if the argument some version of 'All'
		if AccountHistory == '':
			cur.execute("SELECT Real_Account.Real_Account_Type,'Transaction'.Previous_Balance,'Transaction'.New_Balance,"
			"'Transaction'.Transaction_Type,'Transaction'.Money_Transferred,'Transaction'.Date_Of_Transaction "
			"FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID")
		#get transaction history of account specified by argument
		else:
			cur.execute("SELECT Real_Account.Real_Account_Type,'Transaction'.Previous_Balance,'Transaction'.New_Balance,"
			"'Transaction'.Transaction_Type,'Transaction'.Money_Transferred,'Transaction'.Date_Of_Transaction "
			"FROM Real_Account INNER JOIN 'Transaction' ON Real_Account.RealAccountID= 'Transaction'.RealAccountID WHERE Real_Account_Type=?",
			(AccountHistory,))
		# get data from executed SELECT statement,
		# close the database, return the account transaction history
		AccountTransactionHistory=cur.fetchall()
		conn.close()
		return AccountTransactionHistory
	
	
	#Handles all the database transactions for transferring money between accounts
	def AccountTransfer(AmountTransferred,GivingAccount,RecipientAccount):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#transform the amount transferred parameter into float data that is rounded
		AmountTransferred=float(AmountTransferred)
		AmountTransferred = round(AmountTransferred, 2)
		#obtains the highest transactionID and makes the next one
		cur.execute('SELECT max(TransactionID) FROM "Transaction"')
		TransID = cur.fetchall()
		for item in TransID:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			if TransID:
				NewTransID=int(String)+1
			else:
				NewTransID=1
		#get the account Id of the recipient account and transform it into integer data
		cur.execute('''SELECT RealAccountID FROM Real_Account WHERE Real_Account_Type=?''',(RecipientAccount,))
		AccountNum=cur.fetchall()
		for item in AccountNum:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			AccountNum=int(String)
			
		#get the balance for the recipient account and turn it into float data and round it
		cur.execute('SELECT Balance FROM Real_Account WHERE RealAccountID = ?', (AccountNum,))
		PreviousBalance = cur.fetchall()
		for item in PreviousBalance:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			PreviousBalance = (String)
		PreviousBalance = float(PreviousBalance)
		PreviousBalance = round(PreviousBalance, 2)
		#get the new balance for recipient account and insert all the data for the recipient account
		NewBalance = PreviousBalance + AmountTransferred
		NewBalance = round(NewBalance, 2)
		cur.execute('''INSERT INTO 'Transaction'VALUES(?,?,date('now','-5 hours'),?,?,?,'Recipient of transfer')'''
		,(NewTransID,AccountNum,AmountTransferred,PreviousBalance,NewBalance))
		cur.execute('''UPDATE Real_Account SET Balance=Balance+? WHERE Real_Account_Type=?''',
					(AmountTransferred, RecipientAccount))
		cur.execute('''UPDATE Real_Account SET Balance=round(Balance,2) WHERE Real_Account_Type=?''', (RecipientAccount,))
		# obtains the highest transactionID and makes the next one
		cur.execute('SELECT max(TransactionID) FROM "Transaction"')
		TransID = cur.fetchall()
		for item in TransID:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			NewTransID = int(String) + 1
		# get the account Id of the giving account and transform it into integer data
		cur.execute('''SELECT RealAccountID FROM Real_Account WHERE Real_Account_Type=?''', (GivingAccount,))
		AccountNum = cur.fetchall()
		for item in AccountNum:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			AccountNum = int(String)
		# get the balance for the giving account and turn it into float data and round it
		cur.execute('SELECT Balance FROM Real_Account WHERE RealAccountID = ?', (AccountNum,))
		PreviousBalance = cur.fetchall()
		for item in PreviousBalance:
			String = str(item)
			String = String.lstrip('(')
			String = String.rstrip(')')
			String = String.rstrip(',')
			PreviousBalance = (String)
		#turn amount transferred, previous balance, and new balance into float data and round to the second decimal place.
		#Amount transferred is made negative because the giving account is giving the money away.
		#New balance is made from previous balance and the now negative amount transferred.
		AmountTransferred = float(AmountTransferred)
		AmountTransferred=-1*(AmountTransferred)
		AmountTransferred = round(AmountTransferred, 2)
		PreviousBalance = float(PreviousBalance)
		PreviousBalance = round(PreviousBalance, 2)
		NewBalance = PreviousBalance + AmountTransferred
		NewBalance = round(NewBalance, 2)
		# make and commit database transactions for giving account, and close the database.
		cur.execute('''INSERT INTO 'Transaction'VALUES(?,?,date('now','-5 hours'),?,?,?,'Giver of Transfer')'''
					, (NewTransID, AccountNum, AmountTransferred, PreviousBalance, NewBalance))
		cur.execute('''UPDATE Real_Account SET Balance=Balance+? WHERE Real_Account_Type=?''',
					(AmountTransferred, GivingAccount))
		cur.execute('''UPDATE Real_Account SET Balance=round(Balance,2) WHERE Real_Account_Type=?''',(GivingAccount,))
		conn.commit()
		conn.close()
		
		##Handles the transformation of account names on the database side
	def RenamingAccount(ToBeChangedAccount,NewName):
		# connect to the database and make a cursor
		conn = lite.connect(DIR_PATH)
		cur = conn.cursor()
		#update the account name for the selected account
		cur.execute('''UPDATE Real_Account SET Real_Account_Type=? WHERE Real_Account_Type=?''',(NewName,ToBeChangedAccount))
		#commit the transaction and close the database
		conn.commit()
		conn.close