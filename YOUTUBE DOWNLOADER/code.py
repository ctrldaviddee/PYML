import os

# re module to handle regular expressions
import re

from pytube import Playlist, YouTube


# download_playlist function takes two parameters; the playlist URL and the desired video resolution.


def download_playlist(playlist_url, resolution):
    
    # create a new Playlist object using the Pytube library and extracts the name of the playlist
    playlist = Playlist(playlist_url)

    # re.sub() function replaces any non-alphanumeric characters in the playlist title with a hyphen ("-") character
    playlist_name = re.sub(r'\W+', '-', playlist.title)

    # check if a folder with the same name exists in the current working directory. If not, create a new folder with the playlist name.
    if not os.path.exists(playlist_name):
        os.mkdir(playlist_name)


    # The Playlist object provides a videos property which is an iterable of YouTube objects. 
    # first iterate through the list of videos in the playlist using a for loop and enumerate function.
        
        # start parameter set to 1 to start counting from 1 instead of 0 because you're going to use the index in the filenames. 
        # Thus it makes sense to start from 1.

    for index, v in enumerate(playlist.videos, start=1):

        # create a YouTube object for each video using its watch URL, and specify to use OAuth for authentication:
        video = YouTube(v.watch_url, use_oauth=True)

        # Filter the available video streams to select the one with the desired resolution, and get its filename
        video_resolution = video.streams.filter(res=resolution).first()
        video_filename = f"{index}. {video_resolution.default_filename}"

        # Determine the full path and filename for the video file, and check if it already exists. 
        # If it does, skip downloading this video and move on to the next one:

        video_path = os.path.join(playlist_name, video_filename)

        if os.path.exists(video_path):
            print(f'{video_filename} already exists. ')
            continue

        # If the desired resolution is not available, download the video with the highest resolution instead:
        video_streams = video.streams.filter(res=resolution)

        if not video_streams:
            highest_resolution_stream = video.streams.get_highest_resolution()
            video_name = highest_resolution_stream.default_filename
            print(f"Downloading {video_name} in {highest_resolution_stream.resolution}" )  
            highest_resolution_stream.download(filename=video_path)

        # If the desired resolution is available, you don't have to download it directly. 
        # If you do so, the downloaded video won't have sound. Instead, download both the video and audio streams separately, 
        # and merge them using the FFmpeg library to create the final video file. Finally, 
        # rename the merged file and delete the temporary video and audio files:
            
        else:
            video_stream = video_streams.first()
            video_name = video_stream.default_filename
            print(f"Downloading video for {video_name} in {resolution}")
            video_stream.download(filename="video.mp4")

            audio_stream = video.streams.get_audio_only()
            print(f"Downloading audio for {video_name}")
            audio_stream.download(filename="audio.mp4")

            os.system("ffmpeg -y -i video.mp4 -i audio.mp4 -c:v copy -c:a aac final.mp4 -loglevel quiet -stats")
            os.rename("final.mp4", video_path)
            os.remove("video.mp4")
            os.remove("audio.mp4")

            # The video stream is initially downloaded as video.mp4 and the audio stream is downloaded as audio.mp4. 
            
            # Next, the ffmpeg command takes two input files (video.mp4 and audio.mp4), copies the video codec from the input file 
             
            # and uses the AAC codec for audio, and saves the output as final.mp4. 
            
            # The output file is created by merging the video and audio streams from the two input files.

            # After ffmpeg finishes processing, the final.mp4 is renamed video_path and the video and audio stream files are deleted.

        print("----------------------------------")


if __name__ == "__main__":

    playlist_url = input("Enter the playlist url: ")

    resolutions = ["240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

    resolution = input(f"Please select a resolution {resolutions}: ")

    download_playlist(playlist_url, resolution)
