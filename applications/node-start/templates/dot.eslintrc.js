module.exports = {
  env: {
    browser: true,
    commonjs: true,
    es2021: true,
    jest: true,
  },
  extends: [
    'airbnb-base',
  ],
  parserOptions: {
    ecmaVersion: 12,
  },
  rules: {
    'no-underscore-dangle': 'off',
    'import/order': [
      'error',
      {
        groups: [
          ['internal', 'sibling'],
          ['parent'],
          ['external'],
          ['builtin'],
        ],
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
      },
    ],
    'spaced-comment': 'off',
    'no-restricted-syntax': 'off',
    'no-use-before-define': ['error', { functions: false }],
    'no-mixed-operators': 'off',
    'prefer-destructuring': 'off',
    'max-classes-per-file': 'off',
    'no-continue': 'off',
    'no-param-reassign': 'off',
    'no-constant-condition': ['warn', { checkLoops: false }],
    'arrow-body-style': 'off',
    'prefer-const': ['error', { destructuring: 'all' }],
    'dot-notation': ['error', { allowPattern: 'null' }],
    'no-unused-vars': [
      'error',
      {
        varsIgnorePattern: '^_',
        argsIgnorePattern: '^_',
      },
    ],
  },
};
