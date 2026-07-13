import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../../hooks/useAuth";
import "./auth.css";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validate() {
    const nextErrors = {};
    if (!username.trim()) nextErrors.username = "Digite seu nome de usuário";
    if (!password) nextErrors.password = "Digite sua senha";
    return nextErrors;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setFormError("");

    const nextErrors = validate();
    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    setIsSubmitting(true);
    try {
      await login({ username, password });
      navigate("/tasks");
    } catch {
      setFormError("Usuário e/ou senha incorreta.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-box">
        <h1 className="auth-title">To-Do List</h1>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          {formError && <div className="auth-alert">{formError}</div>}

          <div className="auth-field">
            <label htmlFor="username">Usuário</label>
            <input
              id="username"
              type="text"
              placeholder="Nome de usuário"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              className={errors.username ? "is-invalid" : ""}
            />
            {errors.username && <span className="auth-field-error">{errors.username}</span>}
          </div>

          <div className="auth-field">
            <label htmlFor="password">Senha</label>
            <input
              id="password"
              type="password"
              placeholder="Senha"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className={errors.password ? "is-invalid" : ""}
            />
            {errors.password && <span className="auth-field-error">{errors.password}</span>}
          </div>

          <button type="submit" className="auth-submit" disabled={isSubmitting}>
            {isSubmitting ? "Entrando..." : "Entrar"}
          </button>
        </form>

        <Link to="/register" className="auth-link">
          Não tem conta? Criar conta
        </Link>
      </div>
    </div>
  );
}
