import React, { ReactElement } from 'react';
import { Link, RouteComponentProps, withRouter } from 'react-router-dom';
import styled from 'styled-components';

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
  width: 4em;
  font-size: 18px;
`;
const Input = styled.input`
  flex-basis: auto;
  flex-grow: 1;
  flex-shrink: 1;
  margin-left: 8px;
  min-width: 6em;
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
  const handleClickLogin = () => {
    props.history.push('/');
  };

  return (
    <Wrapper>
      <Title>한성대학교 POCS</Title>
      <SubTitle>이메일과 패스워드를 입력해주세요.</SubTitle>
      <RowWrapper>
        <Row>
          <Label htmlFor="email">이메일</Label>
          <Input id="email" type="text"></Input>
        </Row>
        <Row>
          <Label htmlFor="password">패스워드</Label>
          <Input id="password" type="pasword"></Input>
        </Row>
        <LoginButton type="button" onClick={handleClickLogin}>
          로그인
        </LoginButton>
      </RowWrapper>
      <SubText>
        계정이 없으신가요? <Link to="/register">여기</Link>로 이동하세요.
      </SubText>
    </Wrapper>
  );
});
