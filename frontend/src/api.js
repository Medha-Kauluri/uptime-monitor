import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
});

export async function fetchUrls() {
  const { data } = await api.get("/urls");
  return data;
}

export async function addUrl(url) {
  const { data } = await api.post("/urls", { url });
  return data;
}
