# ANSI escape codes for text colors
COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'purple': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m'
}

@staticmethod
def color_print(text, color):
    """Print text in the specified color."""
    if color in COLORS:
        print(f"{COLORS[color]}{text}{COLORS['reset']}")
    else:
        print(text)

if __name__ == '__main__':
    # Example usage:
    color_print("This text is in red.",'red')
    color_print("This text is in green.",'green')
    color_print("This text is in yellow.",'yellow')
    color_print("This text is in blue.",'blue')
    color_print("This text is in purple.",'purple')
    color_print("This text is in cyan.",'cyan')
