const icon = `<svg width="16" height="16" class="Draftail-Icon" aria-hidden="true" viewBox="0 0 576 512" fill="currentColor"><path d="M234.7 42.7L197 56.8c-3 1.1-5 4-5 7.2s2 6.1 5 7.2l37.7 14.1L248.8 123c1.1 3 4 5 7.2 5s6.1-2 7.2-5l14.1-37.7L315 71.2c3-1.1 5-4 5-7.2s-2-6.1-5-7.2L277.3 42.7 263.2 5c-1.1-3-4-5-7.2-5s-6.1 2-7.2 5L234.7 42.7zM46.1 395.4c-18.7 18.7-18.7 49.1 0 67.9l34.6 34.6c18.7 18.7 49.1 18.7 67.9 0L529.9 116.5c18.7-18.7 18.7-49.1 0-67.9L495.3 14.1c-18.7-18.7-49.1-18.7-67.9 0L46.1 395.4zM484.6 82.6l-105 105-23.3-23.3 105-105 23.3 23.3zM7.5 117.2C3 118.9 0 123.2 0 128s3 9.1 7.5 10.8L64 160l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L128 160l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L128 96 106.8 39.5C105.1 35 100.8 32 96 32s-9.1 3-10.8 7.5L64 96 7.5 117.2zm352 256c-4.5 1.7-7.5 6-7.5 10.8s3 9.1 7.5 10.8L416 416l21.2 56.5c1.7 4.5 6 7.5 10.8 7.5s9.1-3 10.8-7.5L480 416l56.5-21.2c4.5-1.7 7.5-6 7.5-10.8s-3-9.1-7.5-10.8L480 352l-21.2-56.5c-1.7-4.5-6-7.5-10.8-7.5s-9.1 3-10.8 7.5L416 352l-56.5 21.2z"></path></svg>`;

class AltTextController extends window.StimulusModule.Controller {
  static targets = ['suggest'];
  static values = {
    imageInput: { default: '', type: String },
    captionInput: { default: '', type: String },
    contextual: { default: false, type: Boolean },
  };

  /** An image-to-text pipeline, shared between all instances of this controller. */
  static captioner;
  /** A text-to-text pipeline for enhancing captions, shared between all instances of this controller. */
  static text2text;
  static {
    import('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2').then(
      ({ pipeline }) => {
        this.captioner = pipeline('image-to-text', 'Mozilla/distilvit');
        this.text2text = pipeline(
          'text2text-generation',
          'Xenova/LaMini-Flan-T5-783M',
        );
      },
    );
  }

  /**
   * Convert an array of input elements into a single string,
   * concatenating their values or inner text.
   * @param {Array<HTMLInputElement | HTMLTextAreaElement | HTMLDivElement>} inputs
   * @returns {string} The concatenated text from the inputs
   */
  static inputsToText = (inputs) =>
    inputs
      .map((input) => input.value || input.innerText)
      .filter((text) => !!text.trim())
      .join('\n\n');

  get imageURL() {
    return this.element.querySelector('img[data-chooser-image]')?.src || '';
  }

  // Override only for JSDoc/typing purposes, not for functionality
  /** @returns {HTMLElement} */
  get element() {
    return super.element;
  }

  /**
   * All text inputs in the form.
   * @returns {Array<HTMLInputElement | HTMLTextAreaElement | HTMLDivElement>}
   */
  get textInputs() {
    return [
      ...this.captionInput.form.querySelectorAll(
        'input[type="text"], textarea, [role="textbox"]',
      ),
    ].filter((input) => input !== this.captionInput);
  }

  /**
   * Text inputs in the form, grouped by their position
   * relative to the caption input (before/after).
   * @returns {{
   *   before: Array<HTMLInputElement | HTMLTextAreaElement | HTMLDivElement>,
   *   after: Array<HTMLInputElement | HTMLTextAreaElement | HTMLDivElement>
   * }}
   */
  get textInputsContext() {
    return Object.groupBy(this.textInputs, (element) =>
      this.captionInput.compareDocumentPosition(element) &
      Node.DOCUMENT_POSITION_PRECEDING
        ? 'before'
        : 'after',
    );
  }

  get textContext() {
    const { inputsToText } = AltTextController;
    return {
      before: inputsToText(this.textInputsContext.before),
      after: inputsToText(this.textInputsContext.after),
    };
  }

  connect() {
    this.generate = this.generate.bind(this);
    this.caption = this.caption.bind(this);
    this.contextualCaption = this.contextualCaption.bind(this);
    this.renderFurniture();
  }

  imageInputValueChanged() {
    if (this.imageInputValue) {
      this.imageInput = this.element.querySelector(this.imageInputValue);
    } else {
      this.imageInput = null;
    }
    if (this.hasSuggestTarget) this.toggleSuggestTarget();
  }

  captionInputValueChanged() {
    if (this.captionInputValue) {
      this.captionInput = this.element.querySelector(this.captionInputValue);
    } else {
      this.captionInput = null;
    }
  }

  toggleSuggestTarget(event) {
    if (event?.target && event.target !== this.imageInput) return;
    this.suggestTarget.disabled = !this.imageInput?.value;
  }

  renderFurniture() {
    this.renderSuggestButton();
    this.renderOutputArea();
    this.toggleSuggestTarget();
  }

  renderSuggestButton() {
    if (this.hasSuggestTarget) return;
    const prefix = this.element.closest('[id]').id;
    const buttonId = `${prefix}-generate`;
    const button = /* html */ `
      <button
        id="${buttonId}"
        type="button"
        data-alt-text-target="suggest"
        data-action="alt-text#generate"
        class="button button-secondary"
      >
        ${icon}

        <span>Generate suggestions</span>
      </button>
    `;
    this.element.insertAdjacentHTML('beforeend', button);
  }

  renderOutputArea() {
    const css = new CSSStyleSheet();
    css.replaceSync(/* css */ `
      .suggestion {
        display: block;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        border-radius: 0.25rem;
        padding: 0.5rem;
        background-color: lightblue;
        color: black;
      }
    `);
    this.outputArea = document.createElement('div');
    document.adoptedStyleSheets.push(css);
    this.element.append(this.outputArea);
  }

  renderSuggestion(suggestion) {
    const template = document.createElement('template');
    template.innerHTML = /* html */ `
      <div class="suggestion">
        <output for="${this.suggestTarget.id}">${suggestion}</output>
        <button class="button button-small" type="button" data-action="alt-text#useSuggestion">Use</button>
      </div>
    `;
    this.outputArea.append(template.content.firstElementChild);
  }

  useSuggestion(event) {
    if (!this.captionInput) return;
    this.captionInput.value = event.target.previousElementSibling.textContent;
  }

  async caption(imageURL) {
    const captioner = await AltTextController.captioner;
    return (await captioner(imageURL))[0].generated_text;
  }

  async contextualCaption(imageURL) {
    const caption = await this.caption(imageURL);
    const text2text = await AltTextController.text2text;
    const { before, after } = this.textContext;

    // Enhance the caption to be more descriptive
    // using the text context from the form.
    const prompt = `
system: Change the following caption to be more descriptive: "${caption}"

system: Given this content shown before the image: ${before}

system: And this content shown after the image: ${after}`;
    return (await text2text(prompt))[0].generated_text;
  }

  async generate() {
    this.outputArea.innerHTML = ''; // Clear previous output
    this.suggestTarget.lastElementChild.textContent = 'Generating…';
    this.suggestTarget.disabled = true;
    const method = this.contextualValue ? this.contextualCaption : this.caption;

    const url = this.imageURL;
    await Promise.allSettled(
      [...Array(3).keys()].map(() =>
        method(url)
          .then((output) => this.renderSuggestion(output))
          .catch((error) => {
            console.error('Error generating suggestion:', error);
          }),
      ),
    );

    this.suggestTarget.disabled = false;
    this.suggestTarget.lastElementChild.textContent = 'Generate suggestions';
  }
}

window.wagtail.app.register('alt-text', AltTextController);
