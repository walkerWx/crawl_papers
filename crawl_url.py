import re
import urllib
import urllib2

volumn_url_f = 'data/jmlr_volumn_url.dat'

'''
urls = [url.rstrip('\n') for url in open(volumn_url_f)]

for url in urls:
    try: 
        request = urllib2.Request(url)  
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason

    content = response.read().decode('utf-8')
    pattern = re.compile('<nav.*?publ">.*?<a href="(.*?)">', re.S);
    items = re.findall(pattern, content)
    f = open(paper_url_f, 'a')
    for item in items:
        f.write(item)
        f.write('\n')
    f.close()
'''


def crawl_url(conference_url, url_f, pattern):
    try: 
        request = urllib2.Request(conference_url)  
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    content = response.read().decode('utf-8')
    items = re.findall(re.compile(pattern, re.S), content)
    f = open(url_f, 'a')
    for item in items:
        f.write(item)
        f.write('\n')
    f.close()

conference_url = 'http://dblp.uni-trier.de/db/conf/cvpr/'
volumn_url_f = 'data/cvpr_volumn_url.dat'
paper_url_f = 'data/cvpr_paper_url.dat'
dblp_volumn_pattern = '<nav.*?publ">.*?<a href="(.*?)">'
dblp_paper_pattern = '<nav.*?publ">.*?<a href="(.*?)">'

#crawl_url(conference_url, volumn_url_f, dblp_volumn_pattern)

urls = [url.rstrip('\n') for url in open(volumn_url_f)]
for url in urls:
    crawl_url(url, paper_url_f, dblp_paper_pattern)

'''
urls = [url.rstrip('\n') for url in open(paper_url_f)]
urls.sort()
f = open(paper_url_f, 'w')
for url in urls:
    f.write(url);
    f.write('\n')
f.close()
'''
