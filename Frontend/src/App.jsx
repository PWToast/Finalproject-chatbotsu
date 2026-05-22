import "./App.css";
import Navbar from "../component/Navbar";
import Loginfrom from "../component/Loginfrom";
function App() {
  return (
    <>
      <div className="flex flex-col">
        <Navbar />
        <Loginfrom />
      </div>
    </>
  );
}

export default App;
