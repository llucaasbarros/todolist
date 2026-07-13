import TaskItem from "./TaskItem";

export default function TaskList({
  tasks,
  categories,
  onToggleComplete,
  onDelete,
  expandedTaskId,
  expandedMode,
  onEdit,
  onEditSubmit,
  onShare,
  onShareSubmit,
  onCancelExpanded,
  isSubmitting,
}) {
  if (tasks.length === 0) {
    return <p className="empty-state">Nenhuma tarefa encontrada.</p>;
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          categories={categories}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
          onEdit={onEdit}
          onShare={onShare}
          isEditing={expandedTaskId === task.id && expandedMode === "edit"}
          isSharing={expandedTaskId === task.id && expandedMode === "share"}
          onEditSubmit={(payload) => onEditSubmit(task, payload)}
          onShareSubmit={(username) => onShareSubmit(task, username)}
          onCancelExpanded={onCancelExpanded}
          isSubmitting={isSubmitting}
        />
      ))}
    </ul>
  );
}
