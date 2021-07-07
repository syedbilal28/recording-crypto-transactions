
class Transaction:
    def __init__(self,name):
        self.name=name
        self.purchase=0
        self.sales=0
    def __str__(self):
        return f"{self.name} {self.purchase} {self.sales}"
def ProfitCalculator(transactions):
    transactions_with_prices=[]

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

        