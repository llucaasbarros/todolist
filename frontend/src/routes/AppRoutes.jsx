import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "../components/layout/Layout";
import LoginPage from "../features/auth/views/LoginPage";
import RegisterPage from "../features/auth/views/RegisterPage";
import TasksPage from "../features/tasks/views/TasksPage";
import CategoriesPage from "../features/categories/views/CategoriesPage";
import ProtectedRoute from "./ProtectedRoute";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/tasks" replace />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/categories" element={<CategoriesPage />} />
        </Route>
      </Route>
    </Routes>
  );
}
