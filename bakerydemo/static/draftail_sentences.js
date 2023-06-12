const countSentences = (str) =>
  str ? (str.match(/[.?!…]+./g) || []).length + 1 : 0;

const SentenceCounter = ({ getEditorState }) => {
  const editorState = getEditorState();
  const content = editorState.getCurrentContent();
  const text = content.getPlainText();

  return window.React.createElement('div', {
    className: 'w-inline-block w-tabular-nums w-help-text w-mr-4',
  }, `Sentences: ${countSentences(text)}`);
}

window.draftail.registerPlugin({
  type: 'sentences',
  meta: SentenceCounter,
}, 'controls');
