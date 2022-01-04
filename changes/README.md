# The Changes Folder
`RPD` chose to use `towncrier` for an easier way to create and make changelogs for every version.

Simply when making a pull request do the following command:
```sh
towncrier create pull_request_number.type
```
`Towncrier` currently allows for the `.feature`, `.bugfix`, `.removal`, `.doc` and `.misc` Types.

If you don't make a changelog for your PR it will be either made for you or not merged until you make one.
