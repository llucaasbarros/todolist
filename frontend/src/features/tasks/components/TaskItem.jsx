import { formatDateBR, formatDateTimeBR } from "../../../utils/formatDate";
import ShareTaskForm from "./ShareTaskForm";
import TaskForm from "./TaskForm";

const PRIORITY_LABELS = {
  low: "Baixa",
  medium: "Média",
  high: "Alta",
};

function isOverdue(task) {
  if (!task.due_date || task.is_completed) return false;
  const today = new Date().toISOString().slice(0, 10);
  return task.due_date < today;
}

export default function TaskItem({
  task,
  categories,
  onToggleComplete,
  onDelete,
  onEdit,
  onShare,
  isEditing,
  isSharing,
  onEditSubmit,
  onShareSubmit,
  onCancelExpanded,
  isSubmitting,
}) {
  return (
    <li className={`task-item ${task.is_completed ? "is-completed" : ""}`}>
      <div className="task-item-main">
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={() => onToggleComplete(task)}
        />

        <div className="task-item-body">
          <span className="task-item-title">{task.title}</span>
          {task.description && <p className="task-item-description">{task.description}</p>}
          <p className="task-item-meta">Criada em {formatDateTimeBR(task.created_at)}</p>
          <div className="task-item-badges">
            {task.category_detail && (
              <span
                className="badge"
                style={{ backgroundColor: task.category_detail.color || undefined, color: "#fff" }}
              >
                {task.category_detail.name}
              </span>
            )}
            <span className="badge">{PRIORITY_LABELS[task.priority]}</span>
            {task.due_date && (
              <span className={`badge ${isOverdue(task) ? "badge-danger" : ""}`}>
                Vence em {formatDateBR(task.due_date)}
              </span>
            )}
            {task.due_date_is_holiday && <span className="badge badge-info">Feriado</span>}
            {!task.is_owner && <span className="badge">Compartilhada</span>}
            {task.is_owner && task.shared_with?.length > 0 && (
              <span className="badge">
                Compartilhada com {task.shared_with.map((user) => user.username).join(", ")}
              </span>
            )}
          </div>
        </div>

        {task.is_owner && (
          <div className="task-item-actions">
            <button type="button" className="btn btn-ghost" onClick={() => onEdit(task)}>
              Editar
            </button>
            <button type="button" className="btn btn-ghost" onClick={() => onShare(task)}>
              Compartilhar
            </button>
            <button type="button" className="btn btn-danger" onClick={() => onDelete(task)}>
              Excluir
            </button>
          </div>
        )}
      </div>

      {isEditing && (
        <div className="task-edit-panel">
          <TaskForm
            categories={categories}
            initialValues={task}
            onSubmit={onEditSubmit}
            onCancel={onCancelExpanded}
            isSubmitting={isSubmitting}
          />
        </div>
      )}

      {isSharing && <ShareTaskForm onShare={onShareSubmit} onCancel={onCancelExpanded} />}
    </li>
  );
}
