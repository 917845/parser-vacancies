import json


def make_list_users_skills():

    list_input_skill = []
    for i in range(10):
        user_skill = input('Введите ваш навык: ')
        user_skill = user_skill.lower()
        if (user_skill == 'no' or user_skill == 'нет'):
            break
        elif len(user_skill) < 2:
            print('Вы не ввели свой навык. Для получения результата поиска введите "no" ')
            continue
        else:
            if user_skill not in list_input_skill:
                list_input_skill.append(user_skill)

    return list_input_skill


def make_list_vacancies_with_index():
    matching_vacancies = {}
    list_input_skills = make_list_users_skills()

    with open('json.txt', 'r', encoding='utf-8') as file_json:
        list_with_json = json.load(file_json)

    for description_position in list_with_json:
        set_key_skills = description_position['key_skills']
        index_vacancy = 0
        for skill in set_key_skills:        
            for input_skill in list_input_skills:
                if input_skill in skill:
                    index_vacancy += 1
                    matching_vacancies[description_position['api_url']] = index_vacancy

    return matching_vacancies


def make_result_api_urls():
    matching_vacancies = make_list_vacancies_with_index()
    list_index_users_skills = list(matching_vacancies.values())
    list_index_users_skills.sort()
    list_index_users_skills.reverse()

    list_index_users_skills[0:3]
    result_selection = []

    for index in list_index_users_skills[0:3]:
        if len(result_selection) == 3:
            break
        for matching_vacancy in matching_vacancies:
            if matching_vacancies[matching_vacancy] == index:
                result_selection.append(matching_vacancy)
                if len(result_selection) == 3:
                    break
            
    return result_selection


def search_result():

    with open('json.txt', 'r', encoding='utf-8') as file_json:
        list_with_json = json.load(file_json)

    final_search_result_list_api_urls = make_result_api_urls()
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


def get_print_view():
    matching_vacancies = search_result()
    if len(matching_vacancies) > 0:

        for position in matching_vacancies:
            if position['salary'] != None:
                if position['salary']['salary_from'] != None:
                    if position['salary']['salary_to'] != None:
                        salary_text = ' (от %d до %d) ' % (
                            position['salary']['salary_from'], position['salary']['salary_to']
                            )
                    else: 
                        salary_text = ' (от %d) ' % (position['salary']['salary_from'])

                else:
                    salary_text = ' (до %d) ' % (position['salary']['salary_to'])
                
                print('%s: %s %s' % (position['name'], salary_text, position['alternate_url']))
                continue

            else:
                print('%s: %s' % (position['name'], position['alternate_url']))
                continue
    else:
        print('Нет подходящих вакансий')


if __name__ == '__main__':
    get_print_view()
