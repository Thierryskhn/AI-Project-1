import piece
from color import Color;
class Board: 
    def __init__(self, num_players, list_players):
        self.num_players = num_players
        self.zones = self.create_zones(self.num_players)
        self.pieces = []
        self.list_players = list_players.copy
        self.coord_in_boards = self.zones[0]+self.zones[1]+self.zones[2]+self.zones[3]+self.zones[4]+self.zones[5]+self.zones[6]
        self.start_zones = {list_players[0]:self.zones[1],list_players[1]:self.zones[4]} if num_players==2 else {list_players[0]:self.zones[1],list_players[1]:self.zones[3],list_players[2]:self.zones[5]} #remplacer les nombres par les players?
        self.end_zones = {list_players[0]:self.zones[4], list_players[1]:self.zones[1]} if num_players == 2 else {list_players[0]:self.zones[4], list_players[1]:self.zones[6],list_players[2]:self.zones[2]}

#create each zones with the correct coordinates
    def create_zones(self,num_players):
        side_size = 4
        zones = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

        #start and end zones player 1
        for q in range(-side_size, 0):
            for r in range(side_size+1, side_size -q + 1):
                    zones[0].append((q,r,-q-r))
                    self.pieces.append(piece(self.list_players[0].id,self.list_players[0].color,(q,r,-q-r)) )
                    zones[4].append((-q,-r,q+r))
                    if num_players == 2 : self.pieces.append(piece(self.list_players[1].id,self.list_players[1].color,(-q,-r,q+r)) )



        
        for q in range(0, side_size + 1):
            for r in range(side_size - q+ 1, side_size + 1):
                zones[2].append((q,r,-q-r))
                zones[5].append((-q,-r,q+r))
                if num_players == 3 : self.pieces.append(piece(self.list_players[2].id,self.list_players[2].color,(-q,-r,q+r)) )
                

        # start and end zone player 3
        for q in range(side_size+1, 2*side_size+1):
            for r in range(-side_size, side_size -q + 1):
                zones[3].append((q,r,-q-r))
                if num_players == 3 : self.pieces.append(piece(self.list_players[1].id,self.list_players[1].color,(q,r,-q-r)) )
                zones[6].append((-q,-r,q+r))

        #neutral zone ie zone 0
        for q in range(-side_size, side_size + 1):
            r1 = max(-side_size, -q - side_size)
            r2 = min(side_size, -q + side_size)
            for r in range(r1, r2 + 1):
                zones[0].append((q,r,-q-r))

        return zones
    
def print_board(self):
    side_size = 8
    pieces_coordinates =  [piece.get_coords() for piece in self.pieces]
    for y in range(2*side_size+1):
        for x in range(3*side_size+1):
            if x%2 == y%2:
                q = int((x+y-20)/2) #x =2*q+r+12
                r = 8-y 
                coords = (q,r,-q-r)
                if not coords in self.coords_in_boards:
                    print(" ",end="")
                elif not coords in pieces_coordinates: 
                    print("*",end="")
                else:
                    p = self.pieces[pieces_coordinates.index(coords)]
                    print(p.get_color().value+str(p)+'\x1b[0m',end="") #use ansi coding for color 
            else: print(" ", end="")
        print()
    
