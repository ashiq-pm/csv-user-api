from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User


class CSVUploadTest(APITestCase):

    def test_valid_and_invalid_data(self):
        csv_content = """name,email,age
John,john@test.com,25
Invalid,invalidemail,200
"""

        file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )

        response = self.client.post("/api/upload-csv/", {'file': file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["saved_records"], 1)
        self.assertEqual(response.data["rejected_records"], 1)

    def test_duplicate_email(self):
        User.objects.create(name="Existing", email="dup@test.com", age=30)

        csv_content = """name,email,age
New User,dup@test.com,25
"""

        file = SimpleUploadedFile(
            "test.csv",
            csv_content.encode('utf-8'),
            content_type="text/csv"
        )

        response = self.client.post("/api/upload-csv/", {'file': file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["skipped_duplicates"], 1)

    def test_invalid_file_type(self):
        file = SimpleUploadedFile("test.txt", b"invalid data")

        response = self.client.post("/api/upload-csv/", {'file': file})

        self.assertEqual(response.status_code, 400)