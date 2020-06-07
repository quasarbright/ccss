sample_text = '''My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink.

I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up.

I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone.'''


class Node:
    def __init__(self, left, right, frequency):
        self.left = left
        self.right = right
        self.frequency = frequency
    
    def decode(self, bits):
        decoded_message = ""
        while len(bits) > 0:
            next_character, bits = self.decode_next_character(bits)
            decoded_message += next_character
        return decoded_message
            
    def decode_next_character(self, bits):
        if len(bits) == 0:
            raise ValueError("invalid encoding")
        next_bit = bits[0]
        rest_bits = bits[1::]
        if next_bit == 0:
            return self.left.decode_next_character(rest_bits)
        else:
            return self.right.decode_next_character(rest_bits)


    def generate_encoding(self):
        encoding = {}
        self.generate_encoding_help([], encoding)
        return encoding

    def generate_encoding_help(self, path, encoding):
        self.left.generate_encoding_help(path + [0], encoding)
        self.right.generate_encoding_help(path + [1], encoding)
    

class Leaf:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
    
    def decode(self, bits):
        raise RuntimeError("tried to decode from a leaf")
    
    def decode_next_character(self, bits):
        return self.character, bits
    
    def generate_encoding(self):
        raise RuntimeError("tried to generate a leaf's encoding")
    
    def generate_encoding_help(self, path, encoding):
        encoding[self.character] = path


def make_initial_forest(text):
    # make text lowercase
    text = text.lower()
    
    # maps characters to their frequencies
    frequencies = {}
    
    # the characters allowed in the encoding
    legal_characters = 'abcdefghijklmnopqrstuvwxyz0123456789 .,\'\n'

    # initialize freqency of all characters to 0
    for character in legal_characters:
        frequencies[character] = 0
    
    #measure actual frequency of characters
    for character in text:
        if character not in frequencies:
            frequencies[character] = 1
        else:
            frequencies[character] += 1
    
    # our initial list of "trees" for each character
    forest = []
    for character in frequencies:
        frequency = frequencies[character]
        forest.append(Leaf(character, frequency))
    
    return forest

# make a forest from sample text
initial_forest = make_initial_forest(sample_text)

# print out letters sorted by frequency
sorted_forest = sorted(initial_forest, key=lambda leaf: -leaf.frequency)
sorted_characters = [leaf.character for leaf in sorted_forest]
print("frequencies:")
print("============")
for leaf in sorted_forest:
    print(f"{repr(leaf.character)}: {leaf.frequency}")
print()

# combine all leaves into one root node
def combine_forest(forest):
    while len(forest) > 1:
        def get_frequency(node):
            return node.frequency
        min1 = min(forest, key=get_frequency)
        forest.remove(min1)

        min2 = min(forest, key=get_frequency)
        forest.remove(min2)
        
        new_node = Node(min1, min2, min1.frequency + min2.frequency)
        forest.append(new_node)
    # now, only the root node is in the forest
    return forest[0]

root = combine_forest(initial_forest)
encoding = root.generate_encoding()

# print the encoding
print("encodings:")
print("==========")
for character in sorted_characters:
    print(f"{repr(character)}: {''.join(map(str, encoding[character]))}")
print()

def encode(message, root):
    # lowercase
    message = message.lower()
    encoding = root.generate_encoding()
    encoded_message = []
    for character in message:
        if character not in encoding:
            raise RuntimeError(f"unknown character: {character}")
        else:
            encoded_message += encoding[character]
    return encoded_message

def decode(message, root):
    return root.decode(message)