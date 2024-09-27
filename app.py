import streamlit as st
from main import generate_list, prompt_generation, image_generator, planner_theme,run_single_exchange,important_dates,calendar_scheduler,clean_and_parse_result,divide_into_weeks,theme_with_date,theme_with_dates_abh
import requests
from PIL import Image
from io import BytesIO
import calendar
from datetime import datetime

# Title of the app
with open("style.css") as source_des:
        st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)


st.title('Campaign Crafter 🧶')

# Upload TXT file for company description
uploaded_file = st.file_uploader("Upload company description (.txt)", type="txt")

# Use session state to store input values
if 'company_goals' not in st.session_state:
    st.session_state.company_goals = ''
if 'target_audience' not in st.session_state:
    st.session_state.target_audience = ''
if 'desired_outcomes' not in st.session_state:
    st.session_state.desired_outcomes = ''
if 'color_palette' not in st.session_state:
    st.session_state.color_palette = ''
if 'posts_per_week' not in st.session_state:
    st.session_state.posts_per_week = ''
if 'month' not in st.session_state:
    st.session_state.month = ''
    # if 'month' not in st.session_state:
#     st.session_state.month = ''
if 'theme_image_story' not in st.session_state:
    st.session_state.theme_image_story = []
if 'selected_day' not in st.session_state:
    st.session_state.selected_day = []

company_goals = st.text_area("Enter company goals",st.session_state.company_goals,
                             placeholder="E.g., Increase brand awareness, drive sales, enhance customer engagement")
target_audience = st.text_area("Enter target audience", st.session_state.target_audience,
                               placeholder="E.g., Young professionals, tech-savvy users, health-conscious individuals")
desired_outcomes = st.text_area("Enter desired outcomes", st.session_state.desired_outcomes,
                                placeholder="E.g., Achieve 20% increase in social media followers, higher engagement rates")
posts_per_week = st.text_area("Information related No. of Posts", st.session_state.posts_per_week ,placeholder="Mention about the details of the  post of the month")
month = st.selectbox("Select the month", list(calendar.month_name)[1:])
color_palette = st.text_area("Preferred Color Palette (optional)", st.session_state.color_palette,
                             placeholder="E.g., Blue and white tones, vibrant and modern colors")
important_date=important_dates()
print("important_dates ",important_date)
festivals=important_date[month]
# print("important",month_important_date)

# Submit button to start the process
submit = st.button('Submit')
current_year = datetime.now().year

if 'active_expander' not in st.session_state:
    st.session_state.active_expander = None

def toggle_expander(post_id):
    if st.session_state.active_expander == post_id:
        st.session_state.active_expander = None
    else:
        st.session_state.active_expander = post_id


if submit and uploaded_file and company_goals and target_audience and desired_outcomes:
    company_description1 = uploaded_file.read().decode('utf-8')
    company_description=company_description1
    print("company_description ",company_description)
    number_of_post1=int(run_single_exchange(posts_per_week))
    a,b,c,d=divide_into_weeks(number_of_post1)
    
    month_num = list(calendar.month_name).index(month)
    cal = calendar.monthcalendar(current_year, month_num)
    print("Calendar", cal)
    month_name=calendar.month_name[month_num]
    print(month_name)
    post_with_month=posts_per_week+" in the month of "+month_name+ " in year 2024"
    print("festivals",festivals,post_with_month )
    list_data,theme_list=theme_with_dates_abh( number_of_post1,festivals,post_with_month,company_goals,target_audience,desired_outcomes)
    print("Abhi theme_list",theme_list)
    group_chat = planner_theme(theme_list[:a],theme_list[a:a+b],theme_list[a+b:a+b+c],theme_list[a+b+c:], company_description, company_goals, target_audience, desired_outcomes)

    theme_storytelling_with_date = generate_list(group_chat,list_data)
    print(theme_storytelling_with_date)

    # Calculate the number of days in the month
    days_in_month = sum(1 for week in cal for day in week if day != 0)
    
    # Calculate total number of posts for the month
    total_posts = number_of_post1
    
    # Ensure we don't exceed the number of themes/storylines available
    total_posts = min(total_posts, len(theme_storytelling_with_date))
    st.session_state.theme_image_story = []
    st.header(f"Campaign Calendar for {month} {current_year}")

    # Create a 7-column layout for the calendar
    cols = st.columns(7)

    # Display day names
    for i, day_name in enumerate(calendar.day_abbr):
        cols[i].write(day_name)

    # Initialize post counter
    post_counter = 0

   

 # Display the calendar with images
    for week_num, week in enumerate(cal):
    # for week in cal:
        cols = st.columns(7)
        week_post_count = 0
        # print("Inside week")
        for i, day in enumerate(week):
            with cols[i]:
                if day != 0:
                    st.write(day)
                
                    for post_detail in theme_storytelling_with_date:
                        # print("Inside the post details ",post_detail)
                        if int(post_detail['Date']) == day:
                            # print("Inside week Date")

                            with st.expander("🗓️"):
                                prompt = prompt_generation(post_detail['Theme'], post_detail['Storyline'], company_description)
                                if color_palette:
                                    prompt += f" with a color palette including {color_palette}"
                                image_url = image_generator(prompt)

                                # Handle image display
                                if image_url.startswith("http"):
                                    try:
                                        response = requests.get(image_url)
                                        if response.status_code == 200:
                                            img = Image.open(BytesIO(response.content))
                                            st.image(img, use_column_width=True)
                                            st.write(f"**Theme:** {post_detail['Theme']}")
                                            st.write(f"{post_detail['Storyline']}")
                                        else:
                                            st.error(f"Failed to fetch image: HTTP status {response.status_code}")
                                    except Exception as e:
                                        st.error(f"Error loading image: {str(e)}")
                                else:
                                    st.error("Invalid URL provided. Please check the URL format.")
               