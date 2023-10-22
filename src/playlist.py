
from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import timedelta
from src.apimixin import APIMixin
import isodate
import os

load_dotenv()

class PlayList(APIMixin):
    def __init__(self, playlist_id: str) -> None:
        """Инициализируется по id плейлиста."""
        self.playlist_id = playlist_id
        youtube = APIMixin.get_service()
        playlists = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"


    def __str__(self) -> str:
        return f"{self.title}"


    @property
    def total_duration(self) -> timedelta:
        """Возвращает общую длительность плейлиста."""
        youtube = APIMixin.get_service()

        playlist_videos = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50, ).execute()

        video_ids = []

        for video in playlist_videos['items']:
            video_id = video['contentDetails']['videoId']
            video_ids.append(video_id)

        video_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)).execute()

        total_duration = timedelta()
        for item in video_response['items']:
            if 'duration' in item['contentDetails']:
                iso_8601_duration = item['contentDetails']['duration']
                duration = isodate.parse_duration(iso_8601_duration)
                total_duration += duration
        return total_duration


    def show_best_video(self):
        '''Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)'''
        youtube = APIMixin.get_service()
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        current_video_likes = 0
        for video_id in video_ids:
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id).execute()
            if int(video_response['items'][0]['statistics']['likeCount']) > current_video_likes:
                current_video_likes = int(video_response['items'][0]['statistics']['likeCount'])
            else:
                continue
        return f"https://youtu.be/{video_id}"
