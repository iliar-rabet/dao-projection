class MN:
    def __init__(self):
        print("init")
        self.measurements = 0
        self.distances=[]
        self.anchors=[]

    def new_measurement(self,dist,anch):
        self.measurements = self.measurements +1
        self.anchors.append(anch)
        self.distances.append(dist)



data={}
obj=MN()
obj.new_measurement(2,(2,3))
data['1']=obj
obj=MN()
data['2']=obj
print data['1'].anchors