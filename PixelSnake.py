import os, time, random

width, height = 20, 10
snake = [(5, 5)]
direction = (1, 0)
food = (random.randint(0, width-1), random.randint(0, height-1))

def draw():
    os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(height):
        for x in range(width):
            if (x, y) == food:
                print("🍎", end="")
            elif (x, y) in snake:
                print("🟩", end="")
            else:
                print("⬛", end="")
        print()

while True:
    time.sleep(0.2)
    head = ((snake[0][0] + direction[0]) % width, (snake[0][1] + direction[1]) % height)
    if head == food:
        snake.insert(0, head)
        food = (random.randint(0, width-1), random.randint(0, height-1))
    else:
        snake.insert(0, head)
        snake.pop()
    draw()
