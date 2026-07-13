import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div>
      <header>
        <nav>
          <Link to="/tasks">Tarefas</Link>
          <Link to="/categories">Categorias</Link>
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
