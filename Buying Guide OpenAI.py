import requests
import os
import openai
from dotenv import load_dotenv
load_dotenv()


def headers_details(username, password):
    import base64
    credential = f'{username}:{password}'
    token = base64.b64encode(credential.encode())
    code = {'Authorization': f'Basic {token.decode("utf-8")}'}
    return code


openai.api_key = os.getenv('OPEN_API_KEY')

def oai_questions(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    output = (response.get('choices')[0].get('text'))
    return output


def wp_paragraph(text):
    code = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return code

def wp_h2(text):
    code = f'<!-- wp:heading --><h2>{text.title()}</h2><!-- /wp:heading -->'
    return code

def wp_html_list(any_list):
    start = '<!-- wp:list --><ul>'
    for elements in any_list:
        start += f'<!-- wp:list-item --><li>{elements}</li><!-- /wp:list-item -->'
    ends = '</ul><!-- /wp:list -->'
    code = start + ends
    return code


file = open('keywords.txt', 'r+')
keyword_list=file.readlines()
file.close()

for keywords in keyword_list:
    keyword = keywords.strip().rstrip('\n')
    title = f'Best {keyword.title()} Buying Guide'

    slug = f'{keyword.replace(" ", "-")}-buying-guide'


    intro = oai_questions(f'Write 50 words intro about {keyword}')

    q_one = wp_h2(f'Why {keyword} is essential to buy?')
    q_answer_one = wp_paragraph(oai_questions(f'Write 50 words paragraph for Why {keyword} is essential to buy?').strip())

    q_two = wp_h2(f'What to consider when buying a {keyword}?')
    q_answer_two = wp_paragraph(oai_questions(f'Write 100 words paragraph for What to consider when buying {keyword}?').strip())

    q_three = wp_h2(f'Five short tips you need to follow when buying a {keyword}:')
    q_answer_three = oai_questions(f'Write five short tips you need to follow when buying {keyword}')
    q_answer_three_list = (q_answer_three.strip().split('\n\n'))
    q_answer_three_html_list = wp_html_list(q_answer_three_list)


    conclusion_h2 = wp_h2('Conclusion')
    conclusion = wp_paragraph(oai_questions(f'Write 50 words conclusion about {keyword}').strip())

    content = f'{q_one}'


    data = {
            'title': title,
            'content': content,
            'categories': '387',
            'slug': slug,
            'status': 'draft'
    }

    headers = headers_details('gafadmin', 'CjUj sPzv Ylxj 4VKB TWq6 odTB')
    endpoint = 'https://gafashion.net/wp-json/wp/v2/posts'
    r = requests.post(endpoint, data=data, headers=headers)


