import { useState } from "react";

const DEFAULT_COLOR = "#338c96";

export default function CategoryForm({ initialValues, onSubmit, onCancel, isSubmitting }) {
  const [name, setName] = useState(initialValues?.name ?? "");
  const [color, setColor] = useState(initialValues?.color || DEFAULT_COLOR);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    if (!name.trim()) {
      setError("Digite um nome para a categoria");
      return;
    }
    setError("");
    await onSubmit({ name: name.trim(), color });
  }

  return (
    <form className="category-form" onSubmit={handleSubmit}>
      <div className="field">
        <label htmlFor="category-name">Nome</label>
        <input
          id="category-name"
          type="text"
          placeholder="Ex.: Trabalho"
          value={name}
          onChange={(event) => setName(event.target.value)}
        />
        {error && <span className="field-error">{error}</span>}
      </div>

      <div className="field category-color-field">
        <label htmlFor="category-color">Cor</label>
        <input
          id="category-color"
          type="color"
          value={color}
          onChange={(event) => setColor(event.target.value)}
        />
      </div>

      <div className="category-form-actions">
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {initialValues ? "Salvar" : "Adicionar"}
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
