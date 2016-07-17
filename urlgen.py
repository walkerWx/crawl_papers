f = open('data/jmlr_volumn_url.dat', 'w')
url = 'http://dblp.uni-trier.de/db/journals/jmlr/jmlr'
for i in range(12, 16):
    f.write(url+str(i)+'.html');
    f.write('\n');
f.close()
