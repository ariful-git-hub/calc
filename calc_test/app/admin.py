from django.contrib import admin

# Register your models here.
from .models import Variable, Formula , VariableWeight


admin.site.register(VariableWeight)

class VariableAdmin(admin.ModelAdmin):
    list_display = ("id","name", "short_names")

admin.site.register(Variable,VariableAdmin)

class VariableInline(admin.TabularInline):
    model = Formula.variables.through  # For the many-to-many relationship
    extra = 1

class FormulaAdmin(admin.ModelAdmin):
    inlines = [VariableInline]  # Show the related variables inline
    list_display = ('id', 'name')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # First save the formula
        # Update the name based on the variables
        if obj.variables.exists():  # Only call if there are variables
            obj.update_name()
admin.site.register(Formula, FormulaAdmin)
