#Simple means don't repeat yourself. Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

# Example without DRY principle:

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def send_welcome_email(self):
        print(f"Sending welcome email to {self.email}")

    def send_password_reset_email(self):
        print(f"Sending password reset email to {self.email}")
# In this example, the email sending logic is duplicated in both methods. If we need to change how emails are sent, we would have to update both methods, which can lead to errors and maintenance issues.

# Example with DRY principle:

class Sender:
    @staticmethod
    def send_email(email, subject, body):
        print(f"Sending email to {email} with subject '{subject}' and body '{body}'")

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def send_welcome_email(self):
        Sender.send_email(self.email, "Welcome!", "Thank you for signing up!")

    def send_password_reset_email(self):
        Sender.send_email(self.email, "Password Reset", "Click here to reset your password.")

# In this refactored example, the email sending logic is centralized in the Sender class. Both methods in the User class call the same method to send emails, adhering to the DRY principle. This makes the code easier to maintain and reduces the chances of bugs when changes are needed.