class VignereTranslator:
    def __init__(self, key: int | str, alphabet: str = 'abcdefghijklmnopqrstuvwxyzæøå'):
        self.alphabet = alphabet
        self.encrypt_translations = []
        self.decrypt_translations = []
        self.set_key(key)

    def set_key(self, key: int | str) -> None:
        """
        Updates `self.encrypt_translations` and `self.decrypt_translations` (Ceasar shifts) based on the given key and `self.alphabet`.

        Parameters
            key
                Indicating the sequence of shifts performed in the encryption (Every letter/digit indicate one shift).
                The shifts are performed on `self.alphabet`. If the key is a string, containing characters not present in the alphabet, these characters will correspont to a 0-shift.
        """
        if key.isnumeric():
            numeric_key = [int(c) for c in key]
        else:
            numeric_key = [self.alphabet.find(c) + 1 for c in key]

        # Reset translations
        self.encrypt_translations = []
        self.decrypt_translations = []

        for num in numeric_key:
            shifted_alphabet = self.alphabet[num:] + self.alphabet[:num]
            self.encrypt_translations.append(str.maketrans(self.alphabet, shifted_alphabet))
            self.decrypt_translations.append(str.maketrans(shifted_alphabet, self.alphabet))

    def set_alphabet(self, alphabet: str) -> None:
        self.alphabet = alphabet

    def get_alphabet(self) -> str:
        return self.alphabet
    
    def translate(self, message: str, process: str = 'encrypt') -> str:
        """
        Run Vignere cipher on the `message`, either encrypting or decrypting the message.

        Parameters:
            `message`: Message to encrypt / decrypt
            `process`: Either 'encrypt' or 'decrypt', indicating what to do with the `message`
            
        Returns:
            Encrypted / Decrypted message.
        """ 
        translated_message = ""
        is_upper = False # Used to handle uppercase letters below
        char_num = 0 # Counting how many chars have been translated
        # Translate message, letter for letter
        for char in message:
            # Handling uppercase letters
            if char.isupper():
                char = char.lower()
                is_upper = True
            # Handling unknown chars (Kept as they are in the translated message)
            if char not in self.alphabet:
                translated_message += char
                continue            
            # ---Encryption / Decryption ---
            if process == 'encrypt': 
                translated_char = char.translate(self.encrypt_translations[char_num % len(self.encrypt_translations)])
            elif process == 'decrypt':
                translated_char = char.translate(self.decrypt_translations[char_num % len(self.decrypt_translations)])
            else:
                raise ValueError(f"`process` only has valid values 'encrypt' and 'decrypt', but was {process}")
            
            char_num += 1
            # ------------------------------

            # Make uppercase if input was uppercase
            if is_upper:
                translated_char = translated_char.upper()
                is_upper = False # Reset for the next char

            # Add result to the translated message
            translated_message += translated_char

        return translated_message


if __name__ == "__main__":
    key = input("""Let's prepare our Vignere cipher encryption by deciding on the key.
The key can be numeric (each digit indicating a shift) or a word (each letter indicating a shift)
Note: If the key only contains one number or character, the Vignere cipher will act like a normal Ceasar shift.
Key: """)
    alph_change = input("By default, we use the Norwegian alphabet. If you want to define your own alphabet, write it now. If not, simply press enter.\n")
    if alph_change == "":
        encryptor = VignereTranslator(key)
    else:
        encryptor = VignereTranslator(key, alphabet=alph_change)
    print("Now, let's do some encryption! Simply type in the message you want to encrypt!")
    modes = ['decrypt', 'encrypt']
    mode_chars = ['d', 'e']
    mode_idx = True # 0 or 1
    while True:
        print(f"""
Press 'k' to change key
      'a' to change alphabet
      'q' to quit
      '{mode_chars[not mode_idx]}' to {modes[not mode_idx]}
Or type message that you want to {modes[mode_idx]}!
""")
        message = input(f"Message to {modes[mode_idx]}: ")
        if message == 'q':
            break
        elif message == 'k':
            encryptor.set_key(input("New key: "))
            continue
        elif message == 'a':
            encryptor.set_alphabet(input("New alphabet: "))
            continue
        elif message == mode_chars[not mode_idx]:
            mode_idx = not mode_idx # Change mode
            continue

        translated_message = encryptor.translate(message, modes[mode_idx])
        print(f"{modes[mode_idx]}ed message: {translated_message}")