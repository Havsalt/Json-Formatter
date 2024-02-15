# JSON Formatter

Indent structure and format keys in your deeply nested `.json`

## Usage

1) Add directory to `PATH`
2) Run command: `jfmt <source> <optional flags>`

Flags:

- `-i` `--indent` `<indentation level>`, defaults to `2 indents`
- `-n` `--norm`, replace repeating separators (like `-` and `_`) with single variant
- `-f` `--format` `<convention>`, enforce naming convention on keys

Casing conventions supported:

- `lower`
- `upper`
- `title`
- `snake`
- `camal`
- `kebab`
- `pascal`
