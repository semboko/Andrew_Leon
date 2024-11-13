text = "UIF GJSTU MFUUFS JO UIF BMQIBCFU JT X"
key = -1

result = ""

for letter in text:
    letter = letter.upper()
    if 65 > ord(letter) or ord(letter) > 90:
        # Non-alphabetic
        result += letter
    else:
        # Alphabetic
        new_letter = ord(letter) + key
        new_letter = (new_letter - 65) % 26 + 65
        result += chr(new_letter)


print(result)
