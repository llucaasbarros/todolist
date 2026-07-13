import "./Pagination.css";

export default function Pagination({ page, hasPrevious, hasNext, onPrevious, onNext }) {
  return (
    <div className="pagination">
      <button
        type="button"
        className="btn btn-ghost"
        onClick={onPrevious}
        disabled={!hasPrevious}
      >
        Anterior
      </button>
      <span className="pagination-page">Página {page}</span>
      <button type="button" className="btn btn-ghost" onClick={onNext} disabled={!hasNext}>
        Próxima
      </button>
    </div>
  );
}
