import { useState } from "react";

const PRIORITY_OPTIONS = [
  { value: "low", label: "Baixa" },
  { value: "medium", label: "Média" },
  { value: "high", label: "Alta" },
];

export default function TaskForm({ categories, initialValues, onSubmit, onCancel, isSubmitting }) {
  const [title, setTitle] = useState(initialValues?.title ?? "");
  const [description, setDescription] = useState(initialValues?.description ?? "");
  const [category, setCategory] = useState(initialValues?.category ?? "");
  const [dueDate, setDueDate] = useState(initialValues?.due_date ?? "");
  const [priority, setPriority] = useState(initialValues?.priority ?? "medium");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    if (!title.trim()) {
      setError("Digite um título para a tarefa");
      return;
    }
    setError("");
    await onSubmit({
      title: title.trim(),
      description: description.trim(),
      category: category || null,
      due_date: dueDate || null,
      priority,
    });
    if (!initialValues) {
      setTitle("");
      setDescription("");
      setCategory("");
      setDueDate("");
      setPriority("medium");
    }
  }

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="field">
        <label htmlFor="task-title">Título</label>
        <input
          id="task-title"
          type="text"
          placeholder="Ex.: Comprar leite"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
        {error && <span className="field-error">{error}</span>}
      </div>

      <div className="field">
        <label htmlFor="task-description">Descrição</label>
        <textarea
          id="task-description"
          rows={2}
          placeholder="Detalhes (opcional)"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
        />
      </div>

      <div className="task-form-row">
        <div className="field">
          <label htmlFor="task-category">Categoria</label>
          <select
            id="task-category"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
          >
            <option value="">Sem categoria</option>
            {categories.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
        </div>

        <div className="field">
          <label htmlFor="task-due-date">Vencimento</label>
          <input
            id="task-due-date"
            type="date"
            value={dueDate}
            onChange={(event) => setDueDate(event.target.value)}
          />
        </div>

        <div className="field">
          <label htmlFor="task-priority">Prioridade</label>
          <select
            id="task-priority"
            value={priority}
            onChange={(event) => setPriority(event.target.value)}
          >
            {PRIORITY_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="task-form-actions">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {initialValues ? "Salvar" : "Adicionar tarefa"}
        </button>
        {onCancel && (
          <button type="button" className="btn btn-ghost" onClick={onCancel}>
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}
