import { collection, getDocs, doc, deleteDoc } from "firebase/firestore";
import { db } from "../firebase";

export async function listUsers() {
  const snap = await getDocs(collection(db, "users"));
  const users = snap.docs.map((d) => {
    const data = d.data();

    const email = data.email || "";
    const emailPrefix = email ? email.split('@')[0].replace(/[._]/g, ' ') : '';
    return {
      id: d.id,
      name: data.name || data.displayName || emailPrefix || "Unknown",
      email: email || "—",
      dob: data.dob || "",
      bookmarks: Array.isArray(data.bookmarks) ? data.bookmarks : [],
      createdAt: data.createdAt || null,
    };
  });

  return users;
}

export async function deleteUser(id) {
  await deleteDoc(doc(db, "users", id));
}
