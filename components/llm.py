import psycopg2
import openai
import json
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# PostgreSQL connection setup
connection = psycopg2.connect(
    dbname="my_database",
    user="your_username",
    password="your_password",
    host="localhost"
)
cursor = connection.cursor()

# Function to send JSON data to OpenAI and extract relevant information
def extract_relevant_data(company_name, search_results):
    # Craft a prompt for OpenAI with the relevant search results
    prompt = f"Extract the contact email address for the company '{company_name}' from the following data: {json.dumps(search_results)}"
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=50,
            temperature=0
        )
        # Extracted information
        extracted_data = response.choices[0].text.strip()
        return extracted_data
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None

# Main processing function
def process_and_store_extracted_data():
    # Step 1: Retrieve data from PostgreSQL
    cursor.execute("SELECT id, company_name, search_results FROM filtered_db WHERE extracted_data IS NULL")
    rows = cursor.fetchall()
    
    # Step 2: Process each row
    for row in rows:
        record_id, company_name, search_results = row
        
        # Step 3: Send data to OpenAI for extraction
        extracted_data = extract_relevant_data(company_name, search_results)
        
        if extracted_data:
            # Step 4: Update the extracted data back into the database
            update_query = """
            UPDATE filtered_db
            SET extracted_data = %s
            WHERE id = %s
            """
            cursor.execute(update_query, (extracted_data, record_id))
            connection.commit()
            print(f"Updated extracted data for {company_name}: {extracted_data}")
        else:
            print(f"No data extracted for {company_name}")

# Run the main processing function
process_and_store_extracted_data()

# Close the connection
cursor.close()
connection.close()
