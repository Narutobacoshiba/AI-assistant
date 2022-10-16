import os,sys
import imaplib
import json
import email
import time
import base64, quopri,re,binascii
import datetime
from yuki.settings import GMAIL_SETTINGS
from yuki.skills.skill import AssistantSkill
from yuki.skills.collection.internet import InternetSkills

class EmailSkill(AssistantSkill):
    @classmethod
    def stop_auto_check_email(cls,**kwargs):
        cls.console(info_log="Stop auto check email.")
        cls.run_auto_check_email = False

    @classmethod
    def check_email(cls,**kwargs):
        if cls.is_checking_email == False:
            cls.is_checking_email = True
            cls.response("sure, i will check email for you")
            new_emails = cls.get_new_email()
            if len(new_emails) > 0:
                cls.email_notifications(len(new_emails))
                cls.insert_into_file(new_emails,cls.skill_dir+"\\collection\\temp\\temporary_container.txt")
                cls.open_notification_console(cls.skill_dir+"\\collection\\temp\\temporary_container.txt")
            else:
                cls.response("You don't have any new mail")
            cls.is_checking_email = False

    @classmethod
    def auto_check_email(cls,**kwargs):
        if cls.run_auto_check_email == False:
            cls.run_auto_check_email = True
            while cls.run_auto_check_email:
                if cls.is_checking_email == False:
                    cls.is_checking_email = True
                    new_emails = cls.get_new_email()
                    if len(new_emails) > 0:
                        cls.email_notifications(len(new_emails))
                        cls.insert_into_file(new_emails,cls.skill_dir+"\\collection\\temp\\temporary_container.txt")
                        cls.open_notification_console(cls.skill_dir+"\\collection\\temp\\temporary_container.txt")
                    cls.is_checking_email = False
                    time.sleep(GMAIL_SETTINGS['sleep_time'])

    @classmethod
    def start_auto_check_email(cls,**kwargs):
        cls.console(info_log="Start auto check email.")
        cls.create_thread(cls.auto_check_email)

    @classmethod
    def email_notifications(cls,count_new_emails):
        response_mail = "My master you got {0} new mails\n\n".format(count_new_emails)
        cls.response(response_mail)
            

    @classmethod
    def get_new_email(cls):
        with open(cls.skill_dir+"\\collection\\temp\\temporary_time.txt","r") as f:
            try:
                lastest_email = json.loads(f.read())['email']
            except:
                lastest_email = 0.
            f.close()

        list_new_emails = []
        list_email = cls.get_recent_email()
        if len(list_email) > 0:
            for email_obj in list_email:
                if email_obj['header']['ts_time'] > lastest_email:
                    list_new_emails.append(email_obj)

            cls.update_temporary_lastest_email(list_email[len(list_email)-1]['header']['ts_time'])

        return list_new_emails

    @classmethod
    def get_recent_email(cls):
        def encoded_words_to_text(encoded_words):
            word_list = encoded_words.split(" ")
            res = ""
            for word in word_list:
                if "?UTF-8?" in word:
                    encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
                    charset, encoding, encoded_text = re.match(encoded_word_regex, word).groups()
                    if encoding == 'B':
                        byte_string = base64.b64decode(encoded_text)
                    elif encoding == 'Q':
                        byte_string = quopri.decodestring(encoded_text)
                    res += byte_string.decode(charset) + " "
                else:
                    res += word + " "
            return res

        def convert_to_vietnamese(input):
            output = ""
            l = len(input)
            i = 0
            while i < l:
                if input[i] == "=" and input[i+3] == "=":
                    if input[i+1:i+3].lower() in ["c3","c4","c5","c6"]:
                        try:
                            output += binascii.unhexlify(input[i+1:i+3]+input[i+4:i+6]).decode("utf-8")
                            i += 5
                        except:
                            output += input[i]
                
                    elif input[i+6] == "=" and input[i+1:i+3].lower() == "e1":
                        try:
                            output += binascii.unhexlify(input[i+1:i+3]+input[i+4:i+6]+input[i+7:i+9]).decode("utf-8")
                            i += 8
                        except:
                            output += input[i]
                    else:
                        output += input[i]           
                else:
                    output += input[i]
                
                i += 1
            
            return output

        final_result = []
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        my_email = GMAIL_SETTINGS['account']
        password = GMAIL_SETTINGS['password']
        try:
            mail.login(my_email, password)
            mail.list()

            mail.select("inbox") 
            result, data = mail.search(None, "ALL")

            ids = data[0] 
            id_list = ids.split() 
            email_id = id_list[-6:-1]

            for idd in email_id:
                email_object = {"header":{"subject":"","from":"","ts_time":0.,"date":""},"content":""}
                result, data = mail.fetch(idd, "(RFC822)") 
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(response_part[1].decode('utf-8'))
                        email_object['header']["subject"] = msg['subject']
                        email_object['header']["from"] = encoded_words_to_text(msg['from'])
                        email_object['header']["date"] = msg["date"]

                        l_date = msg["date"].split(" ")
                        date = ""
                        for i in range(0,5):
                            date += l_date[i] + " "

                        email_object['header']["ts_time"] = float(datetime.datetime.strptime(date[:-1], "%a, %d %b %Y %H:%M:%S").timestamp())

                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)
                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        try:
                            text = base64.b64decode(part.get_payload().encode("utf-8")).decode("utf-8")
                        except:
                            text = part.get_payload()
                        email_object['content'] += convert_to_vietnamese(text)

                final_result.append(email_object)
        except Exception as e:
            if InternetSkills.internet_availability():
                cls.console(error_log=imaplib.IMAP4.error)
    
        return final_result

    @classmethod
    def update_temporary_lastest_email(cls,lastest_email_time):
        if lastest_email_time > 0.0:
            with open(cls.skill_dir+"\\collection\\temp\\temporary_time.txt","w") as f:
                try:
                    temporary_lastest_time = json.loads(f.read())
                except:
                    temporary_lastest_time = {"email":0.}
                temporary_lastest_time["email"] = lastest_email_time
                json.dump(temporary_lastest_time,f)
                f.close()
            
    @classmethod
    def insert_into_file(cls,emails,file_path):
        f = open(file_path,"r+")
        try:
            background_notification = json.loads(f.read())
        except:
            background_notification = {}
        if not background_notification.get('email'):
            background_notification['email'] = []
            
        for new_email in emails:
            background_notification['email'].append(new_email)
        
        json.dump(background_notification,f)
        f.close()

         
        
        
