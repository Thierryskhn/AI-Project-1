class Board: 
    zones = dict
    def __init__(self,side_size,num_players):
       if num_players in (2,3,4,6) : self.num_players = num_players 
       else: self.num_players = 2 #number of players by default
       self.side_size = side_size #change the size of the board because why not?
       self.zones = self.create_zones(self.num_players,self.side_size)

#create each zones with the correct cooridnates
    def create_zones(self,num_players,side_size):
        zones = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}

        #start and end zones player 1
        for x in range(-side_size, 0):
            for y in range(side_size+1, side_size -x + 1):
                    zones[0].append((x,y))
                    zones[4].append((-x,-y))

        # start and end zone player 2
        for x in range(0, side_size + 1):
            for y in range(side_size - x + 1, side_size + 1):
                zones[2].append((x,y))
                zones[5].append((-x,-y))
                

        # start and end zone player 3
        for x in range(side_size+1, 2*side_size+1):
            for y in range(-side_size, side_size -x + 1):
                zones[3].append((x,y))
                zones[6].append((-x,y))

        #neutral zone ie zone 0
        for x in range(-side_size, side_size + 1):
            y1 = max(-side_size, -x - side_size)
            y2 = min(side_size, -x + side_size)
            for y in range(y1, y2 + 1):
                zones[0].append((x,y))