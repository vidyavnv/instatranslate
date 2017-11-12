
def merge(video_id,output_lang):
    import os
    video_file = video_id+".mp4"
    audio_file = video_id+"_tts.mp3"
    final_output_file =  video_id+"_"+output_lang+".mp4"
    os.system("ffmpeg -i "+ video_file +" -i "+ audio_file +" -c:v copy -map 0:v:0 -map 1:a:0 -strict -2 -shortest "+ final_output_file)
    return final_output_file
