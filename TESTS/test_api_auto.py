from fastapi.testclient import TestClient
import time
import sys,os
sys.path.append('../APP')
from main import app

client = TestClient(app=app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"length": 4}


def test_get_question():
    response = client.get("/get_question/1")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"question": "What is your name?"}


def test_question_contains_attachment():
    response = client.get("/get_question/4")
    assert response.status_code == 200
    assert '4_input' in str(response.json())
    assert '4_starter' in str(response.json())


def test_submit_answer():
    response = client.post("/submit_answer", json={"id": "1", "answer": "Sanjin", "team_name": "team1"})
    assert response.status_code == 200
    assert "Correct" in response.json()["message"]


def test_submit_second_answer():
    response = client.post("/submit_answer", json={"id": "2", "answer": "38", "team_name": "team1"})
    assert response.status_code == 200
    assert "Correct" in response.json()["message"]


def test_submit_answer_again():
    response = client.post("/submit_answer", json={"id": "1", "answer": "Sanjin", "team_name": "team1"})
    assert response.status_code == 200
    assert "Already solved" in response.json()["message"]


def test_submit_answer_wrong():
    response = client.post("/submit_answer", json={"id": "1", "answer": "Bob", "team_name": "team1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Incorrect"}


def test_submit_answer_nonexisting():
    response = client.post("/submit_answer", json={"id": "10000", "answer": "Bob", "team_name": "team1"})
    assert response.status_code == 200
    assert response.json() == {"message": "Question not found"}


def test_download_input_file():
    response = client.get("/download_input_file/4")
    assert response.status_code == 200
    assert "tiptxlhgxngznvwy" in response.text


def test_download_starter_code():
    response = client.get("/download_starter_code/4")
    assert response.status_code == 200
    assert "for s in strings:" in response.text


def test_valid_login():
    response = client.post("/login", json={"name": "team1", "password": "team1"})
    assert response.status_code == 200
    assert "Login successful" in response.json()["message"]


def test_invalid_login():
    response = client.post("/login", json={"name": "team1", "password": "xxxxx"})
    print(response.json())
    assert response.status_code == 200
    assert "Login failed" in response.json()["message"]


def test_get_teams_table():
    response = client.get("/get_teams_table")
    assert response.status_code == 200
    assert "team1" in response.json()["teams"][0][0]
    assert "team2" in response.json()["teams"][1][0]
    assert "team3" in response.json()["teams"][2][0]
    assert "team4" in response.json()["teams"][3][0]
    assert response.json()["teams"][0][2] == 20
    assert response.json()["teams"][1][2] == 0
    assert response.json()["teams"][2][2] == 0
    assert response.json()["teams"][3][2] == 0
    assert response.json()["teams"][0][3] == '[1, 2]'

def submit_answer1():
    response = client.post("/submit_answer", json={"id": "1", "answer": "Sanjin", "team_name": "team1"})
    print(response.json())
    print(response.status_code)
    print(response.content)

def get_teams_table():
    response = client.get("/get_teams_table")
    print(response.json())


#this always needs to be the last test
def reset_db_just_run_file():
    time.sleep(1)
    script_path = os.path.join(os.path.dirname(__file__), '..', 'APP', 'reset_db.py')
    with open(script_path) as f:
        exec(f.read())
    time.sleep(1)


reset_db_just_run_file()
get_teams_table()
