from bs4 import BeautifulSoup
import requests
import os

print('Welcome to Job Finder\n')

print('What kind of skill you are searching a job for?')
skill = input('> ')
print(f'Searching jobs related to {skill}...\n')
skill = skill.replace(' ', '+')

print('What are some of the skills you are not familiar with?')
print('P.S (You can mention different skills with spaces in between)')
unfamiliar_skills = list(map(str, input('> ').split(' ')))
print(f'Filtering out {unfamiliar_skills}')

html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={skill.lower()}&txtLocation=').text
soup = BeautifulSoup(html_text, 'lxml')
jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

for index, job in enumerate(jobs):
    published_date = job.find('span', class_='sim-posted').span.text

    if 'few' or '1' in published_date:
        job_name = job.find('h3', class_='joblist-comp-name').text.strip()
        job_details = job.find('ul', class_='top-jd-dtl clearfix')
        job_location = job_details.find('span').text.replace(' ', '').strip()
        job_skills = job.find('span', class_='srp-skills').text.replace(' ', '').strip()
        job_url = job.find('a')['href']

        # checking whether skills are met by the user
        skill_met = True
        for skill in unfamiliar_skills:
            if skill_met and skill in job_skills.lower():
                skill_met = False

        if skill_met:
            # creating a directory to store all the company details
            path = './posts'
            if not os.path.exists(path):
                os.mkdir(path)

            # saving the resulted company details in a directory
            with open(f'posts/{index}.txt', 'w') as file:
                file.write(f'Company Name: {job_name}\n')
                file.write(f'Company Location: {job_location}\n')
                file.write(f'Skill Required: {job_skills}\n')
                file.write(f'More Info: {job_url}\n')
                print(f'File Saved: {index}')
