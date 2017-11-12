There is abundance of knowledge on the web in the form of videos and a large majority of the population can not make the most of it because of language barriers. We aim to reduce that by providing an instant way to translate videos to any language of your choice which will be available instantaneously. It is really dificult to find the right videos because of badly titled content and lack of detailed description. We use latest advancements in AI and ML to extract the main entities in the video and index them so that there is an efficient way to store them and thus allow users to access most relevant contents efficiently. 

## Inspiration
- Videos exist in just 1 language
- In this era of MOOCs, students, professionals would like to learn from videos in their own language without depending on the language of the video
- Even though subtitles are available, it becomes difficult to focus on the content of the video and the subtitles shown at the botton of the video
- It is really dificult to find the right videos because of badly titled content and lack of detailed description


## What it does
Feature 1: Translates a video to any language and processes the video to retrieve essential information from the video 
Feature 2: Efficiently indexes the processed information for quick search and retrieval
Feature 3: Provides User friendly interface to search, upload, view and translate them to any language
Feature 4: Get access to the translated videos on any device including mobile phones, tablets and laptops
Feature 5: Enables users to seach for videos based on people, objects and entities occurring in the video 

## How we built it
Technologies:
- Python (Flask) + AngularJS : We built our application using Python for backend and used AngularJS for frontend
- Microsoft Azure Blob Storage : User uploads video on the page. This video gets uploaded to Microsoft's Blob Storage
- Microsoft Video Indexer : Simultaneously, the video is uploaded to Microsoft's Video indexer to convert the audio in the video to text and get relevant tags in the video such as if there is a red car in the video, it adds one of the relevant tags as red
- Microsoft Cosmos Database (MongoDB) : MongoDB is used to store details such as tags and input language
- Microsoft Text to Speech Translator : The text is translated to an audio in the lamnguage mentioned by the user
- Microsoft Email Service : An email is sent once the video is ready to be viewed 

Use Case 1: User Uploads Video -> Audio is extracted and converted to text format -> Relevant tags associated with the video is discovered and entered into MongoDB collection 
Use Case 2: User selects video to be translated -> Text file for the video is translated to speech format in the relevant language -> Video and new audio is merged to produce video in the relevant language -> Email is sent to the user once the video is ready

## Challenges we ran into
- No API which provides direct speech to speech translation : We found Microsoft's API to convert speech to text and text to speech conversion. 
- Search - To find videos based on keywords/objects found in the video

## Accomplishments that we’re proud of
- Synced speech with the video with right amount of pause. There is no algorithm that exists as of now which syncs audio with video properly. 

## What we learned
- Learned to deal with complex audio and video structures
- Learned to use Azure technologies and Cognitive Services
- Learned to efficiently index and search for large text data

## What’s next for InstaTranslate
- Translate videos of longer length. 
- Better sync with translated audio and video
- Add emotions to the translated speech

## How to run this code
pip install -r requirements.txt
python app.py