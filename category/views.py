# views.py
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Category

def add_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    error = ""
    
    if request.method == "POST":
        category_name = request.POST['category_name']
        slug = request.POST['slug']
        description = request.POST['description']
        cat_image = request.FILES.get('cat_image', None)

        try:
            Category.objects.create(category_name=category_name, slug=slug, description=description, cat_image=cat_image)
            error = "no"
        except:
            error = "yes"

    return render(request, 'add_category.html', locals())

def manage_category(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    categories = Category.objects.all()
    
    return render(request, 'manage_category.html', locals())
def edit_category(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    error = ""
    category = Category.objects.get(id=pid)

    if request.method == "POST":
        category_name = request.POST['category_name']
        slug = request.POST['slug']
        description = request.POST['description']
        cat_image = request.FILES.get('cat_image', None)

        category.category_name = category_name
        category.slug = slug
        category.description = description

        if cat_image:
            category.cat_image = cat_image

        try:
            category.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_category.html', locals())

def delete_category(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    category = Category.objects.get(id=pid)
    category.delete()

    return redirect('manage_category')