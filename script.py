from bs4 import BeautifulSoup
import json

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        return soup

def extract_data(soup):
    data = {}
    countries = soup.find_all('div', class_='grid2col') + soup.find_all('div', class_='grid3col')

    for country in countries:
        h2_element = country.find('h2')
        country_name = h2_element.get('id') if h2_element else country.find_previous('h2').get('id')
        services = [service.text for service in country.find_all('li')]
        data.setdefault(country_name, []).extend(services)

    return data

def write_to_json(data):
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def main():
    html_file_path = 'index.html'
    soup = parse_html(html_file_path)
    extracted_data = extract_data(soup)
    write_to_json(extracted_data)

if __name__ == "__main__":
    main()
