from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# 1. Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in immediately after signing up
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 2. Protect your Employee views
@login_required(login_url='login')

def home(request):
    employee = Employee.objects.all() 
    return render(request, 'home.html', {'employee': employee})

def create_view(request):
    return render(request, 'create.html')

def create_emp(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        emp_name = request.POST.get('emp_name')
        emp_dept = request.POST.get('emp_dept')

        if emp_id and emp_name and emp_dept:
            Employee.objects.create(emp_id=emp_id, emp_name=emp_name, emp_dept=emp_dept)
        return redirect('/')
    return render(request, 'create.html')

def update_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'update.html', {'employee': employee})

def update_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.emp_id = request.POST.get('emp_id', employee.emp_id)
        employee.emp_name = request.POST.get('emp_name', employee.emp_name)
        employee.emp_dept = request.POST.get('emp_dept', employee.emp_dept)
        employee.save()
        return redirect('/')
    return render(request, 'update.html', {'employee': employee})

def delete_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('/')