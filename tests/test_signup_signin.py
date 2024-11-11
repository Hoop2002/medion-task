import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_sign_up_sign_in(client):
    url = reverse("sign_up")
    fake_data = {
        "email": "test@test.te",
        "full_name": "Иванов Иван Иванович",
        "password1": "passwordpassword",
        "password2": "passwordpassword",
    }

    response = client.post(url, fake_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data["email"] == fake_data["email"]
    assert response.data["full_name"] == fake_data["full_name"]

    User = get_user_model()
    user = User.objects.get(email=fake_data["email"])
    assert user is not None

    url_2 = reverse("sign_in")

    fake_data_2 = {"email": "test@test.te", "password": "passwordpassword"}

    response_2 = client.post(url_2, fake_data_2, format="json")

    assert response_2.status_code == status.HTTP_200_OK

    assert response_2.data.get("access", False)
    assert response_2.data.get("refresh", False)
