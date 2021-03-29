rssfile="rssi.dat"
c=0
rss={}
with open(rssfile) as fp:
   for line in fp:
       if(c%4==0):
           print(line.split())
           rss.update({line.split()[1]:line.split()[0]})
       c+=1

print(rss)