/** @type {import("prettier").Config} */
const config = {
  semi: false, // без точек с запятой
  singleQuote: true, // одинарные кавычки
  jsxSingleQuote: false, // двойные кавычки в JSX/TSX
  trailingComma: 'all', // запятые в конце списков (удобно для git-диффов)
  tabWidth: 2, // стандарт в JS/TS
  useTabs: false,
  printWidth: 80, // ширина строки
  bracketSpacing: true, // { foo: bar } вместо {foo:bar}
  arrowParens: 'always', // (x) => вместо x =>
}

export default config
