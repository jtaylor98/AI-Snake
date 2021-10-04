from random import randint, uniform
from math import floor

class DNA():
    def __init__(self, net_struct):
        self.net_struct = net_struct
        self.data, self.length = self.generate(net_struct)
    
    def generate(self, net_struct): #generating DNA in from of byte array
        dna = []
        length = 0
        for i in range(1, len(net_struct)):
            length += net_struct[i] * net_struct[i-1]
            length += net_struct[i]
            dna.extend(uniform(-2,2) for _ in range(net_struct[i] * net_struct[i-1]))
            dna.extend(0 for _ in range(net_struct[i]))
        return dna, length
    
    def calc_length(self, net_struct): #counting # of coeff in NN to set as length for DNA
        length = 0
        for i in range(1, len(net_struct)):
            length += net_struct[i] * net_struct[i-1]
        length += sum(net_struct[1:])
        return length
    
    def multipoint_crossover(self, partner, mutation_rate):
        swap_points = [randint(0,(self.length)) for _ in range(int(self.length/10))]
        swap_points.sort()
        switch = False
        child_DNA = DNA(self.net_struct)
        for i in range(self.length):
            dna = self.data[:] if not switch else partner.DNA.data[:] #choosing which parent to inherit
            child_DNA.data[i] = dna[i]
            if uniform(0,1) < mutation_rate: #applying mutation
                child_DNA.data[i] += uniform(-1,1)
        return child_DNA
                
    def avg_crossover(self, partner, mutation_rate):
        child_DNA = DNA(self.net_struct)
        for i in range(self.length):
            avg = (self.data[i] + partner.DNA.data[i]) / 2
            child_DNA.data[i] = avg
            if uniform(0,1) < mutation_rate: #applying mutation
                child_DNA.data[i] += uniform(-1,1)
        return child_DNA
    
    def mutate(self, mutation_rate): #not used
        new_DNA = DNA(self.net_struct)
        for i in range(self.length):
            if uniform(0,1) < mutation_rate:
                self.data[i] = uniform(-1,1)  
        new_DNA.data = self.data[:]      
        return new_DNA
    #not used
    def crossover_bits(self, partner, mutation_rate): #bitwise
        swap_points = [randint(0,(self.length*8)) for _ in range(int(self.length/10))]
        swap_points.sort()
        switch = False
        child_DNA = DNA(self.net_struct, False)
        index = 0            
        for i in range(self.length*8):
            if index < len(swap_points):
                if i == swap_points[index]:
                    index += 1                
                    switch = not switch
            dna = self.data[:] if not switch else partner.DNA.data[:] #choosing which parent to inherit
            rem = (i % 8) #gives us index in sub list 
            shift = 8-rem-1
            bit = (dna[floor(i/8)] >> shift) & 1 #getting bit at specified index (&1 returns specified bit and flips remaining bits to 0)
            if uniform(0,1) < mutation_rate: #applying mutation
                bit = 1-bit #flipping bit
            bit <<= shift #shifting back to original position
            #noise not added since crossover done bitwise
            child_DNA.data[floor(i/8)] |= bit #adding bit to child dna
        child_DNA = self.add_noise(child_DNA)
        return child_DNA
    #not used
    def crossover_bytes(self, partner, mutation_rate):
        #color = partner.DNA.data.pop(-1)
        swap_points = [randint(0,(self.length*8)) for _ in range(int(self.length/10))]
        swap_points.sort()
        switch = False
        child_DNA = DNA(self.net_struct, False)
        index = 0            
        for i in range(self.length):
            if index < len(swap_points):
                if i == swap_points[index]:
                    index += 1                
                    switch = not switch
            dna = self.data[:] if not switch else partner.DNA.data[:] #choosing which parent to inherit
            byte = dna[i]
            if uniform(0,1) < mutation_rate: #applying mutation
                byte = 1-byte #flipping bit
            #noise not added since crossover done bitwise
            child_DNA.data = byte #adding bit to child dna        
        return child_DNA

