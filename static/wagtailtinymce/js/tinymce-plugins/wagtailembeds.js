(function() {
    'use strict';

    (function($) {
        tinymce.PluginManager.add('wagtailembeds', function(editor) {

            /* stop editing and resizing of embedded media content */
            function fixContent() {
                $(editor.getBody()).find('[data-embedtype=media]').each(function () {
                    $(this).attr('contenteditable', false).attr('data-mce-contenteditable', 'false').find('div,table,img').attr('data-mce-resize', 'false');
                });
            }

            function showDialog() {
                var url, urlParams, mceSelection, $currentNode, $targetNode, insertElement;

                url = window.chooserUrls.embedsChooser;
                mceSelection = editor.selection;
                $currentNode = $(mceSelection.getEnd());
                // target selected embed (if any)
                $targetNode = $currentNode.closest('[data-embedtype=media]');
                if ($targetNode.length) {
                    urlParams = {
                        edit: 1,
                        url: $targetNode.data('url'),
                        caption: $targetNode.data('caption')
                    };
                    // select and replace target
                    insertElement = function(elem) {
                        mceSelection.select($targetNode.get(0));
                        mceSelection.setNode(elem);
                    };
                }
                else {
                    urlParams = {};
                    // otherwise target immediate child of nearest div container
                    $targetNode = $currentNode.parentsUntil('div:not([data-embedtype])').not('body,html').last();
                    if (0 == $targetNode.length) {
                        // otherwise target current node
                        $targetNode = $currentNode;
                    }
                    // select and insert after target
                    insertElement = function(elem) {
                        $(elem).insertBefore($targetNode);
                        mceSelection.select(elem);
                    };
                }

                ModalWorkflow({
                    url: url,
                    urlParams: urlParams,
                    onload: EMBED_CHOOSER_MODAL_ONLOAD_HANDLERS,
                    responses: {
                        embedChosen: function(embedData) {
                            var elem = $(embedData).get(0);
                            editor.undoManager.transact(function() {
                                editor.focus();
                                insertElement(elem);
                                fixContent();
                            });
                        }
                    }
                });
            }

            editor.ui.registry.addButton('wagtailembed', {
                icon: 'media',
                text: 'Embed',
                onAction: showDialog,
                stateSelector:  '[data-embedtype=media]'
            })

            editor.ui.registry.addMenuItem('wagtailembed', {
                icon: 'media',
                text: 'Embed',
                onAction: showDialog,
                context: 'insert',
                prependToContext: true
            })

            editor.addCommand('mceWagtailEmbed', showDialog);

            editor.on('LoadContent', function (e) {
                console.log("EMBED")
                fixContent();
            });
        });
    })(jQuery);

}).call(this);
