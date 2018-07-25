import xml.sax
import csv

class Joint:
    JointType = ""
    TrackingState = -1
    X = 0
    Y = 0
    Z = 0
    def __init__(self,JointType,TrackingState,X,Y,Z):
        self.JointType = JointType
        self.TrackingState = TrackingState
        self.X = X
        self.Y = Y
        self.Z = Z



class MovieHandler(xml.sax.ContentHandler):
    num = 0
    globalTab = ""  # 全局标签Joints
    localTab = ""  # 局部标签Position
    CurrentTab = ""
    JointType = ""
    TrackingState = -1
    X = -1
    Y = -1
    Z = -1
    Skeleton = []

    def __init__(self):
        pass
    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentTab = tag
        if tag == "Joints":
            self.globalTab = "Joints"
            print("**********解析开始**********")
        elif tag == "Joint":
            self.num += 1
            print("*****第%d个关节点*****" % self.num)
        elif tag == "Position":
            if self.globalTab == "Joints":
                self.localTab = "Position"

    # 内容事件处理
    def characters(self, content):
        if self.CurrentTab == "JointType":
            self.JointType = content
            print("JointType：", content)
        elif self.CurrentTab == "TrackingState":
            if self.globalTab == "Joints":
                print("TrackingState：", content)
                if content == "Tracked":
                    self.TrackingState = 1
                elif content == "Inferred":
                    self.TrackingState = 2
                else:
                    self.TrackingState = 3
        elif self.localTab == "Position":
            if self.CurrentTab == "X":
                self.X = content
                print("X：", content)
            if self.CurrentTab == "Y":
                self.Y = content
                print("Y：", content)
            if self.CurrentTab == "Z":
                self.Z = content
                print("Z：", content)

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "Joint":
            joint = Joint(self.JointType,self.TrackingState,self.X,self.Y,self.Z)
            self.Skeleton.append(joint)
        if tag == "Position":
            self.localTab = ""
        if tag == "Joints":
            self.globalTab = ""
            print("**********解析结束**********")
        self.CurrentTab = ""




if __name__ == '__main__':
    Skeleton = []
    temp = []
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    parser.parse("skeleton.xml")
    Skeleton = Handler.Skeleton

#["1,2,3","3,4,5,xz"]
    with open('test.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(Skeleton)):
            print(i)
            te = "%s,%s,%s,%s" %(Skeleton[i].X , Skeleton[i].Y , Skeleton[i].Z , Skeleton[i].TrackingState)
            temp.append(te)
        print(temp)
        writer.writerow(temp)