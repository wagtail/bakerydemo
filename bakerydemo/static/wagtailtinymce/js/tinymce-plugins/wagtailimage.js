

(function() {
    'use strict';

    (function($) {
        tinymce.PluginManager.add('wagtailimage', function(editor) {
            /* stop editing and resizing of embedded image content */
            function fixContent() {
                $(editor.getBody()).find('picture').each(function () {
                    $(this).attr('contenteditable', false).attr('data-mce-contenteditable', 'false').find('div,table,img').attr('data-mce-resize', 'false');
                });
            }

            function showDialog() {
                var url, urlParams, mceSelection, $currentNode, $targetNode, insertElement;
                mceSelection = editor.selection;
                $currentNode = $(mceSelection.getEnd());
                // target selected image (if any)
                $targetNode = $currentNode.closest('[data-embedtype=image]');
                if ($targetNode.length) {
                    url = window.chooserUrls.imageChooserSelectFormat;
                    url = url.replace('00000000', $targetNode.data('id'));
                    console.log($targetNode)
                    console.log("$targetNode")
                    urlParams = {
                        edit: 1,
                        format: $targetNode.data('format'),
                        alt_text: $targetNode.data('alt'),
                        caption: $targetNode.data('caption')
                    };
                    // select and replace target
                    insertElement = function(elem) {
                        mceSelection.select($targetNode.get(0));
                        mceSelection.setNode(elem);
                    };
                }
                else {
                    url = window.chooserUrls.imageChooser;

                    urlParams = {
                        select_format: true
                    };
                    // otherwise target immediate child of nearest div container
                    $targetNode = $currentNode.parentsUntil('div:not([data-embedtype])').not('body,html').last();

                    if (0 == $targetNode.length) {
                        // otherwise target current node
                        $targetNode = $currentNode;
                    }
                    // select and insert after target
                    insertElement = function(elem) {
                        $(elem).insertBefore($targetNode);
                        // editor.insertContent(elem);
                        mceSelection.select(elem);
                    };
                }

                var x = ModalWorkflow({
                    url: url,
                    urlParams: urlParams,
                    onload: IMAGE_CHOOSER_MODAL_ONLOAD_HANDLERS,
                    responses: {
                        chosen: function(loadUrl) {
                            var elem = $(loadUrl.html).get(0);
                            editor.undoManager.transact(function() {
                                editor.focus();
                                insertElement(elem);
                                console.log(elem)
                                fixContent();
                            });
                        }
                    }
                });
            }

            editor.ui.registry.addButton('wagtailimage', {
                icon: 'image',
                text: 'Image',
                onAction: showDialog,
                stateSelector: '[data-embedtype=image]'
            })

            editor.ui.registry.addMenuItem('wagtailimage', {
                icon: 'image',
                text: 'Image',
                onAction: showDialog,
                context: 'insert',
                prependToContext: true
            })

            editor.addCommand('mceWagtailImage', showDialog);

            editor.on('LoadContent', function (e) {
                fixContent();
            });
        });
    })(jQuery);

}).call(this);
