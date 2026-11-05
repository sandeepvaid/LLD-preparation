#parent Notificatio class

class Notification:
    def __init__(self, message):
        self.message = message

    def send(self):
        print(f"Sending notification: {self.message}")

    def message_formater(self):
        return f"Formatted message: {self.message}" 
    


#child EmailNotification class inheriting from Notification
class EmailNotification(Notification):
    def __init__(self, message, email_address):
        super().__init__(message) # Call the parent class constructor to initialize the message
        self.email_address = email_address

    def send(self):
        formatted_message = self.message_formater() # Use the method from the parent class to format the message
        print(f"Sending email to {self.email_address} with message: {formatted_message}")


#child SMSNotification class inheriting from Notification
class SMSNotification(Notification):
    def __init__(self, message, number):
        super().__init__(message)
        self.number = number;

    def send(self):
        formatted_message = self.message_formater()
        print(f"Sending SMS with message: {formatted_message} to this {self.number}")


# Create instances of the child classes and call their send methods
email_notification = EmailNotification("Hello, this is an email notification!", "user@example.com")
sms_notification = SMSNotification("Hello, this is an SMS notification!", "123-456-7890")   


email_notification.send()
sms_notification.send()