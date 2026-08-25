from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Skill, Connection
from django.db.models import Count


User = get_user_model()


@login_required
def add_skill(request):
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name', '').strip()
        skill_type = request.POST.get('skill_type', 'Teach')

        if not skill_name:
            messages.warning(request, "⚠️ Please enter a skill name.")
            return redirect('dashboard')

        skill, created = Skill.objects.get_or_create(
            user=request.user,
            skill_name=skill_name,
            skill_type=skill_type,
        )
        if created:
            messages.success(
                request, f"✅ '{skill_name}' added to your {skill_type} list!")
        else:
            messages.warning(
                request, f"⚠️ You already have '{skill_name}' in your {skill_type} list.")

    return redirect('dashboard')


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    skill.delete()
    messages.success(
        request, f"🗑️ '{skill.skill_name}' removed from your {skill.skill_type} list.")
    return redirect('dashboard')


@login_required
def find_skills(request):
    query = request.GET.get('q', '').strip()
    results = []

    # All skills on the platform for the tag cloud
    all_skills = Skill.objects.filter(
        skill_type='Teach'
    ).exclude(
        user=request.user
    ).values_list('skill_name', flat=True).distinct()

    if query:
        # Synonym expansion so "maths" finds "Calculus" etc.
        synonyms = {
            'maths':   'mathematics calculus statistics algebra',
            'math':    'mathematics calculus statistics algebra',
            'coding':  'python programming javascript web development',
            'design':  'graphic design ui ux adobe illustrator canva',
            'science': 'data science biology chemistry biochemistry',
            'writing': 'english writing research writing essay',
            'lang':    'french spanish english modern languages',
        }
        expanded = query
        for key, expansion in synonyms.items():
            if key in query.lower():
                expanded = query + ' ' + expansion
                break

        # Get all Teach skills excluding the logged-in user
        teach_skills = Skill.objects.filter(
            skill_type='Teach'
        ).exclude(
            user=request.user
        ).select_related('user')

        if teach_skills.exists():
            skill_list = list(teach_skills)
            corpus = [s.skill_name for s in skill_list] + [expanded]
            vectorizer = TfidfVectorizer(
                analyzer='char_wb', ngram_range=(2, 4), lowercase=True
            )
            tfidf = vectorizer.fit_transform(corpus)
            scores = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()

            for skill, score in zip(skill_list, scores):
                if score > 0.01:
                    results.append({
                        'skill':   skill,
                        'user':    skill.user,
                        'score':   round(score * 100),
                        'label':   ('Strong' if score >= 0.7
                                    else 'Good' if score >= 0.4
                                    else 'Partial'),
                        'color':   ('#1e7e34' if score >= 0.7
                                    else '#b35a00' if score >= 0.4
                                    else '#1a5fb4'),
                    })
            results.sort(key=lambda x: x['score'], reverse=True)

    return render(request, 'skills/find_skills.html', {
        'query':      query,
        'results':    results,
        'all_skills': all_skills,
    })


@login_required
def connect(request, user_id, skill_name):
    provider = get_object_or_404(User, id=user_id)

    if provider == request.user:
        messages.warning(request, "⚠️ You cannot connect with yourself.")
        return redirect('find_skills')

    connection, created = Connection.objects.get_or_create(
        requester=request.user,
        provider=provider,
        skill_name=skill_name,
        defaults={'status': 'Accepted'}
    )

    if created:
        messages.success(
            request,
            f"🎉 Connected with {provider.display_name} for '{skill_name}'! "
            f"You can now chat with them."
        )
    else:
        messages.info(
            request,
            f"You're already connected with {provider.display_name} for '{skill_name}'."
        )

    return redirect('chat_room', user_id=provider.id, skill_name=skill_name)


@login_required
def home_view(request):

    total_users = User.objects.count()
    total_skills = Skill.objects.values('skill_name').distinct().count()
    teach_count = Skill.objects.filter(skill_type='Teach').count()
    learn_count = Skill.objects.filter(skill_type='Learn').count()

    popular_teach = (
        Skill.objects.filter(skill_type='Teach')
        .values('skill_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    popular_learn = (
        Skill.objects.filter(skill_type='Learn')
        .values('skill_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    all_skills = (
        Skill.objects.values_list('skill_name', flat=True)
        .distinct().order_by('skill_name')
    )

    return render(request, 'skills/home.html', {
        'total_users':   total_users,
        'total_skills':  total_skills,
        'teach_count':   teach_count,
        'learn_count':   learn_count,
        'popular_teach': popular_teach,
        'popular_learn': popular_learn,
        'all_skills':    all_skills,
    })
