from flask import Flask, render_template, request
import string

app = Flask(__name__)

# --- CIPHER ALGORITHMS ---
def caesar_cipher(text, shift, mode):
    result = ""
    if mode == 'decrypt':
        shift = -shift
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            result += shifted_char
        else:
            result += char
    return result

def vigenere_cipher(text, key, mode):
    result = ""
    key = key.upper()
    key_index = 0
    key = "".join(filter(str.isalpha, key))
    if not key:
        return "Error: Key must contain at least one letter."
    for char in text:
        if char.isalpha():
            direction = 1 if mode == 'encrypt' else -1
            shift = ord(key[key_index % len(key)]) - ord('A')
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - start + (shift * direction)) % 26 + start)
            result += new_char
            key_index += 1
        else:
            result += char
    return result

def rail_fence_cipher(text, rails, mode):
    if rails <= 1:
        return text
    if mode == 'encrypt':
        fence = [""] * rails
        rail = 0
        direction = 1
        for char in text:
            fence[rail] += char
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        return "".join(fence)
    elif mode == 'decrypt':
        pattern = []
        rail = 0
        direction = 1
        for i in range(len(text)):
            pattern.append(rail)
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction *= -1
        rail_counts = [0] * rails
        for r in pattern:
            rail_counts[r] += 1
        fence = []
        index = 0
        for count in rail_counts:
            fence.append(list(text[index:index+count]))
            index += count
        result = ""
        rail_index = [0] * rails
        for r in pattern:
            result += fence[r][rail_index[r]]
            rail_index[r] += 1
        return result

def playfair_cipher(text, key, mode):
    # 1. Prepare the text and key
    text = "".join(filter(str.isalpha, text.upper()))
    key = "".join(filter(str.isalpha, key.upper()))
    
    if not key:
        return "Error: Key must contain letters."
        
    # Remove J (standard Playfair convention)
    text = text.replace("J", "I")
    key = key.replace("J", "I")

    # 2. Build the 5x5 Grid
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # No J
    grid_chars = []
    for char in key + alphabet:
        if char not in grid_chars:
            grid_chars.append(char)
            
    grid = [grid_chars[i:i+5] for i in range(0, 25, 5)]

    # 3. Format text into pairs
    if mode == 'encrypt':
        pairs = []
        i = 0
        while i < len(text):
            a = text[i]
            b = text[i+1] if i+1 < len(text) else 'X'
            if a == b:
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2
    else:
        pairs = [text[i:i+2] for i in range(0, len(text), 2)]

    # Helper to find coordinates
    def get_coords(char):
        for r in range(5):
            for c in range(5):
                if grid[r][c] == char:
                    return r, c
        return 0, 0

    # 4. Apply Playfair rules
    result = ""
    for pair in pairs:
        r1, c1 = get_coords(pair[0])
        r2, c2 = get_coords(pair[1])

        direction = 1 if mode == 'encrypt' else -1

        if r1 == r2:
            # Same row: shift right (or left)
            result += grid[r1][(c1 + direction) % 5]
            result += grid[r2][(c2 + direction) % 5]
        elif c1 == c2:
            # Same column: shift down (or up)
            result += grid[(r1 + direction) % 5][c1]
            result += grid[(r2 + direction) % 5][c2]
        else:
            # Rectangle: swap columns
            result += grid[r1][c2]
            result += grid[r2][c1]

    return result

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        text = request.form.get('text', '')
        mode = request.form.get('mode')
        algorithm = request.form.get('algorithm')
        
        if algorithm == 'caesar':
            try:
                shift = int(request.form.get('shift', 3))
                result = caesar_cipher(text, shift, mode)
            except ValueError:
                result = "Error: Please enter a valid number for the shift key."
                
        elif algorithm == 'vigenere':
            key = request.form.get('vigenere_key', '')
            result = vigenere_cipher(text, key, mode)
            
        elif algorithm == 'railfence':
            try:
                rails = int(request.form.get('rails', 3))
                result = rail_fence_cipher(text, rails, mode)
            except ValueError:
                result = "Error: Please enter a valid number for the rails."
                
        elif algorithm == 'playfair':
            key = request.form.get('playfair_key', '')
            result = playfair_cipher(text, key, mode)
        
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)