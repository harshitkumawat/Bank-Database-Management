import pymysql
import os
import datetime
from prettytable import PrettyTable
con = pymysql.connect('localhost','root','','Bank5')
cur = con.cursor()
def signup() :
	os.system('clear')
	now = str(datetime.datetime.now())
	name = input("\nEnter Your Name -: ");
	address = input("\nEnter Your Address -: ")
	date = input("\nEnter date(yyy-mm-dd) -: ")
	contact = input("\nEnter Your Contact Number -: ")
	email = input("\nEnter Your Email -: ")
	try:
		cur.execute("insert into customer (account_no,name,address,email,contact_no,account_type,balance,open_date,status) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(1001*(10**10)+int(contact),name,address,email,contact,"",int("0"),date,"open"))
		print("\n\nYou Have Successfully Registered with our Bank...")
		l = name.split()
		password = l[0]+"123"
		username = 1001*(10**10)+int(contact)
		print("Your Username is -: ",username)
		print("Your Password is -: ",password)
		cur.execute("insert into login (user_name,password) values(%s,%s)",(username,password))
	except Exception as e:
		print(e)
		input()
		signup()
	con.commit()
	input()


def signin() :
	os.system('clear')
	username = input("Enter Username -: ")
	password = input("Enter Password -: ")
	cur.execute("select * from login")
	data = cur.fetchall()
	for i in data:
		if i[0]==username and i[1]==password:
			print("Login Successfull...\nPress Enter to Continue..")
			input()
			os.system('clear')
			ch = 0
			while ch!=7:
				cur.execute("select * from customer where account_no = %s",(username))
				check = cur.fetchall()
				if check[0][8]=='open' or check[0][8]=='Open':
					print("1. Address Change..\n2. Open New Account\n3. Money Deposit..\n4. Money Withdrawl..\n5. Print Statement..\n6. Transfer Money..\n7. Account Closure..\n8. Avail Loan\n9. Customer Logout..")
					ch = input("\nEnter Your Choice -:")
					if ch=="1":             ## Address Change
						address = input("\nEnter New Address to Update -: ")
						try:
							cur.execute("update customer set address = %s where account_no = %s",(address,username))
							print("Address Changed Successfully..\nPress Enter to Continue..")
							input()
						except Exception as e:
							print(e)
							input()
						con.commit()
					elif ch=="2": # Open New Account
						print("1. Open Saving Account..\n2. Open Current Account..\n3. Open FD..\n")
						select = input("Enter Account Option -: ")
						cur.execute("select * from transaction")
						count = cur.rowcount
						now = str(datetime.datetime.now())
						if select=="1":
							cur.execute("select * from customer")
							cust = cur.fetchall()
							for x in cust:
								if x[0]==i[0]:
									if x[5]=="saving" or x[5]=="current" or x[5]=="FD":
										print("Account Already exist......\n")
										input()
									else:
										balance = int(input("Enter Balance to Deposit -:"))
										try:
											cur.execute("update customer set balance = %s where account_no = %s",(balance,i[0]))
											cur.execute("update customer set account_type = %s where account_no = %s",("saving",i[0]))
											cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Credited",i[0],now[:11],balance,"saving"))
										except Exception as e:
											print(e)
											input()
							con.commit()
						elif select=="2":
							cur.execute("select * from customer")
							cust = cur.fetchall()
							for x in cust:
								if x[0]==i[0]:
									if x[5]=="saving" or x[5]=="current" or x[5]=="FD":
										print("Account Already exist......\n")
										input()
									else:
										balance = int(input("\nEnter Balance to deposit -: "))
										while balance<5000:
											print("Minimum Balance Should be 5000 Rs.")
											balance = int(input("Enter Balance to Deposit -:"))
										try:
											cur.execute("update customer set balance = %s where account_no = %s",(balance,i[0]))
											cur.execute("update customer set account_type = %s where account_no = %s",("current",i[0]))
											cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Credited",i[0],now[:11],balance,"current"))
										except Exception as e:
											print(e)
											input()
									con.commit()
									break;
						if select=="3":
							cur.execute("select * from customer")
							cust = cur.fetchall()
							for x in cust:
								if x[0]==i[0]:
									if x[5]=="saving" or x[5]=="current":
										print("Account Already exist......\n")
										input()
									else:
										c = ""
										cur.execute("select * from fd")
										fd = cur.fetchall()
										for y in fd:
											if y[0]==i[0]:
												c = str(y[1])
												c = c[:1]
										if c=="":
											fdaccount_no = "1FD"+i[0][4:]
										else:
											c = int(c)+1
											fdaccount_no = str(c)+"FD"+i[0][4:]
										balance = int(input("Enter Balance to Deposit in FD -: "))
										while balance<1000:
											print("Minimum Balance Should be 5000 Rs.")
											balance = int(input("Enter Balance to Deposit -:"))
										duration = int(input("Enter Duration of FD (in Months) -:"))
										while duration<12:
											print("Minimum Duration Should be 12 months.")
											duration = int(input("Enter Duration of FD (in Months) -:"))
										try:
											cur.execute("update customer set balance = %s where account_no = %s",(balance+int(x[6]),i[0]))
											cur.execute("update customer set account_type = %s where account_no = %s",("FD",i[0]))
											cur.execute("insert into fd (account_no,fd_account_no,amount,duration) values(%s,%s,%s,%s)",(i[0],fdaccount_no,balance,duration))
											cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Credited",i[0],now[:11],balance,fdaccount_no))
											print("\nMoney Successfully Deposited in FD.....\n")
											input()
										except Exception as e:
											print(e)
											input()
									con.commit()
							

					elif ch=="3":  # Money Deposit
						cur.execute("select * from customer")
						money = cur.fetchall()
						cur.execute("select * from transaction")
						count = cur.rowcount
						now = str(datetime.datetime.now())
						for j in money:
							if j[0]==i[0]:
								if j[5]!="FD":
									amount = int(input("\nEnter Amount to be deposited -: "))
									newamount = amount + int(j[6])
									try:
										cur.execute("update customer set balance = %s where account_no = %s",(newamount,i[0]))
										print("Amount Deposited Successfully..\nYour Total Balance is ",newamount,"\nPress Enter to Continue..")
										cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Credited",j[0],now[:11],amount,j[5]))
										input()
										break
									except Exception as e:
										print(e)
										input()
								else :
									fdno = input("\nEnter FD number to Deposit Money -:")
									cur.execute("select * from fd")
									fd_data = cur.fetchall()
									flag = -1
									for z in fd_data:
										if z[1]==fdno:
											flag = 0
											amount = int(input("\nEnter Amount to be deposited -: "))
											newamount = amount + int(j[6])
											try:
												cur.execute("update customer set balance = %s where account_no = %s",(newamount,username))
												print("\nAmount Deposited Successfully..\n")
												cur.execute("update fd set amount = %s where fd_account_no = %s",(z[2]+amount,fdno))
												print("Total FD Amount is -: ",z[2]+amount)
												cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Credited",j[0],now[:11],amount,fdno))
												input()
												break
											except Exception as e:
												print(e)
									if flag==-1:
										print("\nSorry FD Number Does Not Exist.....\n")
										input()
						con.commit()
					elif ch=="4":  #Money Withdrawl
						cur.execute("select * from customer")
						money = cur.fetchall()
						cur.execute("select * from transaction")
						count = cur.rowcount
						now = str(datetime.datetime.now())
						flag = -1
						for j in money:
							if j[0]==i[0] and (j[5]=="current" or j[5]=="saving"):
								flag = 0
								amount = int(input("\nEnter Amount to be withdrawl -: "))
								if amount<int(j[6]):
									newamount = int(j[6]) - amount
									try:
										cur.execute("update customer set balance = %s where account_no = %s",(newamount,username))
										print("Amount Withdrawl Successfully..\nYour Total Balance is ",newamount,"\nPress Enter to Continue..")
										cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Debited",j[0],now[:11],amount,j[5]))
										input()
										con.commit()
									except Exception as e:
										print(e)
								else :
									print("Entered Amount is greater than your balance..\nPress Enter to continue...")
									input()
									break
						if flag==-1:
							print("\nMoney Cannot be Withdrawl From FD....")
							input()
						con.commit()
					elif ch=="5": # Print Statement
						cur.execute("select * from transaction")
						statement = cur.fetchall()
						cur.execute("select * from customer where account_no=%s",i[0])
						acc = cur.fetchall()
						print("\nName       : ",acc[0][1],"\tEmail Id     : ",acc[0][3],"\nMobile No. : ",acc[0][4],"\tAccount Type : ",acc[0][5],"\nBalance    : ",acc[0][6])
						cur.execute("select account_type from customer where account_no = %s ",i[0])
						sorc = cur.fetchall()
						if sorc[0][0]=="saving" or sorc[0][0]=="current":
							t = PrettyTable(['Date','Transaction Type','Amount'])
							for j in statement:
								if i[0]==j[2]:
									t.add_row([j[3],j[1],j[4]])
							print("\n",t)
						else:
							t = PrettyTable(['Date','FD Number','Amount Deposited'])
							for j in statement:
								if i[0]==j[2]:
									t.add_row([j[3],j[5],j[4]])
							print("\n",t)
					elif ch=="6":  # Transfer Money
						cur.execute("select * from customer")
						transf = cur.fetchall()
						for w in transf:
							if w[0]==i[0] and w[5]=="FD":
								print("Money Cannot be Transferred From FD Account...")
								input()
							elif w[0]==i[0] and w[5]!="FD":
								cur.execute("select * from transaction")
								count = cur.rowcount
								now = str(datetime.datetime.now())
								accno = input("\nEnter Account Number to Transfer Money -: ")
								flag = -1
								for j in transf:
									if i[0]==j[0]:
										m = j
								for j in transf:
									if accno==j[0] and j[5]!="FD":
										l = j
										flag = 0
										print("\nName : ",l[1])
										amount = int(input("\nEnter Amount to be Transfer -: "))
										if amount<int(m[6]):
											newamount = int(m[6]) - amount
											try:
												cur.execute("update customer set balance = %s where account_no = %s",(newamount,username))
												cur.execute("update customer set balance = %s where account_no = %s",(amount+l[6],accno))
												print("Amount Transferred Successfully..\nYour Total Balance is ",newamount,"\nPress Enter to Continue..")
												cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Debited",m[0],now[:11],amount,m[5]))
												cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+2,"Credited",accno,now[:11],amount,l[5]))
												input()
												con.commit()
											except Exception as e:
												print(e)
										else :
											print("Entered Amount is greater than your balance..\nPress Enter to continue...")
											input()
											break
									elif accno==j[0] and j[5]=="FD":
										l = j
										fdno = input("Enter FD Number to transfer Money -: ")
										flag1 = -1
										cur.execute("select * from fd")
										fddata = cur.fetchall()
										for q in fddata:
											if q[1]==fdno:
												flag1 = 0
												print("\nName : ",j[1])
												amount = int(input("\nEnter Amount to be Transfer -: "))
												if amount<int(m[6]):
													newamount = int(m[6]) - amount
													try:
														cur.execute("update customer set balance = %s where account_no = %s",(newamount,username))
														cur.execute("update customer set balance = %s where account_no = %s",(amount+l[6],accno))
														print("Amount Transferred Successfully..\nYour Total Balance is ",newamount,"\nPress Enter to Continue..")
														cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Debited",m[0],now[:11],amount,m[5]))
														cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+2,"Credited",accno,now[:11],amount,fdno))
														cur.execute("update fd set amount = %s where fd_account_no = %s",(q[2]+amount,fdno))
														input()
														con.commit()
													except Exception as e:
														print(e)
												else :
													print("Entered Amount is greater than your balance..\nPress Enter to continue...")
													input()
													break
										if flag1==-1:
											print("\nFD Number Does not Exist...")
											input()
									else:
										print("\nAccount Number Does not Exist...")
										input()
						
					elif ch=="7":   # Account Closure
						cur.execute("select * from customer")
						status = cur.fetchall()
						choice = input("\nWant to Close the Account(Y/N) -: ")
						if choice=="y" :
							try:
								cur.execute("update customer set status = %s where account_no = %s",("close",username))
								con.commit()
							except Exception as e:
								print(e)
					elif ch=="8":
						cur.execute("select * from transaction")
						count = cur.rowcount
						now = str(datetime.datetime.now())
						cur.execute("select * from customer")
						cust = cur.fetchall()
						for x in cust:
							if x[0]==i[0]:
								if x[5]=="FD" or x[5]=="current":
									print("Loan Facility Not Available......\n")
									input()
								else:
									c = ""
									cur.execute("select * from loan")
									ln = cur.fetchall()
									for y in ln:
										if y[0]==i[0]:
											c = str(y[1])
											c = c[:1]
									if c=="":
										lnaccount_no = "1LN"+i[0][4:]
									else:
										c = int(c)+1
										lnaccount_no = str(c)+"LN"+i[0][4:]
									balance = int(input("Enter Loan Amount -: "))
									while balance>2*int(x[6]):
										print("Loan Amount Should be Less than ",2*int(x[6]))
										balance = int(input("Enter Loan Amount -:"))
									duration = int(input("Enter Duration of Repayment (in Months) -:"))
									try:
										cur.execute("update customer set balance = %s where account_no = %s",(balance+int(x[6]),i[0]))
										cur.execute("insert into loan (account_no,loan_no,amount,repayment_term) values(%s,%s,%s,%s)",(i[0],lnaccount_no,balance,duration))
										cur.execute("insert into transaction (trans_id,trans_type,account_no,date,amount,account_type) values(%s,%s,%s,%s,%s,%s)",(count+1,"Credited",i[0],now[:11],balance,lnaccount_no))
										print("\nLoan Passed Successfully.....\n")
										input()
										con.commit()
									except Exception as e:
										print(e)
										input()
 						
					elif ch=="9":   # Log Out
						print("You Have been loged out Successfully\nPress Enter to Continue..")
						input()
						return
					else:
						print("\nINVALID CHOICE...")
						input()
				else:
					print("\nAccount is Closed.....\nSorry Can't Perform Operations...")
					input()
					return
	print("INVALID ID AND PASSWORD...")
	input()
	return

ch = 0
while ch!=4:
	os.system('clear')
	print("1. Sign Up(New Customer) \n2. Sign In(Existing Customer) \n3. Admin Sign In \n4. Exit..")
	print("Enter Your Choice -: ")
	ch = int(input())
	if ch==1:
		signup()
	elif ch==2:
		signin()
	elif ch==3:
		os.system('clear')
		q = 0
		while q!=4:
			print("1. Print Closed Account History..\n2. FD Report..\n3. Loan Report..\n4. Admin log out..")
			q = input("Enter Your Choice -: ")
			if q=="1":
				cur.execute("select * from customer where status = %s","close")
				data = cur.fetchall()
				t = PrettyTable(['Account Number','Name','Status'])
				for i in data:
					t.add_row([i[0],i[1],i[8]])
				print(t)
			elif q=="2":
				cur.execute("select * from fd")
				data = cur.fetchall()
				t = PrettyTable(['Account Number','FD Number','Amount','Duration'])
				for i in data:
					t.add_row([i[0],i[1],i[2],i[3]])
				print(t)
			elif q=="3":
				cur.execute("select * from loan")
				data = cur.fetchall()
				t = PrettyTable(['Account Number','Loan Number','Amount','Repayment Term'])
				for i in data:
					t.add_row([i[0],i[1],i[2],i[3]])
				print(t)
			elif q=="4":
				print("You Have Been Logged out Successfully...")
				input()
				break
			else:
				print("Invalid Choice...")
				input()
cur.close()