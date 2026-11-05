
# Interfaces are more than just method declarations, they are the foundation of flexible software design.

# Here are their most important characteristics:

# a) Defines Behavior Without Dictating Implementation
# An interface only declares what operations are expected. It doesn’t define how they are carried out.

# This gives freedom to implementers to provide their own version of the logic, while still honoring the same contract.

# b) Enables Polymorphism
# Different classes can implement the same interface in different ways.This allows your code to work with multiple implementations interchangeably.

# c) Promotes Decoupling
# Code that depends on interfaces is insulated from changes in the concrete classes that implement them.

# This makes your code easier to:

# Extend (add new implementations without modifying existing ones),
# Test (mock interfaces in unit tests),
# Maintain (fewer ripple effects from code changes).

from abc import abstractmethod

#create an interface class 
class MessageService:
    
    @abstractmethod
    def send_message(self, message):
        pass



#Implementing the interface in a concrete class
class EmailService(MessageService):
    def send_message(self, message):
        print(f"Sending email with message: {message}")

class SMSService(MessageService):
    def send_message(self, message):
        print(f"Sending SMS with message: {message}")


# Using the services via the interface
class NotificationManager:
    def __init__(self, service: MessageService):
        self.service = service

    def send_notification(self, message):
        self.service.send_message(message)


# Create instances of the services
email_service = EmailService();
sms_service = SMSService();
notification_manager = NotificationManager(email_service);
notification_manager.send_notification("Hello via Email!")
notification_manager.service = sms_service
notification_manager.send_notification("Hello via SMS!")            