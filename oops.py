class computer:

    def __init__(self,cpu,ram):
       self.cpu=cpu
       self.ram=ram

    def config(self):
        print("Config is", self.cpu, self.ram)

comp1=computer('i5',16) #assigned to self comp1 #Object1
comp2=computer('i7',16) #assigned to self comp2 #Object2

#print(type(comp1))

# computer.config(comp1)
# computer.config(comp2)

comp1.config() 
comp2.config()

if comp1.ram==comp2.ram:
    print('same ram')