from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.student_id = form.cleaned_data.get('student_id', '')
            user.course = form.cleaned_data.get('course', '')
            user.auth_type = 'manual'
            user.save()
            messages.success(
                request, f"✅ Account created! Welcome, {user.first_name}. Please log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {error}")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(
                    request, f"✅ Welcome back, {user.display_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "❌ Incorrect username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "👋 You've been logged out successfully.")
    return redirect('home_page')


@login_required
def dashboard_view(request):
    from skills.models import Skill, Connection
    teach_skills = Skill.objects.filter(user=request.user, skill_type='Teach')
    learn_skills = Skill.objects.filter(user=request.user, skill_type='Learn')
    sent_connections = Connection.objects.filter(
        requester=request.user).select_related('provider')
    recv_connections = Connection.objects.filter(
        provider=request.user).select_related('requester')

    # Clear connection history
    if request.method == 'POST' and 'clear_history' in request.POST:
        from skills.models import Connection
        Connection.objects.filter(requester=request.user).delete()
        from django.contrib import messages as msg
        msg.success(request, "🗑️ Connection history cleared.")
        return redirect('dashboard')

    # Accept a connection request
    if request.method == 'POST' and 'accept_id' in request.POST:
        conn_id = request.POST.get('accept_id')
        try:
            conn = Connection.objects.get(id=conn_id, provider=request.user)
            conn.status = 'Accepted'
            conn.save()
            from django.contrib import messages
            messages.success(
                request, f"✅ You accepted {conn.requester.display_name}'s request!")
        except Connection.DoesNotExist:
            pass
        return redirect('dashboard')

    return render(request, 'accounts/dashboard.html', {
        'teach_skills':     teach_skills,
        'learn_skills':     learn_skills,
        'connections':      sent_connections,
        'recv_connections': recv_connections,
        'teach_count':      teach_skills.count(),
        'learn_count':      learn_skills.count(),
        'conn_count':       sent_connections.count(),
    })
