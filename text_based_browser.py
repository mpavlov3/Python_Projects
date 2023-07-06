import requests
import os
import sys
from collections import deque
from bs4 import BeautifulSoup
import colorama

colorama.init()

pages_stack = deque()
downloaded_pages = {}


def save_file(path, name):
    if name not in downloaded_pages:
        return
    filename = name.split('//')[-1].split('/')[0].split('.')[0]
    with open(os.path.join(path, filename), 'wt', encoding='utf-8') as f:
        f.write(downloaded_pages[name])


def read_file(path, name):
    with open(os.path.join(path, name.split('/')[-1]), 'rt') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # Extract and display the text content without HTML tags for each desired tag
    tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    for tag in tags:
        if tag.name == 'a':
            formatted_content = f"{colorama.Fore.BLUE}{tag.get_text(strip=True)}{colorama.Style.RESET_ALL}" + '\n'
        else:
            formatted_content = tag.get_text()
            formatted_content += '\n'
        print(formatted_content)


def download_page(url):
    r = requests.get(url, verify=True)
    if r.status_code != 200:
        print("Error: Failed to download page")
        return
    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    formatted_content = ""
    for tag in tags:
        if tag.name == 'a':
            formatted_content += f"{colorama.Fore.BLUE}{tag.get_text(strip=True)}{colorama.Style.RESET_ALL}" + '\n'
        else:
            formatted_content += tag.get_text()
            formatted_content += '\n'
    downloaded_pages[url] = formatted_content
    pages_stack.appendleft(url)
    print(formatted_content)


def main():
    directory = sys.argv[1]
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            print("Error: Failed to create directory")
            return
    while True:
        option = input()
        if option == 'exit':
            break
        elif option in os.listdir(directory):
            pages_stack.appendleft(option)
            read_file(directory, option)
        elif option == 'back':
            if len(pages_stack) > 0:
                x = pages_stack.pop()
                print(downloaded_pages[x])
            else:
                break
        elif option.startswith('https://') or option.startswith('http://'):
            url = option
            download_page(url)
            save_file(directory, url)
        elif option[0] != "h":
            if '.' not in option:
                print("Invalid URL")
            else:
                url = 'https://' + option
                download_page(url)
                save_file(directory, url)


if __name__ == '__main__':
    main()
