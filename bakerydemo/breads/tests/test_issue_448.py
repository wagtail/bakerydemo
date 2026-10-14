import uuid
from bs4 import BeautifulSoup
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from bakerydemo.breads.models import Country, BreadIngredient

class Issue448Tests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin'
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_country_2_character_string_pk(self):
        country = Country.objects.create(id='XY', title='Xylos')
        self.assertEqual(country.pk, 'XY')
        self.assertIsInstance(country.id, str)
        country.refresh_from_db()
        self.assertEqual(country.id, 'XY')

    def test_bread_ingredient_auto_uuid_pk(self):
        ingredient = BreadIngredient.objects.create(name='Salt')
        self.assertIsInstance(ingredient.id, uuid.UUID)

        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, 'Salt')

    def test_country_admin_add_edit_behavior(self):
        # Add view
        response = self.client.get('/admin/country/new/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        id_input = soup.find('input', {'name': 'id'})
        title_input = soup.find('input', {'name': 'title'})

        self.assertIsNotNone(id_input, "Country ID must be visible when creating.")
        self.assertFalse(id_input.has_attr('readonly'), "Country ID must be editable when creating.")
        self.assertIsNotNone(title_input, "Country title must be visible when creating.")

        # Edit view
        country = Country.objects.create(id='ZZ', title='Test Country')
        response = self.client.get(f'/admin/country/edit/{country.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # In edit view, id should not be an editable input. It is rendered as text.
        id_input_edit = soup.find('input', {'name': 'id'})
        self.assertIsNone(id_input_edit, "Country ID must NOT be an editable input in edit view.")

        # Verify read-only representation exists
        id_readonly_div = soup.find('div', {'aria-readonly': 'true'})
        self.assertIsNotNone(id_readonly_div, "Country ID must be displayed as a read-only field.")
        self.assertIn('ZZ', id_readonly_div.text)

        title_input_edit = soup.find('input', {'name': 'title'})
        self.assertIsNotNone(title_input_edit, "Country title must remain editable in edit view.")

    def test_breadingredient_admin_uuid_hidden(self):
        # Add view
        response = self.client.get('/admin/snippets/breads/breadingredient/add/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNone(soup.find('input', {'name': 'id'}), "BreadIngredient UUID must be hidden in add view.")

        # Edit view
        ingredient = BreadIngredient.objects.create(name='Pepper')
        response = self.client.get(f'/admin/snippets/breads/breadingredient/edit/{ingredient.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIsNone(soup.find('input', {'name': 'id'}), "BreadIngredient UUID must be hidden in edit view.")

        # Inspect view
        response = self.client.get(f'/admin/snippets/breads/breadingredient/inspect/{ingredient.pk}/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract <dt> tags for labels
        dts = soup.find_all('dt')
        labels = [dt.text.strip().lower() for dt in dts]
        self.assertNotIn('id', labels, "BreadIngredient UUID must be hidden in inspect view.")
        self.assertIn('name', labels, "BreadIngredient name must remain in inspect view.")
