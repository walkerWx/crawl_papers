import cookielib
import urllib
import urllib2
import re
from enum import Enum
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from time import sleep

class Conference(Enum):
    ai = 1
    pami = 2
    ijcv = 3
    jmlr = 4
    aaai = 5

ai_paper_url_f = 'data/ai_paper_url.dat'
pami_paper_url_f = 'data/pami_paper_url.dat' 
ijcv_paper_url_f = 'data/ijcv_paper_url.dat'
jmlr_paper_url_f = 'data/jmlr_paper_url.dat'
aaai_paper_url_f = 'data/aaai_paper_url.dat'
cvpr_paper_url_f = 'data/cvpr_paper_url.dat'

icml_paper_url_f = 'data/icml_paper_url.dat'
ijcai_paper_url_f = 'data/ijcai_paper_url.dat'
nips_paper_url_f = 'data/nips_paper_url.dat'
acl_paper_url_f = 'data/acl_paper_url.dat'

ai_urls = [url.rstrip('\n') for url in open(ai_paper_url_f)]
pami_urls = [url.rstrip('\n') for url in open(pami_paper_url_f)] 
ijcv_urls = [url.rstrip('\n') for url in open(ijcv_paper_url_f)] 
jmlr_urls = [url.rstrip('\n') for url in open(jmlr_paper_url_f)] 
aaai_urls = [url.rstrip('\n') for url in open(aaai_paper_url_f)] 
cvpr_urls = [url.rstrip('\n') for url in open(cvpr_paper_url_f)] 

icml_urls = [url.rstrip('\n') for url in open(icml_paper_url_f)] 
ijcai_urls = [url.rstrip('\n') for url in open(ijcai_paper_url_f)] 
nips_urls = [url.rstrip('\n') for url in open(nips_paper_url_f)] 
acl_urls = [url.rstrip('\n') for url in open(acl_paper_url_f)] 


 
pattern_str = {}
pattern_str[Conference.ai] = '<span class="affiliation__text".*?>(.*?)</span>'
pattern_str[Conference.pami] = '<div class="bio">.*?<p>(.*?)</p>'
pattern_str[Conference.ijcv] = '<span.*?class="affiliation__[name|department].*?>(.*?)</span>'
pattern_str[Conference.jmlr] = 'Institutional Profile Page">.*?<small>(.*?)</small>'
pattern_str[Conference.aaai] = '<a href="javascript:openRTWindow(\'(.*?)\');">About the author'

paper_found_f = 'data/paper_found.dat'
paper_tbd_f = 'data/paper_tbd.dat'


def save_url(url, fname):
    f = open(fname, 'a')
    f.write(url)
    f.write('\n')
    f.close()

def search_ai_url(url):
    print "Search in URL: " + url
    try:
        cookie_f = 'cookies/ai_cookie.txt'
        #cookie = cookielib.MozillaCookieJar(cookie_f)
        cookie = cookielib.MozillaCookieJar()
        cookie.load(cookie_f, ignore_discard=True, ignore_expires=True)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        request = urllib2.Request(url, None, headers)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        #response = opener.open(request, data_encoded)
        response = opener.open(request)
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    content = response.read().decode('utf-8')
    #print content.encode('utf-8')

    found = False
    
    pattern = re.compile('<span class="affiliation__text".*?>(.*?)</span>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print item.encode('utf-8')
        if "wuhan" in item.lower() or "whu" in item.lower():
            found = True
    
    pattern = re.compile('<li id="aff.*?<span id="">(.*?)</span>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print item.encode('utf-8')
        if "wuhan" in item.lower() or "whu" in item.lower():
            found = True
    
    if found:
        f = open(paper_found_f, 'a')
        f.write(url)
        f.write('\n')
        f.close()
        print "find one"
    print ""

def search_pami_url(url):
    print "Search in pami URL: " + url
    cookie_f = 'cookies/cookie.txt'
    cookie = cookielib.MozillaCookieJar(cookie_f)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    headers = { 'User-Agent' : user_agent }

    try:
        request = urllib2.Request(url, None, headers)
        response = opener.open(request) 
        cookie.save(ignore_discard=True, ignore_expires=True);
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason

    content = response.read().decode('utf-8')
    pattern = re.compile('id="full-text-html" href="(.*?)"', re.S)
    items = re.findall(pattern, content)
    if len(items) == 0:
        print "Can not find full text as html!\n"
        return

    detail_url = 'http://ieeexplore.ieee.org' + items[0]

    items = search(detail_url, pattern_str[Conference.pami])
    found = False
    for item in items:
        print item.encode('utf-8')
        if "wuhan" in item.lower() or "whu" in item.lower():
            found = True
    if found:
        save_url(url, paper_found_f)
        print "find one"
    print ""

def search_aaai(url):

    author_info_url =  url[:url.find("paper/view")] + 'rt/bio/' + url[url.find("view")+5:] + '/0'
    pattern = '<div id="author">(.*?)</div>'
    items = search(author_info_url, pattern)

    if len(items) == 0:
        save_url(url, paper_tbd_f)
        print "No author info! TBD.."

    found = False
    for item in items:
        print item.encode('utf-8')
        if "wuhan" in item.lower() or "whu" in item.lower():
            found = True
    if found:
        save_url(url, paper_found_f)
        print "find one"
    print ""


def search(url, pattern):

    print "Search in URL: " + url

    cookie_f = 'cookies/cookie.txt'
    cookie = cookielib.MozillaCookieJar(cookie_f)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    headers = { 'User-Agent' : user_agent }

    try:
        request = urllib2.Request(url, None, headers)
        response = opener.open(request) 
        cookie.save(ignore_discard=True, ignore_expires=True);
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    content = response.read().decode('utf-8')
    items = re.findall(re.compile(pattern, re.S), content)

    '''
    if len(items) == 0:
        driver = webdriver.PhantomJS()
        driver.set_page_load_timeout(60)
        try:
            driver.get(url)
            content = driver.page_source
            items = re.findall(pattern, content)
        except TimeoutException:
            #save_url(url, paper_tbd_f)
            print "Can not load page content, give up.."
            return 
    '''

    return items

def download_icmf():
    directory = 'papers/icml/'
    for url in icml_urls:
        if url.endswith('html'):
            url = url[:-4] + 'pdf'
        pdf_f = directory + url.split('/')[-1] 
        response = urllib2.urlopen(url)
        f = open(pdf_f, 'wb')
        f.write(response.read())
        f.close()
        print "Download " + url + " complete!"

def download(urls, directory):

    for url in urls:
        if url.endswith('pdf'):
            pdf_f = directory + url.split('/')[-2] + '_' +  url.split('/')[-1] 
            response = urllib2.urlopen(url)
            f = open(pdf_f, 'wb')
            f.write(response.read())
            f.close()
            print "Download " + url + " complete!"

        elif url.startswith('http://doi.acm.org'):
            items = search(url, pattern_str[Conference.jmlr]) 
            if len(items) == 0:
                save_url(url, paper_tbd_f)
                print "No author info! TBD.."
            found = False
            for item in items:
                print item.encode('utf-8')
                if "wuhan" in item.lower() or "whu" in item.lower():
                    found = True
            if found:
                save_url(url, paper_found_f)
                print "find one"
            print ""

        elif url.startswith('http://ijcai.org/'):
            pattern = '<div class="content".*?<a href="(.*?pdf)">PDF</a>'
            items = search(url, pattern)
            pdf_url = 'http://ijcai.org' + items[0]
            print pdf_url
            pdf_f = directory + items[0].replace("/", "_");
            response = urllib2.urlopen(pdf_url)
            f = open(pdf_f, 'wb')
            f.write(response.read())
            f.close()
            print "Download " + pdf_url + " complete!"

        elif url.startswith('http://www.aaai.org'):
            search_aaai(url)             

        elif url.startswith('http://jmlr.org'):        
            if url.endswith('html'):
                url = url[:-4] + 'pdf'
            pdf_f = directory + url.split('/')[-1] 
            response = urllib2.urlopen(url)
            f = open(pdf_f, 'wb')
            f.write(response.read())
            f.close()
            print "Download " + url + " complete!"

        elif url.startswith('http://papers.nips.cc'):
            pdf_url = url + '.pdf' 
            pdf_f = directory + pdf_url.split('/')[-1]
            response = urllib2.urlopen(pdf_url)
            f = open(pdf_f, 'wb')
            f.write(response.read())
            f.close()
            print "Download " + pdf_url + " complete!"

        elif url.startswith('http://aclweb.org'):
            if not url.endswith('pdf'):
                url = url + '.pdf'
            response = urllib2.urlopen(pdf_url)
            f = open(pdf_f, 'wb')
            f.write(response.read())
            f.close()
            print "Download " + pdf_url + " complete!"

        elif url.startswith('http://dx.doi.org'):

            pattern = 'id="full-text-pdf".*?href=\'(.*?)\'.*?>'            
            items = search(url, pattern)
            full_text_pdf_url = 'http://ieeexplore.ieee.org' + items[0]
            pattern = '<frame src="(http://ieeexplore.ieee.org.*?\.pdf.*?)" frameborder=0 />'
            items = search(full_text_pdf_url, pattern)

            pdf_url = items[0]
            pdf_f = directory + pdf_url.split('&')[-2].split('=')[-1] + '_' + pdf_url.split('&')[-1].split('=')[-1] + '.pdf'


            cookie_f = 'cookies/cookie.txt'
            cookie = cookielib.MozillaCookieJar(cookie_f)
            handler = urllib2.HTTPCookieProcessor(cookie)
            opener = urllib2.build_opener(handler)
            user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
            headers = { 'User-Agent' : user_agent }

            try:
                request = urllib2.Request(pdf_url, None, headers)
                response = opener.open(request) 
                cookie.save(ignore_discard=True, ignore_expires=True);
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

            f = open(pdf_f, 'wb')
            f.write(response.read())
            f.close()
            print "Download " + pdf_url + " complete!"

download(cvpr_urls, 'papers/cvpr/')

'''
for url in aaai_urls:
    sleep(1)
    search_aaai(url)

finished = False
while not finished:
    finished = True
    if pami_urls:
        search_pami_url(pami_urls.pop())
        sleep(30)
        finished = False
    if ijcv_urls:
        search(ijcv_urls.pop(), Conference.ijcv)
    if jmlr_urls:
        search(jmlr_urls.pop(), Conference.jmlr)
        finished = False
    sleep(20)

for url in pami_urls:
    sleep(40)
    search_pami_url(url)

for url in ai_urls:
    seach_ai_url(url)

for url in pami_urls:
    search_pami_url(url)
'''

'''
request = urllib2.Request(url)
response = urllib2.urlopen(request)
print 
'''

