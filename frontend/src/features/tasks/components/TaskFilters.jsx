export default function TaskFilters({ categories, filters, onChange }) {
  function handleFieldChange(field, value) {
    onChange({ ...filters, [field]: value });
  }

  return (
    <div className="task-filters">
      <div className="field">
        <label htmlFor="filter-status">Status</label>
        <select
          id="filter-status"
          value={filters.is_completed}
          onChange={(event) => handleFieldChange("is_completed", event.target.value)}
        >
          <option value="">Todas</option>
          <option value="false">Pendentes</option>
          <option value="true">Concluídas</option>
        </select>
      </div>

      <div className="field">
        <label htmlFor="filter-category">Categoria</label>
        <select
          id="filter-category"
          value={filters.category}
          onChange={(event) => handleFieldChange("category", event.target.value)}
        >
          <option value="">Todas</option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
      </div>

      <div className="field">
        <label htmlFor="filter-priority">Prioridade</label>
        <select
          id="filter-priority"
          value={filters.priority}
          onChange={(event) => handleFieldChange("priority", event.target.value)}
        >
          <option value="">Todas</option>
          <option value="low">Baixa</option>
          <option value="medium">Média</option>
          <option value="high">Alta</option>
        </select>
      </div>
    </div>
  );
}
