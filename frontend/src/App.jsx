import { Link, Navigate, Route, Routes } from "react-router-dom";
import { Button } from "./components/ui";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./context/AuthContext";
import AdminLogin from "./pages/admin/AdminLogin";
import Dashboard from "./pages/admin/Dashboard";
import CitizenLogin from "./pages/citizen/Login";
import MyReports from "./pages/citizen/MyReports";
import CitizenRegister from "./pages/citizen/Register";
import SubmitIncident from "./pages/citizen/SubmitIncident";
import Home from "./pages/Home";

function TopBar() {
  const { user, logout } = useAuth();

  return (
    <header className="mx-auto flex max-w-page flex-wrap items-center justify-between gap-x-4 gap-y-3 px-6 py-6 sm:px-10">
      <Link to="/" className="font-serif text-xl tracking-tight text-ink">
        CloudRelief
      </Link>

      {user?.role === "citizen" && (
        <nav className="flex items-center gap-1 sm:gap-2">
          <Button as={Link} to="/report" variant="quiet" className="px-2.5 sm:px-5">
            Report
          </Button>
          <Button as={Link} to="/my-reports" variant="quiet" className="px-2.5 sm:px-5">
            My Reports
          </Button>
          <Button variant="ghost" onClick={logout} className="px-3.5 sm:px-5">
            Log out
          </Button>
        </nav>
      )}
    </header>
  );
}

export default function App() {
  return (
    <div className="min-h-screen">
      <TopBar />
      <Routes>
        <Route path="/" element={<Home />} />

        {/* Citizen portal */}
        <Route path="/login" element={<CitizenLogin />} />
        <Route path="/register" element={<CitizenRegister />} />
        <Route
          path="/report"
          element={
            <ProtectedRoute role="citizen">
              <SubmitIncident />
            </ProtectedRoute>
          }
        />
        <Route
          path="/my-reports"
          element={
            <ProtectedRoute role="citizen">
              <MyReports />
            </ProtectedRoute>
          }
        />

        {/* Admin portal */}
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route
          path="/admin"
          element={
            <ProtectedRoute role="admin">
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
