const PUNCTUATION = /(\.\.\.|!!|\?!)/g;

const punctuationStrategy = (block, callback) => {
  const text = block.getText();
  let matches;
  while ((matches = PUNCTUATION.exec(text)) !== null) {
    callback(matches.index, matches.index + matches[0].length);
  }
};

const errorHighlight = {
  color: 'var(--w-color-text-error)',
  outline: '1px solid currentColor',
}

const PunctuationHighlighter = ({ children }) => (
  window.React.createElement('span', { style: errorHighlight, title: 'refer to our styleguide' }, children)
);

window.draftail.registerPlugin({
  type: 'punctuation',
  strategy: punctuationStrategy,
  component: PunctuationHighlighter,
}, 'decorators');
