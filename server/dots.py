class Game: 
    # dots = [0,1,2,3,4,5,6,7,8]
    col_size = 3
    row_size = 3

    numberOfPlayers = 2

    current_player_turn = 0

# (number of dots excluding far right col and bottom row)*2(2 connections for each dot) + 
#   (number of dots in far right col and bottom row)*1(one connection for each dot)
    totalNumberOfConnections = (((col_size*row_size)-(col_size+row_size-1))*2) + (col_size+row_size-2)

# 0 -> 1,3 // Store only the connection from lower number to higher number.
# 1 -> 2,4
    connections = {}
# 0 -> 1,2,3,4 means all 4 blocks are created around vertex 0
    closed_blocks = []


    def __init__(self):
    #     self.numberOfPlayers = numberOfPlayers
    #     closed_blocks = [None]*numberOfPlayers
        self.connections = {}
        self.closed_blocks = []

    def create_edge(self, x, y):
        # Check if it is a valid edge
        if (self.is_valid_edge(x,y) == False):
            print("eeeenn! Invalid edge!", x,y)
            return False
        # Check if it already exists
        if (self.is_exist(x,y) == True):
            print("pooooon! Already exists!", x,y)
            return False
        
        # connect the dots
        # edges.append(order_pair(x, y))
        (x, y) = self.order_pair(x, y)
        if (x not in self.connections):
            self.connections[x] = []
        self.connections[x].append(y)


        # process the turn
        # if is_block_closed(x, y):
        #     print("Closed blocks: ", closed_blocks)

        return True

# Determine whether a block is closed or not.
# Assume that x,y are such that x<=y.
# Find shortest cycle from current edge.
# that means find cycle of 1 unit edge from the current edge. 
# A block is said to be closed with connection x,y when 
#   x is connected with y
#   if the x,y connection direction is verticle
#       either (only if x%col_size != 0 or y%col_size != 0)
#           x -> x-1 , y -> y-1 , x-1 -> y-1  connections exists
#       or (only if (x+1)%col_size != 0 or (y+1)%col_size != 0)
#           x -> x+1, y -> y+1, x+1 -> y+1 connections exists
#   if the x,y connection direction is horizontal
#       either (only if x-col_size>=0 or y-col_size>=0)
#           x -> x-col_size, y -> y-col_size, x-col_size -> y-col_size connections exists
#       or (only if x+col_size<=col_size*row_size-1 or y+col_size<=col_size*row_size-1)
#           x -> x+col_size, y -> y+col_size, x+col_size -> y+col_size connections exists  
# Return: Way to spot the blocks: Lowest number in the block (0 -> 0,1,3,4)
    def is_block_closed(self, x, y):
        (x, y) = self.order_pair(x, y)

        current_connections = []

        if x+self.col_size == y: # Vertical
            if ((x%self.col_size != 0) and (x-1 in self.connections) and (y-1 in self.connections)): # Left side
                # Check the higher value in lower values list.
                if  ((x in self.connections[x-1]) and 
                    ((y in self.connections[y-1])) and
                    ((y-1) in self.connections[x-1])):
                    # closed_blocks.append(x-1)
                    # found = True
                    # return x-1
                    current_connections.append(x-1)

            if (((x+1)%self.col_size != 0) and (x+1 in self.connections) and (y in self.connections)): # Right side
                if (((x+1) in self.connections[x]) and
                    ((y+1) in self.connections[y]) and
                    ((y+1) in self.connections[x+1])):
                    # closed_blocks.append(x)
                    # found = True
                    # return x
                    current_connections.append(x)
                

        if x+1 == y: # Horizontal
            if ((x-self.col_size >= 0) and (x-self.col_size in self.connections) and (y-self.col_size in self.connections)): # Upper side
                if ((x in self.connections[x-self.col_size]) and
                    (y in self.connections[y-self.col_size]) and
                    ((y-self.col_size) in self.connections[x-self.col_size])):
                    # closed_blocks.append(x-self.col_size)
                    # found = True
                    # return x-self.col_size
                    current_connections.append(x-self.col_size)

            if ((x+self.col_size <= self.col_size*self.row_size-1) and (x+self.col_size in self.connections) and (y in self.connections)): # Down side
                if (((x+self.col_size) in self.connections[x]) and
                    ((y+self.col_size) in self.connections[y]) and
                    ((y+self.col_size) in self.connections[x+self.col_size])):
                    # closed_blocks.append(x)
                    # found = True
                    # return x
                    current_connections.append(x)

        self.closed_blocks.extend(current_connections)
        return current_connections


    def total_number_of_blocks(self):
        return (self.col_size*self.row_size) - (self.col_size+self.row_size-1)

    def is_valid_edge(self, x, y):
        (x, y) = self.order_pair(x, y)
        if (((x-self.col_size == y) and (x>self.col_size-1)) or
            ((x+self.col_size == y) and (x<self.col_size*self.row_size-self.col_size)) or
            ((x-1 == y) and (x%self.col_size != 0)) or
            ((x+1 == y) and ((x+1)%self.col_size != 0))):
            return True
        else:
            return False
    
# Assumes that the x,y pair is a valid pair
# FIX: check for case (0,1) (1,0), these are the same cases
    def is_exist(self, x, y):
        (x, y) = self.order_pair(x, y)

        if (x in self.connections):
            if (y in self.connections[x]):
                return True
        return False


    def order_pair(self, x, y):
        if x<y:
            return (x, y)
        else:
            return (y, x)



# create_edge(0,1) # Valid pair
# create_edge(1,4)
# create_edge(0,3)
# create_edge(2,5)

# create_edge(3,6)
# create_edge(4,7)
# create_edge(5,8)
# create_edge(6,7)
# create_edge(7,8)

# create_edge(3,4)
# create_edge(4,5)
# create_edge(1,2)

# create_edge(19,24)

# create_edge(0,4) # Invalid pair
# create_edge(0,1) # Invalid pair, already exist

# print(connections)

# 0__1__2
# |  |  |
# 3__4__5
# |  |  |
# 6__7__8

    def print_game(self):
        print("--Game data--")
        print("Connections: ", self.connections)
        print("Closed blocks: ", self.closed_blocks)
        print("-------------")

        for j in range(0, self.row_size):

            # i = i+j*col_size

            # print first row
            print(("0"+str(j*self.col_size)) if (j*self.col_size<10) else (str(j*self.col_size)), end="")
            for i in range(0, self.col_size-1): # from 0[][]1[][]2, don't insert anything after last bit
                print(("--" if self.is_exist(i+(j*self.col_size), i+(j*self.col_size)+1) else "  ") + (("0"+str(i+(j*self.col_size)+1)) if ((i+(j*self.col_size)+1)<10) else (str(i+(j*self.col_size)+1))), end="")

            print() # new line

            # print the verticle pipes
            print("|" if self.is_exist((j*self.col_size), (j*self.col_size)+self.col_size) else " ", end="")
            for i in range(0, self.col_size-1):
                print("  " + ("|" if self.is_exist(i+(j*self.col_size)+1, i+(j*self.col_size)+1+self.col_size) else " "), end="")
            
            print() # new line


        print() # End of displaying the game

# print_game()

# Game Logic
# turn = 1

# while totalNumberOfConnections>0: # connections can be made
#     print("Turn: ", turn)
#     print("Remaining connections: ", totalNumberOfConnections)
#     print("Closed blocks: ", closed_blocks)
#     print_game()
#     print("Enter first dot to connect:")
#     first_dot = int(input())
#     print("Enter second dot to connect:")
#     sec_dot = int(input())

#     if create_edge(first_dot, sec_dot) == False: # if connection unsuccessful
#         continue # Try asking them again since the connection was invalid
    
#     totalNumberOfConnections -= 1

#     # Update the turn
#     block_closed = is_block_closed(first_dot,sec_dot)
#     if block_closed == -1: # block not closed
#         if turn == numberOfPlayers:
#             turn = 1
#         else:
#             turn += 1
#     else: 
#         #Store which block is closed by which player
#         if turn not in closed_blocks:
#             closed_blocks[turn] = []
#         closed_blocks[turn].append(block_closed)


# game1 = Game()
# game1.print_game()
# game1.create_edge(0,1)
# game1.print_game()


# Game logic pending to own a block by player when closed.
# Manager players and turns.

# Overall game logic - 
# Client                    Server
# Player connects 2 dots -> Requests is made to the backend server to connect 2 dots.
# (which player made the move, which dots were connected) (is valid move, connect the dots, )
# Update all client UIs  <- notify all the registered clients about the move.