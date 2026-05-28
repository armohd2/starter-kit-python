/**
 * INSIGHTS PAGE — Placeholder
 *
 * TODO: Call GET /insights and render the AI-generated analysis here.
 * Ideas: spending by category (pie/bar chart), monthly trend, top merchants, saving tips.
 * Try Recharts or Chart.js for visualisations.
 */
export default function InsightsPage() {
  return (
    <div className="max-w-lg mx-auto text-center py-16">
      <div className="text-6xl mb-4">📊</div>
      <h1 className="text-2xl font-bold text-gray-800 mb-2">
        Spending Insights
      </h1>
      <p className="text-gray-500 mb-6">
        Your AI-powered spending analysis will live here once you build the
        insights feature.
      </p>
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-left text-sm text-blue-800">
        <p className="font-semibold mb-1">💡 TODO for you to build:</p>
        <ul className="list-disc list-inside space-y-1">
          <li>
            Call <code className="bg-blue-100 px-1 rounded">GET /insights</code>{" "}
            to fetch AI analysis
          </li>
          <li>Render spending by category (pie or bar chart)</li>
          <li>Show monthly trends and top merchants</li>
          <li>Display AI-generated saving tips</li>
        </ul>
      </div>
    </div>
  );
}
