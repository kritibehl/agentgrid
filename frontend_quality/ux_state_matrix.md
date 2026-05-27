# AgentGrid UX State Matrix

| State | UI behavior | User value |
|---|---|---|
| Loading | spinner + loading text | shows request progress |
| Error | error panel + retry button | recoverable failure |
| Retry | retry count visible | makes request state inspectable |
| Empty | deterministic fallback data | dashboard remains useful |
| Success | metrics, trace, timeline rendered | operational visibility |
| HOLD decision | yellow badge and blocked release state | clear safety decision |
| ESCALATE decision | red badge and review routing | clear human review path |
| SHIP decision | green badge and released state | clear safe outcome |
