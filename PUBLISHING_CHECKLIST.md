# Publishing Checklist

Run this review before making the repository public.

## Permission

- Confirm whether the employer, products, agents, platforms and collaborators may be named.
- Confirm whether screenshots or redacted logs may be shown.

## Accuracy

- Keep behavioural authorship separate from infrastructure work.
- Describe domain operators' knowledge, training and smaller corrections accurately.
- Do not claim measured impact until the underlying numbers are available.

## Safety

- Use synthetic customers, orders, products and shipment identifiers.
- Remove credentials, internal URLs, host paths, channels and personal data.
- Generalise commercial policies and private procedures.
- Run `python3 scripts/validate_public_content.py`.

## GitHub polish

- Add a short repository description.
- Add an open-source licence only if publication rights are clear.
- Pin the repository on Helena's GitHub profile after review.
