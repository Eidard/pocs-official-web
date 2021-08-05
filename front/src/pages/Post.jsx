import React, { useEffect, useState } from 'react';
import { Link, useParams }            from 'react-router-dom';
import styled                         from 'styled-components';

import Backdrop from '../components/Backdrop';
import { getPost } from '../api/Api';
import { formatDate } from '../utils/Format';

const Wrapper = styled.main`
  margin: 0px;
  background-color: white;
  height: 100%;
`;

const Header = styled.header`
  display: inline-block;
  width: 100%;
  min-height: 300px;
  background-color: black;
`;

const HeaderContent = styled.div`
  text-align: left;
  font-size: 24px;
  color: white;
  padding-left: 40px;
  padding-right: 40px;
  padding-top: 100px;

  margin: auto;
  margin-top: 40px;
  margin-bottom: 60px;
  max-width: 1024px;
`;

const LogoText = styled.div`
  display: inline-block;
  float: left;
  margin: 15px;
  margin-right: 20px;
  line-height: 30px;
  vertical-align: middle;
  font-size: 28px;
  font-weight: bold;
  color: white;
`;

const NavigationBarRoot = styled.nav`
  float: right;
`;

const NavigationBarList = styled.ul`
  list-style-type: none;
  display: inline-block;
  margin: 5px;
  overflow: hidden;
`;

const NavigationBarItem = styled.li`
  font-size: 14px;
  line-height: 30px;
  margin: 10px;
  margin-left: 16px;
  margin-right: 16px;
  display: inline-block;
  vertical-align: middle;
  text-decoration: none;
  color: white;
`;

const NavigationBarImageItem = styled.img`
  width: 20px;
  height: 20px;
  margin-left: 16px;
  margin-right: 16px;
  filter: invert(1);
  vertical-align: middle;
`;

const HeaderContentTitle = styled.p`
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 30px;
`;

const HeaderContentDate = styled.p`
  font-size: 16px;
  color: lightgray;
  margin-bottom: 40px;
`;

const Section = styled.section`
  margin: auto;
  max-width: 1024px;
  padding: 40px;
  background-color: white;
`;

const Article = styled.article`
  margin: 0px;
`;

const Logo = (props) => {
  return (
    <Link to="/">
      <LogoText>{props.text}</LogoText>
    </Link>
  );
};

const NavigationBarButton = (props) => {
  return (
    <Link to={props.to}>
      <NavigationBarItem>{props.text}</NavigationBarItem>
    </Link>
  );
};

const AccountButton = () => {
  return (
    <Link to="/login">
      <NavigationBarImageItem src="/images/main/account.png" />
    </Link>
  );
};

const SearchButton = () => {
  return <NavigationBarImageItem src="/images/main/search.png" />;
};

export default function Post(props) {
  const [post, setPost] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    (async () => {
      try {
        setPost(await getPost(id));
      } catch {
        alert('문제가 발생했습니다. 관리자에게 문의해주세요.');
      }
    })();
  }, []);

  return post ? (
    <Wrapper>
      <Header>
        <Logo text="POCS" />
        <NavigationBarRoot>
          <NavigationBarList>
            <NavigationBarButton text="Board 1" to="board" />
            <AccountButton />
            <SearchButton />
          </NavigationBarList>
        </NavigationBarRoot>
        <HeaderContent>
          <HeaderContentTitle>{post.title}</HeaderContentTitle>
          <HeaderContentDate>
            {formatDate(new Date(post.created_at))}
          </HeaderContentDate>
        </HeaderContent>
      </Header>
      <Section>
        <Article dangerouslySetInnerHTML={{ __html: post.content }} />
      </Section>
    </Wrapper>
  ) : (
    <Backdrop open={!post} />
  );
};
