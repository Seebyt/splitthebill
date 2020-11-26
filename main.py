from __future__ import print_function
import cv2
import pytesseract
import numpy as np
import argparse



# Returns the user dict
def get_user_dict():
    user_dict = dict()

    user = ""
    while user == "":
        try:
            user = int(input("Wieviele Leute teilen heute?"))
            if user == 0:
                print("Noch eine null und dein Handy implodiert ;)")
        except:
            print("Bitte gib eine Zahl ein")
    counter = 0
    while counter < user:
        user_dict[input(f"Name von Nr.{str(counter + 1)}")] = ""
        counter += 1
    return user_dict



# Clean the image and return new_image
def clean_image(img="index1.jpg"):
    image = cv2.imread(img)

    alpha = 2.52  # Simple contrast control, 1.0 - 3.0
    beta = -60  # Simple brightness control, 0 - 100

    new_image = cv2.addWeighted(image, alpha, np.zeros(image.shape, image.dtype), 0, beta)
    return cv2.imwrite("index_new.jpg", new_image)



# Return a string from an image
def get_text_from_img():
    image = cv2.imread("index1.jpg")
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(image)
    return text



# extract needed  data from text
def get_item_dict(string=""):
    item_dict = dict()
    list = string.splitlines()

    for word in list:
        stripped = word.rstrip("+")
        word = stripped.rstrip()

        if word.endswith("B") or word.endswith("A"):
            word = word.rstrip("A")
            word = word.rstrip("B")
            word = word.rstrip()

            word_list = word.split()

            try:
                if len(word_list) == 3:
                    item_dict[word_list[0] + word_list[1]] = float(word_list[-1].replace(",", "."))

                elif len(word_list) == 4:
                    item_dict[word_list[0] + word_list[1] + word_list[2]] = float(word_list[3].replace(",", "."))

                else:
                    item_dict[word_list[0]] = float(word_list[1].replace(",", "."))

            except:
                print(f"{word_list} konnte  nicht gelesen werden")

    return item_dict



# GUI method, links data to gui logic
def gui_method(user_dict, item_dict):

    # prints the total sum to the user
    total_sum = 0
    total_values = item_dict.values()
    for value in total_values:
        total_sum += float(value)
    print(f"Die Rechnung beträgt insgesamt {total_sum}€")

    # prints the users to the screen
    counter = 1
    for i in user_dict:
        print(str(counter)  + ".    "+i)
        counter += 1

    # sorts single items to users
    runner = True
    while runner:

        user_index = False
        while user_index == False:
            try:
                user_index = input("Wer hatte einzelnde Items? \"1,3,4.. etc.\"")
            except:
                print("Bitte gib eine Zahl ein")

        user_index = user_index.replace(",", "").replace(" ", "").rstrip()

        if user_index == "q" or user_index == "Q":
            runner = False

        elif len(user_index) > len(user_dict):
            print("Bitte gib eine niedrigere Zahl ein")

        elif len(user_index) <= len(user_dict):

            for i in user_index:
                user_list = list(user_dict.keys())
                user = user_list[int(i) - 1]

                counter = 1
                for i in item_dict:
                    print(str(counter) + ".    " + i)
                    counter += 1

                item_index = ""
                while not isinstance(item_index, int):
                    try:
                        item_index = input(f"Welche Items gehören {user}? \"1, 2, 3, ... etc.\"")
                        item_index = item_index.replace(",","").replace(" ", "").rstrip()
                        item_index = int(item_index)

                    except:
                        print("Bitte gib eine Zahl ein")

                item_index = str(item_index)
                counter = 1
                for i in item_index:
                    item_list = list(item_dict.keys())

                    item = item_list[int(i) - counter]
                    counter += 1

                    if user_dict[user] == "":
                        user_dict[user] = float(item_dict[item])
                    else:
                        user_dict[user] = float(user_dict[user]) + float(item_dict[item])

                    item_dict.pop(item)
                    runner = False

    total_rest_sum = 0
    rest_values = item_dict.values()
    for value in rest_values:
        total_rest_sum += float(value)

    for i in user_dict:
        if user_dict[i] == "":
            user_dict[i] = total_rest_sum / (len(user_dict))
        else:
            user_dict[i] = float(user_dict[i]) + total_rest_sum / (len(user_dict))

    counter = 1
    for i in user_dict:
        print(f"{counter}.  {i}:    {round(user_dict[i], 2)}€")
        counter += 1
    exit()



# Main method, cleans image for reading text from it gives
def main():
    running = True
    while running:
        clean_image()
        text = get_text_from_img()
        item_dict = get_item_dict(text)
        user_dict = get_user_dict()
        gui_method(user_dict, item_dict)

main()