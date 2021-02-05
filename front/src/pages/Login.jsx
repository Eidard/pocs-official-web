import React, { ReactElement, useState } from 'react';
import { Link, RouteComponentProps, withRouter } from 'react-router-dom';
import styled from 'styled-components';

import Backdrop from '../components/Backdrop';

import { authenticate } from '../api/Api';

const Wrapper = styled.main`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 12px;
  height: 100%;
`;
const Title = styled.h1`
  font-size: 24px;
  font-weight: normal;
`;
const SubTitle = styled.p`
  margin-top: 16px;
  font-size: 16px;
  font-weight: normal;
  color: #666666;
`;
const RowWrapper = styled.div`
  padding: 24px 0 32px;
`;
const Row = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  & + & {
    margin-top: 12px;
  }
`;
const Label = styled.label`
  flex-basis: auto;
  flex-grow: 0;
  flex-shrink: 0;
  width: 5em;
  font-size: 18px;
`;
const Input = styled.input`
  flex-basis: auto;
  flex-grow: 1;
  flex-shrink: 1;
  margin-left: 8px;
  border: 1px solid #222222;
  border-radius: 3px;
  padding: 4px 6px;
  min-width: 6em;
  height: 1.75em;
  font-size: 18px;
  font-weight: normal;
`;
const LoginButton = styled.button`
  display: block;
  margin: 36px auto 0;
  width: 10em;
  height: 2.5em;
  font-size: 14px;
`;
const SubText = styled.p`
  font-size: 14px;
  font-weight: normal;
  color: #999999;
`;

export default withRouter(function Login(props) {
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleClickLogin = () => {
    (async () => {
      setLoading(true);

      try {
        await authenticate(username, password);
        props.history.push('/');
      } catch (response) {
        alert('잘못된 아이디 또는 패스워드입니다.');
        setLoading(false);
      }
    })();
  };

  return (
    <>
      <Wrapper>
        <Title>한성대학교 POCS</Title>
        <SubTitle>아이디와 패스워드를 입력해주세요.</SubTitle>
        <RowWrapper>
          <Row>
            <Label htmlFor="username">아이디</Label>
            <Input
              id="username"
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="password">패스워드</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </Row>
          <LoginButton type="button" onClick={handleClickLogin}>
            로그인
          </LoginButton>
        </RowWrapper>
        <SubText>
          계정이 없으신가요? <Link to="/register">여기</Link>로 이동하세요.
        </SubText>
      </Wrapper>
      <Backdrop open={loading} />
    </>
  );
});
