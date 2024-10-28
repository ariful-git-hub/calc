from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Variable(models.Model):
    """Models for storing Variables."""
    
    name = models.CharField(max_length=100)
    short_names = models.CharField(max_length=50,blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
class Formula(models.Model):
    """Models for storing the formula."""
    name = models.CharField(max_length=100, blank=True)
    variables = models.ManyToManyField(Variable)

    def __str__(self):
        return self.name if self.name else "Unnamed Formula"

    def update_name(self):
        if self.variables.exists():
            short_names = sorted([var.short_names for var in self.variables.all()])
            formula_name = ''.join(short_names)
            # Update the formula name if it has changed
            if self.name != formula_name:
                self.name = formula_name
                self.save(update_fields=['name'])  # Save only the name field to avoid recursion
        else:
            print(f"No variable detected.")
    
# @receiver(post_save, sender=Formula)
# def generate_formula_name(sender, instance, created, **kwargs):
#     print(f"Formula saved: {instance.id}, Created: {created}")  # Debugging line
#     if created:  # Only run for new instances
#         if instance.variables.exists():
#             short_names = sorted([var.short_name for var in instance.variables.all()])
#             formula_name = ''.join(short_names)
#             print(f"Formula name {formula_name}")
#             if instance.name != formula_name:
#                 print(f"Updating name from '{instance.name}' to '{formula_name}'")  # Debugging line
#                 instance.name = formula_name
#                 instance.save(update_fields=['name'])

    
class VariableWeight(models.Model):
    """Models for storing the weight of the varible for different types of Formula."""
    weight = models.DecimalField(max_digits=5,decimal_places=3)
    variable = models.ForeignKey(Variable,on_delete=models.CASCADE)
    formula = models.ForeignKey(Formula,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("variable", "formula")
        
    def __str__(self):
        return f"The weight of the {self.variable} in {self.formula.name} is {self.weight}."