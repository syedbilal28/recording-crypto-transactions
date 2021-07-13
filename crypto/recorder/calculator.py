import copy
from .models import Product
class Transaction:
    def __init__(self,name):
        self.name=name
        self.purchase=0
        self.sales=0
    def __str__(self):
        return f"{self.name} {self.purchase} {self.sales}"

def get_distinct_products(transactions):
    products=[]
    for i in transactions:
        temp_product=i.product
        if temp_product not in products:
            products.append(temp_product)
    return products
def ProfitCalculator(transactions):
    transactions_with_profits={}
    for i in transactions:
        try:
            transactions_with_profits[i.product.name].append(i.profit)
        except:
            transactions_with_profits[i.product.name]=[]
    for key,value in transactions_with_profits.items():
        try:
            transactions_with_profits[key]=sum(value)/len(value)
        except:
            transactions_with_profits[key]=0
    print(transactions_with_profits)
    return transactions_with_profits

    for i in transactions:
        flag=True
        for j in transactions_with_prices:
            if j.name== i.product.name:
                # print(j)
                if i.Type=="purchase":
                    j.purchase+=i.price
                else:
                    j.sales+=i.price
                flag=False
        if flag:
            temp=Transaction(i.product.name)
            if i.Type=="purchase":
                temp.purchase+=i.price
            else:
                temp.sales+=i.price
            transactions_with_prices.append(temp)
    
    
    return transactions_with_prices

def GetAvailableTransaction(transactions,available_quantity):
    print(f"original transaction {transactions}")
    transactions=list(transactions)[::-1]
    print(f"reversed {transactions}")
    available_transactions=[]
    count=0
    for i in transactions:
        if count < available_quantity:
            available_transactions.append(copy.deepcopy(i))
            count+=i.quantity
        if count > available_quantity:
            difference= count-available_quantity
            available_transactions[-1].quantity-=difference
            break
    return available_transactions[::-1]

