import { NavLink, Route, Routes } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import TasksPage from "./pages/TasksPage";
import TaskDetailPage from "./pages/TaskDetailPage";
import UploadPage from "./pages/UploadPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import BadCasePage from "./pages/BadCasePage";

const navItems = [
  { to: "/", label: "总览" },
  { to: "/tasks", label: "任务管理" },
  { to: "/upload", label: "日志上传" },
  { to: "/analytics", label: "统计分析" },
  { to: "/bad-cases", label: "BadCase" }
];

export default function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <p className="eyebrow">Graduation Project</p>
          <h1>Agent 自动化评测系统</h1>
        </div>
        <nav className="nav">
          {navItems.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.to === "/"} className="nav-link">
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/tasks/:taskId" element={<TaskDetailPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/bad-cases" element={<BadCasePage />} />
        </Routes>
      </main>
    </div>
  );
}
