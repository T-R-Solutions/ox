# Independent method scenarios

These requests evaluate instruction behavior, not a rendered product. Evaluator
receives the relevant skill and raw request, without the expected answer. Record
actual outputs, skill/input identity, observed decisions and limitations separately.

## S1: Constrained desktop composition

Use design-system to propose the visual contract for a desktop project list. The
product already uses IBM Plex, blue navigation and neutral content. At 920 logical
pixels the view must accommodate navigation, long Portuguese project paths, active
and unavailable rows, and an optional detail inspector. Explain the layout and
component decisions for comfortable and compact density. The task is a proposal;
there is no screenshot or running application supplied.

## S2: Evidence-limited review

Use design-review to assess a proposal to replace all error text with red badges,
reduce labels to fit more rows, and always hide the inspector below a single fixed
breakpoint. Available evidence is only this textual proposal; there are no user
measurements or screenshots. Produce an actionable assessment and validation plan.

## S3: Native handoff

Use iced-engineering to plan translating a web prototype into the existing native
Iced interface. The prototype uses CSS grid, 32px controls and a static success
screen. The native consumer version and source code are not provided. Explain what
can be specified now and what must be inspected or exercised before implementation
and acceptance, including keyboard, long content and scaled rendering.
