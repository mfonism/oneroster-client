from datetime import datetime

import pytest
import requests

import api
import entity


def test_client():
    client = api.Client("a-test-client-id", "a-test-client-secret")

    assert client.token_url == "https://test.com/token"
    assert client.base_url == "https://test.com/api"
    assert client.client_id == "a-test-client-id"
    assert client.client_secret == "a-test-client-secret"

    assert client.access_token == "a-test-access-token"


def test_get_headers(client_id, client_secret):
    client = api.Client(client_id, client_secret)
    headers = client.get_headers()

    assert headers == {
        "Authorization": "Bearer a-test-access-token",
        "Content-Type": "application/json",
    }


def test_fetch_data(requests_mock, client_id, client_secret):
    client = api.Client(client_id, client_secret)
    url = f"{client.base_url}/test-data"

    requests_mock.get(url, json={"key": "value"})

    response = client.fetch_data(url)
    assert response == {"key": "value"}


def test_fetch_data_raises_for_status(requests_mock, client_id, client_secret):
    client = api.Client(client_id, client_secret)
    url = f"{client.base_url}/test-data"

    requests_mock.get(url, status_code=404)

    with pytest.raises(requests.exceptions.HTTPError):
        client.fetch_data(url)


def test_get_all_teachers(requests_mock, client_id, client_secret):
    client = api.Client(client_id, client_secret)

    url = f"{client.base_url}/teachers"
    mock_response = {
        "users": [
            {
                "sourcedId": "a-test-teacher-sourced-id",
                "status": "active",
                "dateLastModified": "2021-08-09T12:30:00Z",
                "metadata": {"meta": "data"},
                "enabledUser": "true",
                "username": "jqdoe",
                "givenName": "Jane",
                "middleName": "Q",
                "familyName": "Doe",
                "role": "teacher",
                "email": "jqdoe@test.com",
            },
        ]
    }

    requests_mock.get(url, json=mock_response)

    teachers = client.get_all_teachers()
    assert len(teachers) == 1
    assert all(isinstance(teacher, api.User) for teacher in teachers)

    teacher = teachers[0]
    assert teacher.sourced_id == "a-test-teacher-sourced-id"
    assert teacher.status == entity.Status.ACTIVE
    assert teacher.last_modified == datetime.fromisoformat("2021-08-09T12:30:00Z")
    assert teacher.metadata == {"meta": "data"}
    assert teacher.active
    assert teacher.username == "jqdoe"
    assert teacher.firstname == "Jane"
    assert teacher.middlename == "Q"
    assert teacher.lastname == "Doe"
    assert teacher.role == entity.Role.TEACHER
    assert teacher.email == "jqdoe@test.com"


def test_get_classes_for_teacher(requests_mock, client_id, client_secret):
    client = api.Client(client_id, client_secret)
    teacher_sourced_id = "a-test-teacher-sourced-id"

    url = f"{client.base_url}/teachers/{teacher_sourced_id}/classes"
    mock_response = {
        "classes": [
            {
                "sourcedId": "a-test-class-sourced-id-01",
                "status": "active",
                "dateLastModified": "2021-08-09T01:01:01Z",
                "title": "Math 101",
                "metadata": {"meta": "data"},
                "periods": ["1", "2"],
            },
            {
                "sourcedId": "a-test-class-sourced-id-02",
                "status": "active",
                "dateLastModified": "2021-08-09T02:02:02Z",
                "title": "English 101",
                "metadata": {"meta": "data"},
                "periods": ["99", "999"],
            },
        ]
    }

    requests_mock.get(url, json=mock_response)

    classes = client.get_classes_for_teacher(teacher_sourced_id)
    assert len(classes) == 2
    assert all(isinstance(class_, api.Class) for class_ in classes)

    class_1 = classes[0]
    assert class_1.sourced_id == "a-test-class-sourced-id-01"
    assert class_1.status == entity.Status.ACTIVE
    assert class_1.last_modified == datetime.fromisoformat("2021-08-09T01:01:01Z")
    assert class_1.name == "Math 101"
    assert class_1.periods == ["1", "2"]
    assert class_1.metadata == {"meta": "data"}

    class_2 = classes[1]
    assert class_2.sourced_id == "a-test-class-sourced-id-02"
    assert class_2.status == entity.Status.ACTIVE
    assert class_2.last_modified == datetime.fromisoformat("2021-08-09T02:02:02Z")
    assert class_2.name == "English 101"
    assert class_2.periods == ["99", "999"]
    assert class_2.metadata == {"meta": "data"}


def test_get_students_for_class(requests_mock, client_id, client_secret):
    client = api.Client(client_id, client_secret)
    class_sourced_id = "a-test-class-sourced-id"

    url = f"{client.base_url}/classes/{class_sourced_id}/students"
    mock_response = {
        "users": [
            {
                "sourcedId": "a-student-sourced-id-01",
                "status": "active",
                "dateLastModified": "2021-08-09T12:30:00Z",
                "metadata": {"meta": "data"},
                "enabledUser": "true",
                "username": "JayDoey",
                "givenName": "Johnny",
                "familyName": "Doey",
                "role": "student",
                "email": "jaydoey@test.com",
            },
            {
                "sourcedId": "a-student-sourced-id-10",
                "status": "active",
                "dateLastModified": "2021-08-10T08:15:00Z",
                "metadata": {"meta": "data"},
                "enabledUser": "true",
                "username": "arlise",
                "givenName": "Arlise",
                "middleName": "Inn",
                "familyName": "Vunderland",
                "role": "student",
            },
        ]
    }

    requests_mock.get(url, json=mock_response)

    students = client.get_students_for_class(class_sourced_id)
    assert len(students) == 2
    assert all(isinstance(student, entity.User) for student in students)

    student = students[0]
    assert student.sourced_id == "a-student-sourced-id-01"
    assert student.status == entity.Status.ACTIVE
    assert student.last_modified == datetime.fromisoformat("2021-08-09T12:30:00Z")
    assert student.metadata == {"meta": "data"}
    assert student.active
    assert student.username == "JayDoey"
    assert student.firstname == "Johnny"
    assert student.middlename is None
    assert student.lastname == "Doey"
    assert student.role == entity.Role.STUDENT
    assert student.email == "jaydoey@test.com"

    student = students[1]
    assert student.sourced_id == "a-student-sourced-id-10"
    assert student.status == entity.Status.ACTIVE
    assert student.last_modified == datetime.fromisoformat("2021-08-10T08:15:00Z")
    assert student.metadata == {"meta": "data"}
    assert student.active
    assert student.username == "arlise"
    assert student.firstname == "Arlise"
    assert student.middlename == "Inn"
    assert student.lastname == "Vunderland"
    assert student.role == entity.Role.STUDENT
    assert student.email is None
