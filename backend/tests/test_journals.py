def test_create_journal(client, auth_headers):
    response = client.post("/journals", headers=auth_headers, json={
        "title": "A Good Day", "content": "Today was peaceful and warm.", "mood_score": 8,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "A Good Day"
    return data

def test_list_journals(client, auth_headers):
    client.post("/journals", headers=auth_headers, json={"title": "Entry 1", "content": "Content 1"})
    response = client.get("/journals", headers=auth_headers)
    assert response.status_code == 200
    assert "items" in response.json()

def test_get_journal(client, auth_headers):
    create_resp = client.post("/journals", headers=auth_headers, json={"title": "My Memory", "content": "Long ago..."})
    journal_id = create_resp.json()["id"]
    response = client.get(f"/journals/{journal_id}", headers=auth_headers)
    assert response.status_code == 200

def test_update_journal(client, auth_headers):
    create_resp = client.post("/journals", headers=auth_headers, json={"title": "Old Title", "content": "Content"})
    journal_id = create_resp.json()["id"]
    response = client.patch(f"/journals/{journal_id}", headers=auth_headers, json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_journal(client, auth_headers):
    create_resp = client.post("/journals", headers=auth_headers, json={"title": "Delete Me", "content": "Gone soon"})
    journal_id = create_resp.json()["id"]
    response = client.delete(f"/journals/{journal_id}", headers=auth_headers)
    assert response.status_code == 204

def test_search_journals(client, auth_headers):
    client.post("/journals", headers=auth_headers, json={"title": "Rose Garden", "content": "Flowers everywhere"})
    response = client.get("/journals?search=Rose", headers=auth_headers)
    assert response.status_code == 200
