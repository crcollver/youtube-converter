# youtube-converter
This script is useful for downloading Youtube playlists as mp3 and adding bare bones metadata to them programmatically. Since youtube video titles vary wildly, a text file should be provided with basic metadata. This ensures that they are properly organized when added to your phone's music library.

### Libraries Used
Uses [youtube-dl](https://github.com/ytdl-org/youtube-dl) to download playlist from Youtube and convert to mp3. Uses [Mutagen](https://mutagen.readthedocs.io/en/latest/user/id3.html) to alter meta information of mp3 after download.

youtube-dl only downloads the video formats associated with the Youtube video. Converting to mp3 requires software that can convert to that file type. I used [ffmpeg](https://ffmpeg.org/about.html), `sudo apt install ffmpeg`.

### Running
1. Setup environment with `pip install -r requirements.txt`

2. Get the converter software of your choice, I mentioned mine above.

3. Find a playlist on Youtube that you want to download.

4. Model the metadata within a text file.  A template is given in song_list.txt.  **Album information** should be the very first line, while **song titles** should start on the second line and each have their own line.

5. Run the following command to convert that playlist:
    ```python3 convert.py -o /path/for/download/ -t /path/to/textfile/ https://www.youtube.com/playlisturl```

    The -o flag is the path where the playlist will be downloaded to. Omitting this will place the download in the directory of the script.

    The -t flag is the path to the text file with your metadata information. Omitting the text file will only convert the playlist to mp3 and will only set title metadata information.

6. If a text file is provided, the output folder will be formatted as "Year - Album Name".  If none is provided, the output folder will have the same name as the playlist title.
