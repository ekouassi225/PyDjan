from django.contrib import admin
from .models import UserProfile, Transaction, FinancialGoal, TransactionCategory

# Enregistrer vos modèles ici
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(FinancialGoal)
admin.site.register(TransactionCategory)
