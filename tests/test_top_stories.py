import pytest

from src.top_stories import TopStoriesAPI


@pytest.mark.top_stories
@pytest.mark.acceptance
def test_get_top_stories_returns_200(client):
    """Top Stories API returns a 200 status code."""
    top_stories = TopStoriesAPI(client)
    response = top_stories.get_top_stories_response()

    assert response.status_code == 200


@pytest.mark.top_stories
@pytest.mark.acceptance
def test_get_top_stories_returns_list(client):
    """Top Stories API returns a list."""
    top_stories = TopStoriesAPI(client)
    stories = top_stories.get_top_stories()

    assert isinstance(stories, list)


@pytest.mark.top_stories
@pytest.mark.acceptance
def test_get_top_stories_returns_non_empty_list(client):
    """Top Stories API returns a list with more than 0 items."""
    top_stories = TopStoriesAPI(client)
    stories = top_stories.get_top_stories()

    assert len(stories) > 0


@pytest.mark.top_stories
@pytest.mark.acceptance
def test_get_top_stories_returns_list_of_ints(client):
    """Top Stories API returns a list of integers."""
    top_stories = TopStoriesAPI(client)
    stories = top_stories.get_top_stories()

    assert all(isinstance(story_id, int) for story_id in stories)


@pytest.mark.top_stories
@pytest.mark.edge_case
def test_get_top_stories_does_not_exceed_500_items(client):
    """Top Stories API returns at most 500 items."""
    top_stories = TopStoriesAPI(client)
    stories = top_stories.get_top_stories()

    assert len(stories) <= 500
