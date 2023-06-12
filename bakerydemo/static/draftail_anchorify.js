const anchorifyPlugin = {
  type: 'anchorify',

  handlePastedText(text, html, editorState, { setEditorState }) {
    let nextState = editorState;

    console.log(text);

    if (text.match(/^#[a-zA-Z0-9_-]+$/)) {
      const selection = nextState.getSelection();
      let content = nextState.getCurrentContent();
      content = content.createEntity("LINK", "MUTABLE", { url: text });
      const entityKey = content.getLastCreatedEntityKey();

      if (selection.isCollapsed()) {
        content = window.DraftJS.Modifier.insertText(
          content,
          selection,
          text,
          undefined,
          entityKey,
        )
        nextState = window.DraftJS.EditorState.push(
          nextState,
          content,
          "insert-fragment",
        );
      } else {
        nextState = window.DraftJS.RichUtils.toggleLink(nextState, selection, entityKey);
      }

      setEditorState(nextState);
      return "handled";
    }

    return "not-handled";
  },
};

window.draftail.registerPlugin(anchorifyPlugin, 'plugins');
