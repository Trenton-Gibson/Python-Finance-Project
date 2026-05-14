CREATE TABLE "Real_Account" (
	"RealAccountID"	INTEGER NOT NULL UNIQUE,
	"Real_Account_Balance"	NUMERIC NOT NULL,
	"Real_Account_Type"	TEXT NOT NULL,
	"Real_Account_Note"	TEXT NOT NULL,
	PRIMARY KEY("RealAccountID" AUTOINCREMENT)
);
CREATE TABLE "Transaction" (
	"TransactionID"	INTEGER NOT NULL UNIQUE,
	"RealAccountID"	INTEGER NOT NULL,
	"LogicalAccountID"	INTEGER NOT NULL,
	"Date_Of_Transaction"	DATETIME NOT NULL,
	"Money_Transferred"	NUMERIC NOT NULL,
	"Real_Account_Previous_Balance"	NUMERIC NOT NULL,
	"Real_Account_New_Balance"	NUMERIC NOT NULL,
	"Logical_Account_Previous_Balance"	NUMERIC NOT NULL,
	"Logical_Account_New_Balance"	NUMERIC NOT NULL,
	"Transaction_Type"	TEXT NOT NULL,
	PRIMARY KEY("TransactionID" AUTOINCREMENT),
	FOREIGN KEY("RealAccountID") REFERENCES "Real_Account"("RealAccountID"),
	FOREIGN KEY("LogicalAccountID") REFERENCES "Logical_Account"("LogicalAccountID")
);
CREATE TABLE "Logical_Account" (
	"LogicalAccountID"	INTEGER NOT NULL UNIQUE,
	"Logical_Account_Type"	TEXT NOT NULL,
	"Logical_Account_Balance"	NUMERIC NOT NULL,
	"Logical_Account_Note"	TEXT NOT NULL,
	PRIMARY KEY("LogicalAccountID" AUTOINCREMENT)
);
CREATE TABLE "Budget_Item" (
	"BudgetItemID"	INTEGER NOT NULL UNIQUE,
	"BudgetID"	INTEGER NOT NULL,
	"LogicalAccountID"	INTEGER NOT NULL,
	"BudgetAllocationID"	INTEGER NOT NULL,
	"Budget_Item_Note"	TEXT NOT NULL,
	PRIMARY KEY("BudgetItemID" AUTOINCREMENT),
	FOREIGN KEY("BudgetAllocationID") REFERENCES "Budget_Allocation"("BudgetAllocationID"),
	FOREIGN KEY("LogicalAccountID") REFERENCES "Logical_Account"("LogicalAccountID"),
	FOREIGN KEY("BudgetID") REFERENCES "Budget"("BudgetID")
);
CREATE TABLE "Budget" (
	"BudgetID"	INTEGER NOT NULL UNIQUE,
	"Budget_Name"	TEXT NOT NULL,
	"Budget_Note"	TEXT NOT NULL,
	PRIMARY KEY("BudgetID" AUTOINCREMENT)
);
CREATE TABLE "Budget_Allocation" (
	"BudgetAllocationID"	INTEGER NOT NULL UNIQUE,
	"Budget_Allocation_Type"	TEXT NOT NULL,
	"Budget_Allocation_Amount"	NUMERIC NOT NULL,
	PRIMARY KEY("BudgetAllocationID" AUTOINCREMENT)
);