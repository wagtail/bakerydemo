# Exposing the Wagtail user bar to the headless frontend

This document explains how the Wagtail user bar is made available to frontend applications in a headless setup, including the use of the custom `UserbarView`, URL configuration, and customization of the accessibility item for cross-origin support.

## 1. UserbarView and URL configuration

A custom Django view, `UserbarView`, is implemented in `bakerydemo/headless.py` to expose the Wagtail user bar as an API endpoint. The example in this repo does not handle authentication; it only renders the user bar and sets the necessary CORS header. This may need to be adjusted depending on how the API is accessed by the frontend.

To make the user bar accessible to the frontend, a URL pattern for the `UserbarView` is added in the main `urls.py`. This exposes the user bar at `/userbar/`, which the frontend can call to retrieve the user bar markup or data.

## 2. Customizing the accessibility item for cross-origin support

The `allowedOrigins` property in Axe's spec must be set to the headless frontend's host. This allows Axe in the page editor to securely communicate with the frontend for accessibility checks. This can be done by overriding `get_axe_spec` in an `AccessibilityItem` subclass. The subclass is then used via the `construct_wagtail_userbar` hook.

## 3. (Optional) Passing preview panel state to the frontend

You may want to override `HeadlessMixin.get_preview_url` so that the request's `in_preview_panel` attribute is included as a query parameter. This allows the frontend to detect when a page is being rendered in a preview panel and, for example, hide the user bar if desired. See `CustomHeadlessMixin` in `bakerydemo/headless.py` for an example implementation.

## References

- [`bakerydemo/headless.py`](./bakerydemo/headless.py): Contains the `UserbarView` implementation and an example of customizing preview URLs.
- [`bakerydemo/urls.py`](./bakerydemo/urls.py): Main URL configuration including the user bar endpoint.
- [`bakerydemo/base/wagtail_hooks.py`](./bakerydemo/base/wagtail_hooks.py): Customizes the accessibility item for cross-origin support.
