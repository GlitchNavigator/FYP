import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime


prepath = list(str(datetime.datetime.now()))
path = '\\PycharmProjects\\Hand_Tracking\\' + "".join(prepath[:10])

if os.path.exists(path) == False:
    os.mkdir(path)

#named as current log
def RecordReal(info,RealTime, headers):
    options = {}

    options['strings_to_formulas'] = False
    options['strings_to_urls'] = False
    df = pd.DataFrame(info, columns= headers)
    writer = pd.ExcelWriter(RealTime, engine='xlsxwriter', options=options)
    df.to_excel(writer, sheet_name="Counter_list")
    writer.save()

def Record(Log,Real):

    Df = pd.read_excel(Log)
    AddDf = pd.read_excel(Real, index_col=0)
    Df = Df.append(AddDf, ignore_index=True)
    Df['date'] = Df['date'].dt.date
    writer = pd.ExcelWriter(Log)
    Df.to_excel(writer, sheet_name="Counter_list", index=False)
    writer.save()

def plot(x_axis,y_axis,figurename):

    plt.style.use('seaborn')
    # make data:

    # plot
    fig, ax = plt.subplots()
    ax.bar(x_axis, y_axis, width=1, edgecolor="white", linewidth=1)
    # ax.set(xlim=(0, 10), xticks=np.arange(1, 10), ylim=(0, 10), yticks=np.arange(1, 10))
    # plt.show()
    plt.savefig(path +"\\" + figurename+" "+id+".png")

def boxplot(dataset,labels,figurename):

    _, ax = plt.subplots()
    ax.boxplot(dataset, labels=labels, vert=True)
    plt.savefig(path +"\\" + figurename+" "+id+".png")


