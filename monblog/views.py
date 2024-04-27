from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.urls import reverse_lazy

from monblog.models import Transaction, FinancialGoal
from .forms import TransactionForm, GoalForm


@login_required
def index(request):
    user = request.user

    # Récupérer les transactions de l'utilisateur connecté
    transactions = Transaction.objects.filter(user=user)

    # Calculer le solde actuel de l'utilisateur
    income_total = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    expense_total = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = income_total - expense_total

    # Récupérer les objectifs financiers de l'utilisateur
    goals = FinancialGoal.objects.filter(user=user)

    # Vérifier si l'utilisateur a atteint tous les objectifs financiers
    all_goals_achieved = all(balance >= goal.target_amount for goal in goals)

    # Afficher un message de succès unique si tous les objectifs ont été atteints
    if all_goals_achieved:
        messages.success(request, "Félicitations ! Vous avez atteint tous vos objectifs financiers.")

    # Passer les données à votre template
    context = {
        'transactions': transactions,
        'balance': balance,
        'goals': goals
    }

    return render(request, 'monblog/index.html', context)



def accueil(request):
    return render(request, 'monblog/accueil.html')




@login_required(login_url=reverse_lazy('account:login'))
def transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # Enregistrer la transaction dans la base de données
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('monblog:index')
    else:
        form = TransactionForm()

    return render(request, 'monblog/transaction.html', {'form': form})

@login_required(login_url=reverse_lazy('account:login'))
def goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            # Enregistrer les informations dans la base de données
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('monblog:index')
    else:
        form = GoalForm()

    return render(request, 'monblog/goal.html', {'form': form})


