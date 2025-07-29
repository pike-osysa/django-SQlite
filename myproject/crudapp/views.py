from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentForm, RegisterForm
from .models import Student

# View to list students
def student_list(request):
    students = Student.objects.all()
    return render(request, 'studentlist.html', {'students': students})

# View to add a student
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'studentform.html', {'form': form})

# View to update a student
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully!")
        return redirect('student_list')
    
    return render(request, 'studentform.html', {'form': form})

# View to delete a student
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, f"Student '{student.name}' has been deleted.")
    return redirect('student_list')

# View to register a user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('student_list')  # or redirect to 'login'
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def log_out(request):
    logout(request)
    return render(request, 'logout.html')


