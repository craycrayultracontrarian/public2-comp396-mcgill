import os
from openai import OpenAI
from data.topic_list.topic_list import list_topics
from data.keys.openai_key import openai_api_key # removed for github upload
# with open('data/topic_list/topic_list.txt', 'r') as file: topics = file.read()
os.environ["OPENAI_API_KEY"] = openai_api_key
client = OpenAI()

def categorize_images(thumbnails):
  descriptions = []
  errors = []
  n=0
  for thumbnail in thumbnails:
    completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
        {"role": "system",
          "content": [{"type": "text",
                      "text": 
                      "You are a precise image analyst. YOU ABSOLUTELY MUST DEFINE THE IMAGE AS EITHER APOLITICAL, RIGHT LEANING, OR LEFT LEANING. USE ONLY THE WORDS APOLITICAL, RIGHT, OR LEFT. DO NOT SAY ANYTHING OTHER THAN ONE OF THOSE 3 WORDS. IF YOU DONT KNOW EXACTLY, TAKE A GUESS, IT DOESNT HAVE TO BE PERFECT. NO PROBLEM IF THE ACCOUNT IS APOLITICAL, JUST BE TRUTHFUL."}],
        },
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "WHAT IS IN THE IMAGE? DEFINE THE IMAGE AS EITHER APOLITICAL, RIGHT LEANING, OR LEFT LEANING. USE ONLY THE WORDS 'APOLITICAL', 'RIGHT', OR 'LEFT'."
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": thumbnail # use current thumbnail url from the array
                }
              }
            ]
          }
        ]
    )
 # cur_post = completion.choices[0].message.content.split(", ")
  #for index, value in enumerate(cur_post):
   # if value not in list_topics:
    #        errors.append(f"Invalid topic at image {n}, {index}, contained {value} from {cur_post}")

  descriptions.append(completion.choices[0].message.content) 
  #n+=1
  return descriptions
  print(descriptions)
  #print(errors)  

# run this code concurrently with the other code that scrolls reels? 
# we could use this topic classifier for our agent to choose what to watch

# i am going to have to implement selenium to download the thumbnails from the reels
# then i'll need to get the downloaded tn into the gpt4-o request, maybe by link
  # if I need the link, i'll likely upload to aws s3 which would take a bit of effort and $0.00Xs

# one issue that could come up is the runtime, if i want to make decisions with it
# ie: should it continue watching the video or not? (if these are the topic it seeks)
# given that the code may take 5s to execute, it could skew our watch times. 