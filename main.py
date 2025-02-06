from langgraph.graph import Graph,END
from langgraph.graph import StateGraph
from typing import TypedDict, List, Annotated
import operator
from langgraph.graph.message import add_messages
import pandas as pd   
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage
from typing import Dict, TypedDict, Optional
import time
from typing import Dict, TypedDict, Optional
import ast
from datetime import datetime
import calendar

from llm_helper import get_llm_response_mini, get_llm_response
from global_areas import *

def get_current_month_and_year():
    # Get the current date
    current_date = datetime.now()
    
    # Format the date as "Mon YY"
    formatted_date = current_date.strftime('%b %y')
    
    return formatted_date

class GraphState(TypedDict):
    question: Optional[str] = None
    classification: Optional[str]=None
    location: Optional[str] = None
    division: Optional[str] = None
    year:Optional[str]=None
    month:Optional[str]=None
    data: Optional[str] = None
    questiontype: Optional[str] = None 
    analysis: Optional[str] = None
    headlines: Optional[str]=None
    
        
workflow = StateGraph(GraphState)

def handle_greeting_node(state):
    question = state.get('question', '').strip()
    prompt = f'''
    you are an ai asistant that answers query based on on user question {question}.
    if the user question is hi or hello ! greet him back and say that you are Cost analyzer of Tata Steel Limited! 
    incase you dont know what to answer 
    Ask them to include keywords like "TSJ", "TSG", "TSK", "TSM" in there query incase its anything other than greeting
    just give response in json form
    '''
    resp = get_llm_response_mini(prompt)
    return {"headlines": resp}

def classify_input_node(state):
    question = state.get('question', '').strip()
    question_class = get_llm_response_mini(f'''
    you are an AI classifier agent.
    based on user query **{question}** 
    you classify it into following sections:
    -if the query asks to retrieve or obtain or provide the value or data or simple direct numerical information, 
    classify it as "Retrieval".
    -if the query asks to understand or explain or deduce or reason or summerize or insights 
    or anything related to reasoning something similar along the line, classify it as "Reasoning"
    if the query does not mean any of the above then , classify it as "Retrieval"
    if the query consists of gettings like hi, hello etc, classify it as 'greetings'
    do not write any code. just classify 
    result must be only classification in string .
    ''')
    
    return {"questiontype": question_class}

def get_location(state):
    question = state.get('question', '').strip()
    prompt = f'''
            You are an AI location classifier agent.

            Based on user query {question}, classify it into following locations:

            if the query contains something like TSJ or Jamshedpur or JSR followed by anything, classify it as "TSJ"

            if the query contains something like TSK or KPO or kallinganagar followed by anything, classify it as "TSK"

            if the query contains something like TSM or Angul or Meramandali followed by anything, classify it as "TSM"

            if the query contains something like TSG or ghamaria or TSLPL or Tata steel long products gahmaria followed by anything, classify it as "TSG"

            if the query contains something like "all plants" or "overall" or "TSL" or "Tata Steel" or no specific location is mentioned, return ['TSJ','TSK','TSM','TSG']

            if the query consists of greetings like hi, hello etc, classify it as 'greetings'

            Do not write any code. Just classify.
            Result must contain only list like ['TSJ'].
            If more than one location is mentioned, return all the locations in a list.
            Example: TSJ and TSK / TSJ or TSK
            response: ['TSJ','TSK']
            '''
    response = get_llm_response_mini(prompt)
    import ast
    try:
        location_list = ast.literal_eval(response)
    except (ValueError, SyntaxError) as e:
        print('Error in parsing month string:', e)
        location_list = ['TSJ','TSK','TSM','TSG']
        
    print('Location list--------------',location_list)
    
    # Return as dictionary instead of list
    return {"location": location_list}

def get_division(state):
    question = state.get('question', '').strip()
    classification=state.get('classification','').strip()
    resp = get_llm_response_mini(f'''
    You are an AI classifier agent which classifies plant areas.
    Based on user query "{state}", Determination of plant is already done as following : {classification}.
    You have to determine the areas weather it is IM,SM 
            or SS or combination of these areas
            Classify into these areas only:
            - IM (Iron Making)
            - SM (Steel Making) 
            - SS (Shared Services)
            
            Return only the area code (IM/SM/SS) without any location prefix.
            If no specific area matches or overall is mentioned or all the plants/area is mentioned
            without mentioning any specific area then
            return ['IM','SM','SS'].
            If there are more than one areas mentioned in the query then return a single list containing all the area codes
            Example response:
            ['IM','SM','SS']
            Respond with just the list of area code - no other text.
    ''')

   
    try:
        area_list = ast.literal_eval(resp)
    except (ValueError, SyntaxError) as e:
        print('Error in parsing month string:', e)
        area_list = ["IM","SM","SS"]  # default to an empty list or some other appropriate default value
    division=area_list
    print(f'llm--------------{division,type(division)}')
    return {"division": division}

def get_financial_year(state):
    
    # Get current date
    current_date = datetime.now()
    # In India, financial year starts from April
    # If current month is >= April, FY is current year + 1
    # If current month is < April, FY is current year
    current_fy = current_date.year + 1 if current_date.month >= 4 else current_date.year
    
    question = state.get('question', '').strip()
    prompt = f'''
    You are an AI classifier agent that extracts financial years from text.
    Based on user query: {question}
    
    Rules for extraction:
    - If FY25 is mentioned, return [2025]
    - If FY24 is mentioned, return [2024]
    - If multiple years like FY24 and FY25 are mentioned, return [2024,2025]
    - If no year is mentioned, return current financial year [2025]
    - Convert any FY notation to full year (FY23 -> 2023)
    
    Return only a list of years as integers.
    Example responses:
    [2025]
    [2024,2025]
    '''
    
    response = get_llm_response_mini(prompt)
    
    import ast
    try:
        year_list = ast.literal_eval(response)
    except (ValueError, SyntaxError) as e:
        print('Error in parsing year string:', e)
        year_list = [current_fy]  # Default to current FY
    
    year=year_list
    print(f"Fin_year: {year,type(year)}")
    return {"year": year}

def get_month_numbers(state):
    question = state.get('question', '').strip()
    current_month_and_year = get_current_month_and_year()
    
    system_prompt = f"""
    You are an AI-based month extractor and formatter agent.
    
    Financial Year (FY) Rules:
    - FY YY covers from April YY-1 to March YY
    - When FY YY is mentioned, return ALL months from April (4) to March (3)
    
    Results must be a list of integers representing months:
    [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
    
    The only output should be a list of integers nothing else.
    """
    
    query = f'''
    Based on user query **{question}**, extract the month numbers:
    
    For single month mentions:
    - May -> [5]
    - January -> [1]
    
    For multiple months:
    - May, June, July -> [5, 6, 7]
    
    For FY mentions:
    - FY25 -> [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
    
    If no month specified, default to current month: {current_month_and_year}
    
    For yearly/annual mentions:
    - Return all months of specified FY
    - If till date mentioned: return months from April to current month
    - If range mentioned (e.g., May to September): return all months in range
    '''
    
    month_string = get_llm_response_mini(prompt=query, system_prompt=system_prompt)
    
    try:
        month_list = ast.literal_eval(month_string)
    except (ValueError, SyntaxError) as e:
        print('Error in parsing month string:', e)
        current_month = int(current_month_and_year.split("'")[0])
        month_list = [current_month]
   
    print(f"Month numbers: {month_list,type(month_list)}")
    return {"month": month_list}

final_df = None

import requests

def get_bigquery_data(state):
    global final_df
    
    locations = state.get('location', [])
    divisions = state.get('division', [])
    months = state.get('month', [])
    years = state.get('year', [])
    
    print(f"Locations: {locations}")
    print(f"Divisions: {divisions}")
    print(f"Months: {months}")
    print(f"Years: {years}")

    # Format lists for SQL IN clause
    locations_str = ','.join([f"'{loc}'" for loc in locations])
    divisions_str = ','.join([f"'{div}'" for div in divisions])
    months_str = ','.join([str(month) for month in months])
    years_str = ','.join([str(year) for year in years])
    
    # Construct query
    query = f"""
    SELECT * 
    FROM BPP.T_TEST_SRM_COST
    WHERE LOCATION in ({locations_str})
    AND DIVISION in ({divisions_str})
    AND MONTH in ({months_str})
    AND FIN_YEAR in ({years_str})
    """
    
    print(f"Constructed query:\n {query}")
    
    url = "http://157.0.151.132:58872/srm/get_llm_data_json"
    payload = {"query": query}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.post(
        url, 
        json=payload,
        headers=headers,
        timeout=30
    )

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    # Check if response is successful and contains data
    if response.status_code == 200 and response.text:
        data = response.json()
        print("Received data:", data)
        return {"data": data}

        # data = pd.DataFrame(response_data['data'])
        
        # # Debug: Print DataFrame structure
        # print("DataFrame columns:", data.columns.tolist())
        
        # # Convert month number to month name if 'MONTH' column exists
        # if 'MONTH' in data.columns:
        #     data['MONTH'] = data['MONTH'].apply(lambda x: calendar.month_name[x])
        
        # final_df = data.copy()
    else:
        # Return empty DataFrame if no data
        data =[]
        return {"data": data}
    

def decide_analysis_type(state):
    if state.get('questiontype') == "Reasoning":
        return "REASONING"
    return "RETRIEVAL"

def handle_reasoning(state):
    data = state.get('data')
    question = state.get('question')
    location = state.get('location')# Get the first location if multiple
    
    
    plant_context = get_location_context(location)
    
    prompt = f"""
    You are a Financial Analyst analyzing cost data for Tata Steel Limited locations. Reference the provided data and follow these steps:
    
    Plant Structure Context(sublocations):
    {plant_context}
    
    - **Step 1: Location-Specific Context**
      - Analyze data for {location} focusing on its major operational areas:
        - Iron Making (IM)
        - Steel Making (SM)
        - Shared Services (SS)

    - **Step 2: Response Precision**
      - Ensure all insights are specific to {location}
      - Maintain focus on the queried operational areas
      - If data isn't available, clearly state the limitations

    - **Step 3: Data Analysis Framework**
      - Support all insights with numerical evidence
      - Clearly state percentage comparisons and their basis
      - For time-series analysis:
        - Exclude zero values from calculations
        - Clearly identify excluded months with zero values
        - Consider both Plan and Actual values
        - Calculate trends based on non-zero values only

    - **Step 4: Cost Interpretation**
      - Negative cost differences indicate Actual > Plan
      - Lower costs are favorable
      - Higher consumption is unfavorable
      - Cost units are in Crores (Cr.)

    - **Step 5: Rate vs Cost Distinction**
      - Differentiate between rate-based and cost-based metrics
      - Provide appropriate metric based on query specification
      - Maintain clarity in unit representation

    Question: {question}
    Data Context: {data}
    Provide a detailed analysis with:
    - Bullet-pointed insights
    - Numerical evidence
    - Clear trends and patterns
    - Specific recommendations where applicable
    """
    
#     analysis = get_llm_response_mini(prompt)
    analysis = get_llm_response(prompt)
    return {"analysis": analysis}


def handle_retrieval(state):
    data = state.get('data')
    question = state.get('question')
    location = state.get('location')
    plant_context = get_location_context(location)
    
    prompt = f"""
    You are a data retrieval expert. Based on the following data and question, provide specific numerical information:
    Just retrieve the data and display results of what is asked. No extra informations or suggestions is required
    Question: {question}
    Data: {data}
    Plant Structure Context(sublocations):
    {plant_context}
    Focus on:
    - Exact values and metrics
    - Simple calculations
    - Direct comparisons
    - Specific data points requested
    **NOTE** Don' give any other informations/suggestions. Just give factual information with exact data. Don't use the 
    keyword project as we are dealing with TATA STEEL PLANT. Also while dealing with any calculation don't mention those 
    months where Actual is 0. Strictly mention the exclusion of those months in response.
    """
    
#     result = get_llm_response_mini(prompt)
    result = get_llm_response(prompt)
    return {"headlines": result} # here key is mentioned as headlines beacause this is the key which app.stream will be looking for 
def generate_headlines(state):
    analysis = state.get('analysis')
    question = state.get('question')
    location = state.get('location')
    division = state.get('division')
    
    prompt = f"""
    You are a Financial News Reporter for Tata Steel Limited specializing in data-driven headlines.
    
    Context:
    Location: {location}
    Division: {division}
    Analysis: {analysis}
    
    Create atleast 1 impactful headlines following these guidelines:
    - Focus on factual, quantitative insights
    - Include specific metrics, percentages, and time periods
    - Highlight key performance indicators and trends
    - Mention any data exclusions or special considerations
    - Maintain professional financial news tone
    - Include location and division context where relevant
    
    Don't repeat the same information.
    Format each headline as:
    HEADLINE: [Crisp, metric-driven headline]
    SUMMARY: [One-line factual summary with specific numbers]
    
    Note: Stick strictly to the data provided. No projections or suggestions.
    """
    
    # headlines = get_llm_response_mini(prompt)
    return {"headlines": analysis}

def decide_question_type(state):
    if state.get('questiontype') in ["Retrieval", "Reasoning"]:
        return "PROCESS_QUESTION"
    return "GREETING"

# Initialize workflow
workflow = StateGraph(GraphState)

# Add all nodes
workflow.add_node("classify_input", classify_input_node)
workflow.add_node("get_location_node", get_location)
workflow.add_node("get_division_node", get_division)
workflow.add_node("handle_greeting", handle_greeting_node)
# Add the node
workflow.add_node("get_financial_year", get_financial_year)

# Add edge after location
workflow.add_edge("get_division_node", "get_financial_year")

workflow.add_node("get_months", get_month_numbers)
workflow.add_edge("get_financial_year", "get_months")
workflow.add_node("get_data", get_bigquery_data)
workflow.add_edge("get_months", "get_data")

# Add nodes to workflow
workflow.add_node("handle_reasoning", handle_reasoning)
workflow.add_node("handle_retrieval", handle_retrieval)

# Add conditional edges
workflow.add_conditional_edges(
    "get_data",
    decide_analysis_type,
    {
        "REASONING": "handle_reasoning",
        "RETRIEVAL": "handle_retrieval"
    }
)




# Add conditional edges for question type routing
workflow.add_conditional_edges(
    "classify_input",
    decide_question_type,
    {
        "PROCESS_QUESTION": "get_location_node",
        "GREETING": "handle_greeting"
    }
)

# Add regular edge for processing path
workflow.add_edge("get_location_node", "get_division_node")


# Add the headline node to workflow
workflow.add_node("generate_headlines", generate_headlines)

# Connect it after both analysis paths
workflow.add_edge("handle_reasoning", "generate_headlines")


# Set entry point
workflow.set_entry_point("classify_input")


# Compile workflow
app = workflow.compile()


# result = []
# query = "Tell me overall performance of TSJ for FY25."
# inputs = {"question": query}

# for output in app.stream(inputs):
#     for key, value in output.items():
#         print(f"Output from node '{key}':")
#         print("---")
#         print(value)
#         print("\n---\n")
#         result.append(value)

# print('Final Result:', result[-1]['headlines'])

def process_query(query):
    result = []
    inputs = {"question": query}
    
    for output in app.stream(inputs):
        for key, value in output.items():
            result.append(value)
    
    return result[-1]['headlines']

if __name__ == "__main__":
    # Your workflow will be imported by Flask but can still run independently
    workflow = workflow.compile()
