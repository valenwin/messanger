from unittest.mock import patch

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from apps.accounts.models import User
from apps.dialogs.models import Thread, Message


def mocked_function():
    return 30


class ThreadTestCase(APITestCase):
    # fixtures = ["initial_data.json"]

    def setUp(self) -> None:
        participants = []
        for i in range(1, 3):
            user = User.objects.create(
                username=f"test{i}",
                first_name=f"Name{i}",
                last_name=f"Lname{i}",
                email=f"test{i}@com",
            )
            user.set_password("testPassword")
            user.save()
            participants.append(user)

        self.thread = Thread.objects.create()
        self.thread.participants.set(participants)

        self.message = Message.objects.create(
            text="hello", thread=self.thread, sender=self.thread.participants.first()
        )

        self.login_url = reverse("api_auth:jwt_login")
        self.threads_list_url = reverse("api_dialogs:threads_list")
        self.thread_details_url = reverse(
            "api_dialogs:thread_details", kwargs={"pk": self.thread.id}
        )

    def _get_user_token(self, username="testUsername", password="testPassword"):
        response = self.client.post(
            self.login_url,
            {"username": username, "password": password},
            format="json",
        )
        response_data = response.json()

        return "JWT {}".format(response_data.get("token", ""))

    def test_get_threads_list_for_user(self):
        user = User.objects.first()
        # call method
        # Force authenticate
        result = self.client.get(
            self.threads_list_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertEqual(data.get("count"), 1)
        self.assertEqual(data["results"][0]["id"], 1)

    def test_get_threads_list_for_user_unauthorized(self):
        # call method
        # Fail due to not authorization
        result = self.client.get(self.threads_list_url)
        # check results
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_valid_thread_for_user(self):
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        valid_payload = {"participants": [{"id": user1.id}, {"id": user2.id}]}
        # call method
        response = self.client.post(
            path=self.threads_list_url,
            data=json.dumps(valid_payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=self._get_user_token(username=user2.username),
        )
        # check results
        data = response.json()
        self.assertEqual(data.get("id"), 2)
        self.assertEqual(len(data.get("participants")), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_thread_for_user_not_exist(self):
        user = User.objects.first()
        invalid_payload = {"participants": [{"id": user.id}, {"id": 144}]}
        # call method
        response = self.client.post(
            path=self.threads_list_url,
            data=json.dumps(invalid_payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_thread_for_user_unauthorized(self):
        user = User.objects.first()
        valid_payload = {"participants": [{"id": user.id}]}
        # call method
        response = self.client.post(
            path=self.threads_list_url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        # check results
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_thread_details_for_user(self):
        user = User.objects.first()
        # call method
        # Force authenticate
        result = self.client.get(
            self.thread_details_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.json()
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(len(data.get("participants")), 2)
        self.assertEqual(data.get("participants"), [{"id": 2}, {"id": 1}])

    def test_get_thread_details_for_user_unauthorized(self):
        # call method
        # Fail due to not authorization
        result = self.client.get(self.thread_details_url)
        # check results
        self.assertEqual(result.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_thread_details_for_user(self):
        user = User.objects.first()
        new_user = User.objects.create(
            username="test3",
            first_name="Name3",
            last_name="Lname3",
            email="test3@com",
        )
        valid_payload = {"participants": [{"id": user.id}, {"id": new_user.id}]}
        # call method
        response = self.client.put(
            path=self.thread_details_url,
            data=json.dumps(valid_payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        data = response.json()
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(len(data.get("participants")), 2)
        self.assertEqual(data.get("participants"), [{"id": 3}, {"id": 2}])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_thread_details_for_user_unauthorized(self):
        user = User.objects.first()
        valid_payload = {"participants": [{"id": user.id}]}
        # call method
        response = self.client.put(
            path=self.thread_details_url,
            data=json.dumps(valid_payload),
            content_type="application/json",
        )
        # check results
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_thread_details_for_user_not_thread_participant(self):
        user = User.objects.first()
        valid_payload = {"participants": [{"id": 3}]}
        # call method
        response = self.client.put(
            path=self.thread_details_url,
            data=json.dumps(valid_payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_thread_for_user_success(self):
        user = User.objects.first()
        # call method
        response = self.client.delete(
            path=self.thread_details_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_thread_not_exists_for_user(self):
        """TODO: check why 204"""
        user = User.objects.first()
        # call method
        response = self.client.delete(
            path=self.thread_details_url,
            kwargs={"pk": 144},
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_thread_no_participants(self):
        """TODO: check why 403"""
        user = User.objects.first()
        valid_payload = {"participants": []}
        # call methods
        result1 = self.client.get(
            self.thread_details_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        response = self.client.put(
            path=self.thread_details_url,
            data=json.dumps(valid_payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        result2 = self.client.get(
            self.thread_details_url,
            HTTP_AUTHORIZATION=self._get_user_token(username=user.username),
        )
        # check results
        data = response.json()
        self.assertEqual(data.get("id"), 1)
        self.assertEqual(len(data.get("participants")), 0)
        self.assertEqual(data.get("participants"), [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result1.status_code, status.HTTP_200_OK)
        self.assertEqual(result2.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(Thread, "get_unread_messages", side_effect=mocked_function)
    def test_get_unread_messages(self, mocked_get_unread_messages):
        self.assertEqual(self.thread.get_unread_messages(), 30)
        message = Message.objects.get(id=1)
        message.is_read = True
        message.save()
        self.assertTrue(mocked_get_unread_messages.called)
        self.assertEqual(mocked_get_unread_messages.call_count, 1)
        self.assertEqual(self.thread.get_unread_messages(), 30)
        self.assertEqual(mocked_get_unread_messages.call_count, 2)

        with patch.object(Thread, "get_unread_messages", return_value=2):
            self.assertEqual(self.thread.get_unread_messages(), 2)
