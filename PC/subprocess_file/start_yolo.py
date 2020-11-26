import requests


def main():
    response = requests.get('http://192.168.11.38:5000/api/start_yolo')

if __name__ == "__main__":
    main()