class PromptController extends window.StimulusModule.Controller {
  static targets = [
    'status',
    'suggest',
    'clear',
    'spinner',
    'feedback',
    'feedbackItemTemplate',
    'suggestions',
    'suggestionItemTemplate',
  ];

  static values = {
    temperature: { default: 1.0, type: Number },
    topK: { default: 3, type: Number },
  };

  static css = /* css */ `
    .wai-spinner {
      padding: 1rem;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .wai-feedback,
    .wai-suggestions {
      list-style-type: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .wai-feedback__item {
      background-color: #f0f8ff;
      color: #333;
      padding: 0.5rem;
      border-radius: 0.25rem;
      margin-bottom: 0.5rem;
    }

    .wai-feedback__item-text {
      margin-bottom: 0;
    }

    .wai-feedback__dismiss,
    .wai-suggestions__dismiss {
      background-color: transparent;
      color: teal;
      padding: 0;
      margin: 0;
      margin-inline-start: auto;
      display: block;
    }

    .wai-suggestions__item {
      background-color: lightblue;
      color: black;
      padding: 0.5rem;
      border-radius: 0.25rem;
    }
  `;

  static status = {
    1: '🔴',
    2: '🟠',
    3: '🟢',
  };

  static icon = /* html */ `
  `;

  static languageNames = new Intl.DisplayNames(['en'], {
    type: 'language',
  });

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
  editorLanguage = document.documentElement.lang || 'en';
  contentLanguageLabel = PromptController.languageNames.of(
    this.contentLanguage,
  );
  editorLanguageLabel = PromptController.languageNames.of(this.editorLanguage);

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

  get schema() {
    return {
      type: 'object',
      properties: {
        qualityScore: {
          type: 'integer',
          enum: [1, 2, 3],
          description:
            'Content quality score (1=needs major improvement, 2=adequate, 3=excellent)',
        },
        qualitativeFeedback: {
          type: 'array',
          items: { type: 'string' },
          description: `3-5 bullet points of qualitative feedback in language: "${this.editorLanguageLabel}"`,
          minItems: 3,
          maxItems: 5,
        },
        specificImprovements: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              originalText: {
                type: 'string',
                description: 'The original text that needs improvement',
              },
              suggestedText: {
                type: 'string',
                description: `The suggested revised text. Translate the text to ${this.contentLanguageLabel} if necessary. The text MUST be in ${this.contentLanguageLabel}.`,
              },
              explanation: {
                type: 'string',
                description: `Brief explanation in ${this.editorLanguageLabel} of why this change improves the content.`,
              },
            },
            additionalProperties: false,
            required: ['originalText', 'suggestedText', 'explanation'],
          },
          description: `Specific text improvements with original and suggested versions in ${this.contentLanguageLabel}.`,
          minItems: 1,
        },
      },
      additionalProperties: false,
      required: ['qualityScore', 'qualitativeFeedback', 'specificImprovements'],
    };
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
          'You are a helpful assistant that responds with structured data according to the provided schema. The language rules specified are IMPORTANT. Always ensure the feedback and improvements are in the correct language.',
      },
      {
        role: 'user',
        content: `Analyze the given content and provide:
1. A quality score between 1 and 3 (1=needs major improvement, 2=adequate, 3=excellent)
2. 3-5 bullet points of qualitative feedback highlighting strengths and areas for improvement in ${this.editorLanguageLabel}
3. Specific text improvements with original text, suggested revised text in ${this.contentLanguageLabel}, and a brief explanation
   in ${this.editorLanguageLabel} for why each change would improve the content

The language rules specified are IMPORTANT. Always ensure the feedback and improvements are in the correct language.

Return JSON with the provided structure WITHOUT the markdown code block. Start immediately with a { character and end with a } character.`,
      },
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

  clear() {
    this.statusTarget.textContent = '';
    this.feedbackTarget.innerHTML = '';
    this.feedbackTarget.hidden = true;
    this.feedbackTarget.previousElementSibling.hidden = true;
    this.suggestionsTarget.innerHTML = '';
    this.suggestionsTarget.hidden = true;
    this.suggestionsTarget.previousElementSibling.hidden = true;
    this.clearTarget.hidden = true;
  }

  dismissItem(event) {
    event.target.closest('li').remove();
  }

  async renderFeedback(feedback) {
    const marked = await PromptController.marked;
    const item =
      this.feedbackItemTemplateTarget.content.firstElementChild.cloneNode(true);
    item.querySelector('[data-template-key="text"]').innerHTML =
      marked.parse(feedback);
    this.feedbackTarget.appendChild(item);
  }

  async renderSuggestion(suggestion) {
    const marked = await PromptController.marked;
    const item =
      this.suggestionItemTemplateTarget.content.firstElementChild.cloneNode(
        true,
      );
    const data = ['originalText', 'suggestedText', 'explanation'];
    data.forEach((key) => {
      const element = item.querySelector(`[data-template-key="${key}"]`);
      element.innerHTML = marked.parse(suggestion[key]);
    });
    this.suggestionsTarget.appendChild(item);
  }

  async getPageContent() {
    const previewController = window.wagtail.app.queryController('w-preview');
    const { innerText, lang } = await previewController.extractContent();
    this.contentLanguage = lang;
    this.contentLanguageLabel = PromptController.languageNames.of(
      this.contentLanguage,
    );
    return innerText;
  }

  async generate() {
    this.clear();
    const label = this.suggestLabel;
    label.textContent = 'Generating…';
    this.suggestTarget.disabled = true;
    this.spinnerTarget.hidden = false;

    const text = await this.getPageContent();
    const session = await this.session;
    await session.append([
      {
        role: 'user',
        content: 'Content to analyze and improve:\n\n' + text,
      },
    ]);
    const marked = await PromptController.marked;
    let result = await session.prompt(text, {
      responseConstraint: this.schema,
    });
    try {
      const data = JSON.parse(result);
      if (data.qualityScore) {
        this.statusTarget.textContent =
          PromptController.status[data.qualityScore];
        this.feedbackTarget.hidden = false;
        this.feedbackTarget.previousElementSibling.hidden = false;
        data.qualitativeFeedback.forEach((feedback) => {
          this.renderFeedback(feedback);
        });
        this.suggestionsTarget.hidden = false;
        this.suggestionsTarget.previousElementSibling.hidden = false;
        data.specificImprovements.forEach((suggestion) => {
          this.renderSuggestion(suggestion);
        });
      } else {
        this.renderFeedback('Invalid response format');
      }
    } catch (error) {
      console.error('Error parsing AI response:', error);
    }

    this.spinnerTarget.hidden = true;
    this.suggestTarget.disabled = false;
    this.clearTarget.hidden = false;
    label.textContent = 'Generate suggestions';
  }
}

window.wagtail.app.register('prompt', PromptController);
