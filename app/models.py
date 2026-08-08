from django.db import models

    # Create your models here.
    """
    Model Fields:
        CharField()
        TextField()
        IntegerField()
        FloatField()
        DecimalField()
        TimeField()
        DateField()
        EmailField()
        URLField()
        ImageField()
        FileField()
        ForeignKey()
    """
    class Department(models.Model):
        name=models.CharField(max_length=50)
        
        def __str__(self):
            return self.name

    class Student(models.Model):
        name=models.CharField(max_length=50)
        address=models.TextField(max_length=50)
        email=models.EmailField(unique=True)
        age=models.IntegerField()
        department=models.ForeignKey(Department, on_delete=models.CASCADE)
        created_at=models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.name    