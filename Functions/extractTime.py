import time

with open("./datasets/wikivote.txt","r") as f_r:
    lines = f_r.readlines()
with open("./datasets/wikivote_date.txt","w") as f_w:
    for line in lines:
        if "%" in line:
            continue
        data = line.strip('\n').split()
        timestamp = time.gmtime(int(data[3]))
        time_str = '%d' %timestamp.tm_year + '-%d' %timestamp.tm_mon + '-%d\n' %timestamp.tm_mday
        new_line = '%s %s' %(line.strip('\n'),time_str)
        print(new_line)
        f_w.write(new_line)
