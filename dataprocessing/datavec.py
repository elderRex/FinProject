class myvec:

    def __init__(self,x,y):
        self.loc = [x,y]
        self.data = []

    def insert(self,dat,time):
        self.data.append([dat,time])