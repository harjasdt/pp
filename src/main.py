# Import necessary libraries
# PyPDF2 is a library for working with PDF files
from PyPDF2 import PdfReader
import streamlit as st
# Import required modules from langchain package
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

# Import load_dotenv function from dotenv module
from dotenv import load_dotenv

# Import os module
import os

# Import regular expression module
import re

# Import json module for JSON manipulation
import json 

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Load environment variables from the .env file
load_dotenv(".env")
import tiktoken

# Initialize an empty list to store extracted skills
global skills 
skills=[]


# Create an empty container for dynamic content

container = st.empty()
container_height=200

global existing_content
existing_content='--------------LOGS HERE-------------------'
# Function to update the content of the container
def update_content(i):
    global existing_content
    # Append new content to existing content
    new_content = f"--> {i}\n"
    existing_content = new_content +'\n'+ existing_content
    
    container.markdown(f"<div style='height: {container_height}px; overflow-y: auto;background:black;color:red;'>{existing_content}</div>", unsafe_allow_html=True)


# PHASE 1
def parsing(text):
    # Define the pattern for section headings
    section_pattern = r"(Summary\n|Experience\n|Education\n|Interests\n|Personal Information\n|Recruiting Tools|Skills \(\d+\)|Similar Profiles)"

    # Use the pattern to find all section headings in the text
    section_headings = re.findall(section_pattern, text)

    # Extract sections using the section headings
    sections = {}
    take=1
    for i, heading in enumerate(section_headings):
        if(take==1):
          start_index=0
          # update_content(heading)
          end_index=text.index(heading)
          section_text = text[start_index:end_index]
          sections["Profile"]=section_text
          take=0
          start_index = text.index(heading)
          if i < len(section_headings) - 1:
              end_index = text.index(section_headings[i + 1])
          else:
              end_index = len(text)
          section_text = text[start_index+len(heading):end_index]
          sections[heading]=section_text
        else:

          start_index = text.index(heading)
          if i < len(section_headings) - 1:
              end_index = text.index(section_headings[i + 1])
          else:
              end_index = len(text)
          section_text = text[start_index+len(heading):end_index]
          if('skills' in heading.lower()):
              sections['Skills\n']=section_text
          else:   
                sections[heading]=section_text

    # # update_content the extracted sections
    # for i, section in enumerate(sections):
    #     update_content(f"Section {i + 1} --------------------------------------------------------:\n{section}")
        # update_content(f"Section {i + 1} --------------------------------------------------------:\n{section}\n{sections[section]}") 

    # Convert Python to JSON  
    json_object = json.dumps(sections, indent = 4,sort_keys=True) 
    
    # update_content JSON object
    # update_content(json_object)
    return json_object


def extract_profile(file_name):
    global json_object
    '''extracts text form te given file path and parses it ( stores as converted.txt file) into different sections and stores as json in data.json file '''
    reader = PdfReader(file_name) 
    # update_contenting number of pages in pdf file 
    total_pages=len(reader.pages)
    text=''
    for i in range(0,total_pages):
        page = reader.pages[i] 
        text+=page.extract_text()
    # update_content(text)
    with open('./data/processed/CONVERTED.txt', 'w',encoding='utf-8') as f:
        f.write(text)

    # text=""
    # with open('./data/processed/CONVERTED.txt',encoding='utf-8') as file:
    #     for line in file:
    #         text+=line
    # update_content(text)
    json_object = parsing(text)
    json_object = json.loads(json_object)


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens





def helper_json_llm(heading, spec):
    """
    Generate the JSON representation for the specified section.

    This function generates the JSON representation for the specified section
    based on the provided specifications. It dynamically handles the token length
    and uses OpenAI's GPT model to generate the JSON.

    Parameters:
    heading (str): The heading of the section.
    spec (str): The specifications for generating the JSON representation.

    Returns:
    str: The generated JSON representation.
    """
    # Extract text from JSON object based on heading
    text = json_object[heading]

    # Create the prompt template
    temp = f'Generate only the JSON representation for each of the individuals {spec}. if some information is not found use NOT GIVEN as default. Do not change key name in the output format given and make sure json is formatted correctly.\n {text}'

    # Calculate total tokens for the prompt
    tkn_total = num_tokens_from_string(temp, "cl100k_base")
    update_content(f'Total Tokens for {heading.strip()} are {tkn_total}')

    # Initialize OpenAI API
    llm = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
         max_tokens=4090 - tkn_total # dynamic token length handling
    )

    # Define prompt template
    prompt = PromptTemplate(
        input_variables=["temp"],
        template="{temp}"
    )

    # Initialize LLMChain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)

    # Generate JSON representation using the chain
    text_json = chain.run(temp=temp)

    # Update JSON object with the generated JSON representation
    json_object[heading] = text_json

    # update_content completion message
    update_content(f'{heading.strip()} JSON done')

    return text_json

    

# Parse the summary section of the JSON object and extract skill phrases.
# The following functions checks if the key 'Summary'etc  exists in the JSON object.
# If found, it extracts skill phrases from the candidate summary.
# The extracted skills are returned in a RFC8259 compliant JSON response format.
def helper_skill_llm(heading):
   
    # Extract text from JSON object based on heading
    text = json_object[heading]

    # Create the prompt template
    temp = f'Generate a python unnumbered list of all the senseble industrial skill phrases that you can extract form the following description  ,\
        return in the following format  [\'skill 1\',\'skill2\'] .do not include numbers and organization names.\n {text}'
            
            # Output format:
            # {{
            #     "key1":"value1",
            # }}'

    # Calculate total tokens for the prompt
    tkn_total = num_tokens_from_string(temp, "cl100k_base")
    update_content(f'Total Tokens for {heading.strip()} are {tkn_total}')

    # Initialize OpenAI API
    llm = OpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
         max_tokens=4090 - tkn_total # dynamic token length handling
    )

    # Define prompt template
    prompt = PromptTemplate(
        input_variables=["temp"],
        template="{temp}"
    )

    # Initialize LLMChain
    chain = LLMChain(llm=llm, prompt=prompt, verbose=False)

    # Generate JSON representation using the chain
    skills= chain.run(temp=temp)
    print(type(skills))
    skills=eval(skills)
    print(type(skills))
    with open('./data/processed/skills.txt', 'a',encoding='utf-8') as f:
        # Iterate over each skill in the 'skills' list
        for skill in skills:
            # Write each skill to the file, followed by a newline character
            f.write(skill + '\n')

    print(skills)
    # update_content completion message
    update_content(f'{heading.strip()} skill done')


def parsing_section_experience():
    if('Experience\n' in json_object):

        helper_skill_llm('Experience\n')
        return helper_json_llm('Experience\n','''employment history divided by companies, only provide a  compliant JSON response  following this format.
    {
        "GeoLocation": location as provided in the following format.
                        {"city": city name,
                        "country": country name,
                        "state": state name}
        "company": comapny name,
        "title": job title,
        "Start_Date": start date,
        "End_Date": end date,
        "span": duration spent in this position,
        "responsibilities": list of responsibilities,
        "Skills": list all the acquired skills from the responsibilities of the current subsection only. do not include any other data.
                         present only the name of the skills in the following format. 
                        {
                        "Skill Count":"serial number,
                        "SkillName":"the actual skill name"

                         }
    }''')

def parsing_section_profile():
    if('Profile' in json_object):

        helper_skill_llm('Profile')
        helper_json_llm('Profile','''profile details. only provide a  RFC8259 compliant JSON response  following this format and ignore other information.
    {
        "Name": "Name of the person",
        "Current_Job_Title": "Current job role",
        "Current_Company": "current working company",
        "Location": "location of the person working at"
    }''')

def parsing_section_education():
    if('Education\n' in json_object):
        helper_skill_llm('Education\n')
        helper_json_llm('Education\n','''education history divided by schools, only provide a  RFC8259 compliant JSON response  following this format.
    {
        "degree": "the degree done",
        "end_year":"end year of the degree"
        "institute": "Instituition name",
        "major": "the major course done",
        "start_year":'start year of the degree',
        "duration":"duration of the course" 
    }''')

def parsing_section_interests():
    if('Interests\n' in json_object):
        helper_json_llm('Interests\n','interests divided by persons')

def parsing_section_skills():
    if('Skills\n' in json_object):
        helper_skill_llm('Skills\n')
        return helper_json_llm('Skills\n','''skills divided properly  only provide a  RFC8259 compliant JSON response  following this format.
    {
        "Skill Count": "Skill serial number",
        "Skill": "Skill name",
        "Endrosements": "the skill Endrosements",
        "Details": "the details"
    }''')

def parsing_section_summary():
    if('Summary\n' in json_object):
        helper_skill_llm('Summary\n')
        return helper_json_llm('Summary\n','''skills.You are a world class recruiter. Extract set of skill phrases from the candidate summary given.only provide a  RFC8259 compliant JSON response  following this format.
    {
        "Skill Count": "Skill serial number",
        "Skill": "Skill name",
    }''')

def parsing_section_main():
    """
    Parse various sections of data and save the results to a JSON file.

    This function calls other parsing functions to parse different sections of data,
    including experience, profile, education, interests, skills, and summary.
    The parsed data is then saved to a JSON file named 'data.json'.

    Parameters:
    None

    Returns:
    None
    """
    with open('./data/processed/skills.txt', 'w',encoding='utf-8') as f:
        f.write('')
    parsing_section_experience()
    # parsing_section_profile()
    # parsing_section_education()
    # parsing_section_interests()
    parsing_section_skills()
    # parsing_section_summary()
    with open('./data/processed/data.json', 'w') as f:
        json.dump(json_object, f, indent=4, sort_keys=False)



def interface_test(path):
    
    
    # Extract profile from the PDF file 'test3.pdf'
    extract_profile(path)
    
    # Parse various sections of the extracted profile
    parsing_section_main()
