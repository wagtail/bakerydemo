from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, StreamBlock, StructBlock, TextBlock,
    ListBlock, EmailBlock, IntegerBlock, FloatBlock, DecimalBlock, RegexBlock,
    URLBlock, BooleanBlock, DateBlock, TimeBlock, DateTimeBlock, RawHTMLBlock,
    BlockQuoteBlock, PageChooserBlock, StaticBlock
)
from wagtail.snippets.blocks import SnippetChooserBlock


class ImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = CharBlock(required=False)
    attribution = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "blocks/image_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """
    heading_text = CharBlock(classname="title", required=True)
    size = ChoiceBlock(choices=[
        ('', 'Select a header size'),
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4')
    ], blank=True, required=False)

    class Meta:
        icon = "title"
        template = "blocks/heading_block.html"


class BlockQuote(StructBlock):
    """
    Custom `StructBlock` that allows the user to attribute a quote to the author
    """
    text = TextBlock()
    attribute_name = CharBlock(
        blank=True, required=False, label='e.g. Mary Berry')

    class Meta:
        icon = "fa-quote-left"
        template = "blocks/blockquote.html"


# StreamBlocks
class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    heading_block = HeadingBlock()
    paragraph_block = RichTextBlock(
        icon="fa-paragraph",
        template="blocks/paragraph_block.html"
    )
    image_block = ImageBlock()
    block_quote = BlockQuote()
    embed_block = EmbedBlock(
        help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks',
        icon="fa-s15",
        template="blocks/embed_block.html")


# More complex things
class AccordionBlock(StructBlock):
    panels = ListBlock(StructBlock([
        ('title', TextBlock(help_text='The headline to display when the accordion panel is closed.')),
        ('body', RichTextBlock(help_text='The inner content of this accordion panel. It is initially hidden.'))
    ], label='Panel'))

    class Meta:
        icon = 'help'
        # template = 'blocks/accordion.html'
        help_text = 'Accordions are elements that help you organize and navigate multiple documents in a single container. They can be used for switching between items in the container.'


class NoticeBlock(StructBlock):
    message = RichTextBlock(help_text='Write the message text.')
    indicator = ChoiceBlock(choices=[
        ('', 'Standard'),
        ('success', 'Success'),
        ('alert', 'Alert'),
        ('warning', 'Warning')
    ], required=False, help_text='Choose what type of notice this is.')

    class Meta:
        icon = 'mail'
        # template = 'blocks/notice.html'
        help_text = "Get the reader's attention using this callout. This is useful for warnings, indications of success, etc."


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock()
    caption = TextBlock(required=False)

    class Meta:
        icon = 'image'
        # template = 'blocks/captioned_image.html'
        help_text = 'Select an image and add a caption (optional).'


class CollapsibleCaptionedImageBlock(CaptionedImageBlock):
    def get_layout(self):
        return 'COLLAPSIBLE'


class LimitedStreamBlock(StreamBlock):
    paragraph = RichTextBlock(icon='pilcrow')
    smaller_heading = TextBlock(
        icon='title', template='blocks/smaller_heading.html')
    another_stream = BaseStreamBlock()

    class Meta:
        # template = 'blocks/streamfield.html'
        pass

class CollapsibleLimitedStreamBlock(LimitedStreamBlock):
    def get_layout(self):
        return 'COLLAPSIBLE'


class CollapsibleBlockQuoteBlock(BlockQuoteBlock):
    def get_layout(self):
        return 'COLLAPSIBLE'


class EveryBlockUnderTheSun(StreamBlock):
    pass
    charblock = CharBlock()
    textblock = TextBlock()
    emailblock = EmailBlock()
    integerblock = IntegerBlock()
    floatblock = FloatBlock()
    decimalblock = DecimalBlock()
    regexblock = RegexBlock(
                            regex=r'^[0-9]{3}$',
                            error_messages={'invalid': "Not a valid library card number."})
    url = URLBlock()
    boolean = BooleanBlock()
    date = DateBlock()
    time = TimeBlock()
    date_time = DateTimeBlock()
    richtext = RichTextBlock()
    blah = RawHTMLBlock()
    blockquote = BlockQuoteBlock()
    collapsible_blockquote = CollapsibleBlockQuoteBlock()
    choices = ChoiceBlock(choices=[
                            ('tea', 'Tea'),
                            ('coffee', 'Coffee'),
                        ], icon='cup')
    pagechooser = PageChooserBlock()
    document = DocumentChooserBlock()
    image = ImageChooserBlock()
    snippets = SnippetChooserBlock('base.people')
    embed = EmbedBlock()
    staticblock = StaticBlock(admin_text='Tom is hot.')
    listblock = AccordionBlock()
    structblock = CaptionedImageBlock()
    collapsible_structblock = CollapsibleCaptionedImageBlock()
    streamblock = LimitedStreamBlock()
    collapsible_streamblock = LimitedStreamBlock()


class PersonBlock(StructBlock):
    name = CharBlock()
    height = DecimalBlock()
    age = IntegerBlock()
    email = EmailBlock()


class ContentStreamBlock(StreamBlock):
    paragraph = RichTextBlock(icon='doc-empty')
    heading = TextBlock(icon='search', template='blocks/heading.html')
    smaller_heading = TextBlock(
        icon='title')  # , template='blocks/smaller_heading.html')
    smallest_heading = TextBlock(
        icon='title')   # , template='blocks/smallest_heading.html')
    image = CaptionedImageBlock()
    embed = EmbedBlock(icon="media")
    download = DocumentChooserBlock(icon='download')   # , template='blocks/download.html')
    accordion = AccordionBlock()
    notice = NoticeBlock()
    limited_stream = LimitedStreamBlock(help_text='blah blah',
                                        label="Limited Stream Field")

    class Meta:
        # template = 'blocks/streamfield.html'
        pass


class SectionBlock(StructBlock):
    headline = TextBlock(help_text='Write a title for this section.')
    subheadline = TextBlock(required=False, help_text='Write a subheadline for this section (optional).')
    body = ContentStreamBlock(required=False, help_text='The section content goes here.', label="Another streamblock", group="Grouped links")

    class Meta:
        icon = 'openquote'
        # template = 'blocks/section.html'
        help_text = 'Sections divide the page into digestible parts.'


class BodyBlock(StreamBlock):
    paragraph = RichTextBlock(icon='doc-empty', group="Text")
    heading = TextBlock(icon='search', template='blocks/heading.html', group="Text")
    smaller_heading = TextBlock(
        icon='title', group="Text")  # , template='blocks/smaller_heading.html')
    smallest_heading = TextBlock(
        icon='title', group="Text")   # , template='blocks/smallest_heading.html')
    image = CaptionedImageBlock(group="Media stuff")
    embed = EmbedBlock(icon="media", group="Media stuff")
    download = DocumentChooserBlock(icon='download', group="Meta stuff")   # , template='blocks/download.html')
    accordion = AccordionBlock(group="Meta stuff")
    notice = NoticeBlock(group="Meta stuff")
    limited_stream = LimitedStreamBlock(help_text='blah blah',
                                        label="Limited streamfield thing",
                                        group="Other streamfields")
    section = SectionBlock(group="Other streamfields")

    class Meta:
        # template = 'blocks/streamfield.html'
        icon = 'tag'
        help_text = 'The main page body.'
