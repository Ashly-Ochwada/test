# workerdata/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Worker, Receipt
from .serializers import WorkerSerializer, ReceiptSerializer
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import WorkerForm
import pytesseract
from PIL import Image

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        worker_serializer = self.get_serializer(data=request.data)
        worker_serializer.is_valid(raise_exception=True)
        worker = worker_serializer.save()

        utility_files = request.FILES.getlist('utility_bill_history')
        rent_files = request.FILES.getlist('rent_payment_history')
        repayment_files = request.FILES.getlist('repayment_history')

        if len(utility_files) != 6:
            worker.delete()
            return Response({'detail': 'Please upload exactly 6 utility bill receipts.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(rent_files) != 6:
            worker.delete()
            return Response({'detail': 'Please upload exactly 6 rent payment receipts.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(repayment_files) != 6:
            worker.delete()
            return Response({'detail': 'Please upload exactly 6 repayment receipts.'}, status=status.HTTP_400_BAD_REQUEST)

        id_photo = request.FILES['id_photo']
        id_text = self.extract_id_text(id_photo)
        if worker.national_id not in id_text:
            worker.delete()
            return Response({'detail': 'The ID number does not match the one in the uploaded photo.'}, status=status.HTTP_400_BAD_REQUEST)

        self.save_receipts(worker, utility_files, 'utility_bill')
        self.save_receipts(worker, rent_files, 'rent_payment')
        self.save_receipts(worker, repayment_files, 'repayment')

        headers = self.get_success_headers(worker_serializer.data)
        return Response(worker_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def extract_id_text(self, id_photo):
        image = Image.open(id_photo)
        text = pytesseract.image_to_string(image)
        return text

    def save_receipts(self, worker, files, receipt_type):
        for file in files:
            Receipt.objects.create(worker=worker, receipt_type=receipt_type, file=file)

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class AddWorkerView(View):
    def get(self, request):
        form = WorkerForm()
        return render(request, 'workerdata/add_worker.html', {'form': form})

    def post(self, request):
        form = WorkerForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            id_photo = request.FILES['id_photo']
            id_text = extract_id_text(id_photo)
            if worker.national_id not in id_text:
                form.add_error('national_id', 'The ID number does not match the one in the uploaded photo.')
            else:
                worker.save()
                utility_files = request.FILES.getlist('utility_bill_history')
                rent_files = request.FILES.getlist('rent_payment_history')
                repayment_files = request.FILES.getlist('repayment_history')

                if len(utility_files) != 6:
                    form.add_error(None, 'Please upload exactly 6 utility bill receipts.')
                elif len(rent_files) != 6:
                    form.add_error(None, 'Please upload exactly 6 rent payment receipts.')
                elif len(repayment_files) != 6:
                    form.add_error(None, 'Please upload exactly 6 repayment receipts.')
                else:
                    save_receipts(worker, utility_files, 'utility_bill')
                    save_receipts(worker, rent_files, 'rent_payment')
                    save_receipts(worker, repayment_files, 'repayment')
                    return redirect('success_url')
        return render(request, 'workerdata/add_worker.html', {'form': form})

def extract_id_text(id_photo):
    image = Image.open(id_photo)
    text = pytesseract.image_to_string(image)
    return text

def save_receipts(worker, files, receipt_type):
    for file in files:
        Receipt.objects.create(worker=worker, receipt_type=receipt_type, file=file)
