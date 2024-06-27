import os
import pandas as pd
from typing import Dict, List, Optional
from pydantic import BaseModel
from enum import Enum
from cat.mad_hatter.decorators import tool, hook, plugin
from cat.log import log

# Set the environment variable ‘nl2gherkin_dir’ to the directory where the plugin is located.
nl2gherkin_dir = os.path.dirname(os.path.abspath(__file__))
os.environ['nl2gherkin_dir'] = nl2gherkin_dir

# Define directories for feature and generated files
features_dir = os.path.join(nl2gherkin_dir, 'features')
generated_dir = os.path.join(nl2gherkin_dir, 'generated')
os.makedirs(generated_dir, exist_ok=True)

# Settings
class LanguageSelect(Enum):
    EN = 'English'
    IT = 'Italian'

class NLToGherkinSettings(BaseModel):
    Language: LanguageSelect = LanguageSelect.EN

@plugin
def settings_schema():
    return NLToGherkinSettings.schema()

def load_feature_file(feature_files_dir: str, file_id: str) -> Optional[str]:
    """Load the content of the .feature file"""
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

def learn_excel_to_gherkin(excel_file: str, feature_files_dir: str) -> Optional[List[Dict]]:
    """Read the excel file and generate Gherkin specifications based on the .feature files."""
    try:
        df = pd.read_excel(excel_file)
        gherkin_specifications = []

        # Load all feature files into a dictionary.
        feature_files = {
            os.path.splitext(file_name)[0]: load_feature_file(feature_files_dir, os.path.splitext(file_name)[0])
            for file_name in os.listdir(feature_files_dir) if file_name.endswith('.feature')
        }

        # Iterate over each row in the excel file
        for _, row in df.iterrows():
            sds = row['SDS']
            feature_content = feature_files.get(sds, "No associated feature file found")

            # Prioritize main columns and use backup columns if needed
            stc = row.get('STC', row.get('Description', ''))
            procedure = row.get('Procedure', row.get('Trigger', ''))
            pass_criteria = row.get('Pass criteria', row.get('Actuation', ''))
            description = row.get('Description', '')
            trigger = row.get('Trigger', '')
            actuation = row.get('Actuation', '')

            # Append the example
            example = {
                'sds': sds,
                'stc': stc,
                'procedure': procedure,
                'pass_criteria': pass_criteria,
                'description': description,
                'trigger': trigger,
                'actuation': actuation,
                'gherkin': feature_content
            }
            gherkin_specifications.append(example)

        return gherkin_specifications
    except Exception as e:
        log.error(f"Error during the reading of excel: {e}")
        return None

def convert_row_to_gherkin(row: Dict) -> str:
    """Convert a row dictionary to Gherkin format."""
    return f"""
Feature: {row['sds']}

Scenario: {row['stc']}
    Given {row['procedure']}
    And {row['pass_criteria']}
    When {row['description']}
    Then {row['trigger']}
    And {row['actuation']}
"""

def save_gherkin_scenario(scenario: str, feature_name: str) -> None:
    """Save a Gherkin scenario to a .feature file."""
    feature_file_name = f"{feature_name}.feature"
    file_path = os.path.join(generated_dir, feature_file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(scenario)

def invoke_llm_to_learn(excel_data: List[Dict], feature_data: Dict[str, str], cat) -> None:
    """
    Invoke the LLM to learn from provided data.
    """
    try:
        # Create training examples by combining excel_data and feature_data
        examples = []
        for data in excel_data:
            if data['gherkin'] != "No associated feature file found":
                examples.append({
                    "input": f"STC: {data['stc']}\nProcedure: {data['procedure']}\nPass criteria: {data['pass_criteria']}\nDescription: {data['description']}\nTrigger: {data['trigger']}\nActuation: {data['actuation']}",
                    "output": data['gherkin']
                })

        # Formulate the prompt for the LLM
        prompt = "Learn from the following examples to convert NL to Gherkin:\n\n"
        for example in examples:
            prompt += f"Input:\n{example['input']}\nOutput:\n{example['output']}\n\n"

        # Call the LLM with the formulated prompt
        response = cat.llm(prompt)
        log.info(f"LLM Response: {response}")
    except Exception as e:
        log.error(f"Error while invoking LLM to learn: {e}")

def do_convert_nl_to_gherkin(excel_file_name: str, cat) -> str:
    """Perform the conversion from NL to Gherkin using the trained LLM."""
    nl2gherkin_dir = os.getenv('nl2gherkin_dir', '')
    filepath = os.path.join(nl2gherkin_dir, excel_file_name)
    if not os.path.exists(filepath):
        log.error(f"The file {excel_file_name} does not exist in the directory {nl2gherkin_dir}!")
        return "Conversion failed"

    try:
        # Read the Excel file and generate the input data for the LLM
        df = pd.read_excel(filepath)
        if df.empty:
            log.error("The Excel file is empty")
            return "Conversion failed"

        gherkin_scenarios = []

        # Iterate over each row in the Excel file
        for _, row in df.iterrows():
            sds = row.get('SDS', '')
            stc = row.get('STC', row.get('Description', ''))
            procedure = row.get('Procedure', row.get('Trigger', ''))
            pass_criteria = row.get('Pass criteria', row.get('Actuation', ''))
            description = row.get('Description', '')
            trigger = row.get('Trigger', '')
            actuation = row.get('Actuation', '')

            # Construct the input for the LLM
            llm_input = (f"STC: {stc}\n"
                         f"Procedure: {procedure}\n"
                         f"Pass criteria: {pass_criteria}\n"
                         f"Description: {description}\n"
                         f"Trigger: {trigger}\n"
                         f"Actuation: {actuation}")

            prompt = f"""Generate a Gherkin scenario based on the following input:{llm_input}

1. Only provide the Gherkin format scenario.
2. The output should start with 'Feature:'.
3. Include only the Gherkin scenario steps without any additional text.
4. Do not include phrases like 'Here is the generated Gherkin scenario:', 'Here is the Gherkin scenario', 'Output:', 'Result:', or any other non-Gherkin text.
5. Ensure that the output is purely in Gherkin format and nothing else.

Example of the expected format:
Feature: User Login and Dashboard Navigation
  Scenario: User logs in and navigates to the dashboard
    Given the user is on the login page
    When the user enters valid credentials
    And ...
    Then the user should be redirected to the dashboard
    And..."""

            llm_response = cat.llm(prompt)

            if llm_response:
                gherkin_scenarios.append({
                    'sds': sds,
                    'gherkin': llm_response
                })
            else:
                log.error(f"LLM failed to generate Gherkin for SDS: {sds}")

        # Save each Gherkin scenario as a separate .feature file
        for scenario in gherkin_scenarios:
            save_gherkin_scenario(scenario['gherkin'], scenario['sds'])

        return "Conversion completed successfully"
    except Exception as e:
        log.error(f"Error during reading the Excel file: {e}")
        return "Conversion failed"

def train_nl_to_gherkin(excel_file_name: str, cat) -> str:
    """Train the system with examples from the given Excel file."""
    filepath = os.path.join(nl2gherkin_dir, excel_file_name)
    if not os.path.exists(filepath):
        log.error(f"The file {excel_file_name} does not exist in the directory {nl2gherkin_dir}!")
        return f"The file {excel_file_name} does not exist in the directory {nl2gherkin_dir}!"

    try:
        training_data = learn_excel_to_gherkin(filepath, features_dir)
        if training_data is None:
            return "Failed to read training data from Excel file."

        # Load all feature files into a dictionary.
        feature_files = {
            os.path.splitext(file_name)[0]: load_feature_file(features_dir, os.path.splitext(file_name)[0])
            for file_name in os.listdir(features_dir) if file_name.endswith('.feature')
        }

        # Invoke the LLM to learn from the provided data.
        invoke_llm_to_learn(training_data, feature_files, cat)

        return "Training completed successfully"
    except Exception as e:
        log.error(f"Error during training with the Excel file: {e}")
        return "An error occurred during the training"

@hook(priority=0)
def agent_fast_reply(fast_reply, cat) -> Dict:
    """Handle fast replies from the agent."""
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
                    return {"output": "Please, provide an Excel file to convert: nl2gherkin convert excel-file.xlsx"}

            if args[0].startswith("train"):
                _, *subargs = args[0].split(maxsplit=1)
                if subargs:
                    excel_filename_to_train = subargs[0]
                    response = train_nl_to_gherkin(excel_filename_to_train, cat)
                    return {"output": response}
                else:
                    return {"output": "Please, provide an Excel file to train: nl2gherkin train excel-file.xlsx"}

        else:
            response = ("How to convert a NL sentence to Gherkin:"
                        "\nType: nl2gherkin convert test.xlsx"
                        "\nHow to train the system:"
                        "\nType: nl2gherkin train example.xlsx")
            return_direct = True

    if return_direct:
        return {"output": response}

    return fast_reply