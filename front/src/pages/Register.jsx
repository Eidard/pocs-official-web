import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

import styled from 'styled-components';
import Backdrop from '../components/Backdrop';
import { requestRegister } from '../api/Api';

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
  width: 8.5em;
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

const Select = styled.select`
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

const Option = styled.option``;

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

export default function Register(props) {
  const history = useHistory();
  const [loading, setLoading] = useState(false);
  const [studentId, setStudentId] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [birth, setBirth] = useState('');
  const [gender, setGender] = useState('male');
  const [phone, setPhone] = useState('');
  const [joinedYear, setJoinedYear] = useState('');

  const handleClickSubmit = () => {
    console.log(studentId);
    console.log(name);
    console.log(email);
    console.log(username);
    console.log(password);
    console.log(passwordConfirm);
    console.log(birth);
    console.log(gender);
    console.log(phone);
    console.log(joinedYear);

    (async () => {
      try {
        setLoading(true);

        await requestRegister(
          studentId,
          name,
          email,
          username,
          password,
          birth,
          gender,
          phone,
          joinedYear
        );

        history.push('/login');
      } catch {
        alert('문제가 발생했습니다. 관리자에게 문의해주세요.');
        setLoading(false);
      }
    })();
  };

  return (
    <>
      <Wrapper>
        <Title>한성대학교 POCS 회원가입</Title>
        <SubTitle>아래 정보를 입력해주세요.</SubTitle>
        <RowWrapper>
          <Row>
            <Label htmlFor="studentId">학번</Label>
            <Input
              id="studentId"
              type="text"
              value={studentId}
              onChange={(event) => setStudentId(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="name">이름</Label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(event) => setName(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="email">이메일</Label>
            <Input
              id="email"
              type="text"
              value={email}
              onChange={(event) => setEmail(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="username">아이디</Label>
            <Input
              id="username"
              type="text"
              value={username}
              onChange={(event) => setUsername(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="password">패스워드</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="passwordConfirm">패스워드 확인</Label>
            <Input
              id="passwordConfirm"
              type="password"
              value={passwordConfirm}
              onChange={(event) =>
                setPasswordConfirm(event.currentTarget.value)
              }
            />
          </Row>
          <Row>
            <Label htmlFor="birth">생년월일</Label>
            <Input
              id="birth"
              type="text"
              value={birth}
              onChange={(event) => setBirth(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="gender">성별</Label>
            <Select
              id="gender"
              value={gender}
              onChange={(event) => setGender(event.currentTarget.value)}
            >
              <Option value="male">남성</Option>
              <Option value="female">여성</Option>
            </Select>
          </Row>
          <Row>
            <Label htmlFor="phone">전화번호</Label>
            <Input
              id="phone"
              type="text"
              value={phone}
              onChange={(event) => setPhone(event.currentTarget.value)}
            />
          </Row>
          <Row>
            <Label htmlFor="joinedYear">동아리 가입 년도</Label>
            <Input
              id="joinedYear"
              type="text"
              value={joinedYear}
              onChange={(event) => setJoinedYear(event.currentTarget.value)}
            />
          </Row>
          <SubmitButton type="button" onClick={handleClickSubmit}>
            회원 가입 신청
          </SubmitButton>
        </RowWrapper>
        <SubText>승인까지 평일 기준 3일 정도 소요됩니다.</SubText>
        <SubText>입력하신 정보가 정확하지 않으면 반려될 수 있습니다.</SubText>
      </Wrapper>
      <Backdrop open={loading} />
    </>
  );
};
