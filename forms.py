from django import forms
from .models import Assets,AssetType,Branch,Department,Allocation

class AssetsForm(forms.ModelForm):
    class Meta:
        model = Assets
        fields = '__all__'
        widgets = {
            'po_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_start_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'comments': forms.Textarea(attrs={'rows': 3}),
        }


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = ['name']


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['branch', 'department', 'employee_name', 'employee_id', 'maintenance_date']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }

