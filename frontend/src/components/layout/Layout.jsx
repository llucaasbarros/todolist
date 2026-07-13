import { Link, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import "./Layout.css";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="layout">
      <header className="layout-header">
        <nav className="layout-nav">
          <Link to="/tasks">Tarefas</Link>
          <Link to="/categories">Categorias</Link>
        </nav>
        <div className="layout-user">
          {user && <span>{user.username}</span>}
          <button type="button" onClick={handleLogout}>
            Sair
          </button>
        </div>
      </header>
      <main className="layout-content">
        <Outlet />
      </main>
    </div>
  );
}
