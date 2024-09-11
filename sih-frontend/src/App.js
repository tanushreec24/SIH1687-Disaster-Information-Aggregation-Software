import Navbar from "./NavBar"
import  DisasterTypes from "./pages/DisasterTypes"
import Home from "./pages/Home"
import PrepardnessTips from "./pages/PrepardnessTips"
import { Route, Routes } from "react-router-dom"
import Announcement from './Announcement';

function App() {
  return (
    <>
    <Announcement />
      <Navbar />
      <div className="container">
      
        <Routes>
          <Route path="/Home" element={<Home />} />
          <Route path="/DisasterTypes" element={<DisasterTypes />} />
          <Route path="/PrepardnessTips" element={<PrepardnessTips />} />
        </Routes><br></br>
      </div>
    </>
  )
}

export default App;