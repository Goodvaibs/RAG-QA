import "./App.css";
import Home from "./home/Home";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AskMe from "./ask-me/AskMe";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          {/* <Route path="/ask-me" element={<AskMe />} /> */}
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
