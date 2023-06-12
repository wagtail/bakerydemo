// Not a real React component – just creates the entities as soon as it is rendered.
class StockSource extends window.React.Component {
  componentDidMount() {
    const { editorState, entityType, onComplete } = this.props;

    const content = editorState.getCurrentContent();
    const selection = editorState.getSelection();

    const demoStocks = ['AMD', 'AAPL', 'TWTR', 'TSLA', 'BTC'];
    const randomStock = demoStocks[Math.floor(Math.random() * demoStocks.length)];

    // Uses the Draft.js API to create a new entity with the right data.
    const contentWithEntity = content.createEntity(
      entityType.type,
      'IMMUTABLE',
      {
        stock: randomStock,
      },
    );
    const entityKey = contentWithEntity.getLastCreatedEntityKey();

    // We also add some text for the entity to be activated on.
    const text = `$${randomStock}`;

    const newContent = window.DraftJS.Modifier.replaceText(
      content,
      selection,
      text,
      null,
      entityKey,
    );
    const nextState = window.DraftJS.EditorState.push(
      editorState,
      newContent,
      'insert-characters',
    );

    onComplete(nextState);
  }

  render() {
    return null;
  }
}

const Stock = (props) => {
  const { entityKey, contentState } = props;
  const data = contentState.getEntity(entityKey).getData();

  return window.React.createElement(
      'a',
      {
          role: 'button',
          onMouseUp: () => {
              window.open(`https://finance.yahoo.com/quote/${data.stock}`);
          },
      },
      props.children,
  );
};

// Legacy API usage for older Wagtail releases.
window.draftail.registerPlugin({
  type: 'STOCK',
  source: StockSource,
  decorator: Stock,
});
