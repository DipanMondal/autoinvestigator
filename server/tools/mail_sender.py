import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

class MailSender:
    """
    This class is a utility class that sends mail to the receivers
    
    Functions:
    sendMail(message:str,dest:str) -> sends mail to a destination mail
    sendMailBatch(message:str,dests:list) -> sends mail to multiple receivers
    """
    def __init__(self):
        try:
            self.__sender_mail = os.getenv("SENDER_MAIL")
            self.__pass = os.getenv("MAIL_PASS")
            self.sender = smtplib.SMTP('smtp.gmail.com', 587)
            self.sender.starttls()
            self.sender.login(self.__sender_mail,self.__pass)
        except Exception as e:
            print("Error occured : \n",e)
            raise e
            
    def sendMail(self,message:str,dest:str)->bool:
        """
        Sends message to a particular receiver
        
        Args:
            message : message to be send
            dest : receiver's email id
        Returns:
            bool : True, on success False, on failure
        """
        try:
            self.sender.sendmail(self.__sender_mail,dest,message)
            return True
        except Exception as e:
            print("Something went wrong :\n",e)
            return False
            
    def sendMailBatch(self,message:str, dests:list)->int:
        """
        Sends mail to a list on receivers
        
        Args:
            message : message to be send
            dests : list receivers email ids
        Returns:
            int : number of successfully sent emails
        """
        nums=0;
        for dest in dests:
            if self.sendMail(message,dest):
                nums+=1
        return nums
        
    def __del__(self):
        self.sender.quit()
        
        
if __name__=='__main__':
    sender = MailSender()
    sender.sendMail(message="SegoMararni",dest="sabarna.saha1308@gmail.com")
    del sender
    
            
    
            
        