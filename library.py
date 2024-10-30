import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.books_with_words = []
        
        for i in range(len(book_titles)):
            book_title = book_titles[i]
            text = texts[i][:]
            self.books_with_words.append((book_title, text)) 

        self.books_with_words = self.merge_sort(self.books_with_words, key=lambda x: x[0])
    
        for i in range(len(self.books_with_words)):
            book_title, words_list = self.books_with_words[i]
            sorted_words = self.merge_sort(words_list)
            unique_words = []
            last_word = None
            
            for word in sorted_words:
                if word != last_word:
                    unique_words.append(word)
                    last_word = word
            
            self.books_with_words[i] = (book_title, unique_words)
    
    def merge_sort(self, items, key=None):
        if len(items) > 1:
            mid = len(items) // 2
            left_half = items[:mid]
            right_half = items[mid:]

            self.merge_sort(left_half, key=key)
            self.merge_sort(right_half, key=key)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if (key(left_half[i]) if key else left_half[i]) < (key(right_half[j]) if key else right_half[j]):
                    items[k] = left_half[i]
                    i += 1
                else:
                    items[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                items[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                items[k] = right_half[j]
                j += 1
                k += 1

        return items
    
    def distinct_words(self, book_title):
        left, right = 0, len(self.books_with_words) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_title, words = self.books_with_words[mid]
            
            if mid_title == book_title:
                return words
            elif mid_title < book_title:
                left = mid + 1
            else:
                right = mid - 1
        return []

    def count_distinct_words(self, book_title):
        left, right = 0, len(self.books_with_words) - 1
        while left <= right:
            mid = (left + right) // 2
            mid_title, words = self.books_with_words[mid]
            
            if mid_title == book_title:
                return len(words)
            elif mid_title < book_title:
                left = mid + 1
            else:
                right = mid - 1
        return 0
    
    def search_keyword(self, keyword):
        found_books = []

        for book_title, words in self.books_with_words:
            left, right = 0, len(words) - 1
            found = False

            while left <= right:
                mid = (left + right) // 2
                if words[mid] == keyword:
                    found = True
                    break
                elif words[mid] < keyword:
                    left = mid + 1
                else:
                    right = mid - 1
            
            if found:
                found_books.append(book_title)

        return found_books
    
    def print_books(self):
        for book_title, words in self.books_with_words:
            print(f"{book_title}: {' | '.join(words)}")


class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos       -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        self.parameters = params
        self.collision_type = None
        
        if name == "Jobs":
            self.collision_type = "Chain"
        elif name == "Gates":
            self.collision_type = "Linear"
        elif name == "Bezos":
            self.collision_type = "Double"

        self.hash_map = ht.HashMap(self.collision_type, self.parameters)
        self.books_list = [] 
    
    def add_book(self, book_title, text):
        book_words = ht.HashSet(self.collision_type, self.parameters)  
        for word in text:
            book_words.insert(word)
            
        self.hash_map.insert((book_title, book_words))
        self.books_list.append((book_title, book_words))
        
    def distinct_words(self, book_title):
        book_words = self.hash_map.find(book_title)
        
        if not book_words:
            return []
        
        distinct_words_list = []
        for slot in book_words.table:
            if self.collision_type == "Chain":
                if slot: 
                    for word in slot:
                        distinct_words_list.append(word)
            else:
                if slot is not None: 
                    distinct_words_list.append(slot)
        
        return distinct_words_list

    
    def count_distinct_words(self, book_title):
        book_words = self.hash_map.find(book_title)
        
        if book_words:
            return book_words.num_elements
        else:
            return 0 

    
    def search_keyword(self, keyword):
        results = []

        for book_title, book_words in self.books_list:
            if book_words.find(keyword):
                results.append(book_title) 
        
        return results 

    
    def print_books(self):
        for book_title, hash_set in self.books_list:
            print(f"{book_title}: {str(hash_set)}")
            
