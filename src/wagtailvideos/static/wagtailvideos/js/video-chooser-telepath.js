const ImageChooserFactory = window.telepath.constructors['wagtail.images.widgets.ImageChooser'];

class VideoChooserFactory extends ImageChooserFactory {
    // eslint-disable-next-line no-undef
    widgetClass = VideoChooser;
}


window.telepath.register('wagtailvideos.widgets.VideoChooser', VideoChooserFactory);
