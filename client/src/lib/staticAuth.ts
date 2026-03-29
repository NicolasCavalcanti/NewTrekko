/**
 * Client-side auth store for the static GitHub Pages demo.
 * Credentials are kept in localStorage — this is intentionally a demo
 * mechanism, not production security.
 */

const USERS_KEY = "trekko_demo_users";
const SESSION_KEY = "trekko_demo_session";

type DemoUser = {
  id: number;
  name: string;
  email: string;
  userType: "trekker" | "guide";
};

type StoredUser = DemoUser & { password: string };

function getUsers(): StoredUser[] {
  try {
    return JSON.parse(localStorage.getItem(USERS_KEY) ?? "[]");
  } catch {
    return [];
  }
}

export function staticLogin(
  email: string,
  password: string,
): { user: DemoUser } | { error: string } {
  const match = getUsers().find(
    (u) => u.email.toLowerCase() === email.toLowerCase() && u.password === password,
  );
  if (!match) return { error: "E-mail ou senha incorretos" };
  const { password: _pw, ...user } = match;
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
  return { user };
}

export function staticRegister(data: {
  name: string;
  email: string;
  password: string;
  userType: "trekker" | "guide";
}): { user: DemoUser } | { error: string } {
  const users = getUsers();
  if (users.some((u) => u.email.toLowerCase() === data.email.toLowerCase())) {
    return { error: "Este e-mail já está cadastrado" };
  }
  const newUser: StoredUser = { id: Date.now(), ...data };
  localStorage.setItem(USERS_KEY, JSON.stringify([...users, newUser]));
  const { password: _pw, ...user } = newUser;
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
  return { user };
}

export function staticGetCurrentUser(): DemoUser | null {
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    return raw ? (JSON.parse(raw) as DemoUser) : null;
  } catch {
    return null;
  }
}

export function staticLogout(): void {
  localStorage.removeItem(SESSION_KEY);
}
