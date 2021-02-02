import React from 'react';
import { Link, withRouter } from 'react-router-dom';

export default withRouter(function Main(props) {
  return (
    <>
      <Link to="/login">로그인 하러 가기</Link>
    </>
  );
});
