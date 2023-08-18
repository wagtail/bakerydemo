(function() {
    'use strict';

    function createLink(pageData, currentText)
    {
        var a, text;

        // Create link
        a = document.createElement('a');
        a.setAttribute('href', pageData.url);
        if(pageData.rel === true){
            a.setAttribute('rel', 'nofollow');
        }
        if(pageData.target === true){
            a.setAttribute('target', '_blank');
        }
        if(pageData.download === true){
            a.setAttribute('download', pageData.title ? pageData.title:'File');
        }
        if (pageData.id) {
            a.setAttribute('data-id', pageData.id);
            a.setAttribute('data-parent-id', pageData.parentId);
            a.setAttribute('data-linktype', 'page');
            // If it's a link to an internal page, `pageData.title` will not use the link_text
            // like external and email responses do, overwriting selection text :(
            text = currentText || pageData.title;
        }
        else {
            text = pageData.title;
        }
        a.appendChild(document.createTextNode(text));

        return a;
    }

    (function($) {
        tinymce.PluginManager.add('wagtaillink', function (editor) {

            function showDialog() {
                var url, urlParams, mceSelection, $currentNode, $targetNode, currentText, insertElement;

                currentText = '';
                url = window.chooserUrls.pageChooser;
                urlParams = {
                    'allow_external_link': true,
                    'allow_email_link': true,
                    'allow_anchor_link': true,
                };

                mceSelection = editor.selection;
                $currentNode = $(mceSelection.getEnd());
                // target selected link (if any)
                $targetNode = $currentNode.closest('a[href]');

                if ($targetNode.length) {
                    currentText = $targetNode.text();
                    var linkType = $targetNode.data('linktype');
                    var parentPageId = $targetNode.data('parent-id');
                    var href = $targetNode.attr('href');
                    if (linkType == 'page' && parentPageId) {
                        url = window.chooserUrls.pageChooser + parentPageId.toString() + '/';
                    }
                    else if (href.startsWith('mailto:')) {
                        url = window.chooserUrls.emailLinkChooser;
                        href = href.replace('mailto:', '');
                        urlParams['link_url'] = href;
                    }
                    else if (href.startsWith('#')) {
                        url = window.chooserUrls.anchorLinkChooser;
                        href = href.replace('#', '');
                        urlParams['link_url'] = href;
                    }
                    else if (!linkType) {
                        url = window.chooserUrls.externalLinkChooser;
                        urlParams['link_url'] = href;
                    }
                    if( $targetNode.children().length == 0 )
                    {
                        // select and replace text-only target
                        insertElement = function(elem) {
                            mceSelection.select($targetNode.get(0));
                            mceSelection.setNode(elem);
                        };
                    }
                    else {
                        // replace attributes of complex target
                        insertElement = function(elem) {
                            mceSelection.select($targetNode.get(0));
                            var $elem = $(elem);
                            $targetNode.attr('href', $elem.attr('href'));
                            if ($elem.data('linktype')) {
                                $targetNode.data($elem.data());
                            }
                            else {
                                $targetNode.removeData('linktype');
                                $targetNode.removeAttr('data-linktype');
                            }
                        };
                    }
                }
                else {
                    if (!mceSelection.isCollapsed()) {
                        currentText = mceSelection.getContent({format: 'text'});
                    }
                    // replace current selection
                    insertElement = function(elem) {
                        mceSelection.setNode(elem);
                    };
                }

                urlParams['link_text'] = currentText;
                urlParams['target'] = $targetNode.attr('target');
                urlParams['download'] = $targetNode.attr('download');
                const rel_attr = $targetNode.attr('rel');
                if(rel_attr !== undefined){
                    if(rel_attr.split(' ').includes('nofollow')){
                        urlParams['rel'] = $targetNode.attr('rel');
                    }
                }

                ModalWorkflow({
                    url: url,
                    urlParams: urlParams,
                    onload: PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS,
                    responses: {
                        pageChosen: function(pageData) {
                            editor.undoManager.transact(function() {
                                editor.focus();
                                insertElement(createLink(pageData, currentText));
                            });
                        }
                    }
                });
            }

            editor.ui.registry.addButton('wagtaillink', {
                icon: 'link',
                text: 'Insert link',
                onAction: showDialog,
                stateSelector:  'a[data-linktype=page],a[href]:not([data-linktype])'
            })

            // editor.ui.registry.addButton('unlink', {
            //     icon: 'unlink',
            //     text: 'Remove link',
            //     onAction: showDialog,
            //     stateSelector:  'a[data-linktype=page],a[href]'
            // })

            editor.ui.registry.addMenuItem('wagtaillink', {
                icon: 'link',
                text: 'Remove link',
                onAction: showDialog,
                 stateSelector: 'a[data-linktype=page],a[href]:not([data-linktype])',
                context: 'insert',
                prependToContext: true
            })

            editor.addShortcut('Meta+K', '', showDialog);
            editor.addCommand('mceLink', showDialog);
        });
    })(jQuery);

}).call(this);
