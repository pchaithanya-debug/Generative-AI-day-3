import numpy as np
import pandas as pd

def create_data():
    data=[
        ["  ravi kumar ","MUMBAI","m",25,"50,000"],
        ["Anita Sharma","delhi","Female",32,"60000"],
        ["Rahul","Hyderabad","male",250,"75000"],
        ["Priya"," Chennai ","F",np.nan,"unknown"],
        ["Kiran","bangalore","Male",28,"45000"],
        ["  ravi kumar ","MUMBAI","m",25,"50,000"],
        ["Sneha","Delhi","female",35,""],
        ["Arjun","Pune","M",np.nan,"55000"],
        ["Meena","mumbai","Female",45,"80000"],
        ["Rahul","Hyderabad","male",250,"75000"]
    ]
    df=pd.DataFrame(data,columns=["Name","City","Gender","Age","Income"])
    df.to_csv("messy_data.csv",index=False)

def clean_data(df):
    df=df.drop_duplicates()
    df["Name"]=df["Name"].str.strip().str.replace(r"\s+"," ",regex=True).str.title()
    df["City"]=df["City"].str.strip().str.title()
    gmap={"m":"Male","male":"Male","f":"Female","female":"Female"}
    df["Gender"]=df["Gender"].str.strip().str.lower().map(gmap)
    df["Income"]=df["Income"].astype(str).str.replace(",","",regex=False).replace({"unknown":np.nan,"":np.nan})
    df["Income"]=pd.to_numeric(df["Income"],errors="coerce")
    df["Age"]=pd.to_numeric(df["Age"],errors="coerce")
    df.loc[df["Age"]>100,"Age"]=np.nan
    df["Age"]=df["Age"].fillna(df["Age"].median()).round().astype(int)
    df["Income"]=df["Income"].fillna(df["Income"].median()).astype(int)
    return df

def main():
    create_data()
    df=pd.read_csv("messy_data.csv")
    print("BEFORE")
    print(df)
    print("\nRows:",len(df))
    print("Missing Values")
    print(df.isnull().sum())
    clean_df=clean_data(df)
    clean_df.to_csv("clean_data.csv",index=False)
    print("\nAFTER")
    print(clean_df)
    print("\nRows:",len(clean_df))
    print("Missing Values")
    print(clean_df.isnull().sum())
    print("\nCleaned data saved to clean_data.csv")

if __name__=="__main__":
    main()