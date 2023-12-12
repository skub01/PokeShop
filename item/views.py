from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
from .models import Item, Category
from .forms import NewItemForm, EditItemForm

def items(request):
    query = request.GET.get('query', '')
    categories = Category.objects.all()
    category_id = request.GET.get('category', 0)
    items = Item.objects.filter(sold=False)
    api_url = "https://api.pokemontcg.io/v2/cards"

    response = requests.get(api_url)

    if response.status_code == 200:
        data_list = response.json().get("data", [])

        items_data = []
        for item_data in data_list:
            name = item_data.get("name", "")
            image = item_data.get("images", {}).get("small", "")
            average_sell_price = item_data.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0)
            series = item_data.get("set", {}).get("series", "")

            item_info = {
                'name': name,
                'image': image,
                'average_sell_price': average_sell_price,
                'series': series
            }

            items_data.append(item_info)

        paginator = Paginator(items_data, 15)  # Show 15 items per page
        page = request.GET.get('page')

        try:
            items_data = paginator.page(page)
        except PageNotAnInteger:
            # If the page parameter is not an integer, deliver the first page.
            items_data = paginator.page(1)
        except EmptyPage:
            # If the page is out of range (e.g., 9999), deliver the last page.
            items_data = paginator.page(paginator.num_pages)

        return render(request, 'item/items.html', {'items_data': items_data, 'paginator': paginator})
    else:
        return render(request, 'item/items.html', {'error_message': 'Failed to fetch data from the API'})

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
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
