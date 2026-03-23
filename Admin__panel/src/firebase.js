import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
 

const firebaseConfig = {
  apiKey: "AIzaSyDG-676Bi-B7EFye-8RNkQK9FpUjKkPvoY",
  authDomain: "vitagita-3c6af.firebaseapp.com",
  projectId: "vitagita-3c6af",
  storageBucket: "vitagita-3c6af.firebasestorage.app",  // FIXED
  messagingSenderId: "1067642694608",
  appId: "1:1067642694608:web:7a597e127a4d67a6fc27d5",
  measurementId: "G-N4161HV02N"
};


const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
export const googleProvider = new GoogleAuthProvider();
