import React, { useEffect, useState } from 'react';
import { Link, withRouter } from 'react-router-dom';
import styled from 'styled-components';

import Backdrop from '../components/Backdrop';

import { getPosts } from '../api/Api';

import { formatDate } from '../utils/Format';

const Wrapper = styled.main`
  margin: 0px;
  background-color: #eee;
  height: 100%;
`;

const Header = styled.header`
  display: inline-block;
  width: 100%;
  height: 300px;
  background-color: #333;
`;

const HeaderContent = styled.div`
  text-align: left;
  font-size: 24px;
  color: white;
  padding-left: 80px;
  padding-top: 120px;
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
  margin-bottom: 10px;
`;

const HeaderContentText = styled.p`
  font-size: 16px;
  color: lightgray;
`;

const Section = styled.section`
  margin: 40px 10px 10px 10px;
`;

const Article = styled.article`
  margin: 5px;
`;

const ArticleTitle = styled.h1`
  font-size: 16px;
  margin: 30px 40px 30px 40px;
`;

const ArticleRowWrapper = styled.div`
  margin: 10px 40px 10px 40px;
  padding: 10px;
  background-color: white;
  text-decoration: none;
`;

const ArticleRowTitle = styled.span`
  display: inline-block;
  font-weight: bold;
  margin: 5px 5px 0px 0px;
  font-size: 14px;
`;

const ArticleRowDate = styled.span`
  float: right;
  font-size: 14px;
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

const ArticleRow = (props) => {
  return (
    <Link to={props.to} style={{ textDecoration: 'none', color: 'black' }}>
      <ArticleRowWrapper>
        <ArticleRowTitle>{props.title}</ArticleRowTitle>
        <ArticleRowDate>{props.date}</ArticleRowDate>
      </ArticleRowWrapper>
    </Link>
  );
};

export default withRouter(function Board(props) {
  const [posts, setPosts] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        setPosts(await getPosts());
      } catch {
        alert('문제가 발생했습니다. 관리자에게 문의해주세요.');
      }
    })();
  }, []);

  return posts ? (
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
          <HeaderContentTitle>Board 1</HeaderContentTitle>
          <HeaderContentText>테스트를 위한 보드 1 입니다.</HeaderContentText>
        </HeaderContent>
      </Header>
      <Section>
        <Article>
          <ArticleTitle>최근 게시글</ArticleTitle>
          {posts.map((post) => (
            <ArticleRow
              key={post.id}
              title={post.title}
              date={formatDate(new Date(post.created_at))}
              to={`/post/${post.id}`}
            />
          ))}
        </Article>
      </Section>
    </Wrapper>
  ) : (
    <Backdrop open />
  );
});
