import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import UserSerializer
from .models import User


class UploadCSVView(APIView):
    """
    API endpoint to upload and process CSV file containing user data.
    Performs validation, duplicate handling, and bulk insertion.
    """

    def post(self, request):
        file = request.FILES.get('file')

        # 1️⃣ File validation
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        if not file.name.endswith('.csv'):
            return Response({"error": "Only CSV files are allowed"}, status=400)

        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
        except Exception:
            return Response({"error": "Invalid CSV file format"}, status=400)

        # 2️⃣ Header validation
        required_fields = {'name', 'email', 'age'}
        if not reader.fieldnames or not required_fields.issubset(set(reader.fieldnames)):
            return Response({
                "error": f"CSV must contain headers: {required_fields}"
            }, status=400)

        success_count = 0
        error_count = 0
        duplicate_count = 0
        errors = []
        valid_users = []

        existing_emails = set(User.objects.values_list('email', flat=True))

        # 3️⃣ Process rows
        for i, row in enumerate(reader, start=1):

            serializer = UserSerializer(data=row)

            if serializer.is_valid():
                email = serializer.validated_data['email']

                if email in existing_emails:
                    duplicate_count += 1
                    continue

                valid_users.append(User(**serializer.validated_data))
                existing_emails.add(email)
                success_count += 1

            else:
                error_count += 1
                errors.append({
                    "row": i,
                    "data": row,
                    "errors": serializer.errors
                })

        # 4️⃣ Bulk insert (PERFORMANCE OPTIMIZATION)
        try:
            with transaction.atomic():
                User.objects.bulk_create(valid_users, batch_size=1000)
        except Exception as e:
            return Response({
                "error": "Database error during bulk insert",
                "details": str(e)
            }, status=500)

        # 5️⃣ Final response
        return Response({
            "status": "success",
            "total_records": success_count + error_count + duplicate_count,
            "saved_records": success_count,
            "rejected_records": error_count,
            "skipped_duplicates": duplicate_count,
            "errors": errors
        }, status=status.HTTP_200_OK)