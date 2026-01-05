'''class computer:

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
    print('same ram')'''



'''class car:
     wheels=4                #class variable
     def __init__(self):     #constructor
          self.mil=10        #instance variable
          self.com="bmw"     #object variable
        
c1=car()                     #object 1
c2=car()                     #object 2

c1.mil=5
c2.com="audi"

car.wheels=6

print(c1.mil,c1.com,c1.wheels)
print(c2.mil,c2.com,c2.wheels)'''



'''class student:
    school="lfcs"

    def __init__(self,m1,m2,m3):
        self.m1=m1
        self.m2=m2
        self.m3=m3
    
    def avg(self):            #instance method
        return(self.m1+self.m2+self.m3)/3
    
    # def get_m1(self):          #get methods (accessors)
    #     return self.m1
    
    # def set_m2(self,value):    #set methods (mutators)
    #     self.m2=value
    
    @classmethod
    def getschool(cls):          #class method
        return cls.school
    
    @staticmethod
    def info():                  #static method
        # return "this is static method used for doing operations"
        print("this is static method used for doing operations")

s1=student(34,67,32)             #s1 goes to self
s2=student(89,32,75)             #s2 goes to self

print(s1.avg())
print(s2.avg())
print(student.getschool())
#print(student.info())

student.info()'''



class student:

    def __init__(self):
        


