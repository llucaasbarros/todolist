import { useEffect, useState } from "react";
import * as categoriesApi from "../../../api/categoriesApi";
import * as tasksApi from "../../../api/tasksApi";
import Pagination from "../../../components/ui/Pagination";
import { useToast } from "../../../hooks/useToast";
import TaskFilters from "../components/TaskFilters";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";
import "./tasks.css";

const EMPTY_FILTERS = { is_completed: "", category: "", priority: "" };

export default function TasksPage() {
  const { showToast } = useToast();
  const [tasks, setTasks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [count, setCount] = useState(0);
  const [hasNext, setHasNext] = useState(false);
  const [hasPrevious, setHasPrevious] = useState(false);
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState(EMPTY_FILTERS);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedTaskId, setExpandedTaskId] = useState(null);
  const [expandedMode, setExpandedMode] = useState(null); // "edit" | "share"
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    categoriesApi.getCategories().then((data) => setCategories(data.results ?? data));
  }, []);

  useEffect(() => {
    loadTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, filters]);

  async function loadTasks() {
    setIsLoading(true);
    setError("");
    try {
      const params = { page };
      if (filters.is_completed) params.is_completed = filters.is_completed;
      if (filters.category) params.category = filters.category;
      if (filters.priority) params.priority = filters.priority;

      const data = await tasksApi.getTasks(params);
      setTasks(data.results);
      setCount(data.count);
      setHasNext(Boolean(data.next));
      setHasPrevious(Boolean(data.previous));
    } catch {
      setError("Não foi possível carregar as tarefas.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleFiltersChange(nextFilters) {
    setFilters(nextFilters);
    setPage(1);
  }

  function closeExpanded() {
    setExpandedTaskId(null);
    setExpandedMode(null);
  }

  async function handleCreateSubmit(payload) {
    setIsSubmitting(true);
    setError("");
    try {
      await tasksApi.createTask(payload);
      setPage(1);
      await loadTasks();
    } catch {
      setError("Não foi possível salvar a tarefa.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleEditSubmit(task, payload) {
    setIsSubmitting(true);
    setError("");
    try {
      const updated = await tasksApi.updateTask(task.id, payload);
      setTasks((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
      closeExpanded();
      showToast("Tarefa atualizada com sucesso!");
    } catch {
      showToast("Não foi possível salvar a tarefa.", "error");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleToggleComplete(task) {
    try {
      const updated = await tasksApi.updateTask(task.id, {
        is_completed: !task.is_completed,
      });
      setTasks((prev) => prev.map((item) => (item.id === updated.id ? updated : item)));
    } catch {
      setError("Não foi possível atualizar a tarefa.");
    }
  }

  async function handleDelete(task) {
    if (!window.confirm(`Excluir a tarefa "${task.title}"?`)) return;
    try {
      await tasksApi.deleteTask(task.id);
      await loadTasks();
      showToast("Tarefa excluída com sucesso!");
    } catch {
      showToast("Não foi possível excluir a tarefa.", "error");
    }
  }

  async function handleShareSubmit(task, username) {
    await tasksApi.shareTask(task.id, { username });
    closeExpanded();
    await loadTasks();
    showToast("Tarefa compartilhada com sucesso!");
  }

  return (
    <div className="tasks-page">
      <h1>Tarefas</h1>

      {error && <div className="alert">{error}</div>}

      <div className="card tasks-form-card">
        <TaskForm categories={categories} onSubmit={handleCreateSubmit} isSubmitting={isSubmitting} />
      </div>

      <div className="card tasks-filters-card">
        <TaskFilters categories={categories} filters={filters} onChange={handleFiltersChange} />
      </div>

      <div className="card tasks-list-card">
        {isLoading ? (
          <p className="empty-state">Carregando...</p>
        ) : (
          <>
            <TaskList
              tasks={tasks}
              categories={categories}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
              expandedTaskId={expandedTaskId}
              expandedMode={expandedMode}
              onEdit={(task) => {
                setExpandedTaskId(task.id);
                setExpandedMode("edit");
              }}
              onEditSubmit={handleEditSubmit}
              onShare={(task) => {
                setExpandedTaskId(task.id);
                setExpandedMode("share");
              }}
              onShareSubmit={handleShareSubmit}
              onCancelExpanded={closeExpanded}
              isSubmitting={isSubmitting}
            />
            {count > 0 && (
              <Pagination
                page={page}
                hasPrevious={hasPrevious}
                hasNext={hasNext}
                onPrevious={() => setPage((prev) => Math.max(1, prev - 1))}
                onNext={() => setPage((prev) => prev + 1)}
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}
