(function(){
    'use strict';

    (function($){
        tinymce.PluginManager.add('wagtailvideo', function(editor){
            function showDialog(){
                var url, mceSelection, $currentNode, $targetNode, renderVideoTag;

                mceSelection = editor.selection;
                $currentNode = $(mceSelection.getEnd());
                $targetNode = $currentNode.closest('[data-embedtype=video]');
                if($targetNode.length){
                    alert('Todo - logic if video is clicked');
                }else{
                    url = window.chooserUrls.videoChooser;
                    $targetNode = $currentNode.parentsUntil('div:not([data-embedtype])').not('body,html').last();
                    if(0 == $targetNode.length){
                        $targetNode = $currentNode;
                    }
                    renderVideoTag = function(video_data){
                        $.ajax({
                            url: GET_VIDEO_MEDIA_URL+video_data.id,
                            success: function(response){
                                const source = `<source src="${response.media_url}" type="video/mp4">`;
                                const elem = '<video ' + `poster="${video_data.preview.url}"` +
                                    'loop muted autoplay playsinline width="300" height="300"">' +
                                    source + '</video>';
                                editor.undoManager.transact(function(){
                                    editor.insertContent(elem);
                                })
                            }
                        })
                    }
                }

                ModalWorkflow({
                    url: url,
                    urlParams: {},
                    onload: IMAGE_CHOOSER_MODAL_ONLOAD_HANDLERS,
                    responses: {
                        chosen: function(videoData){
                            console.log(videoData)
                            console.log("videoData")
                            renderVideoTag(videoData);
                        }
                    }
                })
            }

            editor.ui.registry.addButton('wagtailvideo', {
                icon: 'preview',
                text: 'Video',
                onAction: showDialog,
                stateSelector: '[data-embedtype=video]'
            })

            editor.ui.registry.addMenuItem('wagtailvideo', {
                icon: 'image',
                text: 'Video',
                onAction: showDialog,
                context: 'insert',
                prependToContext: true
            })

            editor.addCommand('mceWagtailVideo', showDialog);
        })
    })(jQuery)
}).call(this);
