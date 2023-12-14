from django.core.management.base import BaseCommand
from item.models import Item, Category
import requests

class Command(BaseCommand):
    help = 'Fetches data from Pokemon card API and saves it to the database'

    def handle(self, *args, **options):
        api_url = "https://api.pokemontcg.io/v2/cards"
        page = 1

        while True:
            response = requests.get(api_url, params={'page': page})

            if response.status_code == 200:
                if isinstance(response.json(), list):
                    data_list = response.json()
                else:
                    data_list = response.json().get("data", [])

                if not data_list:
                    break 

                for item_data in data_list:
                    name = item_data.get("name", "")
                    image = item_data.get("images", {}).get("small", "")
                    description = item_data.get("flavorText", "")
                    price = item_data.get("cardmarket", {}).get("prices", {}).get("averageSellPrice", 0)
                    series = item_data.get("set", {}).get("series", "")
                    category_name = item_data.get("rarity", "")

                    category_instance, created = Category.objects.get_or_create(name=category_name)

                    Item.objects.create(
                        name=name,
                        image=image,
                        description=description,
                        price=price,
                        series=series,
                        category=category_instance,
                    )

                next_page = response.json().get("meta", {}).get("page", {}).get("next", None)

                if not next_page:
                    break 

                page += 1
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch data from the API. Status code: {response.status_code}'))
                break