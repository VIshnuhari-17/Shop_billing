cn=1
def dataentrymenu():
    while True:
        print("_-" * 9, "DATA ENTRY MENU", "-_" * 10)
        print("Please Select the Choice you wish to proceed:")
        print("\t1.Add Stock")
        print("\t2.Update Stock")
        print("\t3.Delete Stock")
        print("\t4.Display Stock")
        print("\t5.Exit")
        choice=int(input("Enter your choice: "))
        if choice==1:
            print("_ _ _ _ _ _ _ _ _ _ Add Stock Selected _ _ _ _ _ _ _ _ _ _  ")
            adddata()
        if choice==2:
            print("_ _ _ _ _ _ _ _ _ _ Update Stock Selected _ _ _ _ _ _ _ _ _ _ ")
            updatedata()
        if choice==3:
            print("_ _ _ _ _ _ _ _ _ _ Delete Stock Selected _ _ _ _ _ _ _ _ _ _ ")
            deldata()
        if choice==4:
            print(" _ _ _ _ _ _ _ _Display Stock Details Selected _ _ _ _ _ _ _ _")
            fetchdata()
        if choice==5:
            print("\t" * 1, "_ " * 22)
            print("\t" * 2, "! ! ! ! ! Exiting ! ! ! ! !")
            print("\t" * 1, "- " * 22)
            break
    else:
        print("\t" * 1, "- " * 15)
        print("\t"*2,"Wrong input!")
        print("\t" * 1, "- " * 15)

def adddata():
    import mysql.connector
    db = mysql.connector.connect(host='localhost', user='root', password='password', database='shop')
    cursor = db.cursor()
    item_code=int(input("Enter Item Code : "))
    cursor.execute("SELECT * FROM stock where item_code='" + str(item_code) + "'")
    results = cursor.fetchall()
    if len(results) == 0:
        item_name = input("Enter Item Name : ")
        item_price = int(input("Enter Price : "))
        quantity = int(input("Enter quantity : "))
        gst = input("Enter GST Catagory(A/B/C) : ")
        cursor.execute(
            "INSERT INTO stock VALUES('" + str(item_code) + "','" + item_name + "','" + str(item_price) + "','" + str(quantity) + "','" + gst + "')")
        db.commit()
        print("\tAll Stocks Added successfully!!")
    else:
        print("\t" * 2, "_ " * 28)
        print("\t" * 3, " Error: Item code already exists!!!")
        print("\t" * 2, "- " * 28)
        fetchdata()
        adddata()


def updatedata():
    import mysql.connector
    try:
        db = mysql.connector.connect(host='localhost', user='root', password='password', database='shop')
        cursor = db.cursor()
        fetchdata()
        item_code=input("Enter code of item to be updated : ")
        quantity=input("Enter New Quantity : ")
        sql=("Update stock set quantity='"+quantity+"' where item_code='"+item_code+"'")
        cursor.execute(sql)
        print("\tRecord Updated Successfully!!")
        db.commit()
    except Exception as e:
        print(e)

def deldata():
    import mysql.connector
    db = mysql.connector.connect(host='localhost', user='root', password='password', database='shop')
    cursor = db.cursor()
    fetchdata()
    item_code=(input("Enter The Code of the item to be deleted : "))
    sql =("delete from stock where item_code='"+item_code+"'")
    cursor.execute(sql)
    print("\t" * 2, "_ " * 23)
    print("\t" * 3, "Record deleted Successfully!!")
    print("\t" * 2, "- " * 23)
    db.commit()

def fetchdata():
    import mysql.connector
    try:
        db = mysql.connector.connect(host='localhost',user='root',password='password',database='shop')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM stock")
        results = cursor.fetchall()
        print("_" * 120)
        print("Item code", "\t\tProduct Name\t", "\t\tPrice\t", "\t\tQuantity\t", "\tGst Catogory\t")
        print("-" * 120)
        for k in results:
            for i in k:
                print("",i,end="\t\t\t")
            print("\n")
        print("-" * 120)
    except:
        print("\t" * 1, "- " * 20)
        print("\t" * 3, "Error:Unable to fetch data")
        print("\t" * 1, "- " * 20)

def billingmenu():
    c="y"
    g=0
    s=1
    total=0
    bill=[]
    import mysql.connector
    db = mysql.connector.connect(host='localhost', user='root', password='password', database='shop')
    cursor = db.cursor()
    cursor.execute("SELECT item_code,item_name FROM stock")
    results = cursor.fetchall()
    print("\t","_" * 50)
    print("\t\tItem code", "\t\tProduct Name\t")
    print("\t","-" * 50)
    for k in results:
        for i in k:
            print("\t\t", i, end="\t")
        print("\n")
    while c=="y" or c=="Y":
        try:
            item_code = int(input("Enter Item Code Of Product : "))
            cursor.execute("SELECT * FROM stock where item_code='"+str(item_code)+"'")
            results = cursor.fetchall()
            if len(results)==0:
                print("\t" * 1, "_ " * 45)
                print("\t" * 3, "Error:No Data Corresponding to Entered Item Code found")
                print("\t" * 1, "- " * 45)
                continue
            req_quantity = int(input("Enter Quantity : "))
            for k in results:
                item_name=k[1]
                price=k[2]
                quantity=k[3]
                if req_quantity > quantity:
                    print("\t" * 1, "_ " * 30)
                    print("\t" * 3, "No sufficient stock!")
                    print("\t" * 1, "- " * 30)
                else:
                    gst = k[4]
                    if gst == "A":
                        gst_percentage = 7
                    if gst == "B":
                        gst_percentage = 17
                    if gst == "C":
                        gst_percentage = 27
                    item_price = price * req_quantity
                    gst_amount = item_price * gst_percentage / 100
                    total_price = item_price + gst_amount
                    g += gst_amount
                    total += total_price
                    k = (s, item_name, req_quantity, price, gst_amount, total_price)
                    s += 1
                    bill.append(k)
                    remaining_quantity = quantity - req_quantity
                    cursor.execute("Update stock set quantity='"+str(remaining_quantity)+"' where item_code='"+str(item_code)+"'")
                    db.commit()
            c = input("Do you want to Enter More?:")
        except:
            print("\t" * 1, "_ " * 20)
            print("\t" * 3, "Error:Unable to fetch data!")
            print("\t" * 1, "- " * 20)
    db.commit()
    print("\n")
    print("\t"*39,"GST INVOICE/BILL")
    print("_" * 100)
    print("S.no", "\t\tProduct Name\t", "\tQuantity\t", "Price\t", "\tGst Amount\t", "Total\t")
    print("_" * 100)
    print("\n")
    for i in bill:
        for s in i:
            print("", s, end="\t\t")
        print("\n")
    print("_" * 100)
    import math
    print("Gst total : ",round(g,2))
    print("Total price : ",round(total,2))
    print("-" * 100)


breaker=False
while True:
    if cn==1:
        password=input("Please enter your Password to continue: ")
        cn=cn+1
        if password!="shop":
            print("\t" * 1, "- " * 25)
            print("\t"*3,"Invalid Password")
            print("\t" * 1, "- " * 25)
            breaker= True
            break
    while True:
        print("\n")
        print("\t" * 5, "..." * 12)
        print("\t"*6,"GST BILLING SYSTEM ")
        print("\t" * 5, "..." * 12)
        print("")
        print("*-"*15,"MAIN MENU","-*"*15)
        print("Please Select the Choice you wish to proceed:")
        print("\t1.Enter stock")
        print("\t2.Billing")
        print("\t3.Exit")
        ch1 = int(input("Enter your Choice : "))
        if ch1 == 1:
            dataentrymenu()
        if ch1 == 2:
            billingmenu()
        if ch1 == 3:
            print("\t"*5,"_ "*18)
            print("\t"*6,"Thanks for Using! :) ")
            print("\t" * 5, "- " * 18)
            breaker = True
            break
    if breaker:
        break
