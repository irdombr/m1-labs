"""CR-0: tēma "Parki un skvēri" un tēmu saraksts."""

EXPECTED_TOPICS = [
    {"code": "ROADS", "name": "Ceļi un ielas"},
    {"code": "WASTE", "name": "Atkritumi"},
    {"code": "PLANNING", "name": "Teritorijas plānošana"},
    {"code": "PARKS", "name": "Parki un skvēri"},
    {"code": "OTHER", "name": "Cits"},
]


def test_list_topics_returns_all_in_order(client):
    # K1 un K4: precīzs saraksts, esošie kodi un nosaukumi nemainās, OTHER beigās
    response = client.get("/topics")
    assert response.status_code == 200
    assert response.json() == EXPECTED_TOPICS


def test_create_submission_with_parks_topic(client, valid_payload):
    # K2
    valid_payload["topic"] = "PARKS"
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 201
    saved = client.get(f"/submissions/{response.json()['id']}").json()
    assert saved["topic"] == "PARKS"


def test_unknown_topic_returns_validation_error(client, valid_payload):
    # K3
    valid_payload["topic"] = "ZOO"
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert [d["field"] for d in error["details"]] == ["topic"]
