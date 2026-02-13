#!/bin/bash
# Atlassian MCP Authentication Setup Script
# This script helps configure Atlassian MCP with API token authentication

echo "=== Atlassian MCP Authentication Setup ==="
echo ""
echo "Before running this script, you need:"
echo "1. Atlassian API token from: https://id.atlassian.com/manage-profile/security/api-tokens"
echo "2. Your Atlassian email address"
echo ""

# Prompt for credentials
read -p "Enter your Atlassian email: " ATLASSIAN_EMAIL
read -sp "Enter your Atlassian API token: " ATLASSIAN_TOKEN
echo ""

# Create base64 encoded credentials
ENCODED_CREDS=$(echo -n "${ATLASSIAN_EMAIL}:${ATLASSIAN_TOKEN}" | base64)

echo ""
echo "=== Configuration Options ==="
echo ""
echo "Option 1: HTTP Transport (Recommended - currently working)"
echo "Command:"
echo "claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp \\"
echo "  --header \"Authorization: Basic ${ENCODED_CREDS}\""
echo ""

echo "Option 2: SSE Transport (Requires auth)"
echo "Command:"
echo "claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/mcp \\"
echo "  --header \"Authorization: Basic ${ENCODED_CREDS}\""
echo ""

read -p "Which option? (1 for HTTP, 2 for SSE, 0 to exit): " CHOICE

case $CHOICE in
  1)
    echo ""
    echo "Removing existing atlassian server if present..."
    claude mcp remove atlassian -s local 2>/dev/null

    echo "Adding Atlassian MCP with HTTP transport..."
    claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp \
      --header "Authorization: Basic ${ENCODED_CREDS}"

    echo ""
    echo "✓ Atlassian MCP configured!"
    echo "Run 'claude mcp list' to verify connection"
    ;;
  2)
    echo ""
    echo "Removing existing atlassian server if present..."
    claude mcp remove atlassian -s local 2>/dev/null

    echo "Adding Atlassian MCP with SSE transport..."
    claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/mcp \
      --header "Authorization: Basic ${ENCODED_CREDS}"

    echo ""
    echo "✓ Atlassian MCP configured!"
    echo "Run 'claude mcp list' to verify connection"
    ;;
  0)
    echo "Exiting without changes"
    exit 0
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "NOTE: You may need to restart your Claude Code session for tools to load"
