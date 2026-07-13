import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../../hooks/useAuth";
import "./auth.css";

export default function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [formError, setFormError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  function validate() {
    const nextErrors = {};
    if (!username.trim()) nextErrors.username = "Digite um nome de usuário";
    if (!email.trim()) nextErrors.email = "Digite seu e-mail";
    if (!password) nextErrors.password = "Digite uma senha";
    if (password && confirmPassword !== password) {
      nextErrors.confirmPassword = "As senhas não coincidem";
    }
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
      await register({ username, email, password });
      navigate("/login");
    } catch {
      setFormError("Não foi possível criar sua conta. Tente novamente.");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-box">
        <h1 className="auth-title">Criar conta</h1>

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
            <label htmlFor="email">E-mail</label>
            <input
              id="email"
              type="email"
              placeholder="email@email.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className={errors.email ? "is-invalid" : ""}
            />
            {errors.email && <span className="auth-field-error">{errors.email}</span>}
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

          <div className="auth-field">
            <label htmlFor="confirmPassword">Confirmar senha</label>
            <input
              id="confirmPassword"
              type="password"
              placeholder="Confirmar senha"
              value={confirmPassword}
              onChange={(event) => setConfirmPassword(event.target.value)}
              className={errors.confirmPassword ? "is-invalid" : ""}
            />
            {errors.confirmPassword && (
              <span className="auth-field-error">{errors.confirmPassword}</span>
            )}
          </div>

          <button type="submit" className="auth-submit" disabled={isSubmitting}>
            {isSubmitting ? "Criando conta..." : "Criar conta"}
          </button>
        </form>

        <Link to="/login" className="auth-link">
          Já tem conta? Entrar
        </Link>
      </div>
    </div>
  );
}
