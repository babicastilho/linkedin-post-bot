# backend/app/testes/test_posts.py
import pytest

@pytest.mark.asyncio
async def test_create_post(client):
    # Create a new post
    response = await client.post("/posts/create", json={
        "title": "Test Post",
        "content": "Content for test",
        "status": "backlog"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["status"] == "backlog"
    assert "_id" in data


@pytest.mark.asyncio
async def test_get_posts(client):
    # Create a new post
    create_response = await client.post("/posts/create", json={
        "title": "Test Get Post",
        "content": "Content for get test",
        "status": "backlog"
    })
    assert create_response.status_code == 200
    created = create_response.json()

    # Retrieve all posts
    response = await client.get("/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(post["_id"] == created["_id"] for post in data)


@pytest.mark.asyncio
async def test_update_post_status(client):
    # Create a post to update
    create_response = await client.post("/posts/create", json={
        "title": "Update Test",
        "content": "Content",
        "status": "draft"
    })
    assert create_response.status_code == 200
    post_id = create_response.json()["_id"]

    # Update the status of the post
    update_response = await client.put(f"/posts/update-status/{post_id}", json={
        "status": "scheduled"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["status"] == "scheduled"
    assert updated_data["updated_at"] is not None


@pytest.mark.asyncio
async def test_delete_post(client):
    # Create a post to delete
    create_response = await client.post("/posts/create", json={
        "title": "Delete Me",
        "content": "Content",
        "status": "draft"
    })
    assert create_response.status_code == 200
    post_id = create_response.json()["_id"]

    # Delete the post
    delete_response = await client.delete(f"/posts/{post_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Post deleted successfully"

    # Ensure the post is no longer present
    get_response = await client.get("/posts/")
    assert get_response.status_code == 200
    assert all(p["_id"] != post_id for p in get_response.json())
