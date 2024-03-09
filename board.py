import piece
class Board: 
    def __init__(self, num_players, list_players):
        self.num_players = num_players
        self.zones = self.create_zones(self.num_players)
        self.pieces = []
        self.list_players = list_players
        self.coordinates = [self.zones[0],self.zones[1],self.zones[2],self.zones[3],self.zones[4],self.zones[5],self.zones[6]]
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


            



