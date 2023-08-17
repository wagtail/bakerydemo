/**
 * @copyright ©Melqui Brito. All rights reserved.
 * @author Melqui Brito
 * @version 1.0.0 (2020-03-24)
 * @description Tinymce custom advanced plugin for source code editing.
 */

var aceEditor, tryToBuildAceTimer;


function displayToxEditorModal(e, display = true) {
    let el = document.getElementById('tox-codeeditor-wrap');
    if (display) {
        el.dataset.editor = e.id;
        el.style.display = "flex";
        el.focus();
        document.body.classList.add('tox-codeeditor__disable-scroll');
    } else {
        e = e || tinymce.get(el.dataset.editor);
        el.style.display = "none";
        document.body.classList.remove('tox-codeeditor__disable-scroll');
        e.focus();
    }
}

function saveContent() {
    let el = document.getElementById('tox-codeeditor-wrap');
    let e = tinymce.get(el.dataset.editor);
    e.focus();
    e.undoManager.transact(function() {
        e.setContent(aceEditor.getValue())
    });
    e.selection.setCursorLocation();
    e.nodeChanged();
    displayToxEditorModal(e,false);
}

function applyTheme(ref) {
    aceEditor.setTheme(ref.options[ref.selectedIndex].value);
}

! function() {
    "use strict";

    let themesPack = function() {
        let customPack = tinymce.activeEditor.getParam('codeeditor_themes_pack');
        if (typeof customPack === "string") {
            return customPack.trim().replace(/(\s+)/g, "?").split("?");
        }
        if (Array.isArray(customPack)) {
            return customPack
        }
        return ['twilight', 'merbivore', 'dawn', 'kuroir']
    }();

    let fontSize = function() {
        let customFontSize = tinymce.activeEditor.getParam('codeeditor_font_size');
        if(typeof customFontSize === "number") {
            return parseInt(customFontSize);
        }
        return 12
    }();

    let wrapMode = function() {
        let wrapContent = tinymce.activeEditor.getParam('codeeditor_wrap_mode');
        if(typeof wrapContent === "boolean") {
            return wrapContent
        }
        return true
    }();

    const getOptions = function() {
        let options = '';
        for(let theme of themesPack) {
            options = options + `<option value="ace/theme/${theme}">${theme[0].toUpperCase() + theme.slice(1)}</option>`
        }
        return options
    }

    let styleInnerHTML = `
#tox-codeeditor-wrap {
    position: fixed;
    display: none;
    align-items: center;
    justify-content: center;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    z-index: 10000;
    -webkit-tap-highlight-color: rgba(0,0,0,0);
}
#tox-codeeditor-modal {
    position: relative;
    display: block;
    height: 650px;
    width: 95vw;
    max-width: 1200px;
    background-color: gainsboro;
    border: 1px solid rgba(204,204,204,.4);
    border-radius: 3px;
    box-shadow: 0 16px 16px -10px rgba(0,0,0,.15), 0 0 40px 1px rgba(0,0,0,.15);
    outline: 0 none;
}
#tox-codeeditor-header {
    position: relative;
    display: flex;
    align-items: center;
    background-color: white;
    border-bottom: none;
    color: #000;
    height: 42px;
    justify-content: space-between;
    padding: 8px 16px 0 16px;
    letter-spacing: 0.01em;
    -webkit-font-smoothing: antialiased;
    border-radius: 3px 3px 0 0;
}
#tox-codeeditor-modal-title {
    display: relative;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
    font-size: 20px;
    font-style: normal;
    font-weight: 400;
    line-height: 1.3;
    margin: 0;
    text-transform: none;
    user-select: none;
}
#tox-codeeditor-editor-container {
    position: relative;
    width: calc(100% + 2px);
    margin-left: -1px;
    height: 555px;
    overflow: auto;
    -webkit-overflow-scrolling: touch;
    padding: 3px 0;
}
#tox-codeeditor-editor {
    position: relative;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
}
#tox-codeeditor-close-button {
    padding: 4px;
    left: 0;
    background-color: transparent;
    border-color: transparent;
    box-shadow: unset;
    color: #000;
    border-radius: 3px;
    border-style: solid;
    border-width: 1px;
    cursor: pointer;
    display: inline-block;
    height: 34px;
    width: 34px;
}
#tox-codeeditor-close-button:hover {
    background-color: #e3e3e3;
    border-color: #e3e3e3;
}
#tox-codeeditor-footer {
    position: relative;
    height: 51px;
    background-color: #fff;
    padding: 8px 16px;
    border-radius: 0 0 3px 3px;
}
#tox-codeeditor-footer-buttons {
    position: relative;
    display: inline-block;
    float: right;
}
#tox-codeeditor-footer-buttons button {
    background-color: #3a3f46;
    border-color: #3a3f46;
    border-radius: 3px;
    border-style: solid;
    border-width: 1px;
    box-shadow: none;
    box-sizing: border-box;
    color: #ffffff;
    cursor: pointer;
    display: inline-block;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
    font-size: 14px;
    font-weight: normal;
    letter-spacing: normal;
    line-height: 24px;
    margin: 0;
    outline: none;
    padding: 4px 16px;
    text-align: center;
    text-decoration: none;
    text-transform: capitalize;
    white-space: nowrap;
    margin-left: 8px;
}
#tox-codeeditor-footer-buttons .tox-codeeditor-secondary-button {
    background-color: #f0f0f0;
    border-color: #f0f0f0;
    border-radius: 3px;
    border-style: solid;
    border-width: 1px;
    box-shadow: none;
    color: #000000;
    outline: none;
    padding: 4px 16px;
    text-decoration: none;
    text-transform: capitalize;
}
#tox-codeeditor-footer-buttons .tox-codeeditor-primary-button:hover {
    background-color: #2e3238;
    background-image: none;
    border-color: #2e3238;
    box-shadow: none;
    color: #fff;
}
#tox-codeeditor-footer-buttons .tox-codeeditor-secondary-button:hover {
    background-color: #e3e3e3;
    background-image: none;
    border-color: #e3e3e3;
    box-shadow: none;
    color: #000;
}
.tox-codeeditor-wrap__backdrop {
    background-color: rgba(0,0,0,.4);
    bottom: 0;
    left: 0;
    position: absolute;
    right: 0;
    top: 0;
    backdrop-filter: blur(3px);
}
#tox-codeeditor-theme-label {
    position: relative;
    font-size: 14px;
    float: left;
    margin-right: 5px;
    font-weight: normal;
    line-height: 20px;
    display: inline-block;
    max-width: 100%;
    margin-bottom: 5px;
    color: #626262;
    font-family: "Segoe UI", Arial, sans-serif;
    letter-spacing: 0.01em;
    -webkit-font-smoothing: antialiased;
}
.tox-codeeditor__disable-scroll {
    overflow: hidden;
}
#tox-codeeditor-modal, #tox-codeeditor-header, #tox-codeeditor-editor-container, #tox-codeeditor-footer {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
}
    `;
    let aceStyle = document.createElement('style');
    aceStyle.media = "screen";
    aceStyle.type = "text/css";
    aceStyle.innerHTML = styleInnerHTML;
    document.head.appendChild(aceStyle);

    let codeeditor = document.createElement('div');
    codeeditor.id = "tox-codeeditor-wrap";
    codeeditor.tabIndex = "-1";
    codeeditor.innerHTML = `
<div class="tox-codeeditor-wrap__backdrop"></div>
<div id="tox-codeeditor-modal" tabindex="-1">
    <div id="tox-codeeditor-header" role="presentation">
        <div id="tox-codeeditor-modal-title">Source Editor</div>
        <button type="button" onclick="displayToxEditorModal(false, false)" tabindex="-1" id="tox-codeeditor-close-button">
            <svg width="24" height="24" xmlns="http://www.w3.org/2000/svg"><path d="M17.953 7.453L13.422 12l4.531 4.547-1.406 1.406L12 13.422l-4.547 4.531-1.406-1.406L10.578 12 6.047 7.453l1.406-1.406L12 10.578l4.547-4.531z" fill-rule="evenodd"></path></svg>
        </button>
    </div>
    <div id="tox-codeeditor-editor-container">
        <div id="tox-codeeditor-editor"></div>
    </div>
    <div id="tox-codeeditor-footer">
        <div role="presentation" id="tox-codeeditor-footer-buttons">

            <button title="Cancel" type="button" tabindex="-1" onclick="displayToxEditorModal(false, false)" class="tox-codeeditor-secondary-button">Cancel</button>
            <button title="Save" type="button" tabindex="-1" onclick="saveContent()" class="tox-codeeditor-primary-button">Save</button>
        </div>
    </div>
</div>
    `;
    document.body.appendChild(codeeditor);

    let aceScript = document.createElement('script');
    aceScript.src = "https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.7/ace.js";
    aceScript.type = "text/javascript";
    aceScript.charset = "utf-8";
    document.body.appendChild(aceScript);

    let beautify = document.createElement('script');
    beautify.src = "https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.10.3/beautify.min.js";
    beautify.type = "text/javascript";
    document.body.appendChild(beautify);

    let beautifyCss = document.createElement('script');
    beautifyCss.src = "https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.10.3/beautify-css.min.js";
    beautifyCss.type = "text/javascript";
    document.body.appendChild(beautifyCss);

    let beautifyHtml = document.createElement('script');
    beautifyHtml.src = "https://cdnjs.cloudflare.com/ajax/libs/js-beautify/1.10.3/beautify-html.min.js";
    beautifyHtml.type = "text/javascript";
    document.body.appendChild(beautifyHtml);

    tryToBuildAceTimer = setInterval(() => {
        try {
            aceEditor = ace.edit("tox-codeeditor-editor");
            aceEditor.setTheme("ace/theme/merbivore");
            aceEditor.setFontSize(fontSize);
            clearInterval(tryToBuildAceTimer);
        } catch (e) {}
    }, 500);

    const clear_video_tag = function(editor_content){
        const video_replaces = [{'from': '<p><video', 'to': '<video', 'cond': '</video>'},
            {'from': '</video></p>', 'to': '</video>', 'cond': '/video'}]
        for(const replaces of video_replaces){
            editor_content = editor_content.replace(replaces.from, replaces.to);
        }
        return editor_content
    }

    tinymce.PluginManager.add('codeeditor', function(e) {
        e.ui.registry.addButton('codeeditor', {
            icon: 'sourcecode',
            tooltip: 'Soure Editor',
            onAction: function() {
                displayToxEditorModal(e);
                let editor_content = e.getContent(({source_view: !0 }));
                editor_content = clear_video_tag(editor_content);
                const content = html_beautify(e.dom.decode(editor_content));
                let session = ace.createEditSession(content, "ace/mode/html");
                session.setUseWrapMode(wrapMode);
                aceEditor.setSession(session);
            }
        });
        return {
            getMetadata: function () {
                return {
                    name: "CodeEditor",
                    url: "https://github.com/melquibrito/Source-code-editor-tinymce-plugin"
                };
            }
        }
    });
}();
