from django.core.management.base import BaseCommand
from bakerydemo.breads.models import BreadIngredient, BreadPage
import random

COMMON_INGREDIENTS = [
    "All-purpose flour", "Bread flour", "Whole wheat flour", "Rye flour", 
    "Spelt flour", "00 flour", "Semolina flour", "Cake flour", 
    "Strong white flour", "Wholemeal flour", "Water", "Salt", 
    "Instant yeast", "Active dry yeast", "Fresh yeast", 
    "Sourdough starter", "Poolish", "Biga", "Diastatic malt", 
    "Non-diastatic malt", "Sugar", "Brown sugar", "Honey", 
    "Molasses", "Maple syrup", "Malt syrup", "Barley malt extract", 
    "Milk", "Buttermilk", "Powdered milk", "Butter", "Olive oil", 
    "Vegetable oil", "Canola oil", "Coconut oil", "Lard", "Ghee", 
    "Eggs", "Egg yolks", "Egg whites", "Vinegar", "Lemon juice", 
    "Orange zest", "Vanilla extract", "Cocoa powder", 
    "Chocolate chips", "Cinnamon", "Nutmeg", "Cardamom", "Anise", 
    "Sesame seeds", "Poppy seeds", "Sunflower seeds", 
    "Pumpkin seeds", "Flaxseed", "Chia seeds", "Nigella seeds", 
    "Oats", "Cornmeal", "Bran", "Raisins", "Currants", 
    "Dried cranberries", "Apricots", "Walnuts", "Almonds", 
    "Pistachios", "Hazelnuts", "Pine nuts", "Peanuts", "Onion", 
    "Garlic", "Roasted garlic", "Chives", "Scallions", "Olives", 
    "Jalapeños", "Tomato paste", "Cheddar", "Parmesan", "Yogurt", 
    "Cream", "Cream cheese", "Ricotta", "Potato flakes", 
    "Mashed potato", "Herbes de Provence", "Rosemary", "Thyme", 
    "Basil", "Caraway", "Oil"
]

STYLE_HINTS = {
    "sourdough": ["Bread flour", "Whole wheat flour", "Water", "Salt", "Sourdough starter"],
    "baguette": ["Bread flour", "Water", "Salt", "Instant yeast", "Diastatic malt"],
    "brioche": ["Bread flour", "Milk", "Eggs", "Butter", "Sugar", "Instant yeast", "Salt"],
    "challah": ["Bread flour", "Eggs", "Sugar", "Oil", "Instant yeast", "Salt", "Water"],
    "rye": ["Rye flour", "Bread flour", "Water", "Salt", "Instant yeast", "Caraway"],
    "ciabatta": ["Bread flour", "Water", "Salt", "Olive oil", "Instant yeast"],
    "focaccia": ["Bread flour", "Water", "Salt", "Olive oil", "Instant yeast", "Rosemary"],
    "whole": ["Whole wheat flour", "Water", "Salt", "Instant yeast", "Honey"],
    "seed": ["Bread flour", "Water", "Salt", "Instant yeast", "Sesame seeds", "Sunflower seeds"],
    "olive": ["Bread flour", "Water", "Salt", "Instant yeast", "Olives", "Olive oil"],
    "garlic": ["Bread flour", "Water", "Salt", "Instant yeast", "Roasted garlic"],
}

class Command(BaseCommand):
    help = "Create BreadIngredients and assign them to BreadPages"

    def handle(self, *args, **options):
        # Create all ingredients
        created_count = 0
        for name in COMMON_INGREDIENTS:
            obj, created = BreadIngredient.objects.get_or_create(name=name)
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Created {created_count} new ingredients"))
        
        # Assign ingredients to bread pages
        pages = BreadPage.objects.live()
        total_assignments = 0
        
        for page in pages:
            title_lower = page.title.lower()
            
            # Find matching style
            ingredients_list = ["Bread flour", "Water", "Salt", "Instant yeast"]
            for style_key, style_ingredients in STYLE_HINTS.items():
                if style_key in title_lower:
                    ingredients_list = style_ingredients
                    break
            
            # Add some random extras to reach 6-10 ingredients
            random.seed(hash(page.title))
            extra_count = max(0, 8 - len(ingredients_list))
            available = [i for i in COMMON_INGREDIENTS if i not in ingredients_list]
            extras = random.sample(available, min(extra_count, len(available)))
            final_list = list(set(ingredients_list + extras))
            
            # Assign to page
            ingredient_objects = BreadIngredient.objects.filter(name__in=final_list)
            page.ingredients.set(ingredient_objects)
            page.save_revision().publish()
            total_assignments += len(final_list)
        
        self.stdout.write(self.style.SUCCESS(f"Updated {pages.count()} bread pages"))
        self.stdout.write(self.style.SUCCESS(f"Total ingredient assignments: {total_assignments}"))
