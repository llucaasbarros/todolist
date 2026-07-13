import axiosClient from "./axiosClient";

export function login(credentials) {
  return axiosClient.post("/auth/login/", credentials).then((res) => res.data);
}

export function register(payload) {
  return axiosClient.post("/auth/register/", payload).then((res) => res.data);
}
