import { useState } from 'react'
import './App.css'
import MLForm from './components/MLForm'

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>ML Prediction Dashboard</h1>
        <p>Enter Permeate TDS and Flow values to get power savings predictions</p>
      </header>
      <main className="app-main">
        <MLForm />
      </main>
    </div>
  )
}

export default App
