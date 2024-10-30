from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
            
        "Chain": params = (z, table_size)
        "Linear": params = (z, table_size)
        "Double": params = (z1, z2, c2, table_size)
        '''
        pass
    
    def insert(self, x):
        pass

    def find(self, key):
        pass
    
    def get_slot(self, key):
        pass

    def get_load(self):
        pass
    
    def __str__(self):
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
    def polynomial_hash(self, key, z, table_size):
        hash_value = 0
        current_power = 1  
        for i, char in enumerate(key):
            if 'a' <= char <= 'z':
                char_value = ord(char) - ord('a')
            elif 'A' <= char <= 'Z':
                char_value = ord(char) - ord('A') + 26
            else:
                continue

            hash_value = (hash_value + char_value * current_power) % table_size
            current_power = (current_power * z) % table_size 

        return hash_value

    
    def secondary_hash(self, key, z2, c2):
        hash_value = 0
        current_power = 1 
        for i, char in enumerate(key):
            if 'a' <= char <= 'z':
                char_value = ord(char) - ord('a')
            elif 'A' <= char <= 'Z':
                char_value = ord(char) - ord('A') + 26
            else:
                continue

            hash_value = (hash_value + char_value * current_power) % c2
            current_power = (current_power * z2) % c2 

        return c2 - hash_value

    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.size = params[-1] 
        
        if collision_type == "Chain":
            self.table = [[] for _ in range(self.size)]
            self.z = params[0]

        elif collision_type == "Linear":
            self.table = [None] * self.size
            self.z = params[0]

        elif collision_type == "Double":
            self.table = [None] * self.size
            self.z1 = params[0]
            self.z2 = params[1]
            self.c2 = params[2]
        
        self.num_elements = 0 
        
    def insert(self, key):
        slot = self.get_slot(key)

        if self.collision_type == "Chain":
            if key not in self.table[slot]:
                self.table[slot].append(key)
                self.num_elements += 1

        elif self.collision_type == "Linear":
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return
                slot = (slot + 1) % self.size
                if slot == original_slot:
                    raise Exception("Table is full")
            self.table[slot] = key
            self.num_elements += 1

        elif self.collision_type == "Double":
            step_size = self.secondary_hash(key, self.z2, self.c2)
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return
                slot = (slot + step_size) % self.size
                if slot == original_slot:
                    raise Exception("Table is full")
            self.table[slot] = key
            self.num_elements += 1
    
    def find(self, key):
        slot = self.get_slot(key)

        if self.collision_type == "Chain":
            return key in self.table[slot]

        elif self.collision_type == "Linear":
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return True
                slot = (slot + 1) % self.size
                if slot == original_slot:
                    return False
            return False

        elif self.collision_type == "Double":
            step_size = self.secondary_hash(key, self.z2, self.c2)
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot] == key:
                    return True
                slot = (slot + step_size) % self.size
                if slot == original_slot:
                    return False
            return False
    
    def get_slot(self, key):
        return self.polynomial_hash(key, self.z1 if self.collision_type == "Double" else self.z, self.size)
    
    def get_load(self):
        return self.num_elements / self.size
    
    def __str__(self):
        result = []
        for entry in self.table:
            if self.collision_type == "Chain":
                if entry:
                    result.append(" ; ".join(str(item) for item in entry))
                else:
                    result.append("<EMPTY>")
            else:
                result.append(str(entry) if entry is not None else "<EMPTY>")
        return " | ".join(result)
    
    def rehash(self):
        old_table = self.table[:]
        new_size = get_next_size()
        self.size = new_size
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(self.size)]

        elif self.collision_type == "Linear":
            self.table = [None] * self.size

        elif self.collision_type == "Double":
            self.table = [None] * self.size

        self.num_elements = 0 
        
        for slot in old_table:
            if self.collision_type == "Chain":
                if slot:
                    for word in slot:
                        self.insert(word)
            else:
                if slot is not None:
                    self.insert(slot)


    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        self.collision_type = collision_type
        self.size = params[-1]
        
        if collision_type == "Chain":
            self.table = [[] for _ in range(self.size)]
            self.z = params[0]

        elif collision_type in ["Linear", "Double"]:
            self.table = [None] * self.size  
            self.z1 = params[0]
            if collision_type == "Double":
                self.z2 = params[1]
                self.c2 = params[2]

        self.num_elements = 0 
    
    def insert(self, x):
        key, value = x
        slot = self.get_slot(key)

        if self.collision_type == "Chain":
            for entry in self.table[slot]:
                if entry[0] == key:
                    return 
            self.table[slot].append((key, value))
            self.num_elements += 1

        elif self.collision_type == "Linear":
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return 
                slot = (slot + 1) % self.size
                if slot == original_slot:
                    raise Exception("Table is full")
            self.table[slot] = (key, value)
            self.num_elements += 1
            
        elif self.collision_type == "Double":
            step_size = self.secondary_hash(key, self.z2, self.c2)
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return  
                slot = (slot + step_size) % self.size
                if slot == original_slot:
                    raise Exception("Table is full")
            self.table[slot] = (key, value)
            self.num_elements += 1
    
    def find(self, key):
        slot = self.get_slot(key)

        if self.collision_type == "Chain":
            for entry in self.table[slot]:
                if entry[0] == key:
                    return entry[1]  
            return False  

        elif self.collision_type == "Linear":
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return self.table[slot][1]  
                slot = (slot + 1) % self.size
                if slot == original_slot:
                    return False 

        elif self.collision_type == "Double":
            step_size = self.secondary_hash(key, self.z2, self.c2)
            original_slot = slot
            while self.table[slot] is not None:
                if self.table[slot][0] == key:
                    return self.table[slot][1]
                slot = (slot + step_size) % self.size
                if slot == original_slot:
                    return False 
    
    def get_slot(self, key):
        return self.polynomial_hash(key, self.z1 if (self.collision_type == "Double" or self.collision_type == "Linear") else self.z, self.size)
    
    def get_load(self):
        return self.num_elements / self.size
    
    def __str__(self):
        result = []
        for entry in self.table:
            if self.collision_type == "Chain":
                if entry:
                    result.append(" ; ".join(f"({k}, {v})" for k, v in entry))
                else:
                    result.append("<EMPTY>")
            else:
                result.append(str(entry) if entry is not None else "<EMPTY>")
        return " | ".join(result)
    
    def rehash(self):
        old_table = self.table[:]
        new_size = get_next_size()
        self.size = new_size
        if self.collision_type == "Chain":
            self.table = [[] for _ in range(self.size)]

        elif self.collision_type == "Linear":
            self.table = [None] * self.size

        elif self.collision_type == "Double":
            self.table = [None] * self.size

        self.num_elements = 0 
        
        for slot in old_table:
            if self.collision_type == "Chain":
                if slot:
                    for item in slot:
                        self.insert(item)
            else:
                if slot is not None:
                    self.insert(slot)