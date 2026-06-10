export default {
  extends: ['@wagtail/stylelint-config-wagtail'],
  rules: {
    'declaration-block-no-redundant-longhand-properties': [
      true,
      { ignoreShorthands: ['gap', 'inset'] },
    ],

    'no-descending-specificity': null, // catch CSS where selector order and specificity create maintenance problems.
    'media-feature-range-notation': null, // Preserve current range-notation usage.
    'custom-property-pattern': '^([a-z][a-z0-9]*)(-{1,2}[a-z0-9]+)*$', // Keep current custom-property naming.

    'declaration-no-important': null, // Allow existing setting !important usage for now.
    'property-disallowed-list': null, // Allow current physical positioning properties.
    'scale-unlimited/declaration-strict-value': null, // Too strict until tokenization is further along.
    'selector-max-id': null, // Relax strict selector limits for existing CSS.
    'selector-max-specificity': null, // Relax strict specificity limits for existing CSS.
  },
};
