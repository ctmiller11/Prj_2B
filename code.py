class Intersection:
    def __init__(self, cordinates=None, connection=[], a_dist=-1, b_dist=-1, c_dist=-1,
                 aa=False, bb=False, cc=False):
        self.cordinates = cordinates
        self.connection  = connection
        self.a_dist = a_dist
        self.b_dist = b_dist
        self.c_dist = c_dist
        self.aa = aa
        self.bb = bb
        self.cc = cc

    def __str__(self):
        return str(self.cordinates)


import csv
import matplotlib.pyplot as plt # Core plotting support

STREETS = []
PARKING = []
LINES = []
POINTS = []
INTERSECTIONS = []
INTERSECTIONS2 = []

ten_st = [723,32]
fif_st = [733,270]
NAB = [760,555]

def main():
    reader = csv.reader(open('roads.csv'), delimiter=',', quotechar='|')
    n = 0
    for row in reader:
        if (n!=0):
            category = row[0]
            x1 = int(float(row[1]))
            y1 = int(float(row[2]))
            x2 = int(float(row[3]))
            y2 = int(float(row[4]))
            capacity = int(float(row[5]))
            comments = row[6]
            if category=="Street":
                STREETS.append([x1, x2, y1, y2, capacity])
                plt.plot([x1,x2], [y1,y2], 'k-')
            elif category=="Parking":
                PARKING.append([x1, x2, y1, y2, capacity])
                plt.plot([x1,x2], [y1,y2], 'r-')
            LINES.append([[x1,y1], [x2,y2]])
        n = n+1
    add_lines(LINES)
    # now lets set up the next connections by dist and set dist
    a = -1
    b = -1
    c = -1
    for i in range(0,len(INTERSECTIONS)):
        cord = INTERSECTIONS[i].cordinates
        if ((cord[0]==ten_st[0])and(cord[1]==ten_st[1])):
            a = i
            INTERSECTIONS[i].a_dist = 0
        elif ((cord[0]==fif_st[0])and(cord[1]==fif_st[1])):
            b = i
            INTERSECTIONS[i].b_dist = 0
        elif ((cord[0]==NAB[0])and(cord[1]==NAB[1])):
            c = i
            INTERSECTIONS[i].c_dist = 0
    INTERSECTIONS2 = (sorted(INTERSECTIONS, key=get_key))
    determine_a_distances(INTERSECTIONS[a])
    for i in range(0,len(INTERSECTIONS)):
        print(INTERSECTIONS[i].cordinates)
        print(INTERSECTIONS[i].a_dist)
        
    plt.show()

def determine_a_distances(item, back=None):
    I = item
    I.aa = True
    cons = I.connection
    for k in range(0,len(cons)):
        C = cons[k][0]
        num = I.a_dist + cons[k][1]
        if C.aa==False:
            C.a_dist = num
            #print(C.a_dist)
            determine_a_distances(C, I)
        elif C!=back and C.aa==True:
            if C.a_dist>num:
                C.a_dist = num
        
                
            

def p_dist(p1,p2):
    #print(p1,p2)
    return (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**0.5

def get_key(item):
    return (item.cordinates[0]+item.cordinates[1])

def add_point(p):
    boo = True
    if len(POINTS)!=0:
        for i in range(0,len(POINTS)):
            poi = POINTS[i]
            if poi==p:
                boo = False
        if boo:
            POINTS.append(p)
            INTERSECTIONS.append(Intersection(p))
    else:
        POINTS.append(p)
        INTERSECTIONS.append(Intersection(p))
    return boo

def add_lines(lines):
    for i in range(0,len(lines)):
        l = lines[i]
        p1 = l[0]
        p2 = l[1]
        c1 = add_point(p1)
        c2 = add_point(p2)
        if not((c1==False)and(c2==False)):
            add_connection(p1, p2)
            add_connection(p2, p1)

def add_connection(orig, dest):
    a = -1
    b = -1
    for i in range(0,len(INTERSECTIONS)):
        c = INTERSECTIONS[i].cordinates
        if orig==c:
            a = i
        elif dest==c:
            b = i
            
    # INTERSECTIONS[a] = origin Intersection
    # INTERSECTIONS[b] = destination Intersection
    (INTERSECTIONS[a].connection).append([INTERSECTIONS[b], p_dist(orig,dest)])























if __name__ == "__main__":
    main()





