
def merge(video_id,output_lang):
    import os
    import wget

    from config import VIDEOS_COLLECTION
    video_file = video_id+".mp4"
    audio_file = video_id+"_tts.mp3"
    video = VIDEOS_COLLECTION.find({"insight_id": video_id}, {"video_url": 1, "_id": 0})
    video_url = [v for v in video]
    video_url = video_url[0]['video_url']
    filename = wget.download(video_url, video_file)
    final_output_file=video_id+"_"+output_lang+"_converted.mp4"
    os.system("ffmpeg -i "+ video_file +" -i "+ audio_file +" -c:v copy -map 0:v:0 -map 1:a:0 -strict -2 -shortest "+ final_output_file)
    return final_output_file
