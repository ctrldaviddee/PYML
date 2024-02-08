import os

# re module to handle regular expressions
import re

from pytube import YouTube



def download_video(video_url, resolution):
    
    video = YouTube(video_url)

    video_name = re.sub(r'\W+', '-', video.title)


    if not os.path.exists(video_name):
        os.mkdir(video_name)




    video_to_download = YouTube(video.watch_url, use_oauth=True)

    video_resolution = video_to_download.streams.filter(res=resolution).first()

    video_filename = f"{video_name}.{video_resolution.default_filename}"

    video_path = os.path.join(video_name, video_filename)

    if os.path.exists(video_path):
        print(f'{video_filename} already exists. ')
        exit()

    video_streams = video_to_download.streams.filter(res=resolution)

    if not video_streams:
        highest_resolution_stream = video_to_download.streams.get_highest_resolution()
        video_name = highest_resolution_stream.default_filename
        print(f"Downloading {video_name} in {highest_resolution_stream.resolution}" )  
        highest_resolution_stream.download(filename=video_path, )

    else:
            video_stream = video_streams.first()
            video_name = video_stream.default_filename
            print(f"Downloading video for {video_name} in {resolution}")
            video_stream.download(filename="video.mp4", )

            audio_stream = video_to_download.streams.get_audio_only()
            print(f"Downloading audio for {video_name}")
            audio_stream.download(filename="audio.mp4", )

            os.system("ffmpeg -y -i video.mp4 -i audio.mp4 -c:v copy -c:a aac final.mp4 -loglevel quiet -stats")
            os.rename("final.mp4", video_path)
            os.remove("video.mp4")
            os.remove("audio.mp4")
            
    print("----------------------------------")



if __name__ == '__main__':
    
    url = input("Please Enter the url of the video: ")

    resolutions = ["240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

    resolution = input(f"Please choose a video resolution {resolutions}:  ")

    download_video(url, resolution)