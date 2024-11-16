from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import render, get_object_or_404, redirect

from .utils import read_data, write_data
from .serializers import BookSerializer
from .models import Employee
from .forms import EmployeeForm
import json
import os
from django.conf import settings
from django.shortcuts import render


class BookListView(APIView):
    def get(self, request):
        data = read_data()
        return Response(data)
        
    

    def post(self, request):
        data = read_data()
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            new_book = serializer.data
            new_book['id'] = max([book['id'] for book in data], default=0) + 1
            data.append(new_book)
            write_data(data)
            return Response(new_book, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    def get(self, request, book_id):
        book = self.get_object(book_id)
        if book is None:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(book)

    def get_object(self, book_id):
        data = read_data()
        for book in data:
            if book['id'] == book_id:
                return book
        return None


class BookDeleteView(APIView):
    def delete(self, request, book_id):
        book = self.get_object(book_id)
        if book is None:
            return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        data = read_data()
        data.remove(book)
        write_data(data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, book_id):
        data = read_data()
        for book in data:
            if book['id'] == book_id:
                return book
        return None


class BookUpdateView(APIView):
    def put(self, request, book_id):
        data = read_data()
        book = self.get_object(book_id)
        if book is None:
            return Response({"error": "Book is not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            update_book = serializer.data
            update_book['id'] = book_id
            for i, b in enumerate(data):
                if b['id'] == book_id:
                    data[i] = update_book
            write_data(data)
            return Response(update_book)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, book_id):
        data = read_data()
        for book in data:
            if book['id'] == book_id:
                return book
        return None
    





    






def list(request):
    items = Employee.objects.all()  
    return render(request, 'app/list.html', {'items': items})


def create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = EmployeeForm()
    return render(request, 'app/form.html', {'form': form})


def update(request, pk):
    item = get_object_or_404(Employee, pk=pk)  
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = EmployeeForm(instance=item) 
    return render(request, 'app/update.html', {'form': form})





def delete(request, pk):
    item = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list')
    return render(request, 'app/delete.html', {'item': item})


from rest_framework.viewsets import ModelViewSet


class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()  # Получение всех записей из модели
    serializer_class = BookSerializer

