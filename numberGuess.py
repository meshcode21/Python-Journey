from random import randint

sec_num = randint(1, 100)
counter = 10

while counter > 0:
    print(f"\nYou have {counter} attempts left.\n")

    try:
        num = int(input("Guess a number between 1 and 100: "))
    except ValueError:
        print("Please enter a valid number!")
        continue

    counter -= 1

    if num == sec_num:
        print("\n🎉 Correct! You guessed the number 🤩🥳\n")
        break

    if num < sec_num:
        print("Low...")
    else:
        print("High...")

    diff = abs(num - sec_num)

    if diff > 90:
        print("Very much far from the number 🤯 !!!")
    elif diff > 60:
        print("Too far from number 🫣 !!!")
    elif diff > 40:
        print("Far from the number 😥 !!!")
    elif diff > 20:
        print("Little bit far 🧐 !!!")
    elif diff > 10:
        print("Just little bit close 😌 !!!")
    elif diff > 5:
        print("Too close, just little 🤗 !!!")
    else:
        print("Almost you touched 😃 !!!")

if counter == 0:
    print(f"\n☹️ Game Over! The correct number was {sec_num}")