# Helen Accessibility Requirements

Helen is a desktop accessibility copilot, so web-only ARIA attributes are
translated into native desktop behavior.

## Background Operation

- Helen runs quietly in the background.
- Helen does not speak at launch.
- Helen only responds after the wake phrase, typed command, hotkey, or explicit
  button activation.
- Wake phrase: `Helen`.

## Live Announcements

Desktop equivalent of `aria-live="polite"`:

- New assistant messages are spoken only when Helen was invoked.
- Status messages are posted to the activity history.
- The transcript reads oldest to newest.
- The user does not need to visually hunt for Helen's latest response.

## Status Feedback

- Show and expose states: idle, listening, processing, speaking.
- Confirm typed commands visually in the activity history.
- Announce failures with clear next steps.
- Avoid vague errors such as "failed".

## Screen Reader-Friendly Layout

- Controls have descriptive accessible names.
- Decorative visuals are not required to understand the interface.
- Keyboard focus starts in the command field.
- Main actions are available as labeled buttons.
- History is text-first and ordered chronologically.

## Focus Management

- Opening the desktop app places focus in the command field.
- The next milestone should trap focus in modal dialogs.
- Destructive confirmations must return focus to the safest action.

## Voice Dictation

- Voice input must work alongside a running screen reader.
- Push-to-talk and wake-word modes are both supported.
- Wake-word daemon runs separately from the visual shell.

## Error Messaging

- Errors include the reason and recovery step.
- Error state must not rely on color alone.
- Examples:
  - "Tesseract OCR is not installed."
  - "Camera could not be accessed."
  - "Speech recognition service is unavailable."

## Human Escalation

Future requirement:

- Provide a configurable support phone number.
- Add a shortcut to read the support option aloud.
- Do not bury escalation behind visual-only controls.

## Media And Attachments

Future requirement:

- Links and files must have descriptive labels.
- Never speak raw URLs unless explicitly requested.
- Generated document summaries should include filename and source.

## Transcript Export

- Helen can export the local transcript to `Documents/Helen`.
- Exported transcript is plain text for braille displays and external screen
  readers.
