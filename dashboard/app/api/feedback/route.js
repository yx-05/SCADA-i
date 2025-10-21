import Database from 'better-sqlite3';

// This forces the route to be dynamic, preventing caching.
export const dynamic = 'force-dynamic';

// Use the exact, absolute path to your database.
// Double backslashes are required in JavaScript strings for paths.
const dbPath = 'D:\\Github\\campus_bms\\Database\\BackendDatabase.db';
let db;

// Establish the database connection when the server starts.
try {
  db = new Database(dbPath, { fileMustExist: true });
  console.log("✅ [Feedback Route] Successfully connected to the database.");
} catch (err) {
  console.error("❌ [Feedback Route] CRITICAL: Failed to connect to the database:", err.message);
}

export async function GET() { 
  // If the database connection failed, return an error.
  if (!db) {
    return new Response(JSON.stringify({ error: "Database connection has failed. Check server logs." }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    // --- VERIFIED SQL QUERY ---
    // This query uses the exact table and column names from your database schema.
    const query = `
      SELECT feedback_id, hardware, name, email, change_req, reason, timestamp
      FROM feedback_requests
      ORDER BY timestamp DESC
      LIMIT 50
    `;
    const rows = db.prepare(query).all();

    // --- VERIFIED DATA MAPPING ---
    // This mapping uses the exact property names from the query's result.
    const formattedText = rows.map(row => {
      return [
        row.feedback_id,
        row.hardware,
        row.name,
        row.email,
        row.change_req,
        row.reason,
        row.timestamp
      ].join('|');
    }).join('\n');

    // Return the correctly formatted text
    return new Response(formattedText, {
      status: 200,
      headers: { 'Content-Type': 'text/plain' },
    });

  } catch (err) {
    // This will catch any errors from the SQL query itself.
    console.error("❌ [Feedback Route] API Error during query:", err);
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}