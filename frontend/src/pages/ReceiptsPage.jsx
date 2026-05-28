/**
 * RECEIPTS PAGE — Placeholder
 *
 * TODO: Fetch uploaded receipts from GET /receipts and display them here.
 * Each receipt card could show: filename, upload date, processing status.
 * Once you've built AI extraction, you can show extracted fields (store, total, date, category).
 */
export default function ReceiptsPage() {
  return (
    <div className="max-w-lg mx-auto text-center py-16">
      <div className="text-6xl mb-4">🗂️</div>
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Your Receipts</h1>
      <p className="text-gray-500 mb-6">
        Your uploaded receipts will appear here once you build this feature out.
      </p>
      <div className="p-4 bg-amber-50 border border-amber-200 rounded-lg text-left text-sm text-amber-800">
        <p className="font-semibold mb-1">💡 TODO for you to build:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>
            Call{" "}
            <code className="bg-amber-100 px-1 rounded">GET /receipts</code> to
            fetch uploaded files
          </li>
          <li>Display each receipt with filename, date, and status</li>
          <li>
            After you add AI extraction — show the parsed data (store, total,
            category)
          </li>
        </ul>
      </div>
    </div>
  );
}
