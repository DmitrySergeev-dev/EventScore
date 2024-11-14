from datetime import datetime

import pytest

from src.domain.model import News


def test_set_wrong_status_for_news():
    news = News(description="test news", deadline=datetime.now())
    with pytest.raises(ValueError):
        news.status = "WrongStatus"
