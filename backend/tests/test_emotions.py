def test_emotion_stats_empty(client, auth_headers):
    response = client.get("/emotions/stats", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "total_entries" in data

def test_emotion_trends(client, auth_headers):
    response = client.get("/emotions/trends", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_emotion_search(client, auth_headers):
    response = client.get("/emotions", headers=auth_headers)
    assert response.status_code == 200
