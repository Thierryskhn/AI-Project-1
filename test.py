git checkout import ASSIGNEMENT_1.piece as piece;
from ASSIGNEMENT_1.color import Color;

pieces = []
def create_zones():
        side_size = 4
        zones = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

        #start and end zones player 1
        for x in range(-side_size, 0):
            for y in range(side_size+1, side_size -x + 1):
                    zones[1].append((x,y,-x-y))
                    pieces.append(piece.Piece(1,Color.PURPLE,(x,y,-x-y),1))
                    zones[4].append((-x,-y,x+y))
        


        # start and end zone player 2
        for x in range(0, side_size + 1):
            for y in range(side_size - x + 1, side_size + 1):
                zones[2].append((x,y,-x-y))
                zones[5].append((-x,-y,x+y))
                pieces.append(piece.Piece(2,Color.RED,(x,y,-x-y),2))

    


        # start and end zone player 3
        for x in range(side_size+1, 2*side_size+1):
            for y in range(-side_size, side_size -x + 1):
                zones[3].append((x,y,-x-y))
                pieces.append(piece.Piece(3,Color.YELLOW,(x,y,-x-y),3))
                zones[6].append((-x,-y,x+y))
        
        

        #neutral zone ie zone 0
        for x in range(-side_size, side_size + 1):
            y1 = max(-side_size, -x - side_size)
            y2 = min(side_size, -x + side_size)
            for y in range(y1, y2 + 1):
                zones[0].append((x,y,-x-y))    
        

        return zones

zones = create_zones()
coordinates = zones[0]+zones[1]+zones[2]+zones[3]+zones[4]+zones[5]+zones[6]

def print_board(pieces):
    side_size = 8
    pieces_coordinates =  [piece.get_coords() for piece in pieces]
    for y in range(2*side_size+1):
        for x in range(3*side_size+1):
            if x%2 == y%2:
                q = int((x+y-20)/2) #x =2*q+r+12
                r = 8-y 
                coords = (q,r,-q-r)
                if not coords in coordinates:
                    print(" ",end="")
                elif not coords in pieces_coordinates: 
                    print("*",end="")
                else:
                    p = pieces[pieces_coordinates.index(coords)]
                    print(p.get_color().value+str(p)+'\x1b[0m',end="")
            else: print(" ", end="")
        print()
        
print_board(pieces)
                
            


        



