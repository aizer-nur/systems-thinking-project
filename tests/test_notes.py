# End-to-end CRUD flow against a test SQLite database (verifies that create, read, update, and delete work together correctly)

def test_crud_flow(client):
    # create
    r = client.post("/notes", json={"title": "t1", "body": "b1"})
    assert r.status_code == 201
    note = r.json()
    note_id = note["id"]
    assert note["title"] == "t1"
    assert note["body"] == "b1"

    # list
    r = client.get("/notes")
    assert r.status_code == 200
    assert any(n["id"] == note_id for n in r.json())

    # get
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert r.json()["body"] == "b1"

    # update (PATCH)
    r = client.patch(f"/notes/{note_id}", json={"body": "b2"})
    assert r.status_code == 200
    assert r.json()["body"] == "b2"

    # delete (204, no body)
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204
    assert r.text == ""

    # get after delete -> 404
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


# Additional tests to cover edge cases and error handling.

def test_create_note_validation_error(client):
    # body missing -> should fail validation (422)
    r = client.post("/notes", json={"title": "only title"})
    assert r.status_code == 422


def test_get_note_not_found(client):
    r = client.get("/notes/999999")
    assert r.status_code == 404


def test_update_note_not_found(client):
    r = client.patch("/notes/999999", json={"body": "x"})
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/999999")
    assert r.status_code == 404


def test_patch_updates_only_one_field(client):
    # create
    r = client.post("/notes", json={"title": "t1", "body": "b1"})
    note_id = r.json()["id"]

    # update only body
    r = client.patch(f"/notes/{note_id}", json={"body": "b2"})
    assert r.status_code == 200
    assert r.json()["title"] == "t1"
    assert r.json()["body"] == "b2"