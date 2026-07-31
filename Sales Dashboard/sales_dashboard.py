import random
import pandas as pd
import matplotlib.pyplot as plt

def generate_data():
    regions=["North","South","East","West"]
    products=["Laptop","Mobile","Tablet","Monitor","Printer"]
    categories={
        "Laptop":"Electronics",
        "Mobile":"Electronics",
        "Tablet":"Electronics",
        "Monitor":"Accessories",
        "Printer":"Accessories"
    }
    months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    data=[]
    for i in range(400):
        product=random.choice(products)
        quantity=random.randint(1,5)
        price=random.randint(10000,80000)
        revenue=quantity*price
        data.append([
            random.choice(regions),
            product,
            categories[product],
            random.choice(months),
            quantity,
            price,
            revenue
        ])
    df=pd.DataFrame(data,columns=["Region","Product","Category","Month","Quantity","Price","Revenue"])
    df.to_csv("sales_data.csv",index=False)
    return df

def analyze(df):
    revenue_by_region=df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    revenue_by_product=df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    revenue_by_month=df.groupby("Month")["Revenue"].sum()
    revenue_by_category=df.groupby("Category")["Revenue"].sum()
    return{
        "total_revenue":int(df["Revenue"].sum()),
        "orders":len(df),
        "best_region":revenue_by_region.index[0],
        "best_product":revenue_by_product.index[0],
        "by_region":revenue_by_region,
        "by_product":revenue_by_product,
        "by_month":revenue_by_month,
        "by_category":revenue_by_category
    }

def dashboard(kpis):
    fig,axes=plt.subplots(2,2,figsize=(14,10))
    kpis["by_region"].plot(kind="bar",ax=axes[0,0],title="Revenue by Region")
    kpis["by_month"].plot(kind="line",ax=axes[0,1],marker="o",title="Monthly Revenue")
    kpis["by_product"].sort_values().plot(kind="barh",ax=axes[1,0],title="Revenue by Product")
    axes[1,1].pie(kpis["by_category"].values,labels=kpis["by_category"].index,autopct="%1.1f%%")
    axes[1,1].set_title("Category Share")
    plt.tight_layout()
    plt.savefig("sales_dashboard.png")
    plt.show()

def main():
    df=generate_data()
    kpis=analyze(df)
    print("Total Revenue :",kpis["total_revenue"])
    print("Orders        :",kpis["orders"])
    print("Best Region   :",kpis["best_region"])
    print("Best Product  :",kpis["best_product"])
    dashboard(kpis)

if __name__=="__main__":
    main()