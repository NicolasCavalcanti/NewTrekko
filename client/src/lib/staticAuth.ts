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
  | "role" | "cadasturValidated"
  | "openId" | "loginMethod" | "passwordHash"
  | "createdAt" | "updatedAt" | "lastSignedIn"
> & { password: string };

function defaultDemoUser(stored: StoredUser): DemoUser {
  return {
    ...stored,
    role: "user",
    photoUrl: stored.photoUrl ?? null,
    bio: stored.bio ?? null,
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

export function staticUpdateProfile(data: {
  name: string;
  email: string;
  bio: string;
  cadasturNumber?: string;
}): DemoUser | null {
  const session = staticGetCurrentUser();
  if (!session) return null;
  const updated: DemoUser = {
    ...session,
    name: data.name,
    email: data.email,
    bio: data.bio || null,
    cadasturNumber: data.cadasturNumber ?? session.cadasturNumber,
  };
  localStorage.setItem(SESSION_KEY, JSON.stringify(updated));
  const stored = getUsers();
  const idx = stored.findIndex((u) => u.id === session.id);
  if (idx !== -1) {
    stored[idx] = {
      ...stored[idx],
      name: data.name,
      email: data.email,
      bio: data.bio || null,
      cadasturNumber: data.cadasturNumber ?? null,
    };
    localStorage.setItem(USERS_KEY, JSON.stringify(stored));
  }
  window.dispatchEvent(new Event("staticAuthUpdated"));
  return updated;
}

export function staticSetPhoto(dataUrl: string): void {
  const session = staticGetCurrentUser();
  if (!session) return;
  localStorage.setItem(SESSION_KEY, JSON.stringify({ ...session, photoUrl: dataUrl }));
  const stored = getUsers();
  const idx = stored.findIndex((u) => u.id === session.id);
  if (idx !== -1) {
    stored[idx] = { ...stored[idx], photoUrl: dataUrl };
    localStorage.setItem(USERS_KEY, JSON.stringify(stored));
  }
  window.dispatchEvent(new Event("staticAuthUpdated"));
}

export function staticRemovePhoto(): void {
  const session = staticGetCurrentUser();
  if (!session) return;
  localStorage.setItem(SESSION_KEY, JSON.stringify({ ...session, photoUrl: null }));
  const stored = getUsers();
  const idx = stored.findIndex((u) => u.id === session.id);
  if (idx !== -1) {
    stored[idx] = { ...stored[idx], photoUrl: null };
    localStorage.setItem(USERS_KEY, JSON.stringify(stored));
  }
  window.dispatchEvent(new Event("staticAuthUpdated"));
}
