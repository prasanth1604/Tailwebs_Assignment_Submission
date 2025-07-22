from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Define the hardcoded subject choices
SUBJECT_CHOICES = [
    ('MATH', 'Mathematics'),
    ('SCI', 'Science'),
    ('HIST', 'History'),
    ('ENG', 'English'),
    ('CS', 'Computer Science'),
]

class Faculty(models.Model):
    fId = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)  # Store hashed passwords
    

    def __str__(self):
        return f"{self.name} ({self.fId})"


class Student(models.Model):
    # This model now directly holds student name, subject, and marks
    student_name = models.CharField(max_length=100) 
    subject_name = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    marks = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0, message="Marks cannot be less than 0."),
            MaxValueValidator(100, message="Marks cannot be greater than 100.")
        ]
    )

    class Meta:
        verbose_name = "Student Subject Mark"
        verbose_name_plural = "Student Subject Marks"

    def __str__(self):
        # get_subject_name_display() is a Django convenience method for choices
        return f"{self.student_name} - {self.get_subject_name_display()}: {self.marks}"