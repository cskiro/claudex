#!/usr/bin/env node
/**
 * Simple Weather MCP Server Example
 *
 * Demonstrates basic MCP server structure with two tools:
 * - get_forecast: Get weather forecast for a location
 * - get_alerts: Get weather alerts for a US state
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const NWS_API_BASE = "https://api.weather.gov";

// Initialize server
const server = new Server(
  {
    name: "weather-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "get_forecast",
      description: "Get weather forecast for a location (latitude, longitude)",
      inputSchema: {
        type: "object",
        properties: {
          latitude: {
            type: "number",
            description: "Latitude coordinate",
          },
          longitude: {
            type: "number",
            description: "Longitude coordinate",
          },
        },
        required: ["latitude", "longitude"],
      },
    },
    {
      name: "get_alerts",
      description: "Get weather alerts for a US state",
      inputSchema: {
        type: "object",
        properties: {
          state: {
            type: "string",
            description: "Two-letter US state code (e.g., CA, NY)",
          },
        },
        required: ["state"],
      },
    },
  ],
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_forecast") {
    const { latitude, longitude } = args as { latitude: number; longitude: number };

    try {
      // Get grid point for location
      const pointResponse = await fetch(
        `${NWS_API_BASE}/points/${latitude},${longitude}`
      );
      const pointData = await pointResponse.json();

      // Get forecast from grid point
      const forecastUrl = pointData.properties.forecast;
      const forecastResponse = await fetch(forecastUrl);
      const forecastData = await forecastResponse.json();

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(forecastData.properties.periods, null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching forecast: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }

  if (name === "get_alerts") {
    const { state } = args as { state: string };

    try {
      const response = await fetch(
        `${NWS_API_BASE}/alerts/active?area=${state}`
      );
      const data = await response.json();

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(data.features || [], null, 2),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error fetching alerts: ${error instanceof Error ? error.message : String(error)}`,
          },
        ],
        isError: true,
      };
    }
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP server running on stdio");
}

main().catch(console.error);
