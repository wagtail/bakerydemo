export default {
  extends: ['@wagtail/stylelint-config-wagtail'],
  rules: {
    'declaration-block-no-redundant-longhand-properties': [
      true,
      { ignoreShorthands: ['gap', 'inset'] },
    ],

    'media-feature-range-notation': null, // Preserve current range-notation usage.
    'custom-property-pattern': '^([a-z][a-z0-9]*)(-{1,2}[a-z0-9]+)*$', // Keep current custom-property naming.

    'scss/media-feature-value-dollar-variable': null, // Bakerydemo uses plain CSS media queries, not SCSS variables.
    'scss/selector-class-pattern': null, // Existing bakerydemo/Wagtail block class names do not fully match this stricter pattern.
    'declaration-property-value-allowed-list': null, // Current CSS still uses values like text-align: left.
    'declaration-property-value-disallowed-list': null, // Current CSS still uses values like border: none.
    'declaration-no-important': null, // Allow existing !important usage for now.
    'property-disallowed-list': null, // Allow current physical positioning properties.
    'scale-unlimited/declaration-strict-value': null, // Too strict until tokenization is further along.
    'selector-max-specificity': null, // Relax strict specificity limits for existing CSS.
  },
};
