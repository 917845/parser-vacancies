import requests
import json
from bs4 import BeautifulSoup
import re


HH_SEARCH_MAX_PAGES = 100


def get_json(url, params=None):
    while True:
        try:
            params = params or {}
            return requests.get(url, params=params, timeout=(1, 10)).json()
        except (TimeoutError, ConnectionError):
            continue


def extract_urls_of_page_vacancy_from_hh(query='разработчик'):
    
    urls_vacancies = []
    url_basic = 'http://api.hh.ru/vacancies'
    url_params = {
        'text': query,
        'area': 1,
        'items_on_page': 20,
        'page': 0
    }

    for page_number in range(HH_SEARCH_MAX_PAGES):
        print(int(page_number/HH_SEARCH_MAX_PAGES*100))
        url_params['page'] = page_number + 1
        url_enumeration = get_json(url_basic, params=url_params)

        if ('items' in url_enumeration.keys() and url_enumeration != None):
            for vacancy in url_enumeration['items']:
                urls_vacancies.append(vacancy['url'])
        else:
            break

    return urls_vacancies


def get_metro(vacancy_info):
    if type(vacancy_info['address']) == dict:
        metro = vacancy_info['address']['metro']
        if type(metro) == dict:
            return metro['station_name']


def get_salary(vacancy_info):
    salary = vacancy_info['salary']
    if type(salary) == dict:
        salary_position = {'salary_from': salary.get('from'), 'salary_to': salary.get('to')}
        return salary_position


def get_experience(vacancy_info):
    experience = vacancy_info.get('experience')
    experience = experience.get('id')
    if 'between' in experience:
        experience = {'from': experience[7], 'to': experience[-1]}
        return experience
    elif 'more' in experience:
        return experience[-1]


def get_key_skills(vacancy_info):
    key_skills = vacancy_info['key_skills']
    list_skills = []
    if len(key_skills) > 0:
        for number_skill in range (len(key_skills)):
            skill = key_skills[number_skill]['name']
            skill = skill.lower()
            list_skills.append(skill)
    else:
        list_skills_from_description = [
            '.net framework',
            '1c',
            'английский',
            'контроль версий',
            'ооп',
            'реляцион',
            'сбд',
            'agile',
            'ajax',
            'android',
            'angularjs',
            'api',
            'bitbucket',
            'bootstrap',
            'c#',
            'c# .net',
            'c++',
            'celery',
            'css',
            'css3',
            'django',
            'flask'
            'git',
            'go',
            'html',
            'ios',
            'java',
            'javascript',
            'jquery',
            'json',
            'linux',
            'maven',
            'mdx',
            'mysql',
            'my sql',
            'mssql'
            't-sql',
            'nix',
            'nosql',
            'hibernate',
            'objective-c',
            'oracle',
            'perl',
            'php',
            'postgresql'
            'python',
            'ruby',
            'rubu on rails'
            'sharepoint',
            'scss',
            'sql',
            'slack',
            'spring framework',
            'stl',
            'swift',
            'tornado',
            'usability',
            'visual studio',
            'xcode',
            'xcode',
            'xml',
            'push',
            ]

        key_skills_from_description = get_listing_requirements(vacancy_info)
        
        for requirement in key_skills_from_description:
            for skills_from_description in list_skills_from_description:
                if skills_from_description in requirement:
                    list_skills.append(skills_from_description)
    
    list_skills = list(set(list_skills))
    
    return list_skills


def selection_requirements(vacancies_info):

    list_requirements = [
        'будет плюсом',
        'ваш профиль',
        'вы нам подходите',
        'знания',
        'кандидата мы хотим'
        'кого мы ищем'
        'мы ожидаем',
        'навыки',
        'наш идеальный кандидат',
        'наши пожелания',
        'наши хотелки',
        'необходимые знания',
        'нужно знать',
        'kбязательно'
        'от вас мы ждем',
        'от кандидата мы ждем',
        'плюсом будет',
        'пожелания',
        'с какими задачами будет работать',
        'соответствовать следующим требованиям',
        'требования',
        'у вас имеется',
        'экспертиза'
        ]

    result = vacancies_info.split('<strong>')
    
    for object_i in result:
        object_i = object_i.split('</strong>')
        for object_j in list_requirements:
            if len(object_i) > 1:
                if object_j in object_i[0]:
                    result = object_i[1]
            else:
                result = ''

    return result


def cleaning_text(element):
    text = str(element)
    text = text.lower()
    exclusion_list = [
        '<p>',
        '</p>',
        '</p'
        '•',
        '·',
        ';',
        '<li>',
        '</li>',
        '</br>',
        '<br/>',
        '</lu>',
        '<ul>',
        '</ul>',
        '</ul',
        '<em>',
        '</em>'
        '<>',
        '- ',
        '<',
        '/>',
        '<strong>',
        '</strong>',
        '<em>необходимая квалификация:</em>',
        '<em>желательно</em>'
        ]

    for element_exclude in exclusion_list:
        text = re.sub(element_exclude, '', text)

    if len(text) > 1:
        if text[0] == ' ':
            text = text[1:]
        if text[0] == '-':
            text = text[1:]
        if text[-1] == ' ':
            text = text[0:-1]
        if text[-1] == '.':
            text = text[0:-1]
    
    return text


def get_listing_requirements(vacancy_info):
    requirement = vacancy_info['description']
    requirement = requirement.lower()
    listing_requirements = []

    requirement = selection_requirements(requirement)

    soup = BeautifulSoup(requirement)
    soup = str(soup)

    if 'li' in soup:
        soup = BeautifulSoup(requirement)
        requirement = soup.find_all('li')
        for objective_li in requirement:
            objective_li = cleaning_text(objective_li)
            if len(objective_li) > 1:
                listing_requirements.append(objective_li)

    elif 'p' in soup:
        if 'br' not in soup:
            soup = BeautifulSoup(requirement)
            requirement = soup.find_all('p')
            for objective_p in requirement:
                objective_p = cleaning_text(objective_p)
                if len(objective_p) > 1:
                    listing_requirements.append(objective_p)

        else:
            requirement = soup.split('br')
            for objective_br in requirement:
                objective_br = cleaning_text(objective_br)
                if len(objective_br) > 1:
                    listing_requirements.append(objective_br)                

    return listing_requirements


# def get_listing_employers(url):
#     urls_position = urls_list_vacancies()
#     list_employer = []
#     for number_position in range(len(urls_position)):
#         urls_position = urls_position['employer']
#         description_employer = {
#             'name_employer': get_json(urls_position[number_position])['name'],
#             'url_employer': get_json(urls_position[number_position])['url'],
#             'vacancies_url': get_json(urls_position[number_position])['vacancies_url']
#         }    
#         list_employer.append(description_employer)

#     return description_employer


def get_description_position():
    urls_position = extract_urls_of_page_vacancy_from_hh()
    list_description_vacancy = []
    
    for number_position in range(len(urls_position)):
        print(int(number_position/(len(urls_position))*100))

        description_vacancy = {
            'id_vacancy': number_position + 1,
            'name_vacancy': get_json(urls_position[number_position])['name'],
            'alternate_url': get_json(urls_position[number_position])['alternate_url'],
            'key_skills': get_key_skills(get_json(urls_position[number_position])),
            'api_url': urls_position[number_position],
            'requirements': get_listing_requirements(get_json(urls_position[number_position])),
            # 'station_name': get_metro(get_json(urls_position[number_position])),
            'salary': get_salary(get_json(urls_position[number_position])),
            # 'experience': get_experience(get_json(urls_position[number_position])),
            # 'employer_url': get_json(urls_position[number_position])['employer']['url']
        }
        
        list_description_vacancy.append(description_vacancy)
        
    with open('json-2.txt', 'w', encoding='utf-8') as text_file:

        json.dump(list_description_vacancy, text_file)

if __name__ == '__main__':
    get_description_position()
    