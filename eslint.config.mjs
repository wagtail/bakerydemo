import js from '@eslint/js';
import globals from 'globals';

export default [
  {
    ignores: ['node_modules', 'venv', '.venv', 'bakerydemo/collect_static'],
  },
  {
    ...js.configs.recommended,
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'script',
      globals: {
        ...globals.browser,
      },
    },
  },
];
