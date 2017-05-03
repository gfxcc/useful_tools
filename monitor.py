#!/usr/bin/python

import urllib2
import smtplib
import textwrap

SOLD_OUT_MAIL = 0
AVAILABLE_MAIL = 0

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
    s.sendmail(FROM, TO, message)
    s.quit()

websites = {
    'bestbuy' : {
        'web' : {
            'gray' : 'http://www.bestbuy.com/site/nintendo-switch-32gb-console-gray-joy-con/5670003.p?skuId=5670003',
            'blue & red' : 'http://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/5670100.p?skuId=5670100'
        },
        'keyword' : ['\"buttonmessage\":\"sold out\"']
    },
    'target'  : {
        'web' : {
            'gray' : 'http://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-52052007',
            'blue & red' : 'http://www.target.com/p/-/A-52189185'
        },
        'keyword' : ['unavailable', 'not available']
    },
    'toysrus' : {
        'web' : {
            'gray' : 'http://www.toysrus.com/product/index.jsp?productId=119513636&cp=2255974.119659196&parentPage=family',
            'blue & red' : 'http://www.toysrus.com/product/index.jsp?productId=119513666&cp=2255974.119659196&parentPage=family'
        },
        'keyword' : ['out of stock']
    },
    'gamestop' :  {
        'web' : {
            'gray' : 'http://www.gamestop.com/nintendo-switch/consoles/nintendo-switch-console-with-gray-joy-con/141820',
            'blue & red' : 'http://www.gamestop.com/nintendo-switch/consoles/nintendo-switch-console-with-neon-blue-and-neon-red-joy-con/141887'
        },
        'keyword' : ['not available']
    },
    'walmart' : {
        'web' : {
            'gray' : 'https://www.walmart.com/ip/Nintendo-Switch-Gaming-Console-with-Gray-Joy-Con-N-A/55449983',
            'blue & red' : 'https://www.walmart.com/ip/Nintendo-Switch-Gaming-Console-with-Neon-Blue-and-Neon-Red-Joy-Con-N-A/55449981'
        },
        'keyword' : ['out of stock']
    }
}

for name, content in websites.iteritems():
    # handle empty entry
    # block walmart since too expensive
    if not content['web'] or name == 'walmart':
        continue

    for color, website in content['web'].iteritems():
        # handle network failure
        try:
            response = urllib2.urlopen(website)
        except Exception, e:
            print '%-10s %s\n' % (name, e)
            continue
        html = response.read().lower()


        if name == 'toysrus':
            output = open('index.html', 'w')
            print >> output, html


        for keyword in content['keyword']:
            if html.find(keyword) != -1:
                print '%-10s %-10s      sold out\n' % (name, color)
                if SOLD_OUT_MAIL == 1:
                    sendMail('gfxcc@ubuntu.com', 'yong_stevens@outlook.com', 'switch sold out', name)
            else:
                print '%-10s %-10s      accessible\n' % (name, color)
                if AVAILABLE_MAIL == 1:
                    sendMail('gfxcc@ubuntu.com', 'yong_stevens@outlook.com', 'switch might available now', name)
