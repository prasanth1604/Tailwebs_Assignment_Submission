from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, Faculty, SUBJECT_CHOICES
from django import forms
from django.db import IntegrityError, transaction

# Custom form for updating Student marks in the dashboard
class StudentMarkUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['marks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The label now reflects the student's name and subject directly from the instance
        if self.instance and self.instance.pk:
            self.fields['marks'].label = f"Marks for {self.instance.student_name} ({self.instance.get_subject_name_display()})"

class StudentEntryForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'subject_name', 'marks']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a custom placeholder for the student name field if it's a new entry
        if not self.instance.pk:
            self.fields['student_name'].widget.attrs.update({'placeholder': 'e.g., John Doe'})
        self.fields['marks'].widget.attrs.update({'placeholder': 'e.g., 85.50'})


# --- Login and Dashboard Views ---

def loginAsFaculty(request):
    error = ""
    if request.method == 'POST':
        faculty_id_input = request.POST['Faculty_Id']
        password = request.POST['password']

        try:
            faculty_obj = Faculty.objects.get(fId=faculty_id_input, password=password)
            request.session['faculty_id'] = faculty_obj.fId
            messages.success(request, f"Welcome, {faculty_obj.name}! You are logged in.")
            return redirect('facultydashboard')
        except Faculty.DoesNotExist:
            # This block handles the authentication error
            error = "Invalid Faculty ID or Password. Please try again."
            messages.error(request, error)

    return render(request, 'core/loginAsfaculty.html', {'error': error})


def faculty_logout(request):
    if 'faculty_id' in request.session:
        del request.session['faculty_id']
        messages.info(request, "You have been logged out.")
    return redirect('loginAsFaculty')


def facultydashboard(request):
    current_f_id = request.session.get('faculty_id', None)
    if not current_f_id:
        messages.warning(request, "Please log in to access the dashboard.")
        return redirect('loginAsFaculty')

    try:
        faculty_item = Faculty.objects.get(fId=current_f_id)
    except Faculty.DoesNotExist:
        # If faculty_id in session doesn't correspond to an actual faculty, log them out
        if 'faculty_id' in request.session:
            del request.session['faculty_id']
        messages.error(request, "Your faculty session is invalid. Please log in again.")
        return redirect('loginAsFaculty')

    all_students_data = Student.objects.order_by('student_name', 'subject_name')

    forms_list = []
    if request.method == 'POST':
        # Process individual forms
        all_valid = True
        with transaction.atomic():
            for student_entry in all_students_data:
                form_prefix = f'student_{student_entry.pk}'
                form = StudentMarkUpdateForm(request.POST, instance=student_entry, prefix=form_prefix)
                forms_list.append(form)

                if form.is_valid():
                    if form.has_changed():
                        form.save()
                else:
                    all_valid = False
                    # Errors are added to messages in the template logic directly for that specific form
        
        if all_valid:
            messages.success(request, "Student marks updated successfully.")
            return redirect('facultydashboard')
        else:
            messages.error(request, "Some marks could not be updated. Please check the errors below.")

    else: # GET request
        for student_entry in all_students_data:
            form_prefix = f'student_{student_entry.pk}'
            form = StudentMarkUpdateForm(instance=student_entry, prefix=form_prefix)
            forms_list.append(form)

    context = {
        'faculty': faculty_item,
        # Pair the instance with its form for easy iteration in the template
        'student_entries': zip(all_students_data, forms_list), 
    }
    return render(request, 'core/facultydashboard.html', context)


# --- Manage Student Entry View (Add/Edit a single student-subject-mark) ---

def manage_student_entry(request, pk=None):
    current_f_id = request.session.get('faculty_id', None)
    if not current_f_id:
        messages.warning(request, "Please log in to manage student entries.")
        return redirect('loginAsFaculty')

    student_entry_instance = None
    if pk: # This is an EDIT operation (pk is provided)
        student_entry_instance = get_object_or_404(Student, pk=pk)
        title = f'Edit Entry: {student_entry_instance.student_name} ({student_entry_instance.get_subject_name_display()})'
        # When editing, the form is bound to the specific instance
        form = StudentEntryForm(request.POST or None, instance=student_entry_instance)
    else: # This is an ADD operation (pk is None)
        title = 'Add New Student Mark Entry'
        # When adding, the form is not initially bound to an instance
        form = StudentEntryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            student_name = form.cleaned_data['student_name']
            subject_name = form.cleaned_data['subject_name']
            marks = form.cleaned_data['marks']

            try:
                with transaction.atomic():
                    if pk: 
                        form.save() 
                        messages.success(request, f"Entry for '{student_name} - {student_entry_instance.get_subject_name_display()}' updated successfully.")
                        return redirect('facultydashboard')
                    else: 
                        existing_entry = Student.objects.filter(
                            student_name__iexact=student_name, 
                            subject_name=subject_name
                        ).first()

                        if existing_entry:
                            if existing_entry.marks != marks:
                                existing_entry.marks = marks + existing_entry.marks
                                existing_entry.save()
                                messages.info(request, f"Entry for '{student_name} - {existing_entry.get_subject_name_display()}' already exists. {marks} has been added to existing marks.")
                            else:
                                messages.info(request, f"Entry for '{student_name} - {existing_entry.get_subject_name_display()}' already exists with the same marks. No change needed.")
                        else:
                            Student.objects.create(
                                student_name=student_name,
                                subject_name=subject_name,
                                marks=marks
                            )
                            messages.success(request, f"New entry for '{student_name} - {Student(subject_name=subject_name).get_subject_name_display()}' added successfully.")
                        
                        return redirect('facultydashboard')

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
        else:
            messages.error(request, "There was an error with your entry. Please check the form.")
    
    context = {
        'form': form,
        'student_entry': student_entry_instance, 
        'title': title
    }
    return render(request, 'core/student_entry_form.html', context)


# --- Delete Student Entry View ---
def delete_student_entry(request, pk):
    current_f_id = request.session.get('faculty_id', None)
    if not current_f_id:
        messages.warning(request, "Please log in to delete student entries.")
        return redirect('loginAsFaculty')

    student_entry = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        entry_description = f"{student_entry.student_name} - {student_entry.get_subject_name_display()}"
        student_entry.delete()
        messages.success(request, f"Entry for '{entry_description}' has been deleted.")
        return redirect('facultydashboard')
    else:
        messages.info(request, f"Confirm deletion of the entry for '{student_entry.student_name} - {student_entry.get_subject_name_display()}'.")
    return render(request, 'core/student_entry_confirm_delete.html', {'student_entry': student_entry})