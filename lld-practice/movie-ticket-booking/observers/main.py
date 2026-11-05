from abc import ABC, abstractmethod

class NotifyObserver(ABC):
    @abstractmethod
    def notify(self, event):
        pass



class ConsoleObserver(NotifyObserver):
    def notify(self, event):
        print("Console Notificaton",event)