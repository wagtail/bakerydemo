class SummarizeController extends window.StimulusModule.Controller {
  static targets = ['suggest', 'clear'];

  static values = {
    input: { default: '', type: String },
    type: { default: 'teaser', type: String },
    length: { default: 'short', type: String },
  };

  static css = /* css */ `
    .summarize-output {
      margin-top: 1rem;
    }
    .suggestion {
      display: block;
      margin-top: 0.5rem;
      margin-bottom: 0.5rem;
      border-radius: 0.25rem;
      padding: 0.5rem;
      background-color: lightblue;
      color: black;
    }
  `;

  static icon = /* html */ `
    <svg
      width="16"
      height="16"
      class="Draftail-Icon"
      aria-hidden="true"
      viewBox="0 0 576 512"
      fill="currentColor"
    >
      <path
        d="M234.7 42.7L197 56.8c-3 1.1-5 4-5 7.2s2 6.1 5 7.2l37.7 14.1L248.8 123c1.1 3 4 5 7.2 5s6.1-2 7.2-5l14.1-37.7L315 71.2c3-1.1 5-4 5-7.2s-2-6.1-5-7.2L277.3 42.7 263.2 5c-1.1-3-4-5-7.2-5s-6.1 2-7.2 5L234.7 42.7zM46.1 395.4c-18.7 18.7-18.7 49.1 0 67.9l34.6 34.6c18.7 18.7 49.1 18.7 67.9 0L529.9 116.5c18.7-18.7 18.7-49.1 0-67.9L495.3 14.1c-18.7-18.7-49.1-18.7-67.9 0L46.1 395.4zM484.6 82.6l-105 105-23.3-23.3 105-105 23.3 23.3zM7.5 117.2C3 118.9 0 123.2 0 128s3 9.1 7.5 10.8L64 160l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L128 160l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L128 96 106.8 39.5C105.1 35 100.8 32 96 32s-9.1 3-10.8 7.5L64 96 7.5 117.2zm352 256c-4.5 1.7-7.5 6-7.5 10.8s3 9.1 7.5 10.8L416 416l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L480 416l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L480 352l-21.2-56.5c-1.7-4.5-6-7.5-10.8-7.5s-9.1 3-10.8 7.5L416 352l-56.5 21.2z"
      ></path>
    </svg>
  `;

  static {
    const css = new CSSStyleSheet();
    css.replaceSync(this.css);
    document.adoptedStyleSheets.push(css);
  }

  static get shouldLoad() {
    return 'Summarizer' in window;
  }

  /** A cached Summarizer instance Promise to avoid recreating it unnecessarily. */
  #summarizer = null;
  contentLanguage = document.documentElement.lang || 'en';

  /** Promise of a browser Summarizer instance. */
  get summarizer() {
    if (this.#summarizer) return this.#summarizer; // Return from cache
    return this.createSummarizer();
  }

  // Override only for JSDoc/typing purposes, not for functionality
  /** @returns {HTMLElement} */
  get element() {
    return super.element;
  }

  get suggestLabel() {
    return this.suggestTarget.lastElementChild;
  }

  connect() {
    this.generate = this.generate.bind(this);
    this.input = this.element.querySelector(this.inputValue);
    this.renderFurniture();
  }

  createSummarizer() {
    const sharedContext =
      'A summary of the content on a webpage, suitable for use as a meta description.';

    // eslint-disable-next-line no-undef
    this.#summarizer = Summarizer.create({
      sharedContext,
      type: this.typeValue,
      length: this.lengthValue,
      format: 'plain-text',
      expectedInputLanguages: [this.contentLanguage],
      outputLanguage: document.documentElement.lang,
      monitor: (m) => {
        m.addEventListener('downloadprogress', (event) => {
          const label = this.suggestLabel;
          const { loaded, total } = event;
          if (loaded === total) {
            if (this.suggestTarget.disabled) {
              label.textContent = 'Generating…';
            } else {
              label.textContent = 'Generate suggestions';
            }
            return;
          }
          const percent = Math.round((loaded / total) * 100);
          label.textContent = `Loading AI… ${percent}%`;
        });
      },
    });
    return this.#summarizer;
  }

  typeValueChanged(newValue, oldValue) {
    if (oldValue) this.createSummarizer();
  }

  lengthValueChanged(newValue, oldValue) {
    if (oldValue) this.createSummarizer();
  }

  renderFurniture() {
    this.renderSuggestButton();
    this.renderOutputArea();
  }

  renderSuggestButton() {
    if (this.hasSuggestTarget) return;
    const prefix = this.element.closest('[id]').id;
    const buttonId = `${prefix}-generate`;
    const button = /* html */ `
      <button
        id="${buttonId}"
        type="button"
        data-summarize-target="suggest"
        data-action="summarize#generate"
        class="button"
      >
        ${SummarizeController.icon}

        <span>Generate suggestions</span>
      </button>
      <button
        type="button"
        data-summarize-target="clear"
        data-action="summarize#clearOutputArea"
        class="button button-secondary"
        hidden
      >
        Clear suggestions
      </button>
    `;
    this.element.insertAdjacentHTML('beforeend', button);
  }

  renderOutputArea() {
    this.outputArea = document.createElement('div');
    this.outputArea.classList.add('summarize-output');
    this.element.append(this.outputArea);
  }

  clearOutputArea() {
    this.outputArea.innerHTML = ''; // Clear previous output
    this.clearTarget.hidden = true; // Hide the clear button
  }

  renderSuggestion(suggestion) {
    const template = document.createElement('template');
    template.innerHTML = /* html */ `
      <div class="suggestion">
        <output for="${this.suggestTarget.id}">${suggestion}</output>
        <button class="button button-small" type="button" data-action="summarize#useSuggestion">Use</button>
      </div>
    `;
    this.outputArea.append(template.content.firstElementChild);
  }

  useSuggestion(event) {
    if (!this.input) return;
    this.input.value = event.target.previousElementSibling.textContent;
    this.input.dispatchEvent(new Event('input')); // Trigger autosize
  }

  async summarize(text) {
    const summarizer = await this.summarizer;
    return summarizer.summarize(text);
  }

  async getPageContent() {
    const previewController = window.wagtail.app.queryController('w-preview');
    const { innerText, lang } = await previewController.extractContent();
    this.contentLanguage = lang;
    return innerText;
  }

  async generate() {
    this.clearOutputArea();
    const label = this.suggestLabel;
    label.textContent = 'Generating…';
    this.suggestTarget.disabled = true;

    const text = await this.getPageContent();
    await Promise.allSettled(
      [...Array(3).keys()].map(() =>
        this.summarize(text)
          .then((output) => this.renderSuggestion(output))
          .catch((error) => {
            console.error('Error generating suggestion:', error);
          }),
      ),
    );

    this.suggestTarget.disabled = false;
    label.textContent = 'Generate suggestions';
    this.clearTarget.hidden = false; // Show the clear button
  }
}

window.wagtail.app.register('summarize', SummarizeController);
