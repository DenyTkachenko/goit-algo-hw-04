from __future__ import annotations

import argparse
import turtle

def koch(length: float, level: int):
    if level == 0:
        turtle.forward(length)
        return
    length /= 3.0
    koch(length, level - 1)
    turtle.left(60)
    koch(length, level - 1)
    turtle.right(120)
    koch(length, level - 1)
    turtle.left(60)
    koch(length, level - 1)

def snowflake(side: float, level: int):
    for _ in range(3):
        koch(side, level)
        turtle.right(120)

def main():
    parser = argparse.ArgumentParser(description="Візуалізація фракталу 'сніжинка Коха' (turtle).")
    parser.add_argument("--level", type=int, default=3, help="Рівень рекурсії (типово 3)")
    parser.add_argument("--length", type=float, default=300.0, help="Довжина сторони базового трикутника (типово 300)")
    parser.add_argument("--speed", type=int, default=0, help="Швидкість малювання (0..10), 0 = миттєво")
    parser.add_argument("--width", type=int, default=2, help="Товщина лінії (типово 2)")
    args = parser.parse_args()

    turtle.title(f"Koch Snowflake — level {args.level}")
    turtle.hideturtle()
    turtle.speed(args.speed)
    turtle.pensize(args.width)
    turtle.penup()
    turtle.goto(-args.length/2, args.length/3)
    turtle.pendown()

    snowflake(args.length, args.level)
    turtle.done()

if __name__ == "__main__":
    main()
