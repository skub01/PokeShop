from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
import random
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
            id = item_data.get("id", "")
            image = item_data.get("images", {}).get("small", "")
            average_sell_price = item_data.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0)
            series = item_data.get("set", {}).get("series", "")

            item_info = {
                'name': name,
                'id': id,
                'image': image,
                'average_sell_price': average_sell_price,
                'series': series
            }

            items_data.append(item_info)

        paginator = Paginator(items_data, 9)  
        page = request.GET.get('page')

        try:
            items_data = paginator.page(page)
        except PageNotAnInteger:
            items_data = paginator.page(1)
        except EmptyPage:
            items_data = paginator.page(paginator.num_pages)

        return render(request, 'item/items.html', {'items_data': items_data, 'paginator': paginator})
    else:
        return render(request, 'item/items.html', {'error_message': 'Failed to fetch data from the API'})

def detail(request, item_id):
    api_url = f"https://api.pokemontcg.io/v2/cards/{item_id}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data_detail = response.json().get("data", {})

        name = data_detail.get("name", "")
        id_detail = data_detail.get("id", "")
        image = data_detail.get("images", {}).get("small", "")
        series = data_detail.get("set", {}).get("series", "")
        rarity = data_detail.get("rarity", "")
        price = data_detail.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0)
        text = data_detail.get("flavorText", "")
        
        item_data = {
            'name': name,
            'id': id_detail,
            'image': image,
            'series': series,
            'rarity': rarity,
            'price': price,
            'text': text
        }
        
        rarity_info = {
            'Rare Holo': {'style': 'text-purple-600 font-bold', 'symbol': '★'},
            'Rare Holo GX': {'style': 'text-purple-600 font-bold', 'symbol': '★'},
            'Rare Holo V': {'style': 'text-purple-600 font-bold', 'symbol': '★'},
            'Rare': {'style': 'text-red-500 font-bold', 'symbol': '★'},
            'Common': {'style': 'text-gray-500 font-bold', 'symbol': '○'},
            'Uncommon': {'style': 'text-blue-500 font-bold', 'symbol': '☆'},
}

        item_data['rarity_info'] = rarity_info.get(item_data['rarity'], {'style': 'font-bold', 'symbol': ''}) 

        api_url_related_items = f"https://api.pokemontcg.io/v2/cards?q=set.series:{series}&pageSize=4"
        response_related_items = requests.get(api_url_related_items)

        if response_related_items.status_code == 200:
            data_related_items = response_related_items.json().get("data", [])

            related_items = [related_item for related_item in data_related_items if related_item.get("id") != id_detail]

            random.shuffle(related_items)
            related_items_info = [
                {
                    'name': related_item.get("name", ""),
                    'id': related_item.get("id", ""),
                    'price': related_item.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0),
                    'image': related_item.get("images", {}).get("small", "")
                }
                for related_item in related_items[:min(3, len(related_items))]
            ]

            return render(request, 'item/detail.html', {
                'item_data': item_data,
                'related_items': related_items_info,
            })
        else:
            return render(request, 'item/detail.html', {'error_message': 'Couldn\'t fetch related items from the API'})
    else:
        return render(request, 'item/detail.html', {'error_message': 'Couldn\'t fetch detail item from the API'})

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', item_id=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, item_id):
    item = get_object_or_404(Item, id=item_id, created_by= request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', item_id=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, item_id):
    item = get_object_or_404(Item, id=item_id, created_by= request.user)
    item.delete()

    return redirect('dashboard:index')