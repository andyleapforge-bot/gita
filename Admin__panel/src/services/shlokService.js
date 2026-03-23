import { db } from '../firebase'
import { collection, addDoc, getDocs, updateDoc, deleteDoc, doc } from 'firebase/firestore'

export async function listShloks() {
  const snap = await getDocs(collection(db, 'shloks'))
  return snap.docs.map((d) => ({ id: d.id, ...d.data() }))
}

export async function addShlok(data) {
  const col = collection(db, 'shloks')
  await addDoc(col, data)
}

export async function updateShlok(id, data) {
  await updateDoc(doc(db, 'shloks', id), data)
}

export async function deleteShlok(id) {
  await deleteDoc(doc(db, 'shloks', id))
}
