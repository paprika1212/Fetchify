import psycopg2
import json

# Connect to PostgreSQL
connection = psycopg2.connect(
    dbname="my_database",
    user="your_username",
    password="your_password",
    host="localhost"
)
cursor = connection.cursor()

# Example JSON response from API
api_response = {
    "company": "Tesla",
    "results": {
        "snippet": "contact@tesla.com",
        "link": "https://www.tesla.com"
    }
}

# Insert JSON data into PostgreSQL
insert_query = """
INSERT INTO filtered_db (company_name, search_results)
VALUES (%s, %s)
"""
cursor.execute(insert_query, (api_response["company"], json.dumps(api_response["results"])))
connection.commit()

# Retrieve data row-wise for LLM processing
cursor.execute("SELECT company_name, search_results FROM filtered_db")
rows = cursor.fetchall()
for row in rows:
    company_name, search_results = row
    # Pass search_results to the LLM
    print(company_name, search_results)

# Close the connection
cursor.close()
connection.close()
