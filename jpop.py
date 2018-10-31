#!/usr/bin/python
# -*- coding: utf-8; -*-
import re
import os, sys
import time
import glob
import urllib2
from bs4 import BeautifulSoup    ### apt-get install BeautifulSoup 
from PIL import Image            ### apt-get install python-imaging/Pillow-2.5.3.win-amd64-py2.7.exe


def get_soup(url):
  try:
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    sf = urllib2.urlopen(req)
    html_page = sf.read()
  except urllib2.URLError, err:
    print(err.reason)
  else:
    return BeautifulSoup(html_page, "html.parser")
  finally:
    print 'Closing url...'
    if sf: sf.close()


def fs_name(fn_text):
  # a[:400][:a[:400].rfind('\\')].decode('unicode-escape')
  fn = fn_text.replace('FHD ','')
  fn = repr(fn).translate(None,"'/[]:|*<>?\"")[1:]
  if (len(fn) > 400):
    fn = fn[:400]
    fn = fn[:fn.rfind('\\')]
  return fn.decode('unicode-escape')


def combine_jpg(cj_list):
  cj_save_name = cj_list[1]+'/'+fs_name(cj_list[4]) 
  cj_files = [cj_list[1]+'/'+s[s.rfind('/')+1::] for s in cj_list[5]]
  if cj_files:
    cj_images = map(Image.open, cj_files)
    widths, heights = zip(*(i.size for i in cj_images))
    max_width = max(widths)
    total_height = sum(heights)
    #total_width = sum(widths)
    #max_height = max(heights)
    new_im = Image.new('RGB', (max_width, total_height))

    yy_offset = 0
    for im in cj_images:
      new_im.paste(im, (0, yy_offset))
      yy_offset += im.size[1]
    new_im.save(cj_save_name+'_SS.jpg') 
  if os.path.isfile(cj_files[0]):
    os.rename(cj_files[0], cj_save_name+'.jpg')
  for i in cj_files:  
    if os.path.isfile(i):
      os.remove(i) 


def download_jpg(dj_url):
  #if re.match(r'[_,a-z,0-9]*-\d.jpg', sj_name):
  #  sj_name = sj_name.replace("-", "-0")
  print "Download image from " + dj_url + " to", 
  dj_fullpath = 'E:/t/'+dj_url[dj_url.rfind('/')+1::]
  print dj_fullpath
  req = urllib2.Request(dj_url, headers={'User-Agent' : "Magic Browser"})
  try:
    sf = urllib2.urlopen(req)
    output = open(dj_fullpath, "wb")
    if output:
      output.write(sf.read())
      output.close()
    return
  except urllib2.URLError, err:
    print(err.reason)
  finally:
    if sf: sf.close()


def javarchive_getimg(jg_list):
  for j in jg_list[5]:
    download_jpg(j)
  combine_jpg(jg_list)


def javarchive_sub1(js1_list):
  #js1_html = open('javarch_avsa-074_sub.html', 'r')
  #js1_soup = BeautifulSoup(js1_html, "html.parser")
  js1_soup = get_soup(js1_list[3])
  if js1_soup:
    #print(js1_soup.prettify())
    js1_list.append(js1_soup.find('h1').text.strip().replace('FHD ',''))
    js1_tmp_list = []
    for js1_i in js1_soup.findAll('div',{'class':'post-content'}):
      for js1_j in js1_i.findAll('img',src=True):
        if ('.th.jpg' not in js1_j['src'].lower() and 'thumbs' not in js1_j['src'].lower()):
          #get_image(js1_j['src'])
          js1_tmp_list.append(js1_j['src'])
    js1_list.append(js1_tmp_list)
  return js1_list


def javarchive_main(jm_list):
  #jm_html = open('javarch_avsa-074.html', 'r')
  #jm_soup = BeautifulSoup(jm_html, "html.parser")
  jm_list.append('http://........./?s='+jm_list[0])
  jm_soup = get_soup(jm_list[-1])
  jm_found = False
  if jm_soup:
    #print(jm_soup.prettify())
    #for a in jm_soup.find_all('a'):
    for jm_i in jm_soup.findAll('div',{'class':'post-meta '}):
      if jm_found:
        break
      #jm_list.append(jm_j.get('href') for jm_j in jm_i.findAll('a') if (jm_list[0].lower() in jm_j.get('href')))
      for jm_j in jm_i.findAll('a'):
        #if jm_text.upper() in jm_j.get('title').upper():
        if jm_list[0].lower() in jm_j.get('href'):
          jm_list.append(jm_j.get('href'))
          jm_found = True
          break
    return jm_list


def javarchive(arg1, arg2):
  javarch_list = javarchive_main([arg1.lower(), arg2.lower()])
  if len(javarch_list) == 4:
    javarch_list = javarchive_sub1(javarch_list)
    if len(javarch_list) == 6:
      javarchive_getimg(javarch_list)
    ## if any('.jpg' in i for i in javarch_list):
    ## for j in [i for i in javarch_list if '.jpg' in i]:
  

if __name__=='__main__':
  if sys.platform == "win32":
    m_path = 'E:/t'
  else:
    m_path = '/t'
  if len(sys.argv) > 1:
    # for i in sys.argv:
    #   print i
    sys.exit(javarchive(sys.argv[1], m_path))
  else:
    print 'Usage: ' + sys.argv[0] + ' <text> e.g.: ' + sys.argv[0] + ' avsa-074'
    sys.exit(1)


'''
[
'hzgd-095',
'e:/t',
'http://javarchive.com/?s=hzgd-095',
u'http://javarchive.com/fhd-hzgd-095-%e6%81%af%e5%ad%90%e3%81%ae%e5%90%8c%e7%b4%9a%e7%94%9f%e3%82%92%e5%a6%8a%e5%a8%a0%e5%8d%b1%e9%99%ba%e6%97%a5%e3%81%ab%e3%83%9e%e3%83%b3%e3%83%81%e3%83%a9%e8%aa%98%e6%83%91-%e4%bd%90/',
u'HZGD-095 \u606f\u5b50\u306e\u540c\u7d1a\u751f\u3092\u598a\u5a20\u5371\u967a\u65e5\u306b\u30de\u30f3\u30c1\u30e9\u8a98\u60d1 \u4f50\u3005\u6728\u3042',
[u'http://img.javstore.net/images/h_1100hzgd095pl.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-1.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-2.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-3.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-4.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-5.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-6.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-7.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-8.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-9.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-10.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-11.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-12.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-13.jpg', u'http://img.javstore.net/images/h_1100hzgd095jp-14.jpg']
]


#get_image('http://javpop.com/2014/12/16/tokyo_hot-n1007.html')

for s in soup.findAll('a'):
  if repr(s.get('title'))[2] == '[':
    print s.get('href')

with open('./path_to_output_f.txt', 'a') as f:
  f.write("{}\t{}\t{}\t{}\n".format(username, auth, role, node))

def get_main(url, outpath):
  #html_file = open('javarchive_avsa-074.html', 'r')
  #soup = BeautifulSoup(html_file, "html")
  soup = get_soup(url)
  if soup:
    arrlist = []
    for file in os.listdir(outpath):
      if file.endswith("_poster.jpg"):
        arrlist.append(repr(file)[1:repr(file).find(' ')].upper())
    result = soup.find('div', attrs={'class' : 'post box'})
    if not result:
      print "Not found"
      return 1
    else:
      for s in result.findAll('a', text=True):
      #for s in soup.findAll('a'):
        if url.find('index.php') > 0:
          print s.get('href')
          rtn_name = get_sub(s.get('href'), outpath)
        else:
          if (s.get('href').find(time.strftime("%Y/%m/%d")) > 0):
          #if (s.get('href').find('2014/12/18') > 0):
            # and (not os.path.isfile(file_name(s.get('title'))+'_poster.jpg')):
            result = False
            for i in arrlist:
              if (i == repr(s.get('title'))[3:repr(s.get('title')).find(']')].upper()):
                result = True
                break
            print s.get('href'), result
            if not result:
              rtn_name = get_sub(s.get('href'), outpath)
      return rtn_name

def get_sub(url, outpath):
  # html_file = open('sample3.html', 'r')
  # soup = BeautifulSoup(html_file, "html")
  soup = get_soup(url)
  if soup:
    for s in soup.findAll("img"):
      if s.get('src').find("_poster") > 0:
        rtn_name = get_image(s.get('src'), s.get('alt'), s.get('src')[-11::], outpath)
      if s.get('src').find("_screenshot") > 0:
        if re.search("_._", s.get('src')):
          rtn_name = get_image(s.get('src'), s.get('alt'), s.get('src')[-17::], outpath)
        else:
          rtn_name = get_image(s.get('src'), s.get('alt'), s.get('src')[-15::], outpath)
    return rtn_name
'''
