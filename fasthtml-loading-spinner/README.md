# Fasthtml form spinner demo

Code for [this blog post](https://github.com/danielcorin/blog/blob/main/content/til/fasthtml/loading-spinner.md)

[Live article](https://danielcorin.com/til/fasthtml/loading-spinner/)

## Setup

```sh
make install
```

## Run

```sh
make run
```

## Add a new dependency

Add dependency to `requirements.in`.

Re-compile `requirements*.txt` files:

```sh
make compile
```

Reinstall dependencies

```sh
make install
```

When the form is submitted, `htmx-request` get added to `<form>`.
This following CSS flips the visibility of the button copy and the bars loading animation

```css
.indicator {
    display: none;
}
.htmx-request .indicator {
    display: inline-block;
}
.button-content {
    display: inline-block;
}
.htmx-request .button-content {
    display: none;
}
```

By adding `hx_disabled_elt="#user_input, #submit_button"`, `disabled=""` gets added to both the `<input>` and the `<button>`, preventing the content from being modified mid-submit or accidental double submission.
Finally, `hx_target="#content"` replaces the contents of the `<p>` with the result returned by the server.

A more [generic selector approach](https://htmx.org/attributes/hx-disabled-elt/) is documented but it appears to only work for a single selector according to [this issue](https://github.com/bigskysoftware/htmx/issues/2660).
