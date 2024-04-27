from django import forms
from .models import Transaction, FinancialGoal

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'category', 'type', 'date', 'description']
        widgets ={
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = FinancialGoal
        fields = ['name', 'target_amount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Vérifier si la date de fin est postérieure à la date de début
        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")

        return cleaned_data
