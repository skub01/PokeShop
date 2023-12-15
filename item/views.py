from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Item, Category
from .forms import NewItemForm, EditItemForm

def items(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    items = Item.objects.filter(sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    items_per_page = 12
    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page', 1)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, sold=False).exclude(pk=pk)[0:3]

    rarity_info = {
        'Rare Holo': {'style': 'text-purple-600 font-bold', 'symbol': '★'},
        'Rare Holo GX': {'style': 'text-purple-600 font-bold', 'symbol': '★'},
        'Rare Holo V': {'style': 'text-purple-600 font-bold', 'symbol': '★'},
        'Rare': {'style': 'text-red-500 font-bold', 'symbol': '★'},
        'Common': {'style': 'text-gray-500 font-bold', 'symbol': '○'},
        'Uncommon': {'style': 'text-blue-500 font-bold', 'symbol': '☆'},
            }
    
    rarity = rarity_info.get(item.category, None)

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'rarity': rarity,
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by= request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by= request.user)
    item.delete()

    return redirect('dashboard:index')