import { auth, db } from '../firebase'
import {
  signInWithEmailAndPassword,
  sendPasswordResetEmail,
  EmailAuthProvider,
  reauthenticateWithCredential,
  updateEmail,
  updatePassword,
  signOut,
} from 'firebase/auth'
import { doc, getDoc, updateDoc } from 'firebase/firestore'

export async function loginAdmin(email, password) {
  const cred = await signInWithEmailAndPassword(auth, email, password)
  const uid = cred.user.uid

  const snap = await getDoc(doc(db, 'admins', uid))
  if (!snap.exists()) {
    await signOut(auth)
    throw new Error('Admin record missing')
  }

  const data = snap.data()
  if (!data.role || data.role.toLowerCase() !== 'admin') {
    await signOut(auth)
    throw new Error('Access denied: not an admin')
  }

  return cred.user
}

// ⭐ FIX — ADD THIS
export async function requestPasswordReset(email) {
  return await sendPasswordResetEmail(auth, email)
}

export async function reauthenticate(password) {
  const user = auth.currentUser
  if (!user?.email) throw new Error('No authenticated user')
  const cred = EmailAuthProvider.credential(user.email, password)
  await reauthenticateWithCredential(user, cred)
}

export async function changeEmail(newEmail) {
  const user = auth.currentUser
  if (!user) throw new Error('No authenticated user')
  await updateEmail(user, newEmail)
  await updateDoc(doc(db, 'admins', user.uid), { email: newEmail })
}

export async function changePassword(newPassword) {
  const user = auth.currentUser
  if (!user) throw new Error('No authenticated user')
  await updatePassword(user, newPassword)
}
