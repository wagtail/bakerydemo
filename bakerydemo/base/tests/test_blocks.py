from django.test import SimpleTestCase, TestCase
from wagtail.models import Page
from wagtail.rich_text import RichText
from wagtail.test.utils import WagtailTestUtils
from wagtail.test.utils.form_data import nested_form_data, rich_text, streamfield

from bakerydemo.base.blocks import (
    BaseStreamBlock,
    BlockQuote,
    CaptionedImageBlock,
    HeadingBlock,
)


class HeadingBlockTest(TestCase):
    """
    Test for the HeadingBlock
    """
    def test_heading_block_renders(self):
        block = HeadingBlock()
        html = block.render({
            'heading_text': 'This is a test heading',
            'size': 'h2',
        })
        self.assertIn('<h2>This is a test heading</h2>', html)

    def test_heading_block_is_valid(self):
        block = HeadingBlock()
        # Should be valid with size
        self.assertTrue(block.clean({
            'heading_text': 'Test Heading',
            'size': 'h2'
        }))
        
        # Should be valid without size (it's optional)
        self.assertTrue(block.clean({
            'heading_text': 'Test Heading',
            'size': ''
        }))
        
        # Should raise an error if heading_text is empty
        with self.assertRaises(Exception):
            block.clean({
                'heading_text': '',
                'size': 'h2'
            })


class BlockQuoteTest(SimpleTestCase):
    """
    Test for the BlockQuote
    """
    def test_blockquote_renders(self):
        block = BlockQuote()
        html = block.render({
            'text': 'This is a test quote',
            'attribute_name': 'Test Author',
        })
        self.assertIn('<blockquote>', html)
        self.assertIn('This is a test quote', html)
        self.assertIn('Test Author', html)

    def test_blockquote_renders_without_attribution(self):
        block = BlockQuote()
        html = block.render({
            'text': 'This is a test quote',
            'attribute_name': '',
        })
        self.assertIn('<blockquote>', html)
        self.assertIn('This is a test quote', html)
        # Attribution element should not be present
        self.assertNotIn('class="attribution"', html)

    def test_blockquote_clean(self):
        block = BlockQuote()
        
        # Basic validation
        self.assertTrue(block.clean({
            'text': 'Test quote',
            'attribute_name': 'Test Author'
        }))
        
        # Valid without attribution (optional)
        self.assertTrue(block.clean({
            'text': 'Test quote',
            'attribute_name': ''
        }))
        
        # Should raise an error if text is empty
        with self.assertRaises(Exception):
            block.clean({
                'text': '',
                'attribute_name': 'Author'
            })


class BaseStreamBlockTest(TestCase, WagtailTestUtils):
    """
    Test for the BaseStreamBlock which contains all of the other blocks
    """
    def test_stream_block_to_python(self):
        """Test that StreamField blocks can be converted from Python representation"""
        block = BaseStreamBlock()
        value = block.to_python([
            {
                'type': 'heading_block',
                'value': {
                    'heading_text': 'Test Heading',
                    'size': 'h2',
                },
            },
            {
                'type': 'paragraph_block',
                'value': '<p>This is a test paragraph with <b>bold text</b>.</p>',
            },
            {
                'type': 'block_quote',
                'value': {
                    'text': 'Test quote',
                    'attribute_name': 'Test Author',
                },
            },
        ])
        
        # Check the value was correctly parsed
        self.assertEqual(len(value), 3)
        self.assertEqual(value[0].block_type, 'heading_block')
        self.assertEqual(value[0].value['heading_text'], 'Test Heading')
        self.assertEqual(value[0].value['size'], 'h2')
        
        # Second block should be a paragraph
        self.assertEqual(value[1].block_type, 'paragraph_block')
        
        # Third block should be a block quote
        self.assertEqual(value[2].block_type, 'block_quote')
        self.assertEqual(value[2].value['text'], 'Test quote')
        self.assertEqual(value[2].value['attribute_name'], 'Test Author')

    def test_streamfield_form_representation(self):
        """
        Test the nested form data utility with StreamField data
        """
        # This demonstrates how to create the POST data for a form containing a StreamField
        post_data = nested_form_data({
            'title': 'Test Page',
            'body': streamfield([
                ('heading_block', {
                    'heading_text': 'Test Heading',
                    'size': 'h2',
                }),
                ('paragraph_block', rich_text('<p>Test paragraph</p>')),
            ]),
        })
        
        # The result should look like this structure
        self.assertIn('body-count', post_data)
        self.assertEqual(post_data['body-count'], '2')
        
        # Check the heading block is correctly represented
        self.assertEqual(post_data['body-0-type'], 'heading_block')
        self.assertEqual(post_data['body-0-value-heading_text'], 'Test Heading')
        self.assertEqual(post_data['body-0-value-size'], 'h2')
        
        # Check the paragraph block is correctly represented - it's now stored as JSON, not plain text
        self.assertEqual(post_data['body-1-type'], 'paragraph_block')
        # Just check that it contains the paragraph text rather than an exact match
        self.assertIn('Test paragraph', post_data['body-1-value']) 