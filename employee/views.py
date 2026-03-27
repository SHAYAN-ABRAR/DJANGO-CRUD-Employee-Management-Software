from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmployeeSerializer
import openpyxl
from django.http import HttpResponse
from reportlab.pdfgen import canvas

# --- 1. AUTHENTICATION ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# --- 2. MAIN VIEWS ---
@login_required(login_url='login')
def home(request):
    query = request.GET.get('search', '')
    base_query = Employee.objects.filter(is_deleted=False)
    
    if query:
        employee_list = base_query.filter(
            Q(emp_id__icontains=query) | 
            Q(emp_name__icontains=query) | 
            Q(emp_dept__icontains=query)
        ).order_by('-id') 
    else:
        employee_list = base_query.order_by('-id')

    paginator = Paginator(employee_list, 5) 
    page_number = request.GET.get('page')
    employee_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'employee': employee_obj, 
        'query': query
    })

# --- 3. CRUD OPERATIONS ---
@login_required(login_url='login')
def create_view(request):
    return render(request, 'create.html')

@login_required(login_url='login')
def create_emp(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        emp_name = request.POST.get('emp_name')
        emp_dept = request.POST.get('emp_dept')

        try:
            emp_id = int(emp_id) 
            if emp_id and emp_name and emp_dept:
                Employee.objects.create(emp_id=emp_id, emp_name=emp_name, emp_dept=emp_dept)
                messages.success(request, f"Employee {emp_name} added successfully!")
                return redirect('home')
        except ValueError:
            messages.error(request, "Error: Employee ID must be a number!")
            return redirect('create_view')
    return redirect('home')

@login_required(login_url='login')
def update_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'update.html', {'employee': employee})

@login_required(login_url='login')
def update_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        employee.emp_id = request.POST.get('emp_id', employee.emp_id)
        employee.emp_name = request.POST.get('emp_name', employee.emp_name)
        employee.emp_dept = request.POST.get('emp_dept', employee.emp_dept)
        employee.save()
        messages.success(request, f"Employee {employee.emp_name} updated!")
        return redirect('home')
    return redirect('update_view', id=id)

# --- 4. TRASH & SOFT DELETE ---
@login_required(login_url='login')
def delete_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.is_deleted = True 
        employee.save()
        messages.warning(request, f"Employee {employee.emp_name} moved to trash.")
    return redirect('home')

@login_required(login_url='login')
def trash_view(request):
    deleted_employees = Employee.objects.filter(is_deleted=True).order_by('-id')
    return render(request, 'trash.html', {'employees': deleted_employees})

@login_required(login_url='login')
def restore_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        employee.is_deleted = False 
        employee.save()
        messages.success(request, f"Employee {employee.emp_name} has been restored!")
    return redirect('trash_view')

@login_required(login_url='login')
def permanent_delete_emp(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == "POST":
        name = employee.emp_name
        employee.delete() 
        messages.error(request, f"Employee {name} has been permanently deleted.")
    return redirect('trash_view')

# --- 5. EXPORT FEATURES (Corrected Indentation & Filtering) ---
@login_required(login_url='login')
def export_employees_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Employees"

    ws.append(['ID', 'Name', 'Department'])

    # Only export employees NOT in trash
    for emp in Employee.objects.filter(is_deleted=False):
        ws.append([emp.emp_id, emp.emp_name, emp.emp_dept])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="employee_list.xlsx"'
    wb.save(response)
    return response

@login_required(login_url='login')
def export_employees_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Employee Records Report")
    
    p.setFont("Helvetica", 12)
    y = 750
    # Only export employees NOT in trash
    for emp in Employee.objects.filter(is_deleted=False):
        p.drawString(100, y, f"ID: {emp.emp_id} | Name: {emp.emp_name} | Dept: {emp.emp_dept}")
        y -= 20 
        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    return response

# --- 6. API VIEWS ---
class EmployeeListAPI(APIView):
    def get(self, request):
        employees = Employee.objects.filter(is_deleted=False)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailAPI(APIView):
    def delete(self, request, pk):
        employee = get_object_or_404(Employee, id=pk)
        employee.is_deleted = True
        employee.save()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)