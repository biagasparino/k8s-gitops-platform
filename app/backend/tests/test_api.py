def test_liveness_does_not_need_the_database(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_readiness_reports_ready_when_database_answers(client):
    response = client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_and_list_tasks(client):
    created = client.post("/api/tasks", json={"title": "  learn kubernetes  "})
    assert created.status_code == 201
    body = created.json()
    assert body["title"] == "learn kubernetes"
    assert body["done"] is False

    listed = client.get("/api/tasks")
    assert listed.status_code == 200
    assert [task["id"] for task in listed.json()] == [body["id"]]


def test_update_task_marks_it_done(client):
    task_id = client.post("/api/tasks", json={"title": "ship it"}).json()["id"]
    response = client.patch(f"/api/tasks/{task_id}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_delete_task(client):
    task_id = client.post("/api/tasks", json={"title": "temporary"}).json()["id"]
    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get("/api/tasks").json() == []


def test_unknown_task_returns_404(client):
    assert client.patch("/api/tasks/999", json={"done": True}).status_code == 404
    assert client.delete("/api/tasks/999").status_code == 404


def test_empty_title_is_rejected(client):
    response = client.post("/api/tasks", json={"title": ""})
    assert response.status_code == 422


def test_info_exposes_pod_name(client):
    body = client.get("/api/info").json()
    assert body["pod"]
    assert "version" in body
