'use strict';
var mcePlugins = ['code', 'lists', 'nonbreaking', 'visualchars', 'wordcount', 'codeeditor', 'media', 'link'],
    mceTools = [],
    // mceToolbar = 'code undo bold styleselect',
    // mceToolbar = 'undo redo | bold italic underline strikethrough | code' ,
    // mceMenubar = ['insert'],
    mceExternalPlugins = {};

function registerMCEPlugin(name, path, language) {
    if (path) {
        mceExternalPlugins[name] = path;
        if (language) {
            tinymce.PluginManager.requireLangPack(name, language);
        }
    } else {
        mcePlugins.push(name);
    }
}

function registerMCETool(name) {
    mceTools.push(name);
}

function makeTinyMCEEditable(id, kwargs) {

    kwargs = kwargs || {valid_elements : "span[*]"};
    $.extend(kwargs, {
        formats : {
            underline : {inline : 'u', exact: true},
        },
        selector: '#' + id.toString(),
        height: 400,
        plugins: mcePlugins,
        tools: mceTools,
        external_plugins: mceExternalPlugins,
        branding: false,
        media_live_embeds: true,
        codeeditor_themes_pack: "merbivore",
        end_container_on_empty_block: true,
        extended_valid_elements : 'video[autoplay|muted|loop|playsinline|class|width|height|poster|controls]',
        custom_elements: 'picture',
        valid_children: 'picture[source|img]',
        relative_urls: false,
        link_context_toolbar: true,
        link_title: false,
        link_quicklink: false,
        paste_as_text: true,
        setup: function (editor) {
            editor.on('change', function () {
                editor.save();
            });
        }
    });

    setTimeout(function () {
        tinymce.init(kwargs);
    }, 1);
}
