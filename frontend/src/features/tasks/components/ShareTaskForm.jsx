import { useState } from "react";

export default function ShareTaskForm({ onShare, onCancel }) {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!username.trim()) {
      setError("Digite o nome de usuário");
      return;
    }
    setIsSubmitting(true);
    setError("");
    try {
      await onShare(username.trim());
      setUsername("");
    } catch (err) {
      const detail =
        err.response?.data?.username ?? err.response?.data?.detail ?? "Não foi possível compartilhar.";
      setError(detail);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="share-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Nome de usuário"
        value={username}
        onChange={(event) => setUsername(event.target.value)}
      />
      <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
        Compartilhar
      </button>
      <button type="button" className="btn btn-ghost" onClick={onCancel}>
        Cancelar
      </button>
      {error && <span className="field-error">{error}</span>}
    </form>
  );
}
