import pytest

from src.items import ItemsAPI
from src.top_stories import TopStoriesAPI


DELETED_COMMENT_ID = 46981689
NESTED_COMMENT_ID = 46982232
TEXT_STORY_ID = 46982505


@pytest.mark.items
@pytest.mark.story
@pytest.mark.acceptance
def test_get_top_story_item_returns_200(client):
    """Items API returns 200 when fetching the first story."""
    top_stories = TopStoriesAPI(client)
    items = ItemsAPI(client)
    story = top_stories.find_first_top_story()
    response = items.get_item_response(story["id"])

    assert response.status_code == 200


@pytest.mark.items
@pytest.mark.story
@pytest.mark.acceptance
def test_get_top_story_item_has_type_story(client):
    """Items API returns an item with type 'story' for the first story."""
    top_stories = TopStoriesAPI(client)
    story = top_stories.find_first_top_story()

    assert story["type"] == "story"


@pytest.mark.items
@pytest.mark.story
@pytest.mark.acceptance
def test_get_top_story_item_returns_dict(client):
    """Items API returns a dict when fetching the first story."""
    top_stories = TopStoriesAPI(client)
    story = top_stories.find_first_top_story()

    assert isinstance(story, dict)


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.acceptance
def test_get_first_comment_returns_200(client):
    """Items API returns 200 when fetching the first comment of a story."""
    top_stories = TopStoriesAPI(client)
    items = ItemsAPI(client)
    story = top_stories.find_first_top_story_with_comments()
    response = items.get_item_response(story["kids"][0])

    assert response.status_code == 200


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.acceptance
def test_get_first_comment_returns_dict(client):
    """Items API returns a dict when fetching the first comment of a story."""
    top_stories = TopStoriesAPI(client)
    items = ItemsAPI(client)
    story = top_stories.find_first_top_story_with_comments()
    comment = items.get_first_comment(story)

    assert isinstance(comment, dict)


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.acceptance
def test_get_first_comment_has_type_comment(client):
    """Items API returns an item with type 'comment' for the first comment."""
    top_stories = TopStoriesAPI(client)
    items = ItemsAPI(client)
    story = top_stories.find_first_top_story_with_comments()
    comment = items.get_first_comment(story)

    assert comment["type"] == "comment"


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.acceptance
def test_get_first_comment_parent_matches_story(client):
    """First comment's parent field matches the story ID."""
    top_stories = TopStoriesAPI(client)
    items = ItemsAPI(client)
    story = top_stories.find_first_top_story_with_comments()
    comment = items.get_first_comment(story)

    assert comment["parent"] == story["id"]


@pytest.mark.items
@pytest.mark.edge_case
@pytest.mark.parametrize("item_id", [0, -1, 99999999999, "abc"])
def test_invalid_item_id_returns_null(client, item_id):
    """Items API returns null for invalid item IDs (0, negative, non-existent)."""
    items = ItemsAPI(client)
    response = items.get_item_response(item_id)

    assert response.status_code == 200
    assert response.json() is None


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.edge_case
def test_deleted_comment_returns_200(client):
    """Items API returns 200 for deleted comment."""
    items = ItemsAPI(client)
    response = items.get_item_response(DELETED_COMMENT_ID)

    assert response.status_code == 200


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.edge_case
def test_deleted_comment_has_expected_fields(client):
    """Deleted comment has deleted, id, type, and parent fields."""
    items = ItemsAPI(client)
    item = items.get_item(DELETED_COMMENT_ID)

    assert item["deleted"] is True
    assert item["id"] == DELETED_COMMENT_ID
    assert item["type"] == "comment"
    assert "parent" in item


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.edge_case
def test_deleted_comment_missing_author_and_text(client):
    """Deleted comment does not have by or text fields."""
    items = ItemsAPI(client)
    item = items.get_item(DELETED_COMMENT_ID)

    assert "by" not in item
    assert "text" not in item


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.edge_case
def test_nested_comment_parent_is_comment(client):
    """Nested comment's parent is another comment, not a story."""
    items = ItemsAPI(client)
    comment = items.get_item(NESTED_COMMENT_ID)
    parent = items.get_item(comment["parent"])

    assert comment["type"] == "comment"
    assert parent["type"] == "comment"


@pytest.mark.items
@pytest.mark.comment
@pytest.mark.edge_case
def test_nested_comment_eventually_reaches_story(client):
    """Following parent chain from nested comment eventually reaches a story."""
    items = ItemsAPI(client)
    item = items.get_item(NESTED_COMMENT_ID)

    max_depth = 100
    depth = 0

    while item["type"] == "comment":
        depth += 1
        assert depth <= max_depth, f"Parent chain exceeded {max_depth} levels"
        item = items.get_item(item["parent"])

    assert item["type"] == "story"


@pytest.mark.items
@pytest.mark.story
@pytest.mark.edge_case
def test_text_story_has_text_field(client):
    """Text story (Ask HN, Show HN) has text field instead of url."""
    items = ItemsAPI(client)
    story = items.get_item(TEXT_STORY_ID)

    assert story["type"] == "story"
    assert "text" in story
    assert "url" not in story
