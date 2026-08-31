from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')  # ← CHANGED

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
        return redirect('accounts:dashboard')  # ← CHANGED

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
                return redirect('accounts:dashboard')  # ← CHANGED
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
        return redirect('accounts:dashboard')  # ← CHANGED

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
        return redirect('accounts:dashboard')  # ← CHANGED

    return render(request, 'accounts/dashboard.html', {
        'teach_skills':     teach_skills,
        'learn_skills':     learn_skills,
        'connections':      sent_connections,
        'recv_connections': recv_connections,
        'teach_count':      teach_skills.count(),
        'learn_count':      learn_skills.count(),
        'conn_count':       sent_connections.count(),
    })


# ============ SKILL MANAGEMENT FUNCTIONS ============

@login_required
def add_skill_view(request):
    """Add a new skill (Teach or Learn)"""
    from skills.models import Skill

    if request.method == 'POST':
        skill_name = request.POST.get('skill_name', '').strip()
        skill_type = request.POST.get('skill_type', '')

        if not skill_name:
            messages.error(request, "❌ Please enter a skill name.")
            return redirect('accounts:dashboard')  # ← CHANGED

        if skill_type not in ['Teach', 'Learn']:
            messages.error(request, "❌ Invalid skill type.")
            return redirect('accounts:dashboard')  # ← CHANGED

        # Check if skill already exists for this user
        existing = Skill.objects.filter(
            user=request.user,
            skill_name__iexact=skill_name,
            skill_type=skill_type
        ).first()

        if existing:
            messages.warning(
                request, f"⚠️ You already have '{skill_name}' in your {skill_type} skills.")
        else:
            Skill.objects.create(
                user=request.user,
                skill_name=skill_name,
                skill_type=skill_type
            )
            messages.success(
                request, f"✅ '{skill_name}' added to your {skill_type} skills!")

    return redirect('accounts:dashboard')  # ← CHANGED


@login_required
def delete_skill_view(request, skill_id):
    """Delete a skill"""
    from skills.models import Skill

    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    skill_name = skill.skill_name
    skill_type = skill.skill_type
    skill.delete()

    messages.success(
        request, f"🗑️ '{skill_name}' removed from your {skill_type} skills.")
    return redirect('accounts:dashboard')  # ← CHANGED
