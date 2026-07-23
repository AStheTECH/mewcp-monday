**Manage boards, items, updates, activity logs, and docs on Monday.com — directly from your AI workflows.**

A Model Context Protocol (MCP) server that exposes Monday.com's GraphQL API (via the official `monday-api-python-sdk`) for managing boards, items, column values, updates, activity logs, and documents.


## Overview

The Monday.com MCP Server provides programmatic access to a Monday.com account:

- Query and inspect boards, columns, groups, and items — with pagination and date-range filtering
- Create, update, and manage items and subitems: column values, group moves, file uploads, archiving, and deletion
- Post and fetch updates (comments), review board activity logs, and read Monday.com docs

Perfect for:

- Automating project and task management workflows from AI agents
- Building assistants that read and update Monday.com boards, items, and comments
- Auditing board activity and syncing Monday.com data into other systems


## Tools


### Boards


<details>
<summary><code>fetch_boards</code> — Query boards with optional filters</summary>

Query boards with optional filters.

**Inputs:**
```
- `limit` (integer, optional, default: 50) — Number of boards to return.
- `page` (integer, optional) — Page number for pagination.
- `ids` (integer[], optional) — Filter by specific board IDs.
- `board_kind` (string enum: `public`, `private`, `share`, optional) — Filter by board type (public, private, share).
- `state` (string enum: `active`, `archived`, `deleted`, `all`, optional) — Filter by state (active, archived, deleted, all).
- `order_by` (string enum: `created_at`, `used_at`, optional) — Sort order (created_at or used_at).
```

**Output `data` schema:**

```typescript
{
  boards: {
    id: string | null;
    name: string | null;
    updated_at: string | null;
    groups: {
      id: string | null;
      title: string | null;
      // additional upstream fields may be present
    }[] | null;
    columns: {
      id: string | null;
      title: string | null;
      type: string | null;
      // additional upstream fields may be present
    }[] | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_boards_by_id</code> — Fetch a single board by ID</summary>

Fetch a single board by ID.

**Inputs:**
```
- `board_id` (string, required) — Board Id
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  updated_at: string | null;
  groups: {
    id: string | null;
    title: string | null;
    // additional upstream fields may be present
  }[] | null;
  columns: {
    id: string | null;
    title: string | null;
    type: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_all_items_by_board_id</code> — Fetch all items with automatic pagination</summary>

Fetch all items with automatic pagination.

**Inputs:**
```
- `board_id` (integer | string, required) — The board ID to fetch items from.
- `query_params` (object, optional) — Query Params for filtering
- `limit` (integer, optional) — Number of items per page
```

**Output `data` schema:**

```typescript
type Item = {
  id: string | null;
  state: string | null;
  name: string | null;
  updated_at: string | null;
  group: {
    id: string | null;
    title: string | null;
    // additional upstream fields may be present
  } | null;
  subitems: Item[] | null;
  parent_item: Item | null;
  column_values: {
    value: string | null;
    text: string | null;
    type: string | null;
    column: {
      id: string | null;
      title: string | null;
      type: string | null;
      // additional upstream fields may be present
    } | null;
    display_value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
};

{
  items: Item[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_item_by_board_id_by_update_date</code> — Fetch items modified within a date range</summary>

Fetch items modified within a date range.

**Inputs:**
```
- `board_id` (integer | string, required) — The board ID to fetch items from.
- `updated_after` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
- `updated_before` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
```

**Output `data` schema:**

```typescript
type Item = {
  id: string | null;
  state: string | null;
  name: string | null;
  updated_at: string | null;
  group: {
    id: string | null;
    title: string | null;
    // additional upstream fields may be present
  } | null;
  subitems: Item[] | null;
  parent_item: Item | null;
  column_values: {
    value: string | null;
    text: string | null;
    type: string | null;
    column: {
      id: string | null;
      title: string | null;
      type: string | null;
      // additional upstream fields may be present
    } | null;
    display_value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
};

{
  items: Item[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_columns_by_board_id</code> — Fetch the column definitions for a board</summary>

Fetch the column definitions (id, title, type) for a given board.

**Inputs:**
```
- `board_id` (string, required) — board id
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  updated_at: string | null;
  groups: {
    id: string | null;
    title: string | null;
    // additional upstream fields may be present
  }[] | null;
  columns: {
    id: string | null;
    title: string | null;
    type: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


### Items


<details>
<summary><code>create_item</code> — Creating an Item</summary>

Creating an Item

**Inputs:**
```
- `board_id` (integer | string, required) — The board ID to fetch items from.
- `group_id` (integer | string, required) — The board ID to fetch items from.
- `item_name` (string, required) — Name of Item
- `column_values` (object, optional) — The column values of the new item.
- `create_labels_if_missing` (boolean, optional, default: false) — Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>create_subitem</code> — Create a subitem</summary>

Create a subitem

**Inputs:**
```
- `parent_item_id` (integer | string, required) — The parent item's unique identifier.
- `subitem_name` (string, required) — The new item's name.
- `column_values` (object, optional) — The column values of the new item.
- `create_labels_if_missing` (boolean, optional, default: false) — Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  column_values: {
    id: string | null;
    text: string | null;
    // additional upstream fields may be present
  }[] | null;
  board: {
    id: string | null;
    name: string | null;
    // additional upstream fields may be present
  } | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>change_simple_column_value</code> — Change an item's column to a new simple text value</summary>

Changes an item's column to a new simple text value. Only this column is changed — other columns keep their current value. NOTE: this overwrites the current value — the prior value is not preserved by this tool. The response includes the updated item's id.

**Inputs:**
```
- `board_id` (integer | string, required) — The board's unique identifier.
- `item_id` (integer | string, required) — The item's unique identifier.
- `column_id` (string, required) — The column's unique identifier.
- `value` (string, required) — The new simple value of the column (pass null to empty the column).
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>change_status_column_value</code> — Set a status column's label</summary>

Sets a status column's label. Only this column is changed — other columns keep their current value. NOTE: this overwrites the current label — the prior label is not preserved by this tool. The response includes the item's id, name, and column_values as returned by the Monday.com API.

**Inputs:**
```
- `board_id` (integer | string, required) — The board's unique identifier.
- `item_id` (integer | string, required) — The item's unique identifier.
- `column_id` (string, required) — The column's unique identifier.
- `value` (string, required) — The status label to set on the column (the exact label text as configured on the board, e.g. 'Done').
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  column_values: {
    id: string | null;
    text: string | null;
    value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>change_date_column_value</code> — Set a date column's value</summary>

Sets a date column's value (pass a datetime object). Only this column is changed — other columns keep their current value. NOTE: this overwrites the current date — the prior date is not preserved by this tool. The response includes the item's id, name, and column_values as returned by the Monday.com API.

**Inputs:**
```
- `board_id` (integer | string, required) — The board's unique identifier.
- `item_id` (integer | string, required) — The item's unique identifier.
- `column_id` (string, required) — The column's unique identifier.
- `timestamp` (string (datetime), required) — The new date value
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  column_values: {
    id: string | null;
    text: string | null;
    value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>change_custom_column_value</code> — Set any column's value using a JSON dict</summary>

Sets any column's value using a JSON dict. Only this column is changed — other columns keep their current value. NOTE: this overwrites the current value — the prior value is not preserved by this tool. The response includes the item's id, name, and column_values as returned by the Monday.com API.

**Inputs:**
```
- `board_id` (integer | string, required) — The board's unique identifier.
- `item_id` (integer | string, required) — The item's unique identifier.
- `column_id` (string, required) — The column's unique identifier.
- `value` (object, required) — The new value of the column as a JSON dict (e.g. {'checked': True} for a checkbox).
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  column_values: {
    id: string | null;
    text: string | null;
    value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>change_multiple_column_values</code> — Set multiple column values at once</summary>

Sets multiple column values at once. Only the columns you provide are changed — others keep their current value. NOTE: this overwrites the current values — the prior values are not preserved by this tool. The response includes the item's id, name, and column_values as returned by the Monday.com API.

**Inputs:**
```
- `board_id` (integer | string, required) — The board's unique identifier.
- `item_id` (integer | string, required) — The item's unique identifier.
- `column_values` (object, required) — Column values in a json format
- `create_labels_if_missing` (boolean, optional, default: false) — Create Status/Dropdown labels if they're missing. (Requires permission to change board structure)
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  column_values: {
    id: string | null;
    text: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>move_item_to_group</code> — Move an item to a different group</summary>

Moves an item to a different group. Only the item's group is changed — other fields keep their current value. NOTE: this overwrites the current group — the prior group is not preserved by this tool. The response includes the updated item's id.

**Inputs:**
```
- `item_id` (integer, required) — The item's unique identifier.
- `group_id` (string, required) — The group's unique identifier.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>archive_item_by_id</code> — Archive an item (reversible)</summary>

Archives an item, removing it from active board views. Unlike delete, this is REVERSIBLE — the item can be restored from Monday.com's archive. Confirm with the user before calling, since it changes the item's visibility across the board.

**Inputs:**
```
- `item_id` (integer, required) — The item's unique identifier.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>delete_item_by_id</code> — Permanently delete an item (destructive, requires explicit user confirmation)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes the item and all its data (column values, subitems, updates). This action is irreversible — the item and its data cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `item_id` (integer, required) — The item's unique identifier.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>upload_file_to_column</code> — Upload a file to a file column</summary>

Upload a file to a file column.

**Inputs:**
```
- `item_id` (integer | string, required) — The item's unique identifier.
- `column_id` (string, required) — The column's unique identifier.
- `file_path` (string, required) — The path of the file on the user's system
- `mimetype` (string, optional) — The mimetype of the file getting uploaded for example: application/json
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  name: string | null;
  url: string | null;
  file_extension: string | null;
  file_size: number | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_items_by_column_value</code> — Fetch items by column value</summary>

Fetch items by column value

**Inputs:**
```
- `board_id` (integer | string, required) — Board Id
- `column_id` (string, required) — column header
- `value` (string, required) — Fetch column by this value
- `limit` (integer, optional) — Limit on number of rows to be fetched
```

**Output `data` schema:**

```typescript
type Item = {
  id: string | null;
  state: string | null;
  name: string | null;
  updated_at: string | null;
  group: {
    id: string | null;
    title: string | null;
    // additional upstream fields may be present
  } | null;
  subitems: Item[] | null;
  parent_item: Item | null;
  column_values: {
    value: string | null;
    text: string | null;
    type: string | null;
    column: {
      id: string | null;
      title: string | null;
      type: string | null;
      // additional upstream fields may be present
    } | null;
    display_value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
};

{
  cursor: string | null;
  items: Item[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_items_by_id</code> — Fetch items by a list of ids</summary>

Fetch items by a list of ids

**Inputs:**
```
- `ids` ((integer | string)[], required) — list of ids for the items to be fetched
```

**Output `data` schema:**

```typescript
type Item = {
  id: string | null;
  state: string | null;
  name: string | null;
  updated_at: string | null;
  group: {
    id: string | null;
    title: string | null;
    // additional upstream fields may be present
  } | null;
  subitems: Item[] | null;
  parent_item: Item | null;
  column_values: {
    value: string | null;
    text: string | null;
    type: string | null;
    column: {
      id: string | null;
      title: string | null;
      type: string | null;
      // additional upstream fields may be present
    } | null;
    display_value: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
};

{
  items: Item[];
  // additional upstream fields may be present
}
```

</details>


### Updates


<details>
<summary><code>create_update</code> — Create an update (comment) on an item</summary>

Create an update (comment) on an item.

**Inputs:**
```
- `item_id` (integer, required) — The item's unique identifier.
- `update_value` (string, required) — Comments to be added to the item
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>delete_update</code> — Permanently delete an update (destructive, requires explicit user confirmation)</summary>

DESTRUCTIVE — REQUIRES EXPLICIT USER CONFIRMATION BEFORE CALLING. Permanently deletes an update (comment) from an item. This action is irreversible — the update's content cannot be recovered. NEVER call this tool autonomously or as part of an automated flow. You MUST stop, tell the user exactly what will be deleted and that it is permanent, and wait for their explicit written confirmation before proceeding.

**Inputs:**
```
- `item_id` (integer, required) — The item's unique identifier.
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_updates</code> — Fetch updates with pagination</summary>

Fetch updates with pagination.

**Inputs:**
```
- `limit` (integer, required) — Number of items to get, the default is 25.
- `page` (integer, required) — Page number to get, starting at 1.
```

**Output `data` schema:**

```typescript
{
  updates: {
    id: string | null;
    body: string | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_updates_for_item</code> — Fetch updates for a specific item</summary>

Fetch updates for a specific item.

**Inputs:**
```
- `item_id` (integer, required) — The item's unique identifier.
- `limit` (integer, required) — Number of items to get, the default is 25.
```

**Output `data` schema:**

```typescript
{
  updates: {
    id: string | null;
    body: string | null;
    created_at: string | null;
    updated_at: string | null;
    creator: {
      id: string | null;
      name: string | null;
      email: string | null;
      // additional upstream fields may be present
    } | null;
    assets: {
      id: string | null;
      name: string | null;
      url: string | null;
      file_extension: string | null;
      file_size: string | null;
      // additional upstream fields may be present
    }[] | null;
    replies: {
      id: string | null;
      body: string | null;
      creator: {
        id: string | null;
        name: string | null;
        email: string | null;
        // additional upstream fields may be present
      } | null;
      created_at: string | null;
      updated_at: string | null;
      // additional upstream fields may be present
    }[] | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_board_updates</code> — Fetch all updates from a board with date filtering</summary>

Fetch all updates from a board with date filtering.

**Inputs:**
```
- `board_ids` (integer, required) — Board Id
- `updated_after` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
- `updated_before` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
```

**Output `data` schema:**

```typescript
{
  updates: {
    id: string | null;
    text_body: string | null;
    item_id: string | null;
    created_at: string | null;
    updated_at: string | null;
    creator: {
      name: string | null;
      id: string | null;
      // additional upstream fields may be present
    } | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_board_updates_page</code> — Fetch a single page of board updates</summary>

Fetch a single page of board updates.

**Inputs:**
```
- `board_id` (integer | string, required) — Board Id
- `limit` (integer, required) — Number of items to get, the default is 25.
- `page` (integer, required) — Page number to get, starting at 1.
- `from_date` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
- `to_date` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
```

**Output `data` schema:**

```typescript
{
  updates: {
    id: string | null;
    text_body: string | null;
    item_id: string | null;
    created_at: string | null;
    updated_at: string | null;
    creator: {
      name: string | null;
      id: string | null;
      // additional upstream fields may be present
    } | null;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


### Activity Logs


<details>
<summary><code>fetch_activity_logs_from_board</code> — Fetch a page of activity logs</summary>

Fetch a page of activity logs.

**Inputs:**
```
- `board_ids` (integer, required) — Board Id
- `page` (integer, required) — Page number to get, starting at 1.
- `limit` (integer, required) — Number of items to get, the default is 25.
- `from_date` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
- `to_date` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
```

**Output `data` schema:**

```typescript
{
  activity_logs: {
    id: string;
    account_id: string;
    created_at: string;
    data: string;
    entity: string;
    event: string;
    user_id: string;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


<details>
<summary><code>fetch_all_activity_logs_from_board</code> — Fetch all activity logs with pagination and event filtering</summary>

Fetch all activity logs with automatic pagination and optional event filtering.

**Inputs:**
```
- `board_ids` (integer, required) — Board Id
- `from_date` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
- `to_date` (string, required) — datetime in the format YYYY-MM-DDTHH:MM:SSZ
- `limit` (integer, required) — Number of items to get, the default is 25.
- `events_filter` (string[], required) — Filter activity logs by specific event types
```

**Output `data` schema:**

```typescript
{
  activity_logs: {
    id: string;
    account_id: string;
    created_at: string;
    data: string;
    entity: string;
    event: string;
    user_id: string;
    // additional upstream fields may be present
  }[];
  // additional upstream fields may be present
}
```

</details>


### Docs


<details>
<summary><code>get_document_with_blocks</code> — Fetch a document with all blocks (auto-paginates)</summary>

Fetch a document with all blocks (auto-paginates).

**Inputs:**
```
- `doc_id` (string, required) — doc id
```

**Output `data` schema:**

```typescript
{
  id: string | null;
  created_at: string | null;
  updated_at: string | null;
  created_by: {
    id: string | null;
    name: string | null;
    // additional upstream fields may be present
  } | null;
  doc_folder_id: string | null;
  doc_kind: string | null;
  name: string | null;
  url: string | null;
  workspace: {
    name: string | null;
    // additional upstream fields may be present
  } | null;
  workspace_id: string | null;
  object_id: string | null;
  settings: string | null;
  blocks: {
    type: string | null;
    content: string | null;
    position: number | null;
    updated_at: string | null;
    id: string | null;
    parent_block_id: string | null;
    // additional upstream fields may be present
  }[] | null;
  // additional upstream fields may be present
}
```

</details>


### System


<details>
<summary><code>monday_health_check</code> — Check server readiness and basic connectivity</summary>

Check server readiness and basic connectivity.

**Inputs:**
```
No inputs.
```

**Output `data` schema:**

```typescript
{
  status: string;
  server: string;
  type: string;
  auth_required: string;
}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Response Envelope</strong></summary>

Every tool returns the same top-level envelope. Only `data` varies per tool.

```json
// Success
{
  "success": true,
  "statusCode": 200,
  "retriable": false,
  "retry_after_seconds": null,
  "error": null,
  "data": { ... }
}

// Error
{
  "success": false,
  "statusCode": 400,
  "retriable": false,
  "retry_after_seconds": null,
  "error": { "code": "VALIDATION_ERROR", "message": "description", "details": {} },
  "data": null
}
```

- `retriable` — `true` when it is safe to retry (rate limit, network error, 503). `false` for validation and auth errors.
- `retry_after_seconds` — seconds to wait before retrying; present only when `retriable` is `true` and the upstream specifies a delay.
- `error.code` — machine-readable string: `VALIDATION_ERROR`, `AUTH_ERROR`, `UPSTREAM_ERROR`, `SERVER_ERROR`.

</details>

<details>
<summary><strong>Common Parameters</strong></summary>

- `board_id` / `board_ids` — Monday.com board's unique identifier. Used across board, item, update, and activity log tools.
- `item_id` — Item's unique identifier. Used across item and update tools.
- `column_id` — Column's unique identifier on a board. Used across item column-value tools.
- `limit` / `page` — Pagination controls used by list/fetch tools (`fetch_updates`, `fetch_board_updates_page`, `fetch_activity_logs_from_board`, etc.).
- `updated_after` / `updated_before` / `from_date` / `to_date` — Datetime bounds used to filter items, updates, and activity logs to a date range.

</details>

<details>
<summary><strong>Resource Formats</strong></summary>

**Board ID:**

```
Numeric string
Example: 1234567890
```

**Item / Column / Update ID:**

```
Integer or numeric string, depending on the tool
Example: 987654321
```

**Datetime:**

```
YYYY-MM-DDTHH:MM:SSZ
Example: 2024-08-13T09:00:00Z
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** API key not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_API_KEY` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check API key is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Monday.com credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Monday.com account (OAuth)
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required tool parameters are included
  3. Check parameter types match expected values

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Monday.com API Error</strong></summary>

- **Cause:** Upstream Monday.com API returned an error
- **Solution:**
  1. Check Monday.com service status at [Monday.com Status Page](https://status.monday.com/)
  2. Verify your credential has the required permissions
  3. Review the error message for specific details

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Monday.com API Documentation](https://developer.monday.com/api-reference/docs)** — Official API reference
- **[monday-api-python-sdk](https://github.com/mondaycom/monday-api-python-sdk)** — Python SDK wrapped by this server
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — FastMCP Credentials package for credential handling

</details>
