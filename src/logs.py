from mitmproxy import http
import json
import urllib.parse


# I want to have a counter that doesnt reset every time the script is run
# its stored somewhere not in memory so that it doesnt reset

# I want that number in a txt file
# I want to read that number from the txt file
# I want to increment that number
# I want to write that number back to the txt file
# I want to print that number
def counter():
    with open("../data/logging_client_events/counter.txt", "r") as file:
        count = int(file.read())
    return count

counter = counter()


def request(flow: http.HTTPFlow) -> None:
    if "logging_client_events" in flow.request.pretty_url:
        try:
            # Parse the request content to get the payload
            parsed_content = urllib.parse.parse_qs(flow.request.text)
            message = parsed_content.get("message")

            if message:
                # Decode the message and parse it as JSON
                parsed_message = json.loads(message[0])
                print("../data/logging_client_events/logging_client_events_" + str(counter) + ".json")
                # Log the parsed message to a JSON file
                with open("../data/logging_client_events/logging_client_events_" + str(counter) + ".json", "a") as log_file:
                    json.dump(parsed_message, log_file, indent=4)
                    log_file.write(",")
                    log_file.write("\n")
        except Exception as e:
            print(f"Error processing request: {e}")
