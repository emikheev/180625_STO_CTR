import os

folder='C:/SSRL/Apr2016/P2016_04_10/Pilatus'


filelist=os.listdir(folder)


csvlist=[];

for a in filelist:
    if 'align' not in a and 'pdi' in a:
        if 'run32' in a:
            csvlist.append(a)

print(csvlist)