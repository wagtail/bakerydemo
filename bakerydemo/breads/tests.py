from django.test import TestCase

from bakerydemo.breads.models import BreadIngredient, Country


class CountryModelTest(TestCase):
    """Test Country model ordering and sort_order field."""

    def test_country_has_sort_order_field(self):
        """Test that Country model has sort_order field."""
        country = Country(title="Test Country", sort_order=10)
        country.save()
        self.assertEqual(country.sort_order, 10)

    def test_country_ordering_respects_sort_order(self):
        """Test that Country model ordering includes sort_order."""
        Country.objects.create(title="Country A", sort_order=20)
        Country.objects.create(title="Country B", sort_order=10)
        Country.objects.create(title="Country C", sort_order=30)

        countries = list(Country.objects.all())
        self.assertEqual(countries[0].title, "Country B")
        self.assertEqual(countries[1].title, "Country A")
        self.assertEqual(countries[2].title, "Country C")

    def test_country_ordering_with_null_sort_order(self):
        """Test that Country with null sort_order is ordered by title."""
        Country.objects.create(title="AAA", sort_order=None)
        Country.objects.create(title="BBB", sort_order=10)
        Country.objects.create(title="CCC", sort_order=None)

        countries = list(Country.objects.all())
        # NULL sort_order values come first in SQL, then ordered by title
        # Then items with sort_order
        self.assertEqual(countries[0].title, "AAA")
        self.assertEqual(countries[1].title, "CCC")
        self.assertEqual(countries[2].title, "BBB")


class BreadIngredientModelTest(TestCase):
    """Test BreadIngredient model ordering and sort_order field."""

    def test_ingredient_has_sort_order_field(self):
        """Test that BreadIngredient model has sort_order field."""
        ingredient = BreadIngredient(name="Test Ingredient", sort_order=10)
        ingredient.save()
        self.assertEqual(ingredient.sort_order, 10)

    def test_ingredient_ordering_respects_sort_order(self):
        """Test that BreadIngredient model ordering includes sort_order."""
        BreadIngredient.objects.create(name="Ingredient A", sort_order=20)
        BreadIngredient.objects.create(name="Ingredient B", sort_order=10)
        BreadIngredient.objects.create(name="Ingredient C", sort_order=30)

        ingredients = list(BreadIngredient.objects.all())
        self.assertEqual(ingredients[0].name, "Ingredient B")
        self.assertEqual(ingredients[1].name, "Ingredient A")
        self.assertEqual(ingredients[2].name, "Ingredient C")

    def test_ingredient_ordering_with_null_sort_order(self):
        """Test that BreadIngredient with null sort_order is ordered by name."""
        BreadIngredient.objects.create(name="AAA", sort_order=None)
        BreadIngredient.objects.create(name="BBB", sort_order=10)
        BreadIngredient.objects.create(name="CCC", sort_order=None)

        ingredients = list(BreadIngredient.objects.all())
        # NULL sort_order values come first in SQL, then ordered by name
        # Then items with sort_order
        self.assertEqual(ingredients[0].name, "AAA")
        self.assertEqual(ingredients[1].name, "CCC")
        self.assertEqual(ingredients[2].name, "BBB")
