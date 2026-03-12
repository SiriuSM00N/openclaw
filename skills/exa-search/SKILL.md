---
name: exa-search
description: "AI-native search using Exa API. Best for: technical queries, academic research, code/documentation search, semantic search. Auto-fallback to Tavily when needed."
metadata: { "openclaw": { "emoji": "🔬", "requires": { "env": ["EXA_API_KEY"] } } }
---

# Exa Search Skill

AI-native search engine optimized for technical and semantic queries.

## 🎯 When to Use Exa

✅ **Technical queries**
- "How does transformer attention work?"
- "Python async/await best practices"
- "Kubernetes pod scheduling algorithm"

✅ **Academic/research**
- "Recent papers on diffusion models"
- "Studies about habit formation"
- "Research on game mechanics engagement"

✅ **Code/documentation**
- "React useEffect cleanup patterns"
- "PostgreSQL index types"
- "Rust lifetime annotations"

✅ **Semantic search**
- Concept-based queries
- When keywords don't capture intent
- "Things like X but for Y"

## 🎯 When to Use Tavily Instead

❌ **Don't use Exa for:**
- Simple factual queries ("What is X?") → Use Tavily basic
- Current news/events → Use Tavily
- Product prices/reviews → Use Tavily
- Local searches → Use Tavily

## 🔧 API Configuration

Add to `~/.openclaw/.env`:

```bash
EXA_API_KEY=1059e9e9-ec4f-4aa5-981b-c42e11ed1f7f
```

## 📋 API Endpoints

### Search

```bash
curl -X POST https://api.exa.ai/search \
  -H "Authorization: Bearer $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "your search query",
    "numResults": 5,
    "type": "neural",
    "useAutoprompt": true
  }'
```

### Find Similar

```bash
curl -X POST https://api.exa.ai/findSimilar \
  -H "Authorization: Bearer $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/article",
    "numResults": 5
  }'
```

### Get Contents

```bash
curl -X POST https://api.exa.ai/contents \
  -H "Authorization: Bearer $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ids": ["result-id-1", "result-id-2"],
    "text": true
  }'
```

## 🔍 Search Types

### Neural Search (default)
- Semantic understanding
- Best for concept-based queries
- Understands intent beyond keywords

### Keyword Search
- Traditional keyword matching
- Best for exact term matching
- Use when neural is too fuzzy

### Magic Search (autoprompt)
- Auto-enhances query
- Best when you're not sure how to phrase it

## 📝 Response Format

```json
{
  "results": [
    {
      "id": "result-uuid",
      "title": "Page Title",
      "url": "https://example.com",
      "score": 0.95,
      "text": "Page content excerpt...",
      "publishedDate": "2026-01-15"
    }
  ]
}
```

## 🚀 Usage Examples

**User:** "How do game economies balance inflation?"
→ **Engine:** Exa (technical game design)

**User:** "What's the best pizza place near me?"
→ **Engine:** Tavily (local search)

**User:** "Explain monad transformers in Haskell"
→ **Engine:** Exa (technical programming)

**User:** "Latest iPhone price"
→ **Engine:** Tavily (factual lookup)

**User:** "Papers on procedural generation in roguelikes"
→ **Engine:** Exa (academic/technical)

## ⚠️ Quota Management

**Free Tier:** Check Exa dashboard for limits

**Best practices:**
- Use for high-value technical queries
- Fallback to Tavily for simple lookups
- Cache results when possible
- Use `numResults: 3-5` instead of defaults

## 🔄 Integration with smart-search

This skill complements `smart-search`:

- `smart-search` → Tavily (general research)
- `exa-search` → Exa (technical/academic)

For best results, use both based on query type.

---

**Quick Reference:**

- Technical? → Exa 🔬
- General research? → Tavily 🎯
- Simple fact? → Tavily basic
- Academic? → Exa 📚
- Code/docs? → Exa 💻
