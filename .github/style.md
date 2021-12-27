<h1 align="center">RPD Commit Styling Guide</h1>

The official one and only commit style to `RPD`

## Conventional Commits Style

this style follows a simple but straight forward commit syle
```txt
<type>(optional-scope): <description>
```

### Displaying extra changes

When desplaying more changes add it to your extendible git description, like so:

Breaking change
```
BREAKING CHANGE: <description>
```
Closing an issue
```
CLOSES: #<issue number>
```

### Types
These are the only currently allowed commit types.

```
feat(optional-scope): <description>
```
for new features
```
fix(optional-scope): <description>
```
used when fixing code or errors
```
chore(optional-scope): <description>
```
used for chore-like commits like bumping the version
```
docs(optional-scope): <description>
```
changes to documentations such as typos
```
refactor(optional-scope): <description>
```
used when refactoring code
```
dev(optional-scope): <description>
```
used when improving developer experience
```
mypy(fix, addition, stubbing): <description>
```
used for mypy commits
```
flake8(optional-scope): <description>
```
used for flake8 commits
```
tests(new, fix, typo, breaking, etc): <description>
```
used when changing tests
```
ci(optional-scope): <description>
```
for ci/cd changes
```
nit(optional-scope): <description>
```
Nit-picky little changes which makes something just look better
```
typo(optional-scope): <description>
```
used when fixing typos
