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
const SubmitButton = styled.button`
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

  & + & {
    margin-top: 6px;
  }
`;

export default withRouter(function Register(props) {
  const handleClickSubmit = () => {
    props.history.push('/');
  };

  return (
    <Wrapper>
      <Title>한성대학교 POCS 회원가입</Title>
      <SubTitle>아래 정보를 입력해주세요.</SubTitle>
      <RowWrapper>
        <Row>
          <Label htmlFor="email">이메일</Label>
          <Input id="email" type="text"></Input>
        </Row>
        <Row>
          <Label htmlFor="password">패스워드</Label>
          <Input id="password" type="pasword"></Input>
        </Row>
        <SubmitButton type="button" onClick={handleClickSubmit}>
          회원 가입 신청
        </SubmitButton>
      </RowWrapper>
      <SubText>승인까지 평일 기준 3일 정도 소요됩니다.</SubText>
      <SubText>입력하신 정보가 정확하지 않으면 반려될 수 있습니다.</SubText>
    </Wrapper>
  );
});
