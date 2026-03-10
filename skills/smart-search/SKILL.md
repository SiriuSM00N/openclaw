---
name: smart-search
description: "Intelligent web search that auto-selects between Brave Search (default) and Tavily (AI-optimized). Use for: research, fact-checking, news, product info, technical queries. Automatically chooses the best engine based on task complexity."
metadata: { "openclaw": { "emoji": "🔍", "requires": { "env": ["TAVILY_API_KEY"] } } }
---

# Smart Search Skill

Intelligent web search that automatically selects the best search engine for your task.

## 🎯 Engine Selection Logic

### Use **Brave Search** (default) for:

✅ Simple factual queries
- "What is [X]?"
- "[Person] birthday"
- "[Product] price"
- Current news and events
- Quick lookups

✅ High-volume searches
- When you need many results
- Exploratory research
- When speed matters most

✅ Privacy-sensitive queries
- Personal information
- Local searches

### Use **Tavily** for:

✅ Complex research tasks
- "Compare X vs Y features"
- "Research [topic] for [purpose]"
- "Find best [product category] for [use case]"

✅ When you need full content
- "Read this article and summarize"
- "Extract key points from [topic]"
- Deep-dive analysis

✅ Structured data needs
- When you need scores/rankings
- Multi-faceted comparisons
- Academic/technical research

✅ High-value queries
- Save Tavily's 1000/month quota for important tasks
- Professional research
- Competitive analysis

## 📋 Decision Matrix

| Query Type | Engine | Why |
|------------|--------|-----|
| "What is..." | Brave | Simple fact |
| "Who is..." | Brave | Biographical fact |
| "Latest news about..." | Brave | Current events |
| "Compare X and Y" | Tavily | Needs structured comparison |
| "Research [topic]" | Tavily | Deep research |
| "Best [product] for [use]" | Tavily | Needs analysis |
| "[topic] tutorial" | Brave | Direct results |
| "Read and summarize [url]" | Tavily | Content extraction |
| "Find studies about..." | Tavily | Academic precision |
| "[product] review" | Brave | Quick overview |

## 🔧 Commands

### Brave Search (Default)

```bash
# Use built-in web_search tool
# No configuration needed
```

### Tavily Search

```bash
# API endpoint
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d '{
    "query": "your search query",
    "max_results": 5,
    "search_depth": "basic",
    "include_answer": true,
    "include_raw_content": false
  }'
```

### Search Depth Options

- `basic` — Fast, surface-level (default)
- `advanced` — Deeper, more comprehensive (uses more quota)

## 🚀 Usage Examples

**User:** "What's the weather today?"
→ **Engine:** Brave (simple fact)

**User:** "Research the best project management tools for remote teams"
→ **Engine:** Tavily (complex comparison needed)

**User:** "Who founded Tesla?"
→ **Engine:** Brave (factual lookup)

**User:** "Compare the features and pricing of Notion vs Obsidian for personal knowledge management"
→ **Engine:** Tavily (detailed comparison)

**User:** "Latest news about AI regulations"
→ **Engine:** Brave (current events)

**User:** "Find academic papers on transformer architecture improvements in 2025"
→ **Engine:** Tavily (research precision)

## ⚠️ Tavily Quota Management

**Free Tier:** 1000 searches/month

**Track usage:**
- Monitor your Tavily dashboard: https://app.tavily.com/home
- Set alerts at 80% usage
- Fallback to Brave when quota is low

**Quota-friendly practices:**
- Use Brave for simple queries
- Batch related searches in one Tavily call
- Cache results when possible
- Use `max_results: 3-5` instead of defaults

## 📝 Response Format

### Brave Search Output
```
- Title
- URL
- Snippet/summary
```

### Tavily Output
```
- Title
- URL
- Content (full excerpt)
- Relevance score
- Optional: AI-generated answer
```

## 🎯 Best Practices

1. **Default to Brave** — It's free and unlimited
2. **Escalate to Tavily** — When results need more depth
3. **Combine tools** — Use `web_fetch` for full article reads
4. **Monitor quota** — Check Tavily usage weekly
5. **Be specific** — Better queries = better results from either engine

## 🔐 Configuration

Add to `~/.openclaw/.env`:

```bash
TAVILY_API_KEY=tvly-dev-xxxxx
```

No configuration needed for Brave Search (built into OpenClaw).

---

**Quick Reference:**

- Simple? → Brave 🦁
- Complex? → Tavily 🎯
- Need full content? → Tavily + web_fetch 📄
- Quota low? → Brave only 🛡️
