import axiosClient from "./axiosClient";

export function getTasks(params) {
  return axiosClient.get("/tasks/", { params }).then((res) => res.data);
}

export function createTask(payload) {
  return axiosClient.post("/tasks/", payload).then((res) => res.data);
}

export function updateTask(id, payload) {
  return axiosClient.patch(`/tasks/${id}/`, payload).then((res) => res.data);
}

export function deleteTask(id) {
  return axiosClient.delete(`/tasks/${id}/`);
}

export function shareTask(id, payload) {
  return axiosClient.post(`/tasks/${id}/share/`, payload).then((res) => res.data);
}
