import { useEffect, useState } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { doc, getDoc } from "firebase/firestore";
import { auth, db } from "../firebase";

export function useAuth() {
  const [user, setUser] = useState(undefined);   // undefined = auth loading
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminLoading, setAdminLoading] = useState(true); // NEW

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (u) => {
      if (!u) {
        setUser(null);
        setIsAdmin(false);
        setAdminLoading(false);
        return;
      }

      setUser(u);

      // ADMIN LOOKUP
      setAdminLoading(true);
      const ref = doc(db, "admins", u.uid);
      const snap = await getDoc(ref);

      if (snap.exists() && snap.data()?.role === "admin") {
        setIsAdmin(true);
      } else {
        setIsAdmin(false);
      }

      setAdminLoading(false);
    });

    return () => unsub();
  }, []);

  return {
    loading: user === undefined || adminLoading, // FIXED
    user,
    isAdmin,
  };
}
