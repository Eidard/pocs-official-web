import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Register from './pages/Register';
import Login    from './pages/Login';
import Board    from './pages/Board';
import Post     from './pages/Post';
import Main     from './pages/Main';

export default function App() {
  return (
    <Router>
      <Switch>
        <Route render={(props)=><Register{...props}/>} path="/register" exact/>
        <Route render={(props)=><Login   {...props}/>} path="/login"    exact/>
        <Route render={(props)=><Board   {...props}/>} path="/board"         />
        <Route render={(props)=><Post    {...props}/>} path="/post"          />
        <Route render={(props)=><Main    {...props}/>}                       />
      </Switch>
    </Router>
  );
}
