"""FastAPI tests using the Arrange-Act-Assert (AAA) pattern."""


def test_get_activities(client):
    """Test that GET /activities returns all activities with expected structure."""
    # Arrange - no setup needed; activities are pre-loaded

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "participants" in data["Chess Club"]
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    """Test that POST /activities/{activity_name}/signup adds a participant."""
    # Arrange
    activity = "Tennis Club"
    email = "new_student@example.com"
    response = client.get(f"/activities")
    initial_count = len(response.json()[activity]["participants"])

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json().get("message", "")
    
    # Verify participant was added
    response = client.get("/activities")
    updated_count = len(response.json()[activity]["participants"])
    assert updated_count == initial_count + 1
    assert email in response.json()[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    """Test that signing up twice for the same activity returns 400."""
    # Arrange
    activity = "Basketball Team"
    email = "duplicate_test@example.com"

    # Act - first signup
    response1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act - duplicate signup
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already signed up" in response2.json().get("detail", "").lower()


def test_delete_removes_participant(client):
    """Test that DELETE /activities/{activity_name}/participants removes a participant."""
    # Arrange
    activity = "Art Studio"
    email = "remove_me@example.com"
    # First, sign up the participant
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json().get("message", "")
    
    # Verify participant was removed
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404."""
    # Arrange
    nonexistent_activity = "Nonexistent Activity"
    email = "test@example.com"

    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")


def test_delete_nonexistent_activity_returns_404(client):
    """Test that deleting from a non-existent activity returns 404."""
    # Arrange
    nonexistent_activity = "Nonexistent Activity"
    email = "test@example.com"

    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")


def test_delete_nonexistent_participant_returns_404(client):
    """Test that deleting a non-existent participant from an activity returns 404."""
    # Arrange
    activity = "Drama Club"
    nonexistent_email = "notreal@example.com"

    # Act
    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": nonexistent_email}
    )

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")
