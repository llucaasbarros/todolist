import CategoryItem from "./CategoryItem";

export default function CategoryList({ categories, onEdit, onDelete }) {
  if (categories.length === 0) {
    return <p className="empty-state">Nenhuma categoria criada ainda.</p>;
  }

  return (
    <ul className="category-list">
      {categories.map((category) => (
        <CategoryItem
          key={category.id}
          category={category}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
