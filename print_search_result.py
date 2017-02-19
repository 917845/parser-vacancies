import requests
import json
from bs4 import BeautifulSoup
import re


def reading_users_skills():
    
    list_input_skill = []
    while True:
        user_skill = input('Введите ваш навык: ')
        if user_skill == 'no':
            break
        else:
            list_input_skill.append(user_skill)

    result_vacancy = {}
    # listing_description_position = get_description_position()

    with open('json.txt', 'r', encoding='utf-8') as file_json:
        list_with_json = json.load(file_json)

    for description_position in list_with_json:
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
    # data_description_vacancy = get_description_position()

    with open('json.txt', 'r', encoding='utf-8') as file_json:
        list_with_json = json.load(file_json)

    final_search_result_list_api_urls = make_search_result()
    print_final_result =[] 

    if len(final_search_result_list_api_urls) > 0:
        for api_url_result in final_search_result_list_api_urls:
            for vacancy_description in list_with_json:
                if api_url_result == vacancy_description['api_url']:
                    dic_final_result = {
                    'name': vacancy_description['name_vacancy'],
                    'alternate_url': vacancy_description['alternate_url'],
                    'salary': vacancy_description['salary']
                    }
                    print_final_result.append(dic_final_result)

        return print_final_result
    else:
        return 'Нет подходящих вакансий'


if __name__ == '__main__':
    for result_vacancy in print_search_result():
        if result_vacancy['salary'] != None:
            if result_vacancy['salary']['salary_from'] != None:
                if result_vacancy['salary']['salary_to'] != None:
                    salary = '(Зарплата от ' + str(result_vacancy['salary']['salary_from']) + ' до ' + str(result_vacancy['salary']['salary_to']) +')'
                    line = result_vacancy['name'] +  ' ' + salary + ' ' + result_vacancy['alternate_url']
                else:
                    salary = '(Зарплата от ' + str(result_vacancy['salary']['salary_from']) + ')'
                    line = result_vacancy['name'] + ' ' + salary +  ' ' + result_vacancy['alternate_url']
            else:
                line = result_vacancy['name'] + ' ' + result_vacancy['alternate_url']
        else: 
            line = result_vacancy['name'] + ' ' + result_vacancy['alternate_url']
        print(line)
    