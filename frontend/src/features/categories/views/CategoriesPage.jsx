import { useEffect, useState } from "react";
import * as categoriesApi from "../../../api/categoriesApi";
import CategoryForm from "../components/CategoryForm";
import CategoryList from "../components/CategoryList";
import "./categories.css";

export default function CategoriesPage() {
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [editingCategory, setEditingCategory] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    loadCategories();
  }, []);

  async function loadCategories() {
    setIsLoading(true);
    try {
      const data = await categoriesApi.getCategories();
      setCategories(data.results ?? data);
    } catch {
      setError("Não foi possível carregar as categorias.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSubmit(payload) {
    setIsSubmitting(true);
    setError("");
    try {
      if (editingCategory) {
        const updated = await categoriesApi.updateCategory(editingCategory.id, payload);
        setCategories((prev) =>
          prev.map((category) => (category.id === updated.id ? updated : category))
        );
        setEditingCategory(null);
      } else {
        const created = await categoriesApi.createCategory(payload);
        setCategories((prev) => [...prev, created]);
      }
    } catch {
      setError("Não foi possível salvar a categoria.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDelete(category) {
    if (!window.confirm(`Excluir a categoria "${category.name}"?`)) return;
    try {
      await categoriesApi.deleteCategory(category.id);
      setCategories((prev) => prev.filter((item) => item.id !== category.id));
    } catch {
      setError("Não foi possível excluir a categoria.");
    }
  }

  return (
    <div className="categories-page">
      <h1>Categorias</h1>

      {error && <div className="alert">{error}</div>}

      <div className="card categories-form-card">
        <CategoryForm
          key={editingCategory?.id ?? "new"}
          initialValues={editingCategory}
          onSubmit={handleSubmit}
          onCancel={editingCategory ? () => setEditingCategory(null) : null}
          isSubmitting={isSubmitting}
        />
      </div>

      <div className="card categories-list-card">
        {isLoading ? (
          <p className="empty-state">Carregando...</p>
        ) : (
          <CategoryList
            categories={categories}
            onEdit={setEditingCategory}
            onDelete={handleDelete}
          />
        )}
      </div>
    </div>
  );
}
