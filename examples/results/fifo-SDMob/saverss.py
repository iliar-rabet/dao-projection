rssfile="5m.dat"
c=0
rss={}
with open(rssfile) as fp:
   for line in fp:
        #    print(line.split())
           rss.update({line.split()[0]:line.split()[1]})
print (rss.get("-61"))