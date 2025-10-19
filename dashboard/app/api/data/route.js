import Database from 'better-sqlite3';

const db = new Database('D:/Github/campus_bms/Database/BackendDatabase.db');

export async function GET(request) {
  try {
    // ✅ Parse the URL to get query parameters
    const { searchParams } = new URL(request.url);
    const hours = searchParams.get('hours') || '3';  // default 3 if not provided

    // ✅ Use parameterized SQL with dynamic hours
    const rows = db
      .prepare(`SELECT * FROM sensor_data WHERE timestamp >= datetime('now', ?)`)
      .all(`-${hours} hours`);

    return new Response(JSON.stringify(rows), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (err) {
    console.error(err);
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
