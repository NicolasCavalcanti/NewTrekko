/**
 * Client-side auth store for the static GitHub Pages demo.
 * Credentials are kept in localStorage — this is intentionally a demo
 * mechanism, not production security.
 */

const USERS_KEY = "trekko_demo_users";
const SESSION_KEY = "trekko_demo_session";

// Must be a superset of every user field accessed in the frontend so
// that the TypeScript union (DemoUser | BackendUser) resolves cleanly.
type DemoUser = {
  id: number;
  name: string;
  email: string;
  userType: "trekker" | "guide";
  role: "user" | "admin";
  photoUrl: string | null;
  bio: string | null;
  cadasturNumber: string | null;
  cadasturValidated: number;
  openId: string | null;
  loginMethod: string | null;
  passwordHash: string | null;
  createdAt: Date | null;
  updatedAt: Date | null;
  lastSignedIn: Date | null;
};

type StoredUser = Omit<DemoUser,
  | "role" | "photoUrl" | "bio" | "cadasturValidated"
  | "openId" | "loginMethod" | "passwordHash"
  | "createdAt" | "updatedAt" | "lastSignedIn"
> & { password: string };

function defaultDemoUser(stored: StoredUser): DemoUser {
  return {
    ...stored,
    role: "user",
    photoUrl: null,
    bio: null,
    cadasturNumber: stored.cadasturNumber ?? null,
    cadasturValidated: 0,
    openId: null,
    loginMethod: "password",
    passwordHash: null,
    createdAt: null,
    updatedAt: null,
    lastSignedIn: null,
  };
}

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
  const user = defaultDemoUser(match);
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
  return { user };
}

export function staticRegister(data: {
  name: string;
  email: string;
  password: string;
  userType: "trekker" | "guide";
  cadasturNumber?: string;
}): { user: DemoUser } | { error: string } {
  const users = getUsers();
  if (users.some((u) => u.email.toLowerCase() === data.email.toLowerCase())) {
    return { error: "Este e-mail já está cadastrado" };
  }
  const stored: StoredUser = {
    id: Date.now(),
    name: data.name,
    email: data.email,
    password: data.password,
    userType: data.userType,
    cadasturNumber: data.cadasturNumber ?? null,
  };
  localStorage.setItem(USERS_KEY, JSON.stringify([...users, stored]));
  const user = defaultDemoUser(stored);
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
