import React from 'react';
import { HashLoader } from 'react-spinners';
import styled from 'styled-components';

const Background = styled.div`
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: black;
  opacity: 0.7;
  z-index: 10000;
`;

export default function Backdrop({ open }) {
  return open ? (
    <Background>
      <HashLoader color="white" loading />
    </Background>
  ) : (
    <></>
  );
}
