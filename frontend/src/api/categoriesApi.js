import axiosClient from "./axiosClient";

export function getCategories() {
  return axiosClient.get("/categories/").then((res) => res.data);
}

export function createCategory(payload) {
  return axiosClient.post("/categories/", payload).then((res) => res.data);
}

export function updateCategory(id, payload) {
  return axiosClient.patch(`/categories/${id}/`, payload).then((res) => res.data);
}

export function deleteCategory(id) {
  return axiosClient.delete(`/categories/${id}/`);
}
