from googleapiclient.discovery import build
import os
from dotenv import load_dotenv


load_dotenv()
# Создаем переменную для API-ключа.
API_KEY: str = os.getenv('API_KEY')


class Video:
    """Класс для видео с YouTube."""

    def __init__(self, video_id: str) -> None:
        """
        Экземпляр инициализируется по id видео.
        Дальше все данные будут подтягиваться по API.
        """
        self.__video_id = video_id
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        snippet = video["items"][0]["snippet"]
        statistics = video["items"][0]["statistics"]
        self.title = snippet['title']
        self.url = f"https://www.youtube.com/watch?v={video_id}"
        self.view_count = statistics['viewCount']
        self.like_count = statistics['likeCount']



    def __str__(self) -> str:
        """Возвращает название видео."""
        return f'{self.title}'

class PLVideo(Video):
    """Класс для плейлиста и видео с YouTube."""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """
        Экземпляр инициализируется по id видео и id плейлиста.
        Дальше все данные будут подтягиваться по API.
        """
        super().__init__(video_id)
        self.__playlist_id = playlist_id



    def __str__(self) -> str:
        """Возвращает название плейлиста."""
        return f'{self.title}'
