# [Feature Request] Session List: Show timestamp + last message preview

## Problem

Currently the session list in Control UI shows long technical IDs like:

```
openai-user:dingtalk-connector:default:333446632538210751:1773...
```

This makes it very hard to:
- Distinguish between different sessions
- Find a specific conversation
- Understand what each session is about

## Current Display

| Session Key | Kind | Updated |
|-------------|------|---------|
| `openai-user:dingtalk-connector:default:333446632538210751:1773...` | direct | 2 minutes ago |
| `openai-user:dingtalk-connector:default:333446632538210751:1773...` | direct | 5 minutes ago |

Both entries look identical!

## Proposed Solution

### Option 1: Frontend-only (Recommended for quick win)

Modify `ui/src/ui/views/sessions.ts` to:
1. Call existing `sessions.preview` API for each session
2. Display format: `[MM/DD HH:mm] Last message preview...`

Example:
```
[03/14 18:30] 能说话了吗
[03/14 18:16] 完成大概需要多长时间
[03/14 14:11] PUA 强化规则已部分执行
```

### Option 2: Backend enhancement (Better performance)

Modify `src/gateway/server-methods/sessions.ts`:
1. Add optional `includePreview` parameter to `sessions.list`
2. Return last message preview along with session metadata
3. Frontend displays the preview directly

## Implementation Notes

- The `sessions.preview` API already exists and returns message previews
- `formatRelativeTimestamp` is already available in `ui/src/ui/format.ts`
- Should respect privacy: truncate long messages, hide sensitive content

## Benefits

- ✅ Much easier to find specific conversations
- ✅ Better UX for users with many sessions
- ✅ No breaking changes (additive feature)

## Priority

Medium - This is a UX improvement that would significantly improve daily usability for active users.

---

**Related:** None
