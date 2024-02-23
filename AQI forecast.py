import openai
import requests

# Set your OpenAI API key
api_key = ''

# Initialize the OpenAI API client
openai.api_key = api_key

# Define your API token
api_token = ""
avg_pm25_list = []  # Initialize a list to store avg_pm25 values

while True:
    user_input = input("City name (or 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break

    city_name = user_input  # Replace with your desired city

    # Define the API endpoint URL
    api_url = f"https://api.waqi.info/feed/{city_name}/?token={api_token}"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Check if the API response contains forecast data
            if "data" in data and "forecast" in data["data"]:
                forecast_data = data["data"]["forecast"]["daily"]["pm25"]

                # Iterate through the forecast data and print it
                for forecast in forecast_data:
                    date = forecast["day"]
                    avg_pm25 = forecast["avg"]
                    max_pm25 = forecast["max"]
                    min_pm25 = forecast["min"]
                    print(f"Date: {date}, Average Air Quality Index: {avg_pm25}, Max Air Quality Index: {max_pm25}, Min Air Quality Index: {min_pm25}")

                    # Append avg_pm25 to the list
                    avg_pm25_list.append(avg_pm25)

            else:
                print("No forecast data available for this city.")
        else:
            print("Error: Unable to fetch data from the API.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    else:
        if avg_pm25_list:  # Check if the list is not empty
            average_pm25 = sum(avg_pm25_list) / len(avg_pm25_list)

            # Determine the overall air quality based on the average
            if 0 < average_pm25 <= 50:
                result = "Most of the time it is Good."
            elif 51 <= average_pm25 <= 100:
                result = "Most of the time it is Moderate."
            elif 101 <= average_pm25 <= 150:
                result = "Most of the time it is Unhealthy for Sensitive Groups."
            elif 151 <= average_pm25 <= 200:
                result = "Most of the time it is Unhealthy."
            elif 201 <= average_pm25 <= 300:
                result = "Most of the time it is very Unhealthy."
            else:
                result = "Most of the time it is Hazardous."

            print(f"Average Air Quality Assessment: {result}")

        # Use OpenAI chatbot with a specific prompt for AQI in the user's input city
        use_input = f"describe air qulaity index in {user_input}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You: {use_input}\n",
            max_tokens=500
        )

        bot_response = response.choices[0].text.strip()
        print(f"Chatbot: {bot_response}")

        choice = input("Do you want to search for another city? (yes/no): ")
        if choice.lower() != 'yes':
            break
