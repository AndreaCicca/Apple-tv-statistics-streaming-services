import json
from collections import Counter

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def top_services(data, top_count=10):
    all_services = [service for services in data.values() for service in services]
    counter = Counter(all_services)
    return counter.most_common(top_count)

def top_countries(data, top_count=10):
    countries_services_count = {country: len(services) for country, services in data.items()}
    sorted_countries = sorted(countries_services_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_countries[:top_count]

def main():
    json_file_path = 'output.json'
    data = read_json(json_file_path)

    top_services_list = top_services(data)
    top_countries_list = top_countries(data)

    print("Top 10 services:")
    for service, count in top_services_list:
        print(f"{service}: {count} services")

    print("\nTop 10 countries with most services:")
    for country, count in top_countries_list:
        print(f"{country}: {count} services")

if __name__ == "__main__":
    main()
