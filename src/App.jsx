import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from "./Login.jsx";
import Reset from "./Reset.jsx";
import Create from "./Create.jsx";
import Dashboard from "./Dashboard.jsx";
import Python from "./Python.jsx";
import CPP from "./CPP.jsx";
import Java from "./Java.jsx";
import Results from "./Results.jsx";

function App() {
  return(
    <>
      <Router>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/reset" element={<Reset />} />
                <Route path="/create" element = {<Create />}/>
                <Route path="/dashboard" element = {<Dashboard />}/>
                <Route path="/python" element = {<Python />}/>
                <Route path="/cpp" element = {<CPP />}/>
                <Route path="/java" element = {<Java />}/>
                <Route path="/results" element = {<Results />}/>
            </Routes>
        </Router>
    </>
  );
}

export default App