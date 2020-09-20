print("Check if words are reversed")
user_choice = input("Enter your first word:  ")
user_second_choice = input("Enter your first word:  ")

#Reversing the words
user_reversed = user_choice[::-1]

if user_reversed == user_second_choice:
    print("These words are the reverse of the other")
else:
    print("These are not reversed words of each other")