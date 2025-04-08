from django.test import TestCase
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase

from bakerydemo.base.models import FormPage, HomePage, FormField


class FormPageTest(WagtailPageTestCase):
    """
    Test FormPage functionality
    """
    @classmethod
    def setUpTestData(cls):
        # Get root page
        cls.root = Page.get_first_root_node()
        
        # Create a site
        Site.objects.create(
            hostname="testserver",
            root_page=cls.root,
            is_default_site=True,
            site_name="testserver",
        )
        
        # Create a homepage with required fields
        cls.home = HomePage(
            title="Home",
            hero_text="Welcome to the Bakery",
            hero_cta="Learn More",
        )
        cls.root.add_child(instance=cls.home)
        
        # Create a form page
        cls.form_page = FormPage(
            title="Contact Us",
            thank_you_text="<p>Thank you for your submission!</p>",
        )
        cls.home.add_child(instance=cls.form_page)
        
        # Add some form fields
        cls.form_field_name = FormField.objects.create(
            page=cls.form_page,
            sort_order=1,
            label="Your Name",
            field_type="singleline",
            required=True,
            clean_name="your_name",
        )
        
        cls.form_field_email = FormField.objects.create(
            page=cls.form_page,
            sort_order=2,
            label="Your Email",
            field_type="email",
            required=True,
            clean_name="your_email",
        )
        
        cls.form_field_message = FormField.objects.create(
            page=cls.form_page,
            sort_order=3,
            label="Your Message",
            field_type="multiline",
            required=True,
            clean_name="your_message",
        )

    def test_form_field_creation(self):
        """Test that form fields are created correctly"""
        form_fields = FormField.objects.filter(page=self.form_page)
        self.assertEqual(form_fields.count(), 3)
        
        # Check field properties
        name_field = form_fields.get(label="Your Name")
        self.assertEqual(name_field.field_type, "singleline")
        self.assertTrue(name_field.required)
        
        email_field = form_fields.get(label="Your Email")
        self.assertEqual(email_field.field_type, "email")
        self.assertTrue(email_field.required)
        
        message_field = form_fields.get(label="Your Message")
        self.assertEqual(message_field.field_type, "multiline")
        self.assertTrue(message_field.required)

    def test_form_submission_create(self):
        """Test creating a form submission directly"""
        # Create a submission
        form_data = {
            'your_name': 'Test User',
            'your_email': 'test@example.com',
            'your_message': 'This is a test message',
        }
        
        submission_class = self.form_page.get_submission_class()
        
        # Create a submission
        submission = submission_class.objects.create(
            page=self.form_page,
            form_data=form_data,
        )
        
        # Check it was saved
        self.assertEqual(submission_class.objects.count(), 1)
        
        # Check the data was saved correctly
        saved_submission = submission_class.objects.first()
        submission_data = saved_submission.get_data()
        self.assertEqual(submission_data['your_name'], 'Test User')
        self.assertEqual(submission_data['your_email'], 'test@example.com')
        self.assertEqual(submission_data['your_message'], 'This is a test message')


class ContactFormTest(TestCase):
    """
    Test suite for ContactForm functionality including:
    - Form validation
    - Field requirements
    - Data processing
    - Form submission handling
    """
    def test_contact_form_submission(self):
        """
        Verify that contact form submission:
        - Accepts valid form data
        - Processes all required fields correctly
        - Handles optional fields appropriately
        - Returns expected response
        """
        # ... existing code ...

    def test_contact_form_validation(self):
        """
        Verify that form validation:
        - Rejects missing required fields
        - Validates email format
        - Enforces field length limits
        - Provides appropriate error messages
        """
        # ... existing code ...

    def test_contact_form_optional_fields(self):
        """
        Verify that optional fields:
        - Can be left empty
        - Are processed correctly when provided
        - Don't affect form validation
        - Are stored properly when submitted
        """
        # ... existing code ... 