import React from 'react'
import "./styles/style.css";
import AppRoutes from "./routes/index";
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
  return (
    <div className="app">
      {/* <h1 className="text-center">Welcome to the App</h1> */}
      <AppRoutes />
    </div>
  )
}

export default App
