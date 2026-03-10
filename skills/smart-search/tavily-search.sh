#!/bin/bash
# Tavily Search CLI
# Usage: ./tavily-search.sh "your search query" [max_results] [search_depth]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load environment from ~/.openclaw/.env if available
if [ -f "$HOME/.openclaw/.env" ]; then
    set -a
    source "$HOME/.openclaw/.env"
    set +a
fi

# Configuration
TAVILY_API_KEY="${TAVILY_API_KEY:-}"
MAX_RESULTS="${2:-5}"
SEARCH_DEPTH="${3:-basic}"

# Check API key
if [ -z "$TAVILY_API_KEY" ]; then
    echo -e "${RED}Error: TAVILY_API_KEY not set${NC}"
    echo "Add to ~/.openclaw/.env or export it:"
    echo "  export TAVILY_API_KEY=tvly-dev-xxxxx"
    exit 1
fi

# Check query
if [ -z "$1" ]; then
    echo -e "${RED}Error: Search query required${NC}"
    echo "Usage: $0 \"your search query\" [max_results] [search_depth]"
    echo "  max_results: 1-10 (default: 5)"
    echo "  search_depth: basic|advanced (default: basic)"
    exit 1
fi

QUERY="$1"

echo -e "${BLUE}🔍 Searching Tavily for: ${GREEN}\"$QUERY\"${NC}"
echo -e "${BLUE}Max results: ${YELLOW}$MAX_RESULTS${NC}, Depth: ${YELLOW}$SEARCH_DEPTH${NC}"
echo ""

# Make API request
RESPONSE=$(curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TAVILY_API_KEY" \
  -d "{
    \"query\": \"$QUERY\",
    \"max_results\": $MAX_RESULTS,
    \"search_depth\": \"$SEARCH_DEPTH\",
    \"include_answer\": true,
    \"include_raw_content\": false
  }")

# Parse and display results
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Show AI answer if available
ANSWER=$(echo "$RESPONSE" | jq -r '.answer // empty')
if [ -n "$ANSWER" ] && [ "$ANSWER" != "null" ]; then
    echo -e "${YELLOW}🤖 AI Answer:${NC}"
    echo -e "${BLUE}$ANSWER${NC}"
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
fi

# Show results
echo -e "${YELLOW}📊 Results:${NC}"
echo ""

echo "$RESPONSE" | jq -r '.results[] | @base64' | while read -r item; do
    [ -z "$item" ] && continue
    
    _jq() {
        echo "$item" | base64 --decode | jq -r "$1"
    }
    
    TITLE=$(_jq '.title')
    URL=$(_jq '.url')
    CONTENT=$(_jq '.content')
    SCORE=$(_jq '.score')
    
    # Calculate score percentage
    SCORE_PCT=$(echo "$SCORE * 100" | bc 2>/dev/null || echo "N/A")
    
    echo -e "${BLUE}📌 $TITLE${NC}"
    echo -e "   ${GREEN}URL:${NC} $URL"
    echo -e "   ${YELLOW}Relevance:${NC} ${SCORE_PCT}%"
    echo -e "   ${WHITE}$(echo "$CONTENT" | head -c 300)...${NC}"
    echo ""
done

# Show query info
QUERY_INFO=$(echo "$RESPONSE" | jq -r '.query')
RESPONSE_TIME=$(echo "$RESPONSE" | jq -r '.response_time // "N/A"')
REQUEST_ID=$(echo "$RESPONSE" | jq -r '.request_id // "N/A"')

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${WHITE}Query: \"$QUERY_INFO\" | Response time: ${RESPONSE_TIME}s${NC}"
