#!/usr/bin/python
# -*- coding: utf-8; -*-
import os, sys
import gc
import time
import urllib2
#import site
import re
#import glob
#import win32api
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
    if sf:  sf.close()
    print 'Closing url...'


def print_to_console(text):
  '''
  # Prints a (unicode) string to the console, encoded depending on the stdout
  # encoding (eg. cp437 on Windows). Works with Python 2 and 3.
  ANZ-132 \u7d76\u5bfe\u670d\u5f93 VIP\u5c02\u7528\u5974\u96b7\u30ca\u30fc\u30b9 \u5bae\u91ce\u77b3
  '''
  try:
    sys.stdout.write(text)
  except UnicodeEncodeError:
    bytes_string = text.encode(sys.stdout.encoding, 'backslashreplace')
    if hasattr(sys.stdout, 'buffer'):
      sys.stdout.buffer.write(bytes_string)
    else:
      text = bytes_string.decode(sys.stdout.encoding, 'strict')
      sys.stdout.write(text)
  sys.stdout.write("\n")
  

def toSearchText(str):
  for j in [
            ['.mkv',''], ['.mp4',''], ['cd1',''],
            [' ','']
           ]:
    str = str.replace(j[0], j[1])
  if re.match('[0-9]+_[0-9]+', str):
    str = str.replace('_','-')
  print str
  return str


def to_Filename(fn):
  # a[:500][:a[:500].rfind('\\')].decode('unicode-escape')
  for i in ['FHD ', '[ENCODE720P] ']:
    fn = fn.replace(i,'')
  fn = repr(fn).translate(None,"'/:*?\"<>|")[1:]
  if (len(fn) > 500):
    fn = fn[:500]
    fn = fn[:fn.rfind('\\')]
  return fn.decode('unicode-escape')


def combine_jpg(cj_list):
  cj_fullpath = cj_list[1]+os.sep+cj_list[4] 
  cj_files = [cj_list[1]+os.sep+os.path.basename(s) for s in cj_list[5]]
  if cj_files and len(cj_files) > 1:
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
    new_im.save(cj_fullpath+'_SS.jpg')
    print u'Saving to '+cj_fullpath+'_SS.jpg'
  if os.path.isfile(cj_files[0]) and not os.path.isfile(cj_fullpath+'.jpg'):
    os.rename(cj_files[0], cj_fullpath+'.jpg')
    print u'Saving to '+cj_fullpath+'.jpg'
  else:
    print u'Destination file already exist.'
  for i in cj_files:  
    if os.path.isfile(i):
      os.remove(i) 


def download_jpg(dj_url, dj_path):
  dj_fullpath = dj_path + os.sep + os.path.basename(dj_url)
  print u'Download ' + dj_url + u' to ' + dj_fullpath
  #time.sleep(0.08)
  req = urllib2.Request(dj_url, headers={'User-Agent' : "Magic Browser"})
  try:
    sf = urllib2.urlopen(req)
    output = open(dj_fullpath, "wb")
    if output:
      output.write(sf.read())
      output.close()
    #return
  except urllib2.URLError, err:
    print(err.reason)
  finally:
    if sf:
      sf.close()
    print "Done."
    del sf, req, output, dj_fullpath
  return


def javarchive_getimg(jg_list):
  for j in jg_list[5]:
    download_jpg(j, jg_list[1])
  combine_jpg(jg_list)
  return


def javarchive_sub1(js1_list):
  #js1_html = open('mavarchive_sa-074_sub.html', 'r')
  #js1_soup = BeautifulSoup(js1_html, "html.parser")
  js1_soup = get_soup(js1_list[3])
  if js1_soup:
    #print(js1_soup.prettify())
    js1_list.append(to_Filename(js1_soup.find('h1').text.strip()))
    js1_tmp_list = []
    for js1_i in js1_soup.findAll('div',{'class':'post-content'}):
      for js1_j in js1_i.findAll('img',src=True):
        if ('.th.jpg' not in js1_j['src'].lower() and 'thumbs' not in js1_j['src'].lower()):
          #get_image(js1_j['src'])
          js1_tmp_list.append(js1_j['src'])
    js1_list.append(js1_tmp_list)
  return js1_list


def javarchive_main(jm_list):
  #jm_html = open('mavarchive_sa-074.html', 'r')
  #jm_soup = BeautifulSoup(jm_html, "html.parser")
  jm_list.append('http://mavarchive.com/?s='+jm_list[0])
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
  result=''
  javarch_list = javarchive_main([arg1.lower(), arg2.lower()])
  if len(javarch_list) == 4:
    javarch_list = javarchive_sub1(javarch_list)
    if len(javarch_list) == 6:
      javarchive_getimg(javarch_list)
      result = javarch_list[4]
    del javarch_list
  return result
    ## if any('.jpg' in i for i in javarch_list):
    ## for j in [i for i in javarch_list if '.jpg' in i]:
  

if __name__=='__main__':
  #site.getusersitepackages()
  #gc.enable()
  #gc.collect()
  if len(sys.argv) > 1:
    #win32api.MessageBox(0, sys.argv[1], 'Archive Window')
    m_path, m_filename = os.path.split(sys.argv[1])
    #print '['+m_path+']', '['+m_filename+']'
    if not m_path:
      m_path = os.getcwd()
    m_ffilename, m_ext = os.path.splitext(sys.argv[1])
    #print '['+m_ffilename+']', '['+m_ext+']'
    m_text = javarchive(toSearchText(m_filename), m_path)
    #print m_text
    multifile = False
    if m_text:
      for j in ['-4', '-3', '-2', '-1', '']:
        if os.path.isfile(m_ffilename+j+m_ext):
          if j <> '' and not multifile:
            multifile = True
          if j == '' and multifile:
            os.rename(m_ffilename+j+m_ext, m_path+os.sep+m_text+'-1'+ m_ext)
          else:
            os.rename(m_ffilename+j+m_ext, m_path+os.sep+m_text+j+ m_ext)
  else:
    print 'Usage: ' + sys.argv[0] + ' <text> e.g.: ' + sys.argv[0] + 'E:\Share\club-074.mp4'
    sys.exit(1)        
  print "Finished"
  #print gc.garbage
  #del gc.garbage
  sys.exit(0)


'''
[
0..'hzgd-095',
1..'e:/t',
2..'http://mav/?s=hzgd-095',
3..u'http://mav/fhd-hzgd-095-%e6%81%af%e5%ad%90%e3%81%ae%e5%90%8c%e7%b4%9a%e7%94%9f%e3%82%92%e5%a6%8a%e5%a8%a0%e5%8d%b1%e9%99%ba%e6%97%a5%e3%81%ab%e3%83%9e%e3%83%b3%e3%83%81%e3%83%a9%e8%aa%98%e6%83%91-%e4%bd%90/',
4..u'HZGD-095 \u606f\u5b50\u306e\u540c\u7d1a\u751f\u3092\u598a\u5a20\u5371\u967a\u65e5\u306b\u30de\u30f3\u30c1\u30e9\u8a98\u60d1 \u4f50\u3005\u6728\u3042',
5..[u'http://img.mav.net/images/110hd095pl.jpg', u'http://img.mav.net/images/1100hzgd095jp-1.jpg']
]


#get_image('http://....1007.html')

for s in soup.findAll('a'):
  if repr(s.get('title'))[2] == '[':
    print s.get('href')

with open('./path_to_output_f.txt', 'a') as f:
  f.write("{}\t{}\t{}\t{}\n".format(username, auth, role, node))

def get_main(url, outpath):
  #html_file = open('sa-074.html', 'r')
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
