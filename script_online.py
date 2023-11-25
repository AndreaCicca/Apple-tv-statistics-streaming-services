import requests
from bs4 import BeautifulSoup
import json
from collections import Counter

def read_url_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        url = file.read().strip()
    return url

def fetch_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch HTML content from {url}. Status code: {response.status_code}")

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def extract_data(soup):
    data = {}
    countries = soup.find_all('div', class_='grid2col') + soup.find_all('div', class_='grid3col')

    for country in countries:
        h2_element = country.find('h2')
        country_name = h2_element.get('id') if h2_element else country.find_previous('h2').get('id')
        if country_name:
            services = [service.text.title() for service in country.find_all('li')]
            data.setdefault(country_name.title(), []).extend(services)

    return data

def clean_special_characters(s):
    # Rimuove caratteri di nuova linea, spazi non breaking e altri caratteri speciali non desiderati
    return s.replace('\n', '').replace('\xa0', '').strip()

def write_to_json(data):
    cleaned_data = {key: [clean_special_characters(value) for value in values] for key, values in data.items()}
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(cleaned_data, json_file, ensure_ascii=False, indent=4)

def top_services(data, top_count=10):
    all_services = [service for services in data.values() for service in services]
    counter = Counter(all_services)
    return counter.most_common(top_count)

def top_countries(data, top_count=10):
    countries_services_count = {country: len(services) for country, services in data.items()}
    sorted_countries = sorted(countries_services_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_countries[:top_count]

def generate_markdown(data, top_services_list, top_countries_list):
    markdown_content = "# Streaming Services Information\n\n"
    
    # Write top services
    markdown_content += "## Top 10 Services\n"
    for service, count in top_services_list:
        markdown_content += f"- {service}: {count} services\n"
    markdown_content += "\n"

    # Write top countries
    markdown_content += "## Top 10 Countries with Most Services\n"
    for country, count in top_countries_list:
        markdown_content += f"- {country}: {count} services\n"
    markdown_content += "\n"

    # Write detailed information
    markdown_content += "## Detailed Information\n"
    for country, services in data.items():
        markdown_content += f"### {country}\n"
        for service in services:
            markdown_content += f"- {service}\n"
        markdown_content += "\n"

    return markdown_content

def write_to_readme(markdown_content):
    with open('README.md', 'w', encoding='utf-8') as readme_file:
        readme_file.write(markdown_content)

def main():
    url_file_path = 'url.txt'
    url = read_url_from_file(url_file_path)

    html_content = fetch_html_content(url)
    soup = parse_html(html_content)
    extracted_data = extract_data(soup)
    write_to_json(extracted_data)

    top_services_list = top_services(extracted_data)
    top_countries_list = top_countries(extracted_data)

    markdown_content = generate_markdown(extracted_data, top_services_list, top_countries_list)
    write_to_readme(markdown_content)

if __name__ == "__main__":
    main()
