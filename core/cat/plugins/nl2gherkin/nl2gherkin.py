import os
import pandas as pd
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
from cat.mad_hatter.decorators import tool, hook, plugin
from cat.log import log

# Set the environment variable 'nl2gherkin_dir' to the directory where the plugin is located
nl2gherkin_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['nl2gherkin_dir'] = nl2gherkin_dir

# Get the full path of the input file
nl2gherkin_dir = os.getenv('nl2gherkin_dir')
features_dir = os.path.join(nl2gherkin_dir, 'features')

# Settings
class LanguageSelect(Enum):
    EN: str = 'English'
    IT: str = 'Italian'

class NLToGherkinSettings(BaseModel):
    Language: LanguageSelect = LanguageSelect.EN

@plugin
def settings_schema():
    return NLToGherkinSettings.schema()

def load_feature_file(feature_files_dir: str, file_id: str) -> Optional[str]:
    """
    Load the content of the .feature file associated with the ID.
    """
    feature_file_path = os.path.join(feature_files_dir, f"{file_id}.feature")
    try:
        with open(feature_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if not content.strip():
                log.error(f"Feature file {file_id}.feature is empty")
                return None
            return content
    except FileNotFoundError:
        log.error(f"Feature file {file_id}.feature not found in {feature_files_dir}")
    except Exception as e:
        log.error(f"Error reading feature file {file_id}.feature: {e}")
    return None

def read_excel_to_gherkin(excel_file: str, feature_files_dir: str) -> Optional[List[Dict]]:
    """
    Read the excel file and generate Gherkin specifications based on the .feature files.
    """
    try:
        df = pd.read_excel(excel_file)
        gherkin_specifications = []
        for _, row in df.iterrows():
            sds = row['SDS']
            feature_content = load_feature_file(feature_files_dir, sds)
            if feature_content:
                example = {
                    'sds': row['SDS'],
                    'description': row['Description'],
                    'trigger': row['Trigger'],
                    'actuation': row['Actuation'],
                    'stc': row['STC'],
                    'procedure': row['Procedure'],
                    'pass_criteria': row['Pass criteria'],
                    'gherkin': feature_content
                }
                gherkin_specifications.append(example)
        return gherkin_specifications
    except Exception as e:
        log.error(f"Errore durante la lettura dell'excel: {e}")
        return None

def convert_row_to_gherkin(row: Dict, cat) -> str:
    """
    Convert a row dictionary to Gherkin format and use LLM for refinement.
    """
    gherkin_scenario = f"""
    Feature: {row['description']}
    
    Scenario: {row['sds']}
        Given {row['trigger']}
        When {row['actuation']}
        Then {row['procedure']}
        And {row['pass_criteria']}
    """
    
    # Call an LLM for more refined translation
    prompt = f"""Convert and indent properly the following scenario to refined Gherkin syntax: {gherkin_scenario}
    
                The indentation must look like the following example:
                
                Feature:

                    Scenario Outline:
                        Given 
                        When 
                        And 
                        And 
                        And 
                        Then 
            """
    try:
        refined_gherkin = cat.llm(prompt)
        return refined_gherkin
    except Exception as e:
        log.error(f"Error during LLM conversion: {e}")
        return gherkin_scenario  # Fallback to the initial conversion

def do_convert_nl_to_gherkin(excel_file_name: str, cat) -> str:
    """
    Perform the conversion from NL to Gherkin.
    """
    nl2gherkin_dir = os.getenv('nl2gherkin_dir', '')
    filepath = os.path.join(nl2gherkin_dir, excel_file_name)
    if not os.path.exists(filepath):
        log.error(f"The file {excel_file_name} does not exist in the directory {nl2gherkin_dir}!")
        return f"The file {excel_file_name} does not exist in the directory {nl2gherkin_dir}!"

    try:
        requirements = read_excel_to_gherkin(filepath, features_dir)
        if requirements is None:
            return "Failed to generate Gherkin specifications from Excel file."

        gherkin_scenarios = [convert_row_to_gherkin(requirement, cat) for requirement in requirements]
        gherkin_output = "\n".join(gherkin_scenarios)

        cat.send_ws_message(content=gherkin_output, msg_type='chat')
        return "Conversion completed successfully"
    except Exception as e:
        log.error(f"Error during reading the Excel file: {e}")
        return "An error occurred during the conversion"

@hook(priority=0)
def agent_fast_reply(fast_reply, cat) -> Dict:
    """
    Handle fast replies from the agent.
    """
    return_direct = False
    user_message = cat.working_memory["user_message_json"]["text"]

    if user_message.startswith("nl2gherkin"):
        _, *args = user_message.split(maxsplit=1)
        if args:
            if args[0] == "list":
                return {"output": "Listing is not implemented yet"}

            if args[0].startswith("convert"):
                _, *subargs = args[0].split(maxsplit=1)
                if subargs:
                    excel_filename_to_convert = subargs[0]
                    response = do_convert_nl_to_gherkin(excel_filename_to_convert, cat)
                    return {"output": response}
                else:
                    return {"output": "Please, provide an Excel file to convert: <i>nl2gherkin convert <b>excel-file.xlsx</b></i>"}

        else:
            response = "<b>How to convert a NL sentence to Gherkin:</b><br>Type: <i>nl2gherkin convert <b>excel-file.xlsx</b></i><br>"
            return_direct = True

    if return_direct:
        return {"output": response}

    return fast_reply
