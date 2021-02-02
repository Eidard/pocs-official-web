import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Login from './pages/Login';
import Main from './pages/Main';
import Register from './pages/Register';

export default function App() {
  return (
    <Router>
      <Switch>
        <Route
          render={(props) => <Register {...props} />}
          path="/register"
          exact
        />
        <Route render={(props) => <Login {...props} />} path="/login" exact />
        <Route render={(props) => <Main {...props} />} />
      </Switch>
    </Router>
  );
}
