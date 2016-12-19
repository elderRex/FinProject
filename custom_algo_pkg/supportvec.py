
import datetime
import math

class supvec:

    '''
    weather vector is <Max temp, Min temp, Humidity, Rain, Wind>
    '''
    def __init__(self,price,loc,time,date,weather=None):
        self.price = price
        self.loc = loc
        self.time = time
        self.date = date
        self.weather = weather

    def __str__(self):
        #t = datetime.datetime.fromtimestamp(float(self.time))
        return str(self.weather) + ' ' + str(self.price) + ' ' + str(self.date) +' '+ str(self.time)