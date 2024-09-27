

from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager
from dotenv import load_dotenv
import os
import ast
import json
import autogen
from openai import OpenAI
load_dotenv()

def important_dates():
    data={
    "January": [
        "1: New Year's Day",
        "13: Lohri",
        "14: Makar Sankranti",
        "15: Pongal",
        "17: Guru Gobind Singh Jayanti",
        "26: Republic Day of India"
    ],
    "February": [
        "4: World Cancer Day",
        "8: Maha Shivratri",
        "14: Vasant Panchami"
    ],
    "March": [
         "1: Zero Discrimination Day",
        "25: Holi",
        "29: Good Friday"
    ],
    "April": [
        "1: April Fool’s Day",
        "9: Gudi Padwa",
        "9: Ugadi",
        "13: Baisakhi",
        "17: Ram Navami",
        "23: Hanuman Jayanti"
    ],
    "May": [
        "1: International Labour Day",
        "10: Eid al-Fitr",
        "23: Buddha Purnima"
    ],
    "July": [
        "7: Rath Yatra",
        "17: Muharram ",
        "21: Guru Purnima"
    ],
    "August": [
        "9: Nag Panchami",
        "15: Independence Day",
        "19: Raksha Bandhan",
        "26: Krishna Janmashtami"
    ],
    "September": [
        "5:Teachers Day",
        "7: Ganesh Chaturthi",
        "15: Onam"
    ],
    "October": [
        "2: Gandhi Jayanti",
        "12: Dussehra",
        "31: National Unity Day"
    ],
    "November": [
        "1: Diwali",
        "3: Bhai Dooj",
        "7: Chhath Puja"
    ],
    "December": [
        "25: Christmas"
    ]
    }
    
    return data

def extract_all_json_objects(text):
    objects = []
    start_index = 0
    while True:
        # Find the start of the next JSON object
        start_index = text.find('{', start_index)
        if start_index == -1:
            break

        # Initialize counters
        brace_count = 0
        in_string = False
        escape_char = False

        # Iterate through the text to find the matching closing brace
        for i in range(start_index, len(text)):
            char = text[i]
            
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                elif char == '"':
                    in_string = True
            else:
                if char == '"' and not escape_char:
                    in_string = False
                elif char == '\\':
                    escape_char = not escape_char
                else:
                    escape_char = False

            # If we've found a complete JSON object, add it to our list
            if brace_count == 0:
                json_string = text[start_index:i+1]
                try:
                    json_object = json.loads(json_string)
                    objects.append(json_object)
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON object: {json_string}")
                start_index = i + 1
                break

        # If we didn't find a closing brace, break the loop
        if brace_count != 0:
            break

    return objects    

def extract_json_from_braces(text):
    start_index = text.find('{')
    if start_index == -1:
        return None
    count = 1
    end_index = start_index + 1
    while end_index < len(text) and count > 0:
        if text[end_index] == '{':
            count += 1
        elif text[end_index] == '}':
            count -= 1
        end_index += 1
    json_string = text[start_index:end_index]
    return json_string

def extract_themes(datas,theme_storytelling):
    for data in datas:
        if isinstance(data, dict):
            if "Theme" in data and "Storyline" in data:
                theme_storytelling.append({
                    "Theme": data["Theme"],
                    "Storyline": data["Storyline"]
                })
            for value in data.values():
                extract_themes(value,theme_storytelling)
        elif isinstance(data, list):
            for item in data:
                extract_themes(item,theme_storytelling)


def planner_theme(l1, l2, l3, l4, info,  company_goals, target_audience, desired_outcomes):
    # n = posts_per_week

    planner = ConversableAgent(
    name="Planner",
    system_message=
    f"""You are an Observer in a group chat of Digital Marketing Campaign Planners. Your role is to listen to the other agents and ensure that each agent (A1, A2, A3, A4) speaks only once and in the specified order. Do not generate any output or contribute to the conversation.

    Information on the company: {info}
    Company Goals: {company_goals}
    Target Audience: {target_audience}
    Desired Outcomes: {desired_outcomes}
    """
    ,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
    human_input_mode="NEVER",
    )


    a1 = ConversableAgent(
        name="A1",
        system_message=f"""You are a Digital Marketing Expert tasked with generating storylines for a specific theme. Your instructions are as follows:

1. You will receive multiple themes in the list {l1}. Focus on each theme one at a time from the provided list.

2. Number of storylines: You will be given a specific number of themes separated by semicolon, generate one storyline per theme.

3. Output format: Your response MUST strictly adhere to the following JSON format:

    {{
        "Theme": "Exact theme in the list ",
        "Storyline": "Storyline"
    }}

4. Critical requirements:
   - Each storyline must be unique and directly related to the respective theme.
   - Do NOT repeat or duplicate any content.
   - Ensure the storylines match the themes accurately.
   
5. Company information: Use the following details to align the storylines with the company’s marketing strategy: {info}

6. Focus on the company goals: {company_goals}, target audience: {target_audience}, and desired outcomes: {desired_outcomes}.

7. Important: Do not add any explanation outside the JSON format.

Accuracy and adherence to the format are essential.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )


    a2 = ConversableAgent(
        name="A2",
        system_message=f"""You are a Digital Marketing Expert tasked with generating storylines for a specific theme. Your instructions are as follows:

1. You will receive multiple themes in the list {l2}. Focus on each theme one at a time from the provided list.

2. Number of storylines: You will be given a specific number of themes separated by semicolon, generate one storyline per theme.

3. Output format: Your response MUST strictly adhere to the following JSON format:

    {{
        "Theme": "Exact theme in the list ",
        "Storyline": "Storyline"
    }}

4. Critical requirements:
   - Each storyline must be unique and directly related to the respective theme.
   - Do NOT repeat or duplicate any content.
   - Ensure the storylines match the themes accurately.

5. Company information: Use the following details to align the storylines with the company’s marketing strategy: {info}

6. Focus on the company goals: {company_goals}, target audience: {target_audience}, and desired outcomes: {desired_outcomes}.

7. Important: Do not add any explanation outside the JSON format.

Accuracy and adherence to the format are essential.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )


    a3 = ConversableAgent(
        name="A3",
        system_message=f"""You are a Digital Marketing Expert tasked with generating storylines for a specific theme. Your instructions are as follows:

1. You will receive multiple themes in the list {l3}. Focus on each theme one at a time from the provided list.

2. Number of storylines: You will be given a number of themes separated by semicolon, generate one storyline per theme.

3. Output format: Your response MUST strictly adhere to the following JSON format:

    {{
        "Theme": "Exact theme in the list ",
        "Storyline": "Storyline"
    }}

4. Critical requirements:
   - Each storyline must be unique and directly related to the respective theme.
   - Do NOT repeat or duplicate any content.
   - Ensure the storylines match the themes accurately.

5. Company information: Use the following details to align the storylines with the company’s marketing strategy: {info}

6. Focus on the company goals: {company_goals}, target audience: {target_audience}, and desired outcomes: {desired_outcomes}.

7. Important: Do not add any explanation outside the JSON format.

Accuracy and adherence to the format are essential.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )


    a4 = ConversableAgent(
        name="A4",
        system_message=f"""You are a Digital Marketing Expert tasked with generating storylines for a specific theme. Your instructions are as follows:

1. You will receive multiple themes in the list {l4}. Focus on each theme one at a time from the provided list.

2. Number of storylines: You will be given a specific number of themes separated by semicolon, generate one storyline per theme.

3. Output format: Your response MUST strictly adhere to the following JSON format:

    {{
        "Theme": "Exact theme in the list ",
        "Storyline": "Storyline"
    }}

4. Critical requirements:
   - Each storyline must be unique and directly related to the respective theme.
   - Do NOT repeat or duplicate any content.
   - Ensure the storylines match the themes accurately.

5. Company information: Use the following details to align the storylines with the company’s marketing strategy: {info}

6. Focus on the company goals: {company_goals}, target audience: {target_audience}, and desired outcomes: {desired_outcomes}.

7. Important: Do not add any explanation outside the JSON format.

Accuracy and adherence to the format are essential.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )

    group_chat = GroupChat(
            agents=[a1, a2, a3, a4],
            messages=[],
            speaker_selection_method='round_robin',
            max_round=5,
        )
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
    )

    chat_result = manager.initiate_chat(
        planner,
        message= f"Information on the company: {info}",
        summary_method="reflection_with_llm",
        max_turns=2,
    )
    return group_chat


def generate_list(group_chat,list_data):
    theme_storytelling = []
    for message in group_chat.messages:
        if message['name'] != 'Planner':
            content = message['content']
            print(content)
            try:
                # Try to parse the entire content as JSON
                json_content = (extract_all_json_objects(content))
                extract_themes(json_content,theme_storytelling)
            except json.JSONDecodeError:
                # If JSON parsing fails, try ast.literal_eval
                try:
                    ast_content = ast.literal_eval(extract_all_json_objects(content))
                    extract_themes(ast_content,theme_storytelling)
                except (ValueError, SyntaxError):
                    # If both JSON and ast parsing fail, print an error message
                    print(f"Failed to parse content for message from {message['name']}")
    merged_themes = []
    for item in list_data:
        print("list_data",len(list_data),"theme_storytelling ", len(theme_storytelling))
        merged_item = item.copy()
        for story_item in theme_storytelling:
            if story_item["Theme"] == item["Theme"]:
                merged_item["Storyline"] = story_item["Storyline"]
                merged_themes.append(merged_item)
                break   
    return merged_themes



def prompt_generation(theme, storyline, info):
    task = (
        f"Generate a descriptive prompt to describe an image that visually represents "
        f"the concept of this storyline: '{storyline}', which is centered around the theme: '{theme}'. "
        f"Use the following company information to incorporate relevant details: {info}. "
        f"Ensure the image prompt is creative but simple, avoiding excessive elements, "
        f"and captures the essence of the storyline and theme in no more than 15 words."
    )

    prompt_generator = autogen.AssistantAgent(
        name="PromptGenerator",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None}, 
        system_message=(
            "You are a highly creative assistant specializing in generating descriptive image prompts. "
            "Your goal is to craft concise yet vivid prompts that effectively capture the user's storyline, "
            "theme, and relevant company information. Avoid overly complex details, focusing on clarity, creativity, and simplicity."
        )
    )

    # Example usage to generate a prompt
    response = prompt_generator.generate_reply(messages=[{"content": task, "role": "user"}])
    return response



def image_generator(prompt):
    
    client = OpenAI()

    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    return image_url

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def extract_number_of_posts(json_string):
    try:
        data = json.loads(json_string)
        number_of_posts = data['number_of_posts']
        return number_of_posts
    except KeyError:
        print("Error: 'number_of_posts' field not found in the JSON data.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON string.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    return None

# Define the system message for the PostCalculatorAgent


# Define the AutoGen agent
class PostCalculatorAgent(autogen.ConversableAgent):
    def __init__(self):
        super().__init__(
            name="PostCalculatorAgent",
            system_message= """You are a logical mathematician tasked with calculating the number of posts for an entire month based on specific requirements. Please follow these instructions:
- Role: Assume the role of a logical mathematician.
- Input: You will be given a requirement for post frequency.
- Calculation: Determine the total number of posts for the entire month based on the given requirement.
- Assumption: Consider one month to consist of exactly 4 weeks.
- Output: Generate a response that strictly adheres to the following JSON template:
{
 "detailed_explanation": "<step-by-step logic>"
 "number_of_posts": "<calculated total>",
}
- Template fields:
 "detailed_explanation": Provide a clear, step-by-step explanation of your calculation logic.
 "number_of_posts": Replace with the calculated total number of posts for the month.
- Response format: Ensure your entire response is in valid JSON format as shown in the template.
- Precision: Be accurate in your calculations and thorough in your explanation.
- Scope: Focus solely on the calculation and explanation based on the given input. Do not include any additional commentary or information outside the JSON structure.
""",
            llm_config={
                "config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"], "temperature" : 0}], "cache_seed": None
            }
        )

# Create an instance of the agent


# Create a user proxy agent


# Function to run a single exchange
def run_single_exchange(user_message):
    user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # Prevent any human input after initial message
    max_consecutive_auto_reply=0,  # Prevent any auto-replies
    code_execution_config={"use_docker": False}
    )
    post_calculator_agent = PostCalculatorAgent()
    # Initiate the chat with a single message
    user_proxy.initiate_chat(
        post_calculator_agent,
        message=user_message
    )
    
    # Get the agent's response
    last_message = post_calculator_agent.last_message()
    if last_message:
        number_of_posts = extract_number_of_posts(last_message['content'])
        return number_of_posts
    
def clean_and_parse_result(result):
    if isinstance(result, dict):
        return result
    
    if isinstance(result, str):
        # Remove any leading/trailing whitespace
        result = result.strip()
        
        # Try to parse as JSON first
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            pass
        
        # If JSON parsing fails, try to clean up the string and use ast.literal_eval
        try:
            # Remove any unexpected indentation
            lines = result.split('\n')
            cleaned_lines = [line.strip() for line in lines]
            cleaned_result = ''.join(cleaned_lines)
            
            # Replace single quotes with double quotes for JSON compatibility
            cleaned_result = cleaned_result.replace("'", '"')
            
            return ast.literal_eval(cleaned_result)
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing result: {e}")
            print("Cleaned result:", cleaned_result)
            return None
    
    print("Unexpected result type:", type(result))
    return None

def calendar_scheduler(calendar_of_month, theme, storyline, festivals, dates_blocked):
    task = f"""
    Schedule the following storyline: '{storyline}', which is centered around the theme: '{theme}',
    to be posted on an available date in the given calendar month. Follow these guidelines:

    1. Calendar: {calendar_of_month}
    2. Theme: {theme}
    3. Storyline: {storyline}
    4. Festivals: {festivals}  
    5. Blocked Dates: {dates_blocked}  

    Guidelines:
    - If the storyline and theme align with a festival date, assign it to that date.
    - If no alignment with festivals, assign to a random available date.
    - Avoid assigning to blocked dates.
    - If all dates are blocked, return an empty dictionary.
    - You must return exactly one date.

    Return the output as a dictionary with a single key 'date' and the value as the day of the month (1-31).

    Example output format:
    {{
        "date": 15
    }}

    Please do not include any explanations or additional information in your response. 
    Return only the dictionary as specified above.
    """

    calendar_scheduler = autogen.AssistantAgent(
        name="CalendarScheduler",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        system_message="""
        You are a highly efficient assistant specializing in calendar scheduling for social media posts.
        Your task is to assign a storyline to a single available date, considering festivals, themes, and avoiding 
        date conflicts with already scheduled posts. Return the output as a dictionary with a single date.
        """
    )

    response = calendar_scheduler.generate_reply(messages=[{"content": task, "role": "user"}])
    return response

def divide_into_weeks(number_of_posts):
    if number_of_posts is None:
        return None

    # Divide the total posts into 4 weeks
    n1 = int(number_of_posts) // 4
    n2 = int(number_of_posts) // 4
    n3 = int(number_of_posts) // 4
    n4 = int(number_of_posts) // 4 # Adjust the last week to handle remainders
    i = number_of_posts%4
    print(n1)
    if i==3:
        n1+=1
        n2+=1
        n3+=1
    elif i ==1:
        n1+=1
    elif i==2:
        n1+=1
        n2+=1
    
    return n1,n2,n3,n4

def theme_with_date(n,info,company_goals,target,desired,festivals,weeks_distribution):
    planner = autogen.AssistantAgent(
    name="Planner",
    system_message= f"""You are a Digital Marketing Campaign Planner who takes into account the following information and returns {n} themes according to the requirement which is planned as {weeks_distribution}, mapping key festivals and events to their corresponding dates. 
    Ensure that festival-related themes align with the exact dates of the festivals, and each theme should reflect a fresh idea while maintaining consistency with the company’s goals.
    Please provide the output in the following format Please do not add any extra Information or Only return json format : 
    {{
        "Date": "DD",
        "Theme": "Theme"
        }}
   

    Information on the company: {info}
    Company Goals: {company_goals}
    Target Audience: {target}
    Desired Outcomes: {desired}
    Notable Festivals & Events for this month: {festivals}
    """,
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
    human_input_mode="NEVER",
    )
    themes = planner.generate_reply(messages=[{"content": info, "role": "user"}])
    print("themes",themes)
    # list_data = ast.literal_eval(f'[{themes}]')
    list_data=extract_all_json_objects(themes)
    theme_list = [ item["Theme"] for item in list_data]

    return list_data,theme_list



#### Abhisar_changes #############
import re

def extract_last_code_block(data):
    # Convert the data to a string
    data_string = str(data)
    
    # Use regex to find all text between triple backticks
    code_blocks = re.findall(r"```(.*?)```", data_string, re.DOTALL)
    
    # If no code blocks are found, return None
    if not code_blocks:
        return None
    
    # Return the last code block, stripping any leading/trailing whitespace
    return code_blocks[-1].strip()

def convert_string_to_json(input_string):
    # Remove leading/trailing parentheses and quotes
    cleaned_string = input_string.strip("()'")
    
    # Remove escaped newlines and extra whitespace
    cleaned_string = cleaned_string.replace('\\n', '').strip()
    
    # Remove backslashes before single quotes
    cleaned_string = cleaned_string.replace("\\'", "'")
    
    # Use regex to find all key-value pairs
    pairs = re.findall(r'"([^"]+)":\s*"([^"]+)"', cleaned_string)
    
    # Create a dictionary from the pairs
    data_dict = {key.strip(): value.strip() for key, value in pairs}
    
    # Convert the dictionary to a JSON string
    json_string = json.dumps(data_dict, indent=2)
    
    return json_string

def theme_with_dates_abh(n,fest,req,company_goals,target,desired):

    a1 = ConversableAgent(
        name="L1",
        system_message=f"""
    Create a social media posting calendar for a digital marketing specialist. Follow these rules:

1. Select dates for posts in this order:
    a) Festival dates within the week
    b) Regular posts to meet remaining weekly quota
2. Month structure: 4 weeks, each with 7 days [1-7], [8-14], [15-21], [22-28].
3. Prioritize requirements in '{req}'. Assume 0 posts for unmentioned weeks.
4. Include festivals from '{fest}' without violating '{req}'. Festivals take precedence.
5. Select dates for posts in this order:
    a) Festival dates within the week
    b) Regular posts to meet remaining weekly quota
6. Evenly distribute regular posts while adhering to '{req}'.
7. Total posts: {n}


Output Format:
```
[
  "Week 1": {{
    "dd/mm/yyyy": "Regular_Post / <Festival_name>",
    ...
  }},
  "Week 2": {{
    "dd/mm/yyyy": "Regular_Post / <Festival_name>",
    ...
  }},
  ...
]
```

Additional Guidelines:
- Use "Regular_Post" for non-festival posts.
- Use <Festival_name> for festival posts.
- Assign only one festival per date, choosing the more widely celebrated one.
- Meet all requirements in the final schedule.
- Cover the entire specified month.
- If given feedback, correct all mistakes and rewrite the entire JSON.
- Ensure that posts are distributed evenly across the week and not focused on any one part of the week.

Create a balanced schedule that meets all requirements, incorporates festivals chronologically, and maintains optimal posting frequency.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )



    a2 = ConversableAgent(
        name="L2",
        system_message=f"""Review and adjust the social media posting schedule to comply with '{req}':

1. Month structure: 4 weeks, each 7 days [1-7], [8-14], [15-21], [22-28].
2. Reference festivals: '{fest}'
3. Total posts: {n}
4. Dates for posts have been selected in strictly this order:
    a) Festival dates within the week
    b) Regular posts to meet remaining weekly quota

Verification rules:
- Strictly follow '{req}' (assume 0 posts for unmentioned weeks).
- Never replace a festival with a regular post.
- Allow only festival-after-festival combinations.
- Only remove a festival post if all the other posts in that week are festival posts AND the requirements are violated.

Output Format:
```
[
  "Week 1": {{
    "dd/mm/yyyy": "Regular_Post / <Festival_name>",
    ...
  }},
  "Week 2": {{
    "dd/mm/yyyy": "Regular_Post / <Festival_name>",
    ...
  }},
  ...
]
```

Task: Adjust the schedule to fully align with requirements, ensuring accuracy and balance. Reflect all necessary changes in the final output.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )

    
    a3 = ConversableAgent(
        name="L3",
        system_message=f"""As a Digital Marketing Campaign Planner, create social media post themes based on the provided input:

Input: JSON with dates and "<Festival_name>" or "Regular_post"
Context:
- Company Goals: {company_goals}
- Target Audience: {target}
- Desired Outcomes: {desired}
- Total posts: {n}
- Use requirement: '{req}' (Assume 0 posts for unmentioned weeks)
- Month structure: 4 weeks, each 7 days [1-7], [8-14], [15-21], [22-28].

Rules:
1. Maintain all input dates
2. Adhere to '{req}'
3. Align themes with company context
4. Incorporate festivals when mentioned
5. Create goal-supporting themes for "Regular_post"
6. Only respond with the output.

Output Format:
```
[
  {{
    "Date": "DD",
    "Theme": "Theme based on input and context"
  }},
  ...
]
```
Note: 'DD' implies the date only.
Return only the JSON output without additional text or explanations.""",
        llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        human_input_mode="NEVER",
    )
    # Information on the company: {info}

    # Generate the calendar
    group_chat = GroupChat(
        agents=[a1, a2, a3],
        messages=[],
        speaker_selection_method='round_robin',
        max_round=3,
    )

    manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": "gpt-4", "api_key": os.environ["OPENAI_API_KEY"]}], "cache_seed": None},
        )

    chat_result = manager.initiate_chat(
            a1,
            # message= f"{req}",
            message=f"{req}",
            summary_method="reflection_with_llm",
            max_turns = 2,
        )
    for message in group_chat.messages:
        if message['name'] == 'L3':
            content = message['content']
            list_data=extract_all_json_objects(content)
            print("Inside theme_with_dates_abhi",list_data)
            theme_list = [ item["Theme"] for item in list_data]

    
    return list_data,theme_list