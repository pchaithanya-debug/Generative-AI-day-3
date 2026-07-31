import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_data():
    data=[]
    for i in range(1,61):
        math=random.randint(20,100)
        science=random.randint(20,100)
        english=random.randint(20,100)
        if random.random()<0.1:
            math=np.nan
        if random.random()<0.1:
            science=np.nan
        if random.random()<0.1:
            english=np.nan
        study=random.randint(1,10)
        data.append([f"S{i:02}",math,science,english,study])
    df=pd.DataFrame(data,columns=["StudentID","Math","Science","English","StudyHours"])
    df.to_csv("student_marks.csv",index=False)

def load_and_clean(filename):
    df=pd.read_csv(filename)
    for subject in ["Math","Science","English"]:
        df[subject]=df[subject].fillna(round(df[subject].mean()))
    df["Total"]=df[["Math","Science","English"]].sum(axis=1)
    df["Percentage"]=(df["Total"]/300*100).round(1)
    df["Result"]=np.where((df[["Math","Science","English"]]>=40).all(axis=1),"Pass","Fail")
    return df

def analyze(df):
    subject_avg=df[["Math","Science","English"]].mean()
    correlation=df["StudyHours"].corr(df["Percentage"])
    topper=df.loc[df["Percentage"].idxmax()]
    print("Students        :",len(df))
    print("Overall Average :",round(df["Percentage"].mean(),1),"%")
    print("Topper          :",topper["StudentID"],f"({topper['Percentage']}%)")
    print("Passed / Failed :",len(df[df["Result"]=="Pass"]),"/",len(df[df["Result"]=="Fail"]))
    print("Study vs Marks  : Correlation",round(correlation,2))
    return subject_avg

def dashboard(df,subject_avg):
    fig,axes=plt.subplots(2,2,figsize=(14,10))
    sns.histplot(df["Percentage"],kde=True,ax=axes[0,0])
    axes[0,0].set_title("Percentage Distribution")
    sns.barplot(x=subject_avg.index,y=subject_avg.values,ax=axes[0,1])
    axes[0,1].set_title("Subject Averages")
    sns.regplot(data=df,x="StudyHours",y="Percentage",ax=axes[1,0])
    axes[1,0].set_title("Study Hours vs Percentage")
    num_cols=["Math","Science","English","StudyHours","Percentage"]
    sns.heatmap(df[num_cols].corr(),annot=True,cmap="coolwarm",ax=axes[1,1])
    axes[1,1].set_title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("student_performance_dashboard.png")
    plt.show()

def main():
    generate_data()
    df=load_and_clean("student_marks.csv")
    subject_avg=analyze(df)
    dashboard(df,subject_avg)

if __name__=="__main__":
    main()