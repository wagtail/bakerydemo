# Contributing

Thank you for your interest in improving this project! There are many ways to contribute - see the [Wagtail contributing documentation](https://docs.wagtail.org/en/latest/contributing/index.html) for some suggestions.

To contribute, first fork the repository, then clone your copy:

```bash
git clone git@github.com:your-username/bakerydemo.git
```

Follow the [README instructions](readme.md) to set up your local development environment.

## AI policy

- **Purely AI-generated contributions are not welcome.** If you have made use of AI assistance, please disclose this in your pull request description, and detail the steps you have taken to verify that the code is correct. See the guidelines for [use of generative AI](https://docs.wagtail.org/en/latest/contributing/general_guidelines.html#use-of-generative-ai).

## Development tasks

### Quality assurance

Our `Makefile` has ready-made commands for common needs:

```bash
make lint - check style with ruff, sort python with ruff, indent html, and lint frontend css/js
make format - enforce a consistent code style across the codebase, sort python files with ruff and fix frontend css/js
```

You can also run the project test suite with:

```bash
./manage.py test
```

### Demo data management

If you change content or images in this repo and need to prepare a new fixture file for export, do the following on a branch:

```bash
./manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e sessions -e wagtailsearch.indexentry -e wagtailsearch.sqliteftsindexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription -e wagtailcore.workflowcontenttype -e wagtailadmin.editingsession > bakerydemo/base/fixtures/bakerydemo.json
npx prettier --write bakerydemo/base/fixtures/bakerydemo.json
```

Please optimize any included images to 1200px wide with JPEG compression at 60%. Note that `media/images` is ignored in the repo by `.gitignore` but `media/original_images` is not. Wagtail's local image "renditions" are excluded in the fixture recipe above.

Make a pull request to https://github.com/wagtail/bakerydemo

### Testing Content-Security-Policy compliance in Wagtail

Bakerydemo is set up in such a way that it can be used to test [Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) compatibility in Wagtail. It uses [django-csp](https://django-csp.readthedocs.io/en/latest/index.html) to generate the appropriate [CSP HTTP header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy).

By default, `django-csp` is not enabled since Wagtail isn't fully compatible yet. Set the `CSP_DEFAULT_SRC` environment variable in your `.env` file to set the default policy. An example can be found in `.env.example`.

### Testing against different versions of Wagtail

The `main` branch of this demo is designed to work with both the latest stable release and the latest `main` branch (development version) of Wagtail. To run the demo against a specific version of Wagtail, we have created [git tags](https://github.com/wagtail/bakerydemo/tags) for the latest commits that work with each feature release.

- [`v6.4`](https://github.com/wagtail/bakerydemo/releases/tag/v6.4)
- [`v6.3`](https://github.com/wagtail/bakerydemo/releases/tag/v6.3)
- [`v6.2`](https://github.com/wagtail/bakerydemo/releases/tag/v6.2)
- [`v6.1`](https://github.com/wagtail/bakerydemo/releases/tag/v6.1)

See the [complete tags list](https://github.com/wagtail/bakerydemo/tags) for older releases.

The tags point to the last commit just before the requirements were updated to the next Wagtail version. For example, the `v4.2` tag points to the commit just before the bakerydemo was updated to use Wagtail 5.0. This ensures that the tagged demo code contains the latest updates possible for the supported version.

There were no updates to the demo between Wagtail 4.1 and 4.2, so the `v4.1` and `v4.2` tags point to the same commit.
