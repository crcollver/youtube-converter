# Cameron Collver
# crcollver@gmail.com | github.com/crcollver
# --------------------------------------------------------
# Simple script to convert youtube playlist -> mp3 album
# Title of playlist parsed into metadata
# Separate text file with song names to add title metadata
# --------------------------------------------------------

import os
import itertools
import youtube_dl
import argparse
from mutagen.easyid3 import EasyID3


def progress(d):
    if d['status'] == 'finished':
        print("Done downloading, now converting...")


def convert(download_path, url, dir_name='%(playlist_title)s'):
    """
    uses the youtube-dl library to convert a playlist to mp3

    PARAMS:
    download_path -- the path to download the playlist
    url -- the youtube url to convert
    dir_name -- formatted name of directory for mp3s

    RETURNS:
    string -- full path of playlist directory
    """
    file_format = '%(playlist_index)s - %(title)s.%(ext)s'
    if download_path:
        full_dir_path = f'{os.path.realpath(download_path)}/{dir_name}'
    else:
        full_dir_path = f'{os.path.dirname(os.path.realpath(__file__))}/{dir_name}'
    ydl_opts = {
        'format': 'bestaudio/best',
        'progress_hooks': [progress],
        'outtmpl': f'{full_dir_path}/{file_format}',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, True)

    return full_dir_path % {"playlist_title": result['title']}


def parse_title(file_path):
    """
    parses the first line of the text file
    [artist] - [album] - [year] - [genre]

    PARAMS:
    file_path -- path of the text file containing the metadata

    RETURNS:
    None -- if no file was provided
    dictionary -- filling empty values with "" and stripping whitespace
    """
    if file_path:
        file = os.path.realpath(file_path)
        with open(file) as f:
            metadata = f.readline().strip()
    else:
        return None
    keys = ["artist", "album", "year", "genre"]
    values = [item.replace("/", "_").strip() for item in metadata.split('-')]
    return dict(itertools.zip_longest(keys, values, fillvalue=""))


def parse_song_titles(file_path):
    """
    parses song titles from the provided text file, starts at second line

    PARAMS:
    file_path -- path of the text file containing the metadata

    RETURNS:
    None -- if no file was provided
    list -- stripped of whitespace
    """
    if file_path:
        file = os.path.realpath(file_path)
        with open(file) as f:
            next(f)
            return [line.strip() for line in f]
    else:
        return None


def add_meta(playlist_path, title_list, all_meta_data):
    """
    adds metadata using mutagen EasyID3

    PARAMS:
    playlist_path -- the directory that the mp3's reside in
    title_list -- the list of parsed titles from the text file
    all_meta_data -- artist, album, genre, and year information
    """
    all_mp3s = os.listdir(playlist_path)
    for index, filename in enumerate(all_mp3s):
        audiofile = EasyID3(f'{playlist_path}/{filename}')
        audiofile["title"] = title_list[index] if title_list else filename
        if(all_meta_data):
            audiofile["album"] = all_meta_data['album']
            audiofile["albumartist"] = all_meta_data['artist']
            audiofile["artist"] = all_meta_data['artist']
            audiofile["genre"] = all_meta_data['genre']
            audiofile["date"] = all_meta_data['year']
        audiofile["tracknumber"] = str(index + 1)
        audiofile.save()
        if title_list:
            os.rename(f'{playlist_path}/{filename}',
                      f'{playlist_path}/{title_list[index].replace("/", "_")}.mp3')


def main():
    parser = argparse.ArgumentParser(description="Converter arguments")
    parser.add_argument(
        '--output', '-o', help="The path to download the playlist to")
    parser.add_argument(
        '--titles', '-t', help="Path to text file with a list of song titles for the album")
    parser.add_argument('url', metavar='URL',
                        help='URL for the youtube playlist')
    args = parser.parse_args()

    title_list = parse_song_titles(args.titles)
    all_meta_data = parse_title(args.titles)

    if all_meta_data and len(all_meta_data) > 1:
        if all_meta_data['album'] and all_meta_data['year']:
            dir_name = f'[{all_meta_data["year"]}] {all_meta_data["album"]}'
        else:
            dir_name = all_meta_data["album"]
        dir_path = convert(args.output, args.url, dir_name)
    else:
        dir_path = convert(args.output, args.url)

    add_meta(dir_path, title_list, all_meta_data)


if __name__ == "__main__":
    main()
