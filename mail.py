#-*- encoding:utf-8 -*-

import email, getpass, poplib, sys,re,string
import httplib2,urllib2,json,urllib


token ='easytokehere'
website ='http://www.yourteamtoywebsite.cn/?'
hostname = 'pop.yourmailsite.cn'
todomail = 'yourtodomail@yourmailsite.cn'
passwd = 'yourtodomailpasswd'



def add_todo(uid,text):       
    text=text.replace(':','')
    values = {'c' : 'api',
              'a' : 'todo_add',
              'is_public' : '1',
              'text' : text.encode("UTF-8"),
              'uid' : uid,
              'stoken' : token, }
    data = urllib.urlencode(values)
    
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'User-Agent' : 'Magic Browser'
     }
     
    h = httplib2.Http(".cache")
    url=website+data
    resp, content = h.request(url, "GET",headers=headers)
    print resp


def get_users():
    h = httplib2.Http(".cache")
    url=website+'c=api&a=team_members&stoken='+token
    user={}
    resp, content = h.request(url, "GET",headers={'User-Agent' : "Magic Browser"})
    encodedjson=json.loads(content)
    for s in encodedjson['data']:
        user[s['email']]= s['id']
    return user



def my_unicode(s, encoding):
    if encoding:
        return unicode(s, encoding)
    else:
        return unicode(s)



def get_mails():
    mails={}
    p = poplib.POP3_SSL(hostname)
    try:
        # 使用POP3.user(), POP3.pass_()方法来登录个人账户
        p.user(todomail) 
        p.pass_(passwd)
    except poplib.error_proto: #可能出现的异常
        print('login failed')
    else:
        response, listings, octets = p.list()
        for listing in listings:
            user=''
            number, size = listing.split() #取出message-id
            number = bytes.decode(number)
            size = bytes.decode(size)            #取邮件头
            response, lines, octets = p.top(number , 0)
            for i in range(0, len(lines)):
                lines[i] = bytes.decode(lines[i])            
            message = email.message_from_string(string.join(lines,'\n')) 
            From = email.Header.decode_header(message['From'])
            for s in From:
                f = my_unicode(s[0], s[1])
                if '@' in f:
                    user=f.replace('<','').replace('>','')
            if user !='' :
                subject = email.Header.decode_header(message["Subject"])
                sub = my_unicode(subject[0][0], subject[0][1])
                mail={}
                mail[user]=sub
                mails[number]=mail
                p.dele(number)
        p.quit()
        return mails


users=get_users()
mails=get_mails()
for s in mails:
    mail=mails[s]
    for t in mail:
        try:
            uid=users[t]
            text=mail[t]
            add_todo(uid,text)
        except KeyError:
            print 'ErrorMail:'+t

        
        
##
##        #取邮件正文
##        response, lines, octets = p.retr(number)
##        for i in range(0, len(lines)):
##                lines[i] = bytes.decode(lines[i])
##        message = email.message_from_string('\n'.join(lines))
##        #print('-' * 72)
##        maintype = message.get_content_maintype()
##        #print maintype
##        part = message
##        while maintype == 'multipart':
##            part = part.get_payload()[0]
##            #print maintype
##            maintype = part.get_content_maintype()
##        if part.get_content_maintype() == 'text':
##            mail_content = part.get_payload(decode=True).strip()
##            #mail_content=html2text.html2text(mail_content)
##            #print(mail_content[0:50])
##
