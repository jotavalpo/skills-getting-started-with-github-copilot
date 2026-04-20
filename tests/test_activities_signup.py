from src import app as app_module


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    signup_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    signup_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    signup_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_returns_400_for_invalid_email_format(client):
    # Arrange
    activity_name = "Chess Club"
    email = "invalid-email"
    signup_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email format"}


def test_signup_returns_400_for_empty_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = ""
    signup_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(signup_path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email format"}


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    email = "capacity.test@mergington.edu"
    signup_path = f"/activities/{activity_name}/signup"
    app_module.activities[activity_name]["max_participants"] = len(
        app_module.activities[activity_name]["participants"]
    )

    # Act
    response = client.post(signup_path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}


def test_delete_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    delete_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(delete_path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_delete_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"
    delete_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(delete_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_delete_returns_404_for_missing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-registered@mergington.edu"
    delete_path = f"/activities/{activity_name}/signup"

    # Act
    response = client.delete(delete_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
