const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

async function jsonOrThrow(res) {
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) {
    const message = data?.error || data?.message || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

export async function register({ email, password, username }) {
  const res = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, username })
  });
  return jsonOrThrow(res);
}

export async function login({ email, password }) {
  const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return jsonOrThrow(res);
}

export async function generateCaption({ imageFile, sentiment, length, userId, token }) {
  const form = new FormData();
  form.append('image', imageFile);
  if (sentiment) form.append('sentiment', sentiment);
  if (length !== undefined && length !== null && `${length}`.trim() !== '') form.append('length', `${length}`);
  if (userId) form.append('user_id', userId);

  const res = await fetch(`${API_BASE_URL}/api/generate-caption`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: form
  });
  return jsonOrThrow(res);
}

export function setAuthSession({ token, user }) {
  if (token) localStorage.setItem('meka_token', token);
  if (user) localStorage.setItem('meka_user', JSON.stringify(user));
}

export function getAuthSession() {
  const token = localStorage.getItem('meka_token');
  const userRaw = localStorage.getItem('meka_user');
  const user = userRaw ? JSON.parse(userRaw) : null;
  return { token, user };
}

export function clearAuthSession() {
  localStorage.removeItem('meka_token');
  localStorage.removeItem('meka_user');
}
