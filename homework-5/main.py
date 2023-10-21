import datetime

from src.playlist import PlayList

if __name__ == '__main__':
    pl = PlayList('PLejGw9J2xE9Xqq2ptRCWx-ssxMFhIqB_Q')
    assert pl.title == "Resident Evil 8: Village Прохождение"
    assert pl.url == "https://www.youtube.com/playlist?list=PLejGw9J2xE9Xqq2ptRCWx-ssxMFhIqB_Q"

    duration = pl.total_duration
    assert str(duration) == "16:48:04"
    assert isinstance(duration, datetime.timedelta)
    assert duration.total_seconds() == 60484

    assert pl.show_best_video() == "https://youtu.be/VQgai7JtMAU"
