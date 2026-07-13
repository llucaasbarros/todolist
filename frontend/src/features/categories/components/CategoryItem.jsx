export default function CategoryItem({ category, onEdit, onDelete }) {
  return (
    <li className="category-item">
      <span className="category-swatch" style={{ backgroundColor: category.color }} />
      <span className="category-name">{category.name}</span>
      <div className="category-item-actions">
        <button type="button" className="btn btn-ghost" onClick={() => onEdit(category)}>
          Editar
        </button>
        <button type="button" className="btn btn-danger" onClick={() => onDelete(category)}>
          Excluir
        </button>
      </div>
    </li>
  );
}
