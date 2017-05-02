#!/usr/bin/python

import urllib2
import smtplib
import textwrap

SOLD_OUT_MAIL = 0
AVAILABLE_MAIL = 1

def sendMail( FROM, TO, SUBJECT, TEXT):

    message = textwrap.dedent("""\
                              From: %s
                              To: %s
                              Subject: %s
                              %s
                              """ % (FROM, ", ".join(TO), SUBJECT, TEXT))
    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(FROM, [TO], message)
    s.quit()

websites = {
    'bestbuy' : {
        'web' : 'http://www.bestbuy.com/site/nintendo-switch-32gb-console-gray-joy-con/5670003.p?skuId=5670003',
        'keyword' : 'sold out'
    },
    'target'  : {
        'web' : 'http://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-52052007',
        'keyword' : 'product not available'
    },
    'toysrus' : {
        'web' : 'http://www.toysrus.com/product/index.jsp?productId=119513636&cp=2255974.119659196&parentPage=family',
        'keyword' : 'out of stock'
    },
    'gamestop' :  {
        'web' : 'http://www.gamestop.com/nintendo-switch/consoles/nintendo-switch-console-with-gray-joy-con/141820',
        'keyword' : 'not available'
    }
}

for name, content in websites.iteritems():
    # handle empty entry
    if not content['web']:
        continue

    # handle network failure
    try:
        response = urllib2.urlopen(content['web'])
    except Exception, e:
        print '%-10s %s\n' % (name, e)
        continue

    html = response.read().lower()
    if html.find(content['keyword']) != -1:
        print '%-10s sold out\n' % name
        if SOLD_OUT_MAIL == 1:
            sendMail('gfxcc@ubuntu.com', 'yong_stevens@outlook.com', 'switch sold out', name)
    else:
        print '%-10s accessible\n' % name
        if AVAILABLE_MAIL == 1:
            sendMail('gfxcc@ubuntu.com', 'yong_stevens@outlook.com', 'switch might available now', name)
