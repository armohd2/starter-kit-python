import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import UploadPage from "./pages/UploadPage";
import ReceiptsPage from "./pages/ReceiptsPage";
import InsightsPage from "./pages/InsightsPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm border-b">
          <div className="max-w-4xl mx-auto px-4 py-3 flex gap-6 items-center">
            <span className="font-bold text-lg text-emerald-600">
              Receipts to Riches
            </span>
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                isActive
                  ? "text-emerald-600 font-medium"
                  : "text-gray-500 hover:text-gray-800"
              }
            >
              Upload
            </NavLink>
            <NavLink
              to="/receipts"
              className={({ isActive }) =>
                isActive
                  ? "text-emerald-600 font-medium"
                  : "text-gray-500 hover:text-gray-800"
              }
            >
              Receipts
            </NavLink>
            <NavLink
              to="/insights"
              className={({ isActive }) =>
                isActive
                  ? "text-emerald-600 font-medium"
                  : "text-gray-500 hover:text-gray-800"
              }
            >
              Insights
            </NavLink>
          </div>
        </nav>

        <main className="max-w-4xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="/receipts" element={<ReceiptsPage />} />
            <Route path="/insights" element={<InsightsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
