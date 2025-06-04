import yaml
from pynput import mouse

def read_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def on_move(x, y):
    if 'move' in config['log_events']:
        for _ in range(config['repeat_events']):
            print(f'Mouse moved to ({x}, {y})')

def on_click(x, y, button, pressed):
    if 'click' in config['log_events']:
        action = 'Pressed' if pressed else 'Released'
        for _ in range(config['repeat_events']):
            print(f'Mouse {action} at ({x}, {y}) with {button}')

def on_scroll(x, y, dx, dy):
    if 'scroll' in config['log_events']:
        direction = 'down' if dy < 0 else 'up'
        for _ in range(config['repeat_events']):
            print(f'Mouse scrolled {direction} at ({x}, {y})')

if __name__ == '__main__':
    config = read_config('config.yaml')
    with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        print("Mouse event logger started. Press Ctrl+C to exit.")
        listener.join()