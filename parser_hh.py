import requests
import json
from bs4 import BeautifulSoup
import re


HH_SEARCH_MAX_PAGES = 1


def get_json(url, params=None):
    params = params or {}
    return requests.get(url, params=params, timeout=10).json()


def extract_urls_of_page_vacancy_from_hh(query='разработчик'):
    
    urls_vacancies = []
    url_basic = 'http://api.hh.ru/vacancies'
    url_params = {
        'text': query,
        'area': 1,
        'items_on_page': 500,
        'page': 0
    }


    for page_number in range(HH_SEARCH_MAX_PAGES):
        url_params['page'] = page_number + 1
        url_enumeration = get_json(url_basic, params=url_params)
        
        if 'items' in url_enumeration.keys():
            if not url_enumeration['items']:
                break
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
        for i in range (len(key_skills)):
            j = key_skills[i]['name']
            j = j.lower()
            list_skills.append(j)
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
            'bootstrap',
            'c#',
            'c# .net',
            'c++',
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
        'Ваш профиль',
        'Вы нам подходите',
        'Знания',
        'кандидата мы хотим'
        'Кого мы ищем'
        'Мы ожидаем',
        'навыки',
        'Наш идеальный кандидат',
        'Наши пожелания',
        'Наши хотелки',
        'Необходимые знания',
        'Нужно знать',
        'Обязательно'
        'От вас мы ждем',
        'От кандидата мы ждем',
        'плюсом будет',
        'Пожелания',
        'С какими задачами будет работать',
        'соответствовать следующим требованиям',
        'Требования',
        'у Вас имеется',
        'Экспертиза'
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
            #'requirements': get_listing_requirements(get_json(urls_position[number_position])),
            # 'station_name': get_metro(get_json(urls_position[number_position])),
            # 'salary': get_salary(get_json(urls_position[number_position])),
            # 'experience': get_experience(get_json(urls_position[number_position])),
            # 'employer_url': get_json(urls_position[number_position])['employer']['url']
        }
        list_description_vacancy.append(description_vacancy)
        
    return list_description_vacancy


def reading_users_skills():
    
    list_input_skill = []
    while True:
        user_skill = input('Введите ваш навык: ') 
        if user_skill == 'no':
            break
        else:
            list_input_skill.append(user_skill)

    result_vacancy = {}
    listing_description_position = get_description_position()
    for description_position in listing_description_position:
        set_key_skills = description_position['key_skills']
        index_vacancy = 0
        for skill in set_key_skills:        
            for input_skill in list_input_skill:
                if input_skill in skill:
                    index_vacancy += 1
                    result_vacancy[description_position['api_url']] = index_vacancy


    return result_vacancy


def make_search_result():
    dict_users_skills = reading_users_skills()
    index_users_skills = dict_users_skills.values()
    list_index_users_skills = []
    api_search_result = []
    for index in index_users_skills:
        list_index_users_skills.append(index)
    list_index_users_skills.sort()

    for key in dict_users_skills:
        listu = [
        list_index_users_skills[-1],
        list_index_users_skills[-2],
        list_index_users_skills[-3]
        ]

        for max_index in listu:
            if max_index > 1:
                if dict_users_skills[key] == max_index:
                    api_search_result.append(key)
                    break

    return api_search_result


def print_search_result():
    data_description_vacancy = get_description_position()
    final_search_result_list_api_urls = make_search_result()
    print_final_result =[]
    if len(final_search_result_list_api_urls) > 0:
        for api_url_result in final_search_result_list_api_urls:
            for vacancy_description in data_description_vacancy:
                if api_url_result == vacancy_description['api_url']:
                    print_final_result.append(vacancy_description)

        return print_final_result
    else:
        return 'Нет подходящих вакансий'


if __name__ == '__main__':
    print(print_search_result())
    