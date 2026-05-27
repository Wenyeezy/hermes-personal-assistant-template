# Desktop Mirror And Voice Input

This note describes two practical patterns for a mobile Hermes gateway:

- using voice input from a messaging app;
- mirroring mobile assistant turns to a local desktop log.

It is intentionally generic and does not include private account IDs, tokens, or local runtime logs.

---

## Voice Input Pattern

Some messaging gateways may deliver voice messages as already-transcribed text.

When that happens, the assistant can treat voice messages like normal text commands:

```text
User speaks into mobile app
  -> Messaging app or gateway transcribes speech
  -> Hermes receives text
  -> Hermes handles the command
```

This is useful for:

- adding tasks;
- adding reminders;
- replying to morning briefs;
- sending quick project updates;
- asking the assistant to triage whether something should become long-term memory.

---

## Raw Audio Caveat

Not every gateway delivers voice as text.

Some platforms may deliver raw audio files instead:

```text
Voice message
  -> audio file
  -> speech-to-text provider
  -> text command
```

In that case, the setup needs:

- a local or cloud speech-to-text provider;
- audio format conversion when needed;
- clear privacy rules for sensitive voice content.

For private voice workflows, prefer local speech-to-text when available.

---

## Desktop Mirror Pattern

Messaging apps do not always sync bot/gateway conversations to every desktop client.

A useful workaround is a local mirror:

```text
Mobile message
  -> Hermes gateway
  -> Gateway hook
  -> Daily markdown log
  -> Desktop tail/viewer window
```

This gives the desktop machine:

- a read-only live view;
- searchable daily logs;
- durable operational history;
- a source for later summaries or weekly reviews.

The mirror is not a chat input. It is a receive-only window unless a separate desktop input channel is added.

---

## Recommended Safety Boundary

Mirror logs should be treated as operational logs, not automatic long-term memory.

Recommended rules:

1. Keep mirror logs private.
2. Do not publish raw mirror logs.
3. Do not automatically convert mirror logs into long-term memory.
4. Use memory triage before saving stable preferences, decisions, or private project state.
5. Redact or skip sensitive content when sharing examples.

---

## Useful Next Enhancements

After the basic mirror works:

1. Add full transcript capture instead of short hook snippets.
2. Add daily or weekly summary generation.
3. Add a desktop input channel such as terminal, dashboard, or a local inbox file.
4. Add task/reminder actions triggered by voice commands.
