import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey:"AIzaSyCr36m9RleRM675RQ5njDrVE9tR42bTVbg",
  authDomain: "ndsoft-7944d.firebaseapp.com",
  projectId: "ndsoft-7944d",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider };


