class PromptController extends window.StimulusModule.Controller {
  static targets = ['suggest', 'output'];

  static values = {
    temperature: { default: 1.0, type: Number },
    topK: { default: 3, type: Number },
  };

  static css = /* css */ `
    .prompt-output {
      margin-top: 2rem;
    }
  `;

  static icon = /* html */ `
  `;

  static marked;
  static {
    this.marked = import(
      'https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js'
    ).then(({ marked }) => marked);
  }

  static {
    const css = new CSSStyleSheet();
    css.replaceSync(this.css);
    document.adoptedStyleSheets.push(css);
  }

  static get shouldLoad() {
    return 'LanguageModel' in window;
  }

  /** A cached LanguageModel instance Promise to avoid recreating it unnecessarily. */
  #session = null;
  contentLanguage = document.documentElement.lang || 'en';

  /** Promise of a browser LanguageModel instance. */
  get session() {
    if (this.#session) return this.#session; // Return from cache
    return this.createModel();
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
  }

  createModel() {
    const initialPrompts = [
      {
        role: 'system',
        content:
          'You are a helpful and friendly assistant for a content management system. Your task is to provide suggestions on how the user provided content can be improved.',
      },
      //       {
      //         role: 'user',
      //         content:
      //           'Can you give me suggestions on how to improve the following content?',
      //       },
      //       {
      //         role: 'user',
      //         content: `Bread is like, you kno, that thing ppl eat all over, it's made of flur and water and stuf, and somtimes yeast or maybe not, but anywy it comes in alot of shapes like round, or long, or just like sliced in bags at the stor. People eat it with butter or sandwhiches or tost or whatever, and some bread is soft but others are hard and cruncy, but basicly it's just bread and peple like it becuz it's food and fills you up.`,
      //       },
      //       {
      //         role: 'assistant',
      //         content: `Here are some suggestions to improve the content:

      // - **Clarify tone and style**: Remove filler words (“like,” “you kno,” “whatever”) and make the writing more professional and concise.
      // - **Fix spelling and grammar**: Correct typos such as “flur,” “stuf,” “sandwhiches,” “tost,” “becuz,” and “peple.”
      // - **Add structure**: Organize into short sentences or bullet points for readability.
      // - **Enrich details**: Mention different bread types (sourdough, rye, flatbread) and cultural significance.
      // - **Improve flow**: Transition smoothly between preparation, forms, uses, and why people enjoy it.
      // - **Refine conclusion**: Replace “it's just bread and people like it becuz it's food” with a more thoughtful closing about bread's role in daily life.`,
      //       },
    ];
    // eslint-disable-next-line no-undef
    this.#session = LanguageModel.create({
      temperature: this.temperatureValue,
      topK: this.topKValue,
      initialPrompts,
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
    return this.#session;
  }

  temperatureValueChanged(newValue, oldValue) {
    if (oldValue && oldValue != newValue) this.createModel();
  }

  topKValueChanged(newValue, oldValue) {
    if (oldValue && oldValue != newValue) this.createModel();
  }

  async getPageContent() {
    const previewController = window.wagtail.app.queryController('w-preview');
    const { innerText, lang } = await previewController.extractContent();
    this.contentLanguage = lang;
    return innerText;
  }

  async generate() {
    this.outputTarget.innerHTML = ''; // Clear previous output
    const label = this.suggestLabel;
    label.textContent = 'Generating…';
    this.suggestTarget.disabled = true;

    const text = await this.getPageContent();
    const session = await this.session;
    await session.append([
      {
        role: 'user',
        content:
          'Can you give me suggestions on how to improve the following content? Just provide suggestions, without any intro or questions.',
      },
    ]);
    const marked = await PromptController.marked;
    const result = session.promptStreaming(text);
    const dialogContent = this.element.closest('.w-dialog__content');
    let markdown = '';
    for await (const chunk of result) {
      markdown += chunk;
      this.outputTarget.innerHTML = marked.parse(markdown);
      dialogContent.scrollTop = dialogContent.scrollHeight; // Scroll to bottom
    }

    this.suggestTarget.disabled = false;
    label.textContent = 'Generate suggestions';
  }
}

window.wagtail.app.register('prompt', PromptController);
