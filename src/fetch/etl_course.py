import bs4

import json
import re
import sys

filename = sys.argv[1]
print(f'{filename}...')

with open(filename) as f:
    soup = bs4.BeautifulSoup(f, features="lxml")

def next_li_set(soup, text):
    co = soup.find(text=text)
    if co:
        return [ li.text.strip() for li in co.parent.parent.find_next_sibling('tr').find('ol').find_all("li") ]
    return []



course = {
        'file':filename,
        'course': soup.find(text=re.compile('.*Course Outline for.*')).next.next.strip(),
        'course_objectives' : next_li_set(soup, "Course Objectives"),
        'student_learning_outcomes' : next_li_set(soup, 'Student Learning Outcomes')
        }



with open(filename +".json", 'w') as out:
    json.dump(course, out, indent=2)
