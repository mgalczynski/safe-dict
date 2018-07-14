import React from 'react'
import { Route, Link } from 'react-router-dom'
import Home from '../home'
import Admin from '../admin'

const App = () => (
  <div>
    <header>
      <Link to="/">Home</Link>
      <Link to="/admin">admin</Link>
    </header>

    <main>
      <Route exact path="/" component={Home} />
      <Route exact path="/admin" component={Admin} />
    </main>
  </div>
)

export default App
