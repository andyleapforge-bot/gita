import { db } from '../firebase'
import { collection, addDoc, getDocs, updateDoc, deleteDoc, doc } from 'firebase/firestore'

export async function listVideos() {
  const snap = await getDocs(collection(db, 'videos'))
  return snap.docs.map((d) => ({ id: d.id, ...d.data() }))
}

export async function addVideo(data) {
  await addDoc(collection(db, 'videos'), data)
}

export async function updateVideo(id, data) {
  await updateDoc(doc(db, 'videos', id), data)
}

export async function deleteVideo(id) {
  await deleteDoc(doc(db, 'videos', id))
}
